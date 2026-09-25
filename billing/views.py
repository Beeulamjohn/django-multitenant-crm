from datetime import datetime
from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from app.models import Company
from app.utils import get_company

from students.models import Student

from .forms import PaymentForm

from .models import (
    BankPaymentSettings,
    BillingAppearanceSettings,
    BillingCompanyProfile,
    BillingSettings,
    EMI,
    FeeConfiguration,
    FeeDiscountSettings,
    GSTSettings,
    Invoice,
    InvoiceSettings,
    LateFeeSettings,
    Payment,
    PaymentReminderSettings,
    PaymentSettings,
)


# ============================================================
# HELPER
# ============================================================

def get_user_company(user):
    try:
        return Company.objects.get(user=user)
    except Company.DoesNotExist:
        return None


def get_billing_company(request):
    return get_object_or_404(
        Company,
        user=request.user,
        company_type="billing"
    )


# ============================================================
# BILLING DASHBOARD
# ============================================================

@login_required(login_url="billing_staff_login")
def billing_dashboard(request):

    company = get_billing_company(request)

    appearance, _ = BillingAppearanceSettings.objects.get_or_create(
        company=company
    )

    billing_settings, _ = BillingSettings.objects.get_or_create(
        company=company
    )

    company_profile, _ = BillingCompanyProfile.objects.get_or_create(
        company=company,
        defaults={
            "company_name": company.company_name,
            "phone": company.phone,
        }
    )

    invoices = (
        Invoice.objects
        .filter(company=company)
        .select_related("student")
        .order_by("-created_at")
    )

    total_collection = (
        invoices.aggregate(
            total=Sum("amount_paid")
        )["total"]
        or Decimal("0.00")
    )

    total_invoices = invoices.count()

    paid_students = (
        invoices
        .filter(status="Paid")
        .values("student")
        .distinct()
        .count()
    )

    pending_payments = invoices.filter(
        status="Pending"
    ).count()

    overdue_payments = invoices.filter(
        status="Overdue"
    ).count()

    # Students belong to the linked Education Company
    education_company = company.linked_education_company

    if education_company:
        total_students = Student.objects.filter(
            company=education_company
        ).count()
    else:
        total_students = 0

    recent_payments = (
        Payment.objects
        .filter(company=company)
        .select_related("student")
        .order_by("-payment_date")[:5]
    )

    context = {
        "company": company,
        "company_profile": company_profile,

        "appearance": appearance,

        "billing_settings": billing_settings,
        "currency": billing_settings.currency,
        "currency_symbol": billing_settings.currency_symbol,
        "billing_enabled": billing_settings.billing_enabled,
        "payment_terms": billing_settings.payment_terms,
        "financial_year": billing_settings.financial_year,
        "default_payment_method": billing_settings.default_payment_method,
        "allow_partial_payment": billing_settings.allow_partial_payment,
        "auto_payment_status": billing_settings.auto_payment_status,
        "payment_receipt": billing_settings.payment_receipt,
        "auto_invoice_generation": billing_settings.auto_invoice_generation,

        "bills": invoices[:5],
        "recent_payments": recent_payments,
        "total_collection": total_collection,
        "total_invoices": total_invoices,
        "paid_students": paid_students,
        "pending_payments": pending_payments,
        "overdue_payments": overdue_payments,
        "total_students": total_students,
    }

    return render(
        request,
        "billing/dashboard_billing.html",
        context
    )


# ============================================================
# CREATE INVOICE
# ============================================================

@login_required(login_url="billing_staff_login")
def create_invoice(request):

    company = get_billing_company(request)

    appearance, _ = BillingAppearanceSettings.objects.get_or_create(
        company=company
    )

    education_company = company.linked_education_company

    students = Student.objects.none()

    if education_company:
        students = (
            Student.objects
            .filter(company=education_company)
            .order_by("first_name", "last_name")
        )

    if request.method == "POST":

        if not education_company:
            messages.error(
                request,
                "Please link an Education Company first."
            )
            return redirect("create_invoice")

        student_id = request.POST.get("student")

        if not student_id:
            messages.error(
                request,
                "Please select a student."
            )
            return redirect("create_invoice")

        student = get_object_or_404(
            Student,
            id=student_id,
            company=education_company
        )

        try:
            course_fee = Decimal(
                request.POST.get("course_fee") or "0"
            )

            registration_fee = Decimal(
                request.POST.get("registration_fee") or "0"
            )

            amount_paid = Decimal(
                request.POST.get("amount_paid") or "0"
            )

        except (InvalidOperation, ValueError):

            messages.error(
                request,
                "Please enter valid amount values."
            )

            return redirect("create_invoice")

        payment_type = request.POST.get(
            "payment_type",
            "Full"
        )

        due_date = None

        due_date_value = request.POST.get(
            "due_date"
        )

        if due_date_value:

            try:
                due_date = datetime.strptime(
                    due_date_value,
                    "%Y-%m-%d"
                ).date()

            except ValueError:

                messages.error(
                    request,
                    "Invalid due date."
                )

                return redirect("create_invoice")

        subtotal = (
            course_fee +
            registration_fee
        )

        gst_amount = Decimal("0.00")

        gst_checked = (
            request.POST.get("gst") == "on"
        )

        if gst_checked:

            gst_amount = (
                subtotal *
                Decimal("0.18")
            )

        total_amount = (
            subtotal +
            gst_amount
        )

        Invoice.objects.create(
            company=company,
            student=student,
            course_fee=course_fee,
            registration_fee=registration_fee,
            gst_amount=gst_amount,
            total_amount=total_amount,
            amount_paid=amount_paid,
            payment_type=payment_type,
            due_date=due_date,
        )

        messages.success(
            request,
            "Invoice created successfully."
        )

        return redirect("create_invoice_list")

    return render(
        request,
        "billing/create_invoice.html",
        {
            "company": company,
            "students": students,
            "appearance": appearance,
        }
    )


# ============================================================
# INVOICE LIST
# ============================================================

@login_required
def create_invoice_list(request):

    company = get_billing_company(request)

    appearance, _ = BillingAppearanceSettings.objects.get_or_create(
        company=company
    )

    invoices = (
        Invoice.objects
        .filter(company=company)
        .select_related("student")
        .order_by("-created_at")
    )

    return render(
        request,
        "billing/create_invoice_list.html",
        {
            "company": company,
            "appearance": appearance,
            "invoices": invoices,
        }
    )


# ============================================================
# UPDATE INVOICE
# ============================================================

@login_required
def create_invoice_update(request, pk):

    company = get_billing_company(request)

    invoice = get_object_or_404(
        Invoice,
        pk=pk,
        company=company
    )

    appearance, _ = BillingAppearanceSettings.objects.get_or_create(
        company=company
    )

    if request.method == "POST":

        invoice.invoice_number = request.POST.get(
            "invoice_number"
        )

        try:

            invoice.total_amount = Decimal(
                request.POST.get(
                    "total_amount"
                ) or "0"
            )

            invoice.amount_paid = Decimal(
                request.POST.get(
                    "amount_paid"
                ) or "0"
            )

        except (InvalidOperation, ValueError):

            messages.error(
                request,
                "Please enter valid amount values."
            )

            return redirect(
                "create_invoice_update",
                pk=pk
            )

        due_date = request.POST.get(
            "due_date"
        )

        if due_date:

            try:

                invoice.due_date = datetime.strptime(
                    due_date,
                    "%Y-%m-%d"
                ).date()

            except ValueError:

                messages.error(
                    request,
                    "Invalid due date."
                )

                return redirect(
                    "create_invoice_update",
                    pk=pk
                )

        else:

            invoice.due_date = None

        invoice.status = request.POST.get(
            "status"
        )

        invoice.save()

        messages.success(
            request,
            "Invoice updated successfully."
        )

        return redirect(
            "create_invoice_list"
        )

    return render(
        request,
        "billing/invoice_update.html",
        {
            "invoice": invoice,
            "appearance": appearance,
        }
    )


# ============================================================
# DELETE INVOICE
# ============================================================

@login_required
def create_invoice_delete(request, pk):

    company = get_billing_company(request)

    invoice = get_object_or_404(
        Invoice,
        pk=pk,
        company=company
    )

    if request.method == "POST":

        invoice.delete()

        messages.success(
            request,
            "Invoice deleted successfully."
        )

        return redirect(
            "create_invoice_list"
        )

    return render(
        request,
        "billing/invoice_delete.html",
        {
            "invoice": invoice
        }
    )


# ============================================================
# FEE CONFIGURATION
# ============================================================

@login_required
def fee_configuration(request):

    company = get_billing_company(request)

    appearance, _ = BillingAppearanceSettings.objects.get_or_create(
        company=company
    )

    education_company = company.linked_education_company

    students = Student.objects.none()

    if education_company:

        students = (
            Student.objects
            .filter(company=education_company)
            .order_by("first_name", "last_name")
        )

    if request.method == "POST":

        student = None

        student_id = request.POST.get(
            "student"
        )

        if student_id:

            if not education_company:

                messages.error(
                    request,
                    "Please link an Education Company first."
                )

                return redirect(
                    "fee_configuration"
                )

            student = get_object_or_404(
                Student,
                id=student_id,
                company=education_company
            )

        course = request.POST.get(
            "course",
            ""
        ).strip()

        department = request.POST.get(
            "department",
            ""
        ).strip()

        fee_type = request.POST.get(
            "fee_type",
            ""
        ).strip()

        amount = request.POST.get(
            "amount"
        )

        if not course or not department or not fee_type or not amount:

            messages.error(
                request,
                "All fields are required."
            )

            return redirect(
                "fee_configuration"
            )

        try:

            amount = Decimal(amount)

        except (InvalidOperation, ValueError):

            messages.error(
                request,
                "Enter a valid amount."
            )

            return redirect(
                "fee_configuration"
            )

        FeeConfiguration.objects.create(
            company=company,
            student=student,
            course=course,
            department=department,
            fee_type=fee_type,
            amount=amount
        )

        messages.success(
            request,
            "Fee configuration added successfully."
        )

        return redirect(
            "fee_configuration"
        )

    fees = (
        FeeConfiguration.objects
        .filter(company=company)
        .select_related("student")
        .order_by("-id")
    )

    return render(
        request,
        "billing/fee_configuration.html",
        {
            "company": company,
            "company_profile": company,
            "appearance": appearance,
            "fees": fees,
            "students": students,
        }
    )


# ============================================================
# EDIT FEE CONFIGURATION
# ============================================================

@login_required
def edit_fee_configuration(request, pk):

    company = get_billing_company(request)

    fee = get_object_or_404(
        FeeConfiguration,
        id=pk,
        company=company
    )

    education_company = company.linked_education_company

    students = Student.objects.none()

    if education_company:

        students = (
            Student.objects
            .filter(company=education_company)
            .order_by("first_name", "last_name")
        )

    if request.method == "POST":

        student_id = request.POST.get(
            "student"
        )

        if student_id:

            if not education_company:

                messages.error(
                    request,
                    "Please link an Education Company first."
                )

                return redirect(
                    "edit_fee_configuration",
                    pk=pk
                )

            fee.student = get_object_or_404(
                Student,
                id=student_id,
                company=education_company
            )

        else:

            fee.student = None

        fee.course = request.POST.get(
            "course",
            ""
        ).strip()

        fee.department = request.POST.get(
            "department",
            ""
        ).strip()

        fee.fee_type = request.POST.get(
            "fee_type",
            ""
        ).strip()

        amount = request.POST.get(
            "amount"
        )

        try:

            if amount:
                fee.amount = Decimal(amount)

        except (InvalidOperation, ValueError):

            messages.error(
                request,
                "Enter a valid amount."
            )

            return redirect(
                "edit_fee_configuration",
                pk=pk
            )

        fee.save()

        messages.success(
            request,
            "Fee configuration updated successfully."
        )

        return redirect(
            "fee_configuration"
        )

    return render(
        request,
        "billing/edit_fee_configuration.html",
        {
            "fee": fee,
            "students": students,
        }
    )


# ============================================================
# DELETE FEE CONFIGURATION
# ============================================================

@login_required
def delete_fee_configuration(request, pk):

    company = get_billing_company(request)

    fee = get_object_or_404(
        FeeConfiguration,
        id=pk,
        company=company
    )

    appearance, _ = BillingAppearanceSettings.objects.get_or_create(
        company=company
    )

    if request.method == "POST":

        fee.delete()

        messages.success(
            request,
            "Fee configuration deleted successfully."
        )

        return redirect(
            "fee_configuration"
        )

    return render(
        request,
        "billing/delete_fee_configuration.html",
        {
            "fee": fee,
            "company": company,
            "appearance": appearance,
        }
    )


# ============================================================
# GST SETTINGS
# ============================================================

@login_required
def gst_settings(request):

    company = get_billing_company(request)

    gst = GSTSettings.objects.filter(
        company=company
    ).first()

    appearance, _ = BillingAppearanceSettings.objects.get_or_create(
        company=company
    )

    if request.method == "POST":

        gst_number = request.POST.get(
            "gst_number",
            ""
        ).strip()

        try:

            cgst = Decimal(
                request.POST.get(
                    "cgst"
                ) or "0.00"
            )

            sgst = Decimal(
                request.POST.get(
                    "sgst"
                ) or "0.00"
            )

            igst = Decimal(
                request.POST.get(
                    "igst"
                ) or "0.00"
            )

        except InvalidOperation:

            messages.error(
                request,
                "Please enter valid GST percentages."
            )

            return redirect(
                "gst_settings"
            )

        is_active = (
            request.POST.get(
                "is_active"
            ) == "on"
        )

        GSTSettings.objects.update_or_create(
            company=company,
            defaults={
                "gst_number": gst_number,
                "cgst": cgst,
                "sgst": sgst,
                "igst": igst,
                "is_active": is_active,
            }
        )

        messages.success(
            request,
            "GST Settings saved successfully."
        )

        return redirect(
            "gst_settings"
        )

    return render(
        request,
        "billing/gst_settings.html",
        {
            "gst": gst,
            "company": company,
            "appearance": appearance,
        }
    )


@login_required
def delete_gst_settings(request):

    company = get_billing_company(request)

    gst = GSTSettings.objects.filter(
        company=company
    ).first()

    if gst:

        gst.delete()

        messages.success(
            request,
            "GST Settings deleted successfully."
        )

    return redirect(
        "gst_settings"
    )


@login_required
def edit_gst_settings(request):

    company = get_billing_company(request)

    gst = get_object_or_404(
        GSTSettings,
        company=company
    )

    appearance, _ = BillingAppearanceSettings.objects.get_or_create(
        company=company
    )

    if request.method == "POST":

        gst.gst_number = request.POST.get(
            "gst_number",
            ""
        ).strip()

        try:

            gst.cgst = Decimal(
                request.POST.get(
                    "cgst"
                ) or "0.00"
            )

            gst.sgst = Decimal(
                request.POST.get(
                    "sgst"
                ) or "0.00"
            )

            gst.igst = Decimal(
                request.POST.get(
                    "igst"
                ) or "0.00"
            )

        except InvalidOperation:

            messages.error(
                request,
                "Please enter valid GST values."
            )

            return redirect(
                "edit_gst_settings"
            )

        gst.is_active = (
            request.POST.get(
                "is_active"
            ) == "on"
        )

        gst.save()

        messages.success(
            request,
            "GST Settings updated successfully."
        )

        return redirect(
            "gst_settings"
        )

    return render(
        request,
        "billing/edit_gst_settings.html",
        {
            "gst": gst,
            "company": company,
            "appearance": appearance,
        }
    )


# ============================================================
# PAYMENT LIST
# ============================================================

@login_required
def billing_payment_list(request):

    company = get_billing_company(request)

    appearance, _ = BillingAppearanceSettings.objects.get_or_create(
        company=company
    )

    payments = (
        Payment.objects
        .filter(company=company)
        .select_related("student")
        .order_by("-payment_date")
    )

    total_collection = (
        payments.aggregate(
            total=Sum("amount")
        )["total"]
        or Decimal("0.00")
    )

    total_payments = payments.count()

    today = timezone.localdate()

    today_collection = (
        payments
        .filter(payment_date=today)
        .aggregate(
            total=Sum("amount")
        )["total"]
        or Decimal("0.00")
    )

    pending_payments = payments.filter(
        status="Pending"
    ).count()

    context = {
        "company": company,
        "appearance": appearance,
        "payments": payments,
        "total_collection": total_collection,
        "total_payments": total_payments,
        "today_collection": today_collection,
        "pending_payments": pending_payments,
    }

    return render(
        request,
        "billing/billing_payment_list.html",
        context
    )


@login_required
def billing_payment_form(request):

    company = get_billing_company(request)

    appearance, _ = BillingAppearanceSettings.objects.get_or_create(
        company=company
    )

    if request.method == "POST":

        form = PaymentForm(request.POST)

        if form.is_valid():

            payment = form.save(
                commit=False
            )

            payment.company = company

            payment.save()

            messages.success(
                request,
                "Payment Added Successfully."
            )

            return redirect(
                "billing_payment_list"
            )

    else:

        form = PaymentForm()

    return render(
        request,
        "billing/billing_payment_form.html",
        {
            "form": form,
            "company": company,
            "appearance": appearance,
        }
    )


# ============================================================
# EDIT PAYMENT
# ============================================================

@login_required
def edit_payment(request, pk):

    company = get_billing_company(request)

    payment = get_object_or_404(
        Payment,
        pk=pk,
        company=company
    )

    appearance, _ = BillingAppearanceSettings.objects.get_or_create(
        company=company
    )

    if request.method == "POST":

        form = PaymentForm(
            request.POST,
            instance=payment
        )

        if form.is_valid():

            payment = form.save(
                commit=False
            )

            payment.company = company

            payment.save()

            messages.success(
                request,
                "Payment Updated Successfully."
            )

            return redirect(
                "billing_payment_list"
            )

    else:

        form = PaymentForm(
            instance=payment
        )

    return render(
        request,
        "billing/billing_payment_form.html",
        {
            "form": form,
            "payment": payment,
            "company": company,
            "appearance": appearance,
        }
    )


# ============================================================
# DELETE PAYMENT
# ============================================================

@login_required
def delete_payment(request, pk):

    company = get_billing_company(request)

    payment = get_object_or_404(
        Payment,
        pk=pk,
        company=company
    )

    if request.method == "POST":

        payment.delete()

        messages.success(
            request,
            "Payment Deleted Successfully."
        )

        return redirect(
            "billing_payment_list"
        )

    return render(
        request,
        "billing/payment_delete.html",
        {
            "payment": payment
        }
    )


# ============================================================
# EMI LIST
# ============================================================

@login_required
def emi_list(request):

    company = get_billing_company(request)

    emis = (
        EMI.objects
        .filter(company=company)
        .select_related("student")
        .order_by("due_date")
    )

    for emi in emis:

        if emi.status != "Paid":
            emi.save()

    emis = (
        EMI.objects
        .filter(company=company)
        .select_related("student")
        .order_by("due_date")
    )

    appearance, _ = BillingAppearanceSettings.objects.get_or_create(
        company=company
    )

    context = {

        "company": company,

        "emis": emis,

        "total_count": emis.count(),

        "paid_count": emis.filter(
            status="Paid"
        ).count(),

        "pending_count": emis.filter(
            status="Pending"
        ).count(),

        "overdue_count": emis.filter(
            status="Overdue"
        ).count(),

        "total_amount": sum(
            emi.amount for emi in emis
        ),

        "appearance": appearance,
    }

    return render(
        request,
        "billing/emi_list.html",
        context
    )


# ============================================================
# CREATE EMI
# ============================================================

@login_required
def emi_create(request):

    company = get_billing_company(request)

    education_company = company.linked_education_company

    students = Student.objects.none()

    if education_company:

        students = (
            Student.objects
            .filter(company=education_company)
            .order_by("first_name", "last_name")
        )

    appearance, _ = BillingAppearanceSettings.objects.get_or_create(
        company=company
    )

    if request.method == "POST":

        if not education_company:

            messages.error(
                request,
                "Please link an Education Company first."
            )

            return redirect(
                "emi_create"
            )

        try:

            student = get_object_or_404(
                Student,
                id=request.POST.get("student"),
                company=education_company
            )

            due_date = datetime.strptime(
                request.POST.get("due_date"),
                "%Y-%m-%d"
            ).date()

            installment = int(
                request.POST.get(
                    "installment"
                )
            )

            amount = Decimal(
                request.POST.get(
                    "amount"
                )
            )

            emi = EMI.objects.create(
                company=company,
                student=student,
                installment_no=installment,
                due_date=due_date,
                amount=amount
            )

            messages.success(
                request,
                f"EMI for {student.first_name} created successfully. "
                f"Status: {emi.status}"
            )

            return redirect(
                "emi_list"
            )

        except (
            ValueError,
            InvalidOperation,
            TypeError
        ):

            messages.error(
                request,
                "Please enter valid EMI details."
            )

        except Exception as error:

            messages.error(
                request,
                f"Unable to create EMI: {error}"
            )

    return render(
        request,
        "billing/emi_form.html",
        {
            "company": company,
            "students": students,
            "appearance": appearance,
        }
    )


# ============================================================
# MARK EMI AS PAID
# ============================================================

@login_required
def emi_paid(request, pk):

    company = get_billing_company(request)

    emi = get_object_or_404(
        EMI,
        pk=pk,
        company=company
    )

    emi.status = "Paid"

    emi.paid_date = timezone.now().date()

    emi.save()

    messages.success(
        request,
        "EMI marked as paid successfully."
    )

    return redirect(
        "emi_list"
    )


# ============================================================
# EDIT EMI
# ============================================================

@login_required
def emi_edit(request, pk):

    company = get_billing_company(request)

    emi = get_object_or_404(
        EMI,
        pk=pk,
        company=company
    )

    education_company = company.linked_education_company

    students = Student.objects.none()

    if education_company:

        students = (
            Student.objects
            .filter(company=education_company)
            .order_by("first_name", "last_name")
        )

    if request.method == "POST":

        student_id = request.POST.get(
            "student"
        )

        if not education_company:

            messages.error(
                request,
                "Please link an Education Company first."
            )

            return redirect(
                "emi_edit",
                pk=pk
            )

        emi.student = get_object_or_404(
            Student,
            id=student_id,
            company=education_company
        )

        try:

            emi.installment_no = int(
                request.POST.get(
                    "installment"
                )
            )

            emi.due_date = datetime.strptime(
                request.POST.get(
                    "due_date"
                ),
                "%Y-%m-%d"
            ).date()

            emi.amount = Decimal(
                request.POST.get(
                    "amount"
                )
            )

        except (
            ValueError,
            InvalidOperation,
            TypeError
        ):

            messages.error(
                request,
                "Please enter valid EMI details."
            )

            return redirect(
                "emi_edit",
                pk=pk
            )

        emi.save()

        messages.success(
            request,
            "EMI updated successfully."
        )

        return redirect(
            "emi_list"
        )

    return render(
        request,
        "billing/emi_edit.html",
        {
            "company": company,
            "emi": emi,
            "students": students,
        }
    )


# ============================================================
# DELETE EMI
# ============================================================

@login_required
def emi_delete(request, pk):

    company = get_billing_company(request)

    emi = get_object_or_404(
        EMI,
        pk=pk,
        company=company
    )

    if request.method == "POST":

        emi.delete()

        messages.success(
            request,
            "EMI deleted successfully."
        )

        return redirect(
            "emi_list"
        )

    return render(
        request,
        "billing/emi_delete.html",
        {
            "company": company,
            "emi": emi,
        }
    )


# ============================================================
# INVOICE REPORT
# ============================================================

@login_required
def invoice_report(request):

    company = get_billing_company(request)

    appearance, _ = BillingAppearanceSettings.objects.get_or_create(
        company=company
    )

    invoices = (
        Invoice.objects
        .filter(company=company)
        .select_related("student")
        .order_by("-created_at")
    )

    total_amount = (
        invoices.aggregate(
            total=Sum("total_amount")
        )["total"]
        or Decimal("0.00")
    )

    paid_amount = (
        invoices.aggregate(
            total=Sum("amount_paid")
        )["total"]
        or Decimal("0.00")
    )

    pending_amount = (
        invoices.aggregate(
            total=Sum("balance_amount")
        )["total"]
        or Decimal("0.00")
    )

    total_invoices = invoices.count()

    paid_count = invoices.filter(
        status="Paid"
    ).count()

    pending_count = invoices.filter(
        status="Pending"
    ).count()

    context = {

        "company": company,

        "invoices": invoices,

        "total_invoices": total_invoices,

        "total_amount": total_amount,

        "paid_amount": paid_amount,

        "pending_amount": pending_amount,

        "paid_count": paid_count,

        "pending_count": pending_count,

        "appearance": appearance,
    }

    return render(
        request,
        "billing/invoice_report.html",
        context
    )


# ============================================================
# BILLING PORTAL
# ============================================================

@login_required
def billing_portal(request):

    company = get_billing_company(request)

    return render(
        request,
        "billing/billing_portal.html",
        {
            "company": company
        }
    )


# ============================================================
# BILLING ADMIN LOGIN
# ============================================================

def billing_admin_login(request):

    if request.method == "POST":

        username = request.POST.get(
            "username"
        )

        password = request.POST.get(
            "password"
        )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None and user.is_superuser:

            login(
                request,
                user
            )

            return redirect(
                "/billing-admin/"
            )

        return render(
            request,
            "billing/billing_admin_login.html",
            {
                "error": "Invalid username or password."
            }
        )

    return render(
        request,
        "billing/billing_admin_login.html"
    )


# ============================================================
# BILLING STAFF LOGIN
# ============================================================

def billing_staff_login(request):

    if request.method == "POST":

        username = request.POST.get(
            "username",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is None:

            return render(
                request,
                "login.html",
                {
                    "error": "Invalid username or password."
                }
            )

        try:

            company = Company.objects.get(
                user=user
            )

        except Company.DoesNotExist:

            messages.error(
                request,
                "No company is linked to this account."
            )

            return render(
                request,
                "login.html"
            )

        if company.company_type != "billing":

            messages.error(
                request,
                "This account is not a Billing account."
            )

            return render(
                request,
                "login.html"
            )

        if not company.is_active:

            messages.error(
                request,
                "Your company account is inactive."
            )

            return render(
                request,
                "login.html"
            )

        login(
            request,
            user
        )

        return redirect(
            "billing_dashboard"
        )

    return render(
        request,
        "login.html"
    )


# ============================================================
# BILLING SETTINGS
# ============================================================

@login_required
def billing_settings(request):

    company = get_billing_company(request)

    appearance_settings, _ = (
        BillingAppearanceSettings.objects.get_or_create(
            company=company
        )
    )

    return render(
        request,
        "billing/billing_settings.html",
        {
            "company": company,
            "appearance_settings": appearance_settings,
        }
    )


# ============================================================
# GENERAL BILLING SETTINGS
# ============================================================

@login_required
def billing_general_settings(request):

    company = get_billing_company(request)

    billing_settings, _ = (
        BillingSettings.objects.get_or_create(
            company=company
        )
    )

    appearance_settings, _ = (
        BillingAppearanceSettings.objects.get_or_create(
            company=company
        )
    )

    if request.method == "POST":

        currency = request.POST.get(
            "currency",
            "INR"
        )

        allowed_currencies = {
            "INR",
            "USD",
            "EUR",
            "GBP",
        }

        if currency not in allowed_currencies:
            currency = "INR"

        currency_symbol = request.POST.get(
            "currency_symbol",
            "₹"
        ).strip()

        if not currency_symbol:
            currency_symbol = "₹"

        currency_symbol = currency_symbol[:5]

        financial_year = request.POST.get(
            "financial_year",
            "april_march"
        )

        allowed_years = {
            "april_march",
            "january_december",
        }

        if financial_year not in allowed_years:
            financial_year = "april_march"

        try:

            payment_terms = int(
                request.POST.get(
                    "payment_terms",
                    "30"
                )
            )

        except (TypeError, ValueError):

            payment_terms = 30

        allowed_payment_terms = {
            0,
            7,
            15,
            30,
            45,
            60,
        }

        if payment_terms not in allowed_payment_terms:
            payment_terms = 30

        billing_enabled = (
            request.POST.get(
                "billing_enabled"
            ) == "1"
        )

        allow_partial_payment = (
            request.POST.get(
                "allow_partial_payment"
            ) == "1"
        )

        auto_payment_status = (
            request.POST.get(
                "auto_payment_status"
            ) == "1"
        )

        payment_receipt = (
            request.POST.get(
                "payment_receipt"
            ) == "1"
        )

        auto_invoice_generation = (
            request.POST.get(
                "auto_invoice_generation"
            ) == "1"
        )

        default_payment_method = request.POST.get(
            "default_payment_method",
            "cash"
        )

        allowed_payment_methods = {
            "cash",
            "bank",
            "upi",
            "card",
            "cheque",
        }

        if default_payment_method not in allowed_payment_methods:
            default_payment_method = "cash"

        billing_settings.currency = currency

        billing_settings.currency_symbol = (
            currency_symbol
        )

        billing_settings.financial_year = (
            financial_year
        )

        billing_settings.payment_terms = (
            payment_terms
        )

        billing_settings.billing_enabled = (
            billing_enabled
        )

        billing_settings.allow_partial_payment = (
            allow_partial_payment
        )

        billing_settings.auto_payment_status = (
            auto_payment_status
        )

        billing_settings.payment_receipt = (
            payment_receipt
        )

        billing_settings.auto_invoice_generation = (
            auto_invoice_generation
        )

        billing_settings.default_payment_method = (
            default_payment_method
        )

        billing_settings.save()

        messages.success(
            request,
            "General billing settings saved successfully."
        )

        return redirect(
            "billing_general_settings"
        )

    return render(
        request,
        "billing/billing_general_settings.html",
        {
            "company": company,
            "settings": billing_settings,
            "appearance_settings": appearance_settings,
        }
    )


# ============================================================
# INVOICE SETTINGS
# ============================================================

@login_required
def billing_invoice_settings(request):

    company = get_billing_company(request)

    settings, _ = InvoiceSettings.objects.get_or_create(
        company=company
    )

    appearance_settings, _ = (
        BillingAppearanceSettings.objects.get_or_create(
            company=company
        )
    )

    if request.method == "POST":

        settings.invoice_prefix = request.POST.get(
            "invoice_prefix",
            "INV"
        ).strip()

        settings.invoice_format = request.POST.get(
            "invoice_format",
            "PREFIX-YEAR-NUMBER"
        )

        try:

            settings.starting_number = int(
                request.POST.get(
                    "starting_number",
                    1
                )
            )

        except (TypeError, ValueError):

            settings.starting_number = 1

        try:

            settings.number_digits = int(
                request.POST.get(
                    "number_digits",
                    5
                )
            )

        except (TypeError, ValueError):

            settings.number_digits = 5

        settings.automatic_numbering = (
            request.POST.get(
                "automatic_numbering"
            ) == "1"
        )

        settings.invoice_date_type = request.POST.get(
            "invoice_date_type",
            "today"
        )

        settings.due_date_mode = request.POST.get(
            "due_date_mode",
            "payment_terms"
        )

        settings.show_student_details = (
            request.POST.get(
                "show_student_details"
            ) == "1"
        )

        settings.show_course_details = (
            request.POST.get(
                "show_course_details"
            ) == "1"
        )

        settings.show_fee_breakdown = (
            request.POST.get(
                "show_fee_breakdown"
            ) == "1"
        )

        settings.show_gst_breakdown = (
            request.POST.get(
                "show_gst_breakdown"
            ) == "1"
        )

        settings.show_payment_status = (
            request.POST.get(
                "show_payment_status"
            ) == "1"
        )

        settings.show_balance_due = (
            request.POST.get(
                "show_balance_due"
            ) == "1"
        )

        settings.auto_total_calculation = (
            request.POST.get(
                "auto_total_calculation"
            ) == "1"
        )

        settings.auto_balance_calculation = (
            request.POST.get(
                "auto_balance_calculation"
            ) == "1"
        )

        settings.auto_pdf_generation = (
            request.POST.get(
                "auto_pdf_generation"
            ) == "1"
        )

        settings.allow_duplicate_invoice = (
            request.POST.get(
                "allow_duplicate_invoice"
            ) == "1"
        )

        settings.save()

        messages.success(
            request,
            "Invoice settings saved successfully."
        )

        return redirect(
            "billing_invoice_settings"
        )

    return render(
        request,
        "billing/billing_invoice_settings.html",
        {
            "company": company,
            "settings": settings,
            "appearance_settings": appearance_settings,
        }
    )


# ============================================================
# PAYMENT SETTINGS
# ============================================================

@login_required
def billing_payment_settings(request):

    company = get_billing_company(request)

    settings, _ = PaymentSettings.objects.get_or_create(
        company=company
    )

    appearance_settings, _ = (
        BillingAppearanceSettings.objects.get_or_create(
            company=company
        )
    )

    if request.method == "POST":

        settings.cash_enabled = (
            request.POST.get(
                "cash_enabled"
            ) == "1"
        )

        settings.upi_enabled = (
            request.POST.get(
                "upi_enabled"
            ) == "1"
        )

        settings.bank_enabled = (
            request.POST.get(
                "bank_enabled"
            ) == "1"
        )

        settings.card_enabled = (
            request.POST.get(
                "card_enabled"
            ) == "1"
        )

        settings.cheque_enabled = (
            request.POST.get(
                "cheque_enabled"
            ) == "1"
        )

        valid_payment_methods = {
            "cash",
            "upi",
            "bank",
            "card",
            "cheque",
        }

        default_payment_method = request.POST.get(
            "default_payment_method",
            "cash"
        )

        if default_payment_method not in valid_payment_methods:

            default_payment_method = "cash"

        settings.default_payment_method = (
            default_payment_method
        )

        settings.allow_partial_payment = (
            request.POST.get(
                "allow_partial_payment"
            ) == "1"
        )

        settings.require_reference = (
            request.POST.get(
                "require_reference"
            ) == "1"
        )

        settings.automatic_payment_status = (
            request.POST.get(
                "automatic_payment_status"
            ) == "1"
        )

        settings.generate_receipt = (
            request.POST.get(
                "generate_receipt"
            ) == "1"
        )

        settings.receipt_prefix = (
            request.POST.get(
                "receipt_prefix",
                "PAY"
            )
            .strip()
            .upper()
        )

        if not settings.receipt_prefix:
            settings.receipt_prefix = "PAY"

        try:

            receipt_digits = int(
                request.POST.get(
                    "receipt_digits",
                    "5"
                )
            )

        except (TypeError, ValueError):

            receipt_digits = 5

        if receipt_digits not in {
            3,
            4,
            5,
            6,
        }:

            receipt_digits = 5

        settings.receipt_digits = receipt_digits

        valid_receipt_formats = {
            "PREFIX-NUMBER",
            "PREFIX-YEAR-NUMBER",
            "YEAR-PREFIX-NUMBER",
        }

        receipt_format = request.POST.get(
            "receipt_format",
            "PREFIX-NUMBER"
        )

        if receipt_format not in valid_receipt_formats:

            receipt_format = "PREFIX-NUMBER"

        settings.receipt_format = receipt_format

        try:

            starting_number = int(
                request.POST.get(
                    "receipt_starting_number",
                    "1"
                )
            )

        except (TypeError, ValueError):

            starting_number = 1

        if starting_number < 1:
            starting_number = 1

        settings.receipt_starting_number = (
            starting_number
        )

        settings.online_payment_enabled = (
            request.POST.get(
                "online_payment_enabled"
            ) == "1"
        )

        settings.payment_confirmation = (
            request.POST.get(
                "payment_confirmation"
            ) == "1"
        )

        settings.payment_notes = (
            request.POST.get(
                "payment_notes",
                ""
            ).strip()
        )

        settings.save()

        messages.success(
            request,
            "Payment settings saved successfully."
        )

        return redirect(
            "billing_payment_settings"
        )

    return render(
        request,
        "billing/billing_payment_settings.html",
        {
            "company": company,
            "settings": settings,
            "appearance_settings": appearance_settings,
        }
    )


# ============================================================
# TAX & GST SETTINGS
# ============================================================

@login_required
def billing_tax_settings(request):

    company = get_billing_company(request)

    settings, _ = GSTSettings.objects.get_or_create(
        company=company
    )

    appearance_settings, _ = (
        BillingAppearanceSettings.objects.get_or_create(
            company=company,
            defaults={
                "theme": "light",
                "accent_color": "#2563eb",
            }
        )
    )

    if request.method == "POST":

        settings.is_active = (
            request.POST.get(
                "gst_enabled"
            ) == "1"
        )

        settings.gst_number = (
            request.POST.get(
                "gst_number",
                ""
            )
            .strip()
            .upper()
        )

        try:

            settings.default_gst_rate = Decimal(
                request.POST.get(
                    "default_gst_rate",
                    "18"
                )
            )

        except (
            InvalidOperation,
            TypeError,
            ValueError
        ):

            settings.default_gst_rate = Decimal(
                "18"
            )

        tax_mode = request.POST.get(
            "tax_mode",
            "exclusive"
        )

        if tax_mode not in {
            "exclusive",
            "inclusive",
        }:

            tax_mode = "exclusive"

        settings.tax_mode = tax_mode

        try:

            settings.cgst = Decimal(
                request.POST.get(
                    "cgst",
                    "9"
                )
            )

        except (
            InvalidOperation,
            TypeError,
            ValueError
        ):

            settings.cgst = Decimal("9")

        try:

            settings.sgst = Decimal(
                request.POST.get(
                    "sgst",
                    "9"
                )
            )

        except (
            InvalidOperation,
            TypeError,
            ValueError
        ):

            settings.sgst = Decimal("9")

        try:

            settings.igst = Decimal(
                request.POST.get(
                    "igst",
                    "18"
                )
            )

        except (
            InvalidOperation,
            TypeError,
            ValueError
        ):

            settings.igst = Decimal("18")

        settings.state = request.POST.get(
            "state",
            ""
        ).strip()

        settings.place_of_supply = request.POST.get(
            "place_of_supply",
            ""
        ).strip()

        settings.hsn_sac_code = request.POST.get(
            "hsn_sac_code",
            ""
        ).strip()

        settings.apply_gst_automatically = (
            request.POST.get(
                "apply_gst_automatically"
            ) == "1"
        )

        settings.show_gst_on_invoice = (
            request.POST.get(
                "show_gst_on_invoice"
            ) == "1"
        )

        settings.tax_inclusive_pricing = (
            request.POST.get(
                "tax_inclusive_pricing"
            ) == "1"
        )

        settings.save()

        messages.success(
            request,
            "Tax & GST settings saved successfully."
        )

        return redirect(
            "billing_tax_settings"
        )

    return render(
        request,
        "billing/billing_tax_settings.html",
        {
            "company": company,
            "settings": settings,
            "appearance_settings": appearance_settings,
        }
    )


# ============================================================
# FEE & DISCOUNT SETTINGS
# ============================================================

@login_required
def billing_fee_settings(request):

    company = get_billing_company(request)

    settings, _ = (
        FeeDiscountSettings.objects.get_or_create(
            company=company
        )
    )

    appearance_settings, _ = (
        BillingAppearanceSettings.objects.get_or_create(
            company=company
        )
    )

    if request.method == "POST":

        settings.fee_system_enabled = (
            request.POST.get(
                "fee_system_enabled"
            ) == "1"
        )

        settings.default_fee_type = request.POST.get(
            "default_fee_type",
            "Tuition Fee"
        )

        settings.allow_custom_fees = (
            request.POST.get(
                "allow_custom_fees"
            ) == "1"
        )

        settings.allow_discounts = (
            request.POST.get(
                "allow_discounts"
            ) == "1"
        )

        settings.default_discount_type = (
            request.POST.get(
                "default_discount_type",
                "percentage"
            )
        )

        try:

            settings.default_discount_value = Decimal(
                request.POST.get(
                    "default_discount_value",
                    "0"
                )
            )

        except (
            TypeError,
            ValueError,
            InvalidOperation
        ):

            settings.default_discount_value = Decimal(
                "0.00"
            )

        try:

            settings.maximum_discount = Decimal(
                request.POST.get(
                    "maximum_discount",
                    "100"
                )
            )

        except (
            TypeError,
            ValueError,
            InvalidOperation
        ):

            settings.maximum_discount = Decimal(
                "100.00"
            )

        settings.apply_discount_before_tax = (
            request.POST.get(
                "apply_discount_before_tax"
            ) == "1"
        )

        settings.round_fee_amounts = (
            request.POST.get(
                "round_fee_amounts"
            ) == "1"
        )

        settings.show_discount_on_invoice = (
            request.POST.get(
                "show_discount_on_invoice"
            ) == "1"
        )

        settings.save()

        messages.success(
            request,
            "Fee & Discount settings saved successfully."
        )

        return redirect(
            "billing_fee_settings"
        )

    return render(
        request,
        "billing/billing_fee_settings.html",
        {
            "company": company,
            "settings": settings,
            "appearance_settings": appearance_settings,
        }
    )


# ============================================================
# LATE FEE SETTINGS
# ============================================================

@login_required
def billing_late_fee_settings(request):

    company = get_billing_company(request)

    settings, _ = (
        LateFeeSettings.objects.get_or_create(
            company=company
        )
    )

    appearance_settings, _ = (
        BillingAppearanceSettings.objects.get_or_create(
            company=company
        )
    )

    if request.method == "POST":

        settings.enabled = (
            request.POST.get(
                "enabled"
            ) == "1"
        )

        try:

            settings.grace_period_days = max(
                0,
                int(
                    request.POST.get(
                        "grace_period_days",
                        0
                    )
                )
            )

        except (
            TypeError,
            ValueError
        ):

            settings.grace_period_days = 0

        late_fee_type = request.POST.get(
            "late_fee_type",
            "percentage"
        )

        if late_fee_type not in {
            "percentage",
            "fixed",
        }:

            late_fee_type = "percentage"

        settings.late_fee_type = late_fee_type

        try:

            late_fee_value = Decimal(
                request.POST.get(
                    "late_fee_value",
                    "0"
                )
            )

            settings.late_fee_value = max(
                Decimal("0.00"),
                late_fee_value
            )

        except (
            TypeError,
            ValueError,
            InvalidOperation
        ):

            settings.late_fee_value = Decimal(
                "0.00"
            )

        try:

            maximum_late_fee = Decimal(
                request.POST.get(
                    "maximum_late_fee",
                    "0"
                )
            )

            settings.maximum_late_fee = max(
                Decimal("0.00"),
                maximum_late_fee
            )

        except (
            TypeError,
            ValueError,
            InvalidOperation
        ):

            settings.maximum_late_fee = Decimal(
                "0.00"
            )

        settings.apply_automatically = (
            request.POST.get(
                "apply_automatically"
            ) == "1"
        )

        settings.apply_on_overdue = (
            request.POST.get(
                "apply_on_overdue"
            ) == "1"
        )

        settings.repeat_late_fee = (
            request.POST.get(
                "repeat_late_fee"
            ) == "1"
        )

        repeat_interval = request.POST.get(
            "repeat_interval",
            "monthly"
        )

        if repeat_interval not in {
            "once",
            "daily",
            "weekly",
            "monthly",
        }:

            repeat_interval = "monthly"

        settings.repeat_interval = repeat_interval

        settings.show_on_invoice = (
            request.POST.get(
                "show_on_invoice"
            ) == "1"
        )

        settings.late_fee_description = (
            request.POST.get(
                "late_fee_description",
                "Late payment fee"
            )
            .strip()
        )

        if not settings.late_fee_description:

            settings.late_fee_description = (
                "Late payment fee"
            )

        settings.save()

        messages.success(
            request,
            "Late Fee settings saved successfully."
        )

        return redirect(
            "billing_late_fee_settings"
        )

    return render(
        request,
        "billing/billing_late_fee_settings.html",
        {
            "company": company,
            "settings": settings,
            "appearance_settings": appearance_settings,
        }
    )


# ============================================================
# PAYMENT REMINDER SETTINGS
# ============================================================

@login_required
def billing_reminder_settings(request):

    company = get_billing_company(request)

    reminder_settings, _ = (
        PaymentReminderSettings.objects.get_or_create(
            company=company
        )
    )

    appearance_settings, _ = (
        BillingAppearanceSettings.objects.get_or_create(
            company=company
        )
    )

    if request.method == "POST":

        reminder_settings.enabled = (
            request.POST.get(
                "enabled"
            ) == "1"
        )

        reminder_settings.reminder_before_due = (
            request.POST.get(
                "reminder_before_due"
            ) == "1"
        )

        try:

            before_due_days = int(
                request.POST.get(
                    "before_due_days",
                    3
                )
            )

            reminder_settings.before_due_days = max(
                0,
                before_due_days
            )

        except (
            TypeError,
            ValueError
        ):

            reminder_settings.before_due_days = 3

        reminder_settings.reminder_on_due_date = (
            request.POST.get(
                "reminder_on_due_date"
            ) == "1"
        )

        reminder_settings.reminder_after_due = (
            request.POST.get(
                "reminder_after_due"
            ) == "1"
        )

        try:

            after_due_days = int(
                request.POST.get(
                    "after_due_days",
                    1
                )
            )

            reminder_settings.after_due_days = max(
                0,
                after_due_days
            )

        except (
            TypeError,
            ValueError
        ):

            reminder_settings.after_due_days = 1

        reminder_settings.repeat_reminders = (
            request.POST.get(
                "repeat_reminders"
            ) == "1"
        )

        repeat_interval = request.POST.get(
            "repeat_interval",
            "weekly"
        )

        allowed_intervals = {
            "daily",
            "weekly",
            "monthly",
        }

        if repeat_interval not in allowed_intervals:

            repeat_interval = "weekly"

        reminder_settings.repeat_interval = (
            repeat_interval
        )

        try:

            maximum_reminders = int(
                request.POST.get(
                    "maximum_reminders",
                    3
                )
            )

            reminder_settings.maximum_reminders = max(
                1,
                maximum_reminders
            )

        except (
            TypeError,
            ValueError
        ):

            reminder_settings.maximum_reminders = 3

        reminder_settings.email_reminders = (
            request.POST.get(
                "email_reminders"
            ) == "1"
        )

        reminder_settings.sms_reminders = (
            request.POST.get(
                "sms_reminders"
            ) == "1"
        )

        reminder_settings.whatsapp_reminders = (
            request.POST.get(
                "whatsapp_reminders"
            ) == "1"
        )

        reminder_settings.show_invoice_number = (
            request.POST.get(
                "show_invoice_number"
            ) == "1"
        )

        reminder_settings.show_due_amount = (
            request.POST.get(
                "show_due_amount"
            ) == "1"
        )

        reminder_settings.show_due_date = (
            request.POST.get(
                "show_due_date"
            ) == "1"
        )

        reminder_settings.reminder_message = (
            request.POST.get(
                "reminder_message",
                ""
            )
            .strip()
        )

        reminder_settings.save()

        messages.success(
            request,
            "Payment reminder settings saved successfully."
        )

        return redirect(
            "billing_reminder_settings"
        )

    return render(
        request,
        "billing/billing_reminder_settings.html",
        {
            "company": company,
            "settings": reminder_settings,
            "appearance_settings": appearance_settings,
        }
    )


# ============================================================
# BILLING APPEARANCE SETTINGS
# ============================================================

@login_required
def billing_appearance_settings(request):

    company = get_billing_company(request)

    billing_appearance, _ = (
        BillingAppearanceSettings.objects.get_or_create(
            company=company
        )
    )

    if request.method == "POST":

        theme = request.POST.get(
            "theme",
            "light"
        )

        if theme not in {
            "light",
            "dark",
        }:

            theme = "light"

        primary_color = request.POST.get(
            "primary_color",
            "#2563EB"
        )

        accent_color = request.POST.get(
            "accent_color",
            "#3B1C35"
        )

        table_header_background = request.POST.get(
            "table_header_background",
            "#3B1C35"
        )

        table_header_text_color = request.POST.get(
            "table_header_text_color",
            "#FFFFFF"
        )

        font_family = request.POST.get(
            "font_family",
            "Arial"
        )

        allowed_fonts = {
            "Arial",
            "Inter",
            "Poppins",
            "Georgia",
        }

        if font_family not in allowed_fonts:
            font_family = "Arial"

        font_size = request.POST.get(
            "font_size",
            "medium"
        )

        if font_size not in {
            "small",
            "medium",
            "large",
        }:

            font_size = "medium"

        invoice_layout = request.POST.get(
            "invoice_layout",
            "standard"
        )

        if invoice_layout not in {
            "standard",
            "modern",
            "compact",
        }:

            invoice_layout = "standard"

        logo_position = request.POST.get(
            "logo_position",
            "left"
        )

        if logo_position not in {
            "left",
            "center",
            "right",
        }:

            logo_position = "left"

        invoice_title = request.POST.get(
            "invoice_title",
            "INVOICE"
        ).strip()

        if not invoice_title:
            invoice_title = "INVOICE"

        date_format = request.POST.get(
            "date_format",
            "DD/MM/YYYY"
        )

        if date_format not in {
            "DD/MM/YYYY",
            "MM/DD/YYYY",
            "YYYY-MM-DD",
        }:

            date_format = "DD/MM/YYYY"

        watermark_text = request.POST.get(
            "watermark_text",
            ""
        ).strip()

        try:

            watermark_opacity = int(
                request.POST.get(
                    "watermark_opacity",
                    10
                )
            )

            watermark_opacity = max(
                0,
                min(
                    watermark_opacity,
                    100
                )
            )

        except (
            TypeError,
            ValueError
        ):

            watermark_opacity = 10

        billing_appearance.theme = theme

        billing_appearance.primary_color = (
            primary_color
        )

        billing_appearance.accent_color = (
            accent_color
        )

        billing_appearance.table_header_background = (
            table_header_background
        )

        billing_appearance.table_header_text_color = (
            table_header_text_color
        )

        billing_appearance.font_family = (
            font_family
        )

        billing_appearance.font_size = (
            font_size
        )

        billing_appearance.invoice_layout = (
            invoice_layout
        )

        billing_appearance.logo_position = (
            logo_position
        )

        billing_appearance.invoice_title = (
            invoice_title
        )

        billing_appearance.date_format = (
            date_format
        )

        billing_appearance.show_company_logo = (
            "show_company_logo" in request.POST
        )

        billing_appearance.show_company_details = (
            "show_company_details" in request.POST
        )

        billing_appearance.show_customer_details = (
            "show_customer_details" in request.POST
        )

        billing_appearance.show_payment_details = (
            "show_payment_details" in request.POST
        )

        billing_appearance.show_tax_details = (
            "show_tax_details" in request.POST
        )

        billing_appearance.show_signature = (
            "show_signature" in request.POST
        )

        billing_appearance.show_qr_code = (
            "show_qr_code" in request.POST
        )

        billing_appearance.show_invoice_footer = (
            "show_invoice_footer" in request.POST
        )

        billing_appearance.show_watermark = (
            "show_watermark" in request.POST
        )

        billing_appearance.watermark_text = (
            watermark_text
        )

        billing_appearance.watermark_opacity = (
            watermark_opacity
        )

        billing_appearance.custom_footer_text = (
            request.POST.get(
                "custom_footer_text",
                ""
            )
            .strip()
        )

        billing_appearance.save()

        messages.success(
            request,
            "Billing appearance settings saved successfully."
        )

        return redirect(
            "billing_appearance_settings"
        )

    return render(
        request,
        "billing/billing_appearance_settings.html",
        {
            "billing_appearance": billing_appearance,
            "company": company,
        }
    )


# ============================================================
# BANK & PAYMENT SETTINGS
# ============================================================

@login_required
def billing_bank_settings(request):

    company = get_billing_company(request)

    settings, _ = (
        BankPaymentSettings.objects.get_or_create(
            company=company
        )
    )

    appearance, _ = (
        BillingAppearanceSettings.objects.get_or_create(
            company=company
        )
    )

    if request.method == "POST":

        settings.bank_name = request.POST.get(
            "bank_name",
            ""
        ).strip()

        settings.account_holder_name = request.POST.get(
            "account_holder_name",
            ""
        ).strip()

        settings.account_number = request.POST.get(
            "account_number",
            ""
        ).strip()

        account_type = request.POST.get(
            "account_type",
            "current"
        )

        if account_type not in {
            "savings",
            "current",
            "cash_credit",
        }:

            account_type = "current"

        settings.account_type = account_type

        settings.ifsc_code = (
            request.POST.get(
                "ifsc_code",
                ""
            )
            .strip()
            .upper()
        )

        settings.branch_name = request.POST.get(
            "branch_name",
            ""
        ).strip()

        settings.bank_address = request.POST.get(
            "bank_address",
            ""
        ).strip()

        settings.upi_enabled = (
            request.POST.get(
                "upi_enabled"
            ) == "1"
        )

        settings.upi_id = request.POST.get(
            "upi_id",
            ""
        ).strip()

        settings.upi_name = request.POST.get(
            "upi_name",
            ""
        ).strip()

        settings.show_bank_details = (
            request.POST.get(
                "show_bank_details"
            ) == "1"
        )

        settings.show_upi_details = (
            request.POST.get(
                "show_upi_details"
            ) == "1"
        )

        settings.show_on_invoice = (
            request.POST.get(
                "show_on_invoice"
            ) == "1"
        )

        settings.payment_instructions = (
            request.POST.get(
                "payment_instructions",
                ""
            )
            .strip()
        )

        settings.save()

        messages.success(
            request,
            "Bank & Payment settings saved successfully."
        )

        return redirect(
            "billing_bank_settings"
        )

    return render(
        request,
        "billing/billing_bank_settings.html",
        {
            "company": company,
            "settings": settings,
            "appearance": appearance,
        }
    )


# ============================================================
# BILLING LOGOUT
# ============================================================

@login_required
def logout_billing(request):

    if request.method == "POST":

        logout(request)

        messages.success(
            request,
            "You have been logged out successfully."
        )

        return redirect(
            "billing_staff_login"
        )

    return render(
        request,
        "billing/logout_billing_confirm.html"
    )


# ============================================================
# BILLING COMPANY PROFILE
# ============================================================

@login_required
def billing_company_profile_settings(request):

    company = get_billing_company(request)

    appearance_settings, _ = (
        BillingAppearanceSettings.objects.get_or_create(
            company=company
        )
    )

    profile, _ = BillingCompanyProfile.objects.get_or_create(
        company=company,
        defaults={
            "company_name": company.company_name
        }
    )

    if request.method == "POST":

        profile.company_name = request.POST.get(
            "company_name",
            ""
        ).strip()

        profile.email = request.POST.get(
            "email",
            ""
        ).strip()

        profile.phone = request.POST.get(
            "phone",
            ""
        ).strip()

        profile.website = request.POST.get(
            "website",
            ""
        ).strip()

        profile.address = request.POST.get(
            "address",
            ""
        ).strip()

        profile.city = request.POST.get(
            "city",
            ""
        ).strip()

        profile.state = request.POST.get(
            "state",
            ""
        ).strip()

        profile.pincode = request.POST.get(
            "pincode",
            ""
        ).strip()

        profile.gst_number = request.POST.get(
            "gst_number",
            ""
        ).strip()

        if request.FILES.get("company_logo"):

            profile.company_logo = request.FILES[
                "company_logo"
            ]

        profile.save()

        messages.success(
            request,
            "Company profile updated successfully."
        )

        return redirect(
            "billing_company_profile_settings"
        )

    return render(
        request,
        "billing/billing_company_profile_settings.html",
        {
            "profile": profile,
            "company": company,
            "appearance_settings": appearance_settings,
        }
    )