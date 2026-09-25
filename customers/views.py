from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from students.decorators import company_type_required
from django.db.models import Sum
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from app.models import Company
from .models import CustomerPayment
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .models import CustomerCompanyProfile
from .forms import CustomerCompanyProfileForm
from .models import CustomerInvoiceSettings
from .forms import CustomerInvoiceSettingsForm
from .models import CustomerPaymentSettings
from .forms import CustomerPaymentSettingsForm
from .models import CustomerTaxGSTSettings
from .forms import CustomerTaxGSTSettingsForm
from .models import CustomerDiscountSettings
from .forms import CustomerDiscountSettingsForm
from .models import CustomerNotificationSettings
from .forms import CustomerNotificationSettingsForm
from .forms import CustomerInvoiceAppearanceForm
from .models import CustomerInvoiceAppearance
from .models import CustomerBankPaymentSettings
from .forms import CustomerBankPaymentSettingsForm
from .models import CustomerSecuritySettings
from .forms import CustomerSecuritySettingsForm
from decimal import Decimal
from datetime import datetime
from decimal import Decimal, InvalidOperation
from django.contrib.auth import logout


from .models import (
    Customer,
    Product,
    CustomerInvoice,
    CustomerPayment,
    CustomerGSTSettings,
)
from app.models import Company


def get_company(request):

    if not request.user.is_authenticated:
        return None

    if request.user.is_superuser:
        return None

    return Company.objects.filter(
        user=request.user
    ).first()

@login_required
@company_type_required("customer")
def admin_dashboard(request):
    companies = Company.objects.all()

    return render(request, "admin/dashboard.html", {
        "companies": companies,
    })

@login_required(login_url="login")
@company_type_required("customer")
def product_dashboard(request):

    company = get_company(request)

    if company is None:
        return HttpResponseForbidden(
            "No company is associated with this account."
        )

    # Company Profile
    company_profile, _ = CustomerCompanyProfile.objects.get_or_create(
        user=request.user,
        defaults={
            "company_name": company.company_name,
            "email": request.user.email,
            "owner_name": request.user.get_full_name(),
        }
    )

    customers = Customer.objects.filter(
        company=company
    )

    products = Product.objects.filter(
        company=company
    )

    invoices = CustomerInvoice.objects.filter(
        company=company
    )

    payments = CustomerPayment.objects.filter(
        company=company
    )

    appearance, _ = CustomerInvoiceAppearance.objects.get_or_create(
        company=company,
        defaults={
            "theme": "light",
            "accent_color": "#2563eb",
        }
    )

    total_customers = customers.count()
    total_products = products.count()
    total_invoices = invoices.count()

    paid_invoices = invoices.filter(
        payment_status__iexact="Paid"
    ).count()

    pending_invoices = invoices.filter(
        payment_status__iexact="Pending"
    ).count()

    total_revenue = (
        payments.aggregate(
            total=Sum("amount")
        )["total"] or Decimal("0.00")
    )

    recent_invoices = invoices.order_by(
        "-created_at"
    )[:5]

    recent_payments = payments.order_by(
        "-payment_date"
    )[:5]

    return render(
        request,
        "customers/product_dashboard.html",
        {
            "company": company,
            "company_profile": company_profile,   # Added

            "appearance": appearance,
            "theme": appearance.theme or "light",
            "accent_color": (
                appearance.accent_color or "#2563eb"
            ),

            "customers": customers,
            "products": products,
            "invoices": invoices,
            "payments": payments,

            "total_customers": total_customers,
            "total_products": total_products,
            "total_invoices": total_invoices,

            "paid_invoices": paid_invoices,
            "pending_invoices": pending_invoices,

            "total_revenue": total_revenue,

            "recent_invoices": recent_invoices,
            "recent_payments": recent_payments,
        }
    )

@login_required
@company_type_required("customer")
def customer_list(request):

    company = get_company(request)

    if company is None:
        return render(
            request,
            "customers/customer_list.html",
            {
                "customers": [],
                "company": None,
                "appearance": None,
                "theme": "light",
                "accent_color": "#2563eb",
            }
        )

    customers = Customer.objects.filter(
        company=company
    ).order_by("-id")

    appearance, created = CustomerInvoiceAppearance.objects.get_or_create(
        company=company
    )

    return render(
        request,
        "customers/customer_list.html",
        {
            "customers": customers,
            "company": company,
            "appearance": appearance,
            "theme": appearance.theme or "light",
            "accent_color": appearance.accent_color or "#2563eb",
        },
    )


@login_required(login_url="login")
@company_type_required("customer")
def customer_create(request):

    company = get_company(request)

    if company is None:
        return redirect("customer_list")

    appearance, created = CustomerInvoiceAppearance.objects.get_or_create(
        company=company
    )

    if request.method == "POST":

        name = request.POST.get("name", "").strip()
        phone = request.POST.get("phone", "").strip()
        email = request.POST.get("email", "").strip()
        address = request.POST.get("address", "").strip()

        Customer.objects.create(
            company=company,
            name=name,
            phone=phone,
            email=email,
            address=address,
        )

        return redirect("customer_list")

    context = {
        "company": company,
        "appearance": appearance,
        "theme": appearance.theme or "light",
        "accent_color": appearance.accent_color or "#2563eb",
    }

    return render(
        request,
        "customers/customer_form.html",
        context
    )

@login_required(login_url="login")
@company_type_required("customer")
def customer_edit(request, customer_id):

    company = get_company(request)

    if company is None:
        return redirect("customer_list")

    customer = get_object_or_404(
        Customer,
        id=customer_id,
        company=company
    )

    appearance, created = CustomerInvoiceAppearance.objects.get_or_create(
        company=company
    )

    if request.method == "POST":

        name = request.POST.get("name", "").strip()
        phone = request.POST.get("phone", "").strip()
        email = request.POST.get("email", "").strip()
        address = request.POST.get("address", "").strip()

        customer.name = name
        customer.phone = phone
        customer.email = email
        customer.address = address

        customer.save()

        return redirect("customer_list")

    context = {
        "company": company,
        "customer": customer,
        "appearance": appearance,
        "theme": appearance.theme or "light",
        "accent_color": appearance.accent_color or "#2563eb",
        "edit_mode": True,
    }

    return render(
        request,
        "customers/customer_form.html",
        context
    )
@login_required(login_url="login")
@company_type_required("customer")
def customer_delete(request, customer_id):

    company = get_company(request)

    if company is None:
        return redirect("customer_list")

    customer = get_object_or_404(
        Customer,
        id=customer_id,
        company=company,
    )

    if request.method == "POST":

        customer.delete()

        return redirect("customer_list")

    return render(
        request,
        "customers/customer_confirm_delete.html",
        {
            "customer": customer,
            "company": company,
        }
    )
@login_required
@company_type_required("customer")
def product_list(request):

    try:
        company = Company.objects.get(user=request.user)

    except Company.DoesNotExist:
        messages.error(request, "Company not found.")
        return redirect("login")

    appearance, created = CustomerInvoiceAppearance.objects.get_or_create(
        company=company
    )

    products = Product.objects.filter(
        company=company
    ).order_by("-id")

    return render(
        request,
        "customers/product_list.html",
        {
            "company": company,
            "products": products,
            "appearance": appearance,

            "theme": appearance.theme,

            "accent_color": appearance.accent_color,
        },
    )

@login_required(login_url="login")
@company_type_required("customer")
def product_create(request):

    try:
        company = Company.objects.get(user=request.user)

    except Company.DoesNotExist:
        messages.error(request, "Company not found.")
        return redirect("login")

    appearance, created = CustomerInvoiceAppearance.objects.get_or_create(
        company=company
    )

    if request.method == "POST":

        name = request.POST.get("name", "").strip()
        sku = request.POST.get("sku", "").strip()
        category = request.POST.get("category", "").strip()
        brand = request.POST.get("brand", "").strip()

        purchase_price = request.POST.get(
            "purchase_price",
            "0"
        ).strip()

        selling_price = request.POST.get(
            "selling_price",
            "0"
        ).strip()

        gst = request.POST.get(
            "gst",
            "0"
        ).strip()

        discount = request.POST.get(
            "discount",
            "0"
        ).strip()

        stock = request.POST.get(
            "stock",
            "0"
        ).strip()

        minimum_stock = request.POST.get(
            "minimum_stock",
            "0"
        ).strip()

        supplier = request.POST.get(
            "supplier",
            ""
        ).strip()

        status = request.POST.get(
            "status",
            "Available"
        ).strip()

        description = request.POST.get(
            "description",
            ""
        ).strip()

        image = request.FILES.get("image")

        # Product name validation

        if not name:

            messages.error(
                request,
                "Product name is required."
            )

            return render(
                request,
                "customers/product_form.html",
                {
                    "company": company,
                    "appearance": appearance,
                    "theme": appearance.theme,
                    "accent_color": appearance.accent_color,
                }
            )

        # Convert decimal values

        try:

            purchase_price = Decimal(
                purchase_price or "0"
            )

            selling_price = Decimal(
                selling_price or "0"
            )

            gst = Decimal(
                gst or "0"
            )

            discount = Decimal(
                discount or "0"
            )

        except (InvalidOperation, ValueError, TypeError):

            messages.error(
                request,
                "Please enter valid price, GST and discount values."
            )

            return render(
                request,
                "customers/product_form.html",
                {
                    "company": company,
                    "appearance": appearance,
                    "theme": appearance.theme,
                    "accent_color": appearance.accent_color,
                }
            )

        # Convert integer values

        try:

            stock = int(stock or 0)

            minimum_stock = int(
                minimum_stock or 0
            )

        except (ValueError, TypeError):

            messages.error(
                request,
                "Stock values must contain valid numbers."
            )

            return render(
                request,
                "customers/product_form.html",
                {
                    "company": company,
                    "appearance": appearance,
                    "theme": appearance.theme,
                    "accent_color": appearance.accent_color,
                }
            )

        # Validation

        if purchase_price < 0:

            messages.error(
                request,
                "Purchase price cannot be negative."
            )

            return render(
                request,
                "customers/product_form.html",
                {
                    "company": company,
                    "appearance": appearance,
                    "theme": appearance.theme,
                    "accent_color": appearance.accent_color,
                }
            )

        if selling_price < 0:

            messages.error(
                request,
                "Selling price cannot be negative."
            )

            return render(
                request,
                "customers/product_form.html",
                {
                    "company": company,
                    "appearance": appearance,
                    "theme": appearance.theme,
                    "accent_color": appearance.accent_color,
                }
            )

        if gst < 0 or gst > 100:

            messages.error(
                request,
                "GST must be between 0 and 100."
            )

            return render(
                request,
                "customers/product_form.html",
                {
                    "company": company,
                    "appearance": appearance,
                    "theme": appearance.theme,
                    "accent_color": appearance.accent_color,
                }
            )

        if discount < 0 or discount > 100:

            messages.error(
                request,
                "Discount must be between 0 and 100."
            )

            return render(
                request,
                "customers/product_form.html",
                {
                    "company": company,
                    "appearance": appearance,
                    "theme": appearance.theme,
                    "accent_color": appearance.accent_color,
                }
            )

        if stock < 0:

            messages.error(
                request,
                "Stock cannot be negative."
            )

            return render(
                request,
                "customers/product_form.html",
                {
                    "company": company,
                    "appearance": appearance,
                    "theme": appearance.theme,
                    "accent_color": appearance.accent_color,
                }
            )

        if minimum_stock < 0:

            messages.error(
                request,
                "Minimum stock cannot be negative."
            )

            return render(
                request,
                "customers/product_form.html",
                {
                    "company": company,
                    "appearance": appearance,
                    "theme": appearance.theme,
                    "accent_color": appearance.accent_color,
                }
            )

        # Create product

        Product.objects.create(

            company=company,

            name=name,

            sku=sku,

            category=category,

            brand=brand,

            purchase_price=purchase_price,

            price=selling_price,

            gst=gst,

            discount=discount,

            stock=stock,

            minimum_stock=minimum_stock,

            supplier=supplier,

            status=status,

            description=description,

            image=image,
        )

        messages.success(
            request,
            "Product added successfully."
        )

        return redirect("product_list")

    return render(
        request,
        "customers/product_form.html",
        {
            "company": company,
            "appearance": appearance,
            "theme": appearance.theme,
            "accent_color": appearance.accent_color,
        }
    )
@login_required(login_url="login")
@company_type_required("customer")
def product_update(request, product_id):

    try:
        company = Company.objects.get(user=request.user)

    except Company.DoesNotExist:
        messages.error(request, "Company not found.")
        return redirect("login")

    appearance, created = CustomerInvoiceAppearance.objects.get_or_create(
        company=company
    )

    # Important:
    # Only get the product belonging to the logged-in company
    product = get_object_or_404(
        Product,
        id=product_id,
        company=company
    )

    if request.method == "POST":

        name = request.POST.get("name", "").strip()
        category = request.POST.get("category", "").strip()
        price = request.POST.get("selling_price", "").strip()
        stock = request.POST.get("stock", "0").strip()
        description = request.POST.get("description", "").strip()

        # Basic validation
        if not name:

            messages.error(
                request,
                "Product name is required."
            )

            return render(
                request,
                "customers/product_form.html",
                {
                    "company": company,
                    "product": product,
                    "edit_mode": True,
                    "appearance": appearance,
                    "theme": appearance.theme,
                    "accent_color": appearance.accent_color,
                },
            )

        try:

            price = float(price or 0)
            stock = int(stock or 0)

        except (ValueError, TypeError):

            messages.error(
                request,
                "Selling price and stock must contain valid numbers."
            )

            return render(
                request,
                "customers/product_form.html",
                {
                    "company": company,
                    "product": product,
                    "edit_mode": True,
                    "appearance": appearance,
                    "theme": appearance.theme,
                    "accent_color": appearance.accent_color,
                },
            )

        if price < 0:

            messages.error(
                request,
                "Selling price cannot be negative."
            )

            return render(
                request,
                "customers/product_form.html",
                {
                    "company": company,
                    "product": product,
                    "edit_mode": True,
                    "appearance": appearance,
                    "theme": appearance.theme,
                    "accent_color": appearance.accent_color,
                },
            )

        if stock < 0:

            messages.error(
                request,
                "Stock cannot be negative."
            )

            return render(
                request,
                "customers/product_form.html",
                {
                    "company": company,
                    "product": product,
                    "edit_mode": True,
                    "appearance": appearance,
                    "theme": appearance.theme,
                    "accent_color": appearance.accent_color,
                },
            )

        # Update existing product
        product.name = name
        product.category = category
        product.price = price
        product.stock = stock
        product.description = description

        product.save()

        messages.success(
            request,
            "Product updated successfully."
        )

        return redirect("product_list")

    return render(
        request,
        "customers/product_form.html",
        {
            "company": company,
            "product": product,
            "edit_mode": True,
            "appearance": appearance,
            "theme": appearance.theme,
            "accent_color": appearance.accent_color,
        },
    )

@login_required(login_url="login")
@company_type_required("customer")
def product_delete(request, product_id):

    try:
        company = Company.objects.get(user=request.user)

    except Company.DoesNotExist:
        messages.error(request, "Company not found.")
        return redirect("login")

    appearance, created = CustomerInvoiceAppearance.objects.get_or_create(
        company=company
    )

    # Only find the product belonging to this company
    product = get_object_or_404(
        Product,
        id=product_id,
        company=company
    )

    if request.method == "POST":

        product_name = product.name

        product.delete()

        messages.success(
            request,
            f'Product "{product_name}" deleted successfully.'
        )

        return redirect("product_list")

    return render(
        request,
        "customers/product_confirm_delete.html",
        {
            "company": company,
            "product": product,
            "appearance": appearance,
            "theme": appearance.theme,
            "accent_color": appearance.accent_color,
        },
    )




@login_required(login_url="login")
@company_type_required("customer")
def invoice_list(request):

    company = get_company(request)

    if company is None:
        messages.error(
            request,
            "Company not found."
        )

        return redirect("login")

    invoices = CustomerInvoice.objects.filter(
        company=company
    ).order_by(
        "-created_at"
    )

    total_invoices = invoices.count()

    paid_invoices = invoices.filter(
        payment_status__iexact="Paid"
    ).count()

    pending_invoices = invoices.filter(
        payment_status__iexact="Pending"
    ).count()

    total_revenue = invoices.filter(
        payment_status__iexact="Paid"
    ).aggregate(
        total=Sum("total_amount")
    )["total"] or Decimal("0.00")

    appearance, created = (
        CustomerInvoiceAppearance.objects.get_or_create(
            company=company
        )
    )

    context = {
        "invoices": invoices,
        "total_invoices": total_invoices,
        "paid_invoices": paid_invoices,
        "pending_invoices": pending_invoices,
        "total_revenue": total_revenue,
        "theme": appearance.theme,
        "accent_color": appearance.accent_color,
    }

    return render(
        request,
        "customers/invoice_list.html",
        context
    )


@login_required(login_url="login")
@company_type_required("customer")
def invoice_create(request):

    company = get_company(request)

    if company is None:
        messages.error(request, "Company not found.")
        return redirect("login")

    customers = Customer.objects.filter(
        company=company
    ).order_by("name")

    products = Product.objects.filter(
        company=company
    ).order_by("name")

    appearance, created = CustomerInvoiceAppearance.objects.get_or_create(
        company=company,
        defaults={
            "theme": "light",
            "accent_color": "#2563eb",
        }
    )

    if request.method == "POST":

        # ------------------------------------------
        # GET FORM VALUES
        # ------------------------------------------

        invoice_number = request.POST.get(
            "invoice_number",
            ""
        ).strip()

        customer_id = request.POST.get("customer")

        product_id = request.POST.get("product")

        invoice_date = request.POST.get("invoice_date")

        due_date = request.POST.get("due_date")

        quantity = request.POST.get(
            "quantity",
            "1"
        ).strip()

        unit_price = request.POST.get(
            "unit_price",
            "0"
        ).strip()

        gst = request.POST.get(
            "gst",
            "0"
        ).strip()

        payment_status = request.POST.get(
            "payment_status",
            "Pending"
        ).strip()

        notes = request.POST.get(
            "notes",
            ""
        ).strip()

        # ------------------------------------------
        # INVOICE NUMBER
        # ------------------------------------------

        if not invoice_number:

            messages.error(
                request,
                "Invoice number is required."
            )

            return render(
                request,
                "customers/invoice_form.html",
                {
                    "customers": customers,
                    "products": products,
                    "theme": appearance.theme or "light",
                    "accent_color": (
                        appearance.accent_color
                        or "#2563eb"
                    ),
                }
            )

        # ------------------------------------------
        # DUPLICATE INVOICE NUMBER
        # ------------------------------------------

        invoice_exists = CustomerInvoice.objects.filter(
            company=company,
            invoice_number=invoice_number
        ).exists()

        if invoice_exists:

            messages.error(
                request,
                f"Invoice number '{invoice_number}' already exists."
            )

            return render(
                request,
                "customers/invoice_form.html",
                {
                    "customers": customers,
                    "products": products,
                    "theme": appearance.theme or "light",
                    "accent_color": (
                        appearance.accent_color
                        or "#2563eb"
                    ),
                }
            )

        # ------------------------------------------
        # CUSTOMER
        # ------------------------------------------

        customer = Customer.objects.filter(
            id=customer_id,
            company=company
        ).first()

        if customer is None:

            messages.error(
                request,
                "Please select a valid customer."
            )

            return render(
                request,
                "customers/invoice_form.html",
                {
                    "customers": customers,
                    "products": products,
                    "theme": appearance.theme or "light",
                    "accent_color": (
                        appearance.accent_color
                        or "#2563eb"
                    ),
                }
            )

        # ------------------------------------------
        # PRODUCT
        # ------------------------------------------

        product = Product.objects.filter(
            id=product_id,
            company=company
        ).first()

        if product is None:

            messages.error(
                request,
                "Please select a valid product."
            )

            return render(
                request,
                "customers/invoice_form.html",
                {
                    "customers": customers,
                    "products": products,
                    "theme": appearance.theme or "light",
                    "accent_color": (
                        appearance.accent_color
                        or "#2563eb"
                    ),
                }
            )

        # ------------------------------------------
        # INVOICE DATE
        # ------------------------------------------

        if not invoice_date:

            messages.error(
                request,
                "Invoice date is required."
            )

            return render(
                request,
                "customers/invoice_form.html",
                {
                    "customers": customers,
                    "products": products,
                    "theme": appearance.theme or "light",
                    "accent_color": (
                        appearance.accent_color
                        or "#2563eb"
                    ),
                }
            )

        # ------------------------------------------
        # DUE DATE
        # ------------------------------------------

        if not due_date:

            messages.error(
                request,
                "Due date is required."
            )

            return render(
                request,
                "customers/invoice_form.html",
                {
                    "customers": customers,
                    "products": products,
                    "theme": appearance.theme or "light",
                    "accent_color": (
                        appearance.accent_color
                        or "#2563eb"
                    ),
                }
            )

        # ------------------------------------------
        # CONVERT DATES
        # ------------------------------------------

        try:

            invoice_date_obj = datetime.strptime(
                invoice_date,
                "%Y-%m-%d"
            ).date()

            due_date_obj = datetime.strptime(
                due_date,
                "%Y-%m-%d"
            ).date()

        except ValueError:

            messages.error(
                request,
                "Please enter valid invoice and due dates."
            )

            return render(
                request,
                "customers/invoice_form.html",
                {
                    "customers": customers,
                    "products": products,
                    "theme": appearance.theme or "light",
                    "accent_color": (
                        appearance.accent_color
                        or "#2563eb"
                    ),
                }
            )

        # ------------------------------------------
        # DATE VALIDATION
        # ------------------------------------------

        if due_date_obj < invoice_date_obj:

            messages.error(
                request,
                "Due date cannot be earlier than invoice date."
            )

            return render(
                request,
                "customers/invoice_form.html",
                {
                    "customers": customers,
                    "products": products,
                    "theme": appearance.theme or "light",
                    "accent_color": (
                        appearance.accent_color
                        or "#2563eb"
                    ),
                }
            )

        # ------------------------------------------
        # CONVERT NUMERIC VALUES
        # ------------------------------------------

        try:

            quantity = Decimal(
                quantity or "1"
            )

            unit_price = Decimal(
                unit_price or "0"
            )

            gst = Decimal(
                gst or "0"
            )

        except (
            InvalidOperation,
            ValueError,
            TypeError
        ):

            messages.error(
                request,
                "Please enter valid numeric values."
            )

            return render(
                request,
                "customers/invoice_form.html",
                {
                    "customers": customers,
                    "products": products,
                    "theme": appearance.theme or "light",
                    "accent_color": (
                        appearance.accent_color
                        or "#2563eb"
                    ),
                }
            )

        # ------------------------------------------
        # QUANTITY VALIDATION
        # ------------------------------------------

        if quantity <= 0:

            messages.error(
                request,
                "Quantity must be greater than zero."
            )

            return render(
                request,
                "customers/invoice_form.html",
                {
                    "customers": customers,
                    "products": products,
                    "theme": appearance.theme or "light",
                    "accent_color": (
                        appearance.accent_color
                        or "#2563eb"
                    ),
                }
            )

        # ------------------------------------------
        # UNIT PRICE VALIDATION
        # ------------------------------------------

        if unit_price < 0:

            messages.error(
                request,
                "Unit price cannot be negative."
            )

            return render(
                request,
                "customers/invoice_form.html",
                {
                    "customers": customers,
                    "products": products,
                    "theme": appearance.theme or "light",
                    "accent_color": (
                        appearance.accent_color
                        or "#2563eb"
                    ),
                }
            )

        # ------------------------------------------
        # GST VALIDATION
        # ------------------------------------------

        if gst < 0 or gst > 100:

            messages.error(
                request,
                "GST must be between 0 and 100."
            )

            return render(
                request,
                "customers/invoice_form.html",
                {
                    "customers": customers,
                    "products": products,
                    "theme": appearance.theme or "light",
                    "accent_color": (
                        appearance.accent_color
                        or "#2563eb"
                    ),
                }
            )

        # ------------------------------------------
        # PAYMENT STATUS VALIDATION
        # ------------------------------------------

        valid_statuses = [
            "Paid",
            "Partial",
            "Pending",
            "Overdue",
        ]

        if payment_status not in valid_statuses:

            payment_status = "Pending"

        # ------------------------------------------
        # CALCULATE SUBTOTAL
        # ------------------------------------------

        subtotal = quantity * unit_price

        # ------------------------------------------
        # CALCULATE GST
        # ------------------------------------------

        gst_amount = (
            subtotal * gst / Decimal("100")
        )

        gst_amount = gst_amount.quantize(
            Decimal("0.01")
        )

        # ------------------------------------------
        # CALCULATE FINAL TOTAL
        # ------------------------------------------

        calculated_total = (
            subtotal + gst_amount
        ).quantize(
            Decimal("0.01")
        )

        # ------------------------------------------
        # PAYMENT VALUES
        # ------------------------------------------

        if payment_status == "Paid":

            amount_paid = calculated_total

            balance_amount = Decimal("0.00")

        else:

            amount_paid = Decimal("0.00")

            balance_amount = calculated_total

        # ------------------------------------------
        # CREATE INVOICE
        # ------------------------------------------

        invoice = CustomerInvoice.objects.create(

            company=company,

            customer=customer,

            product=product,

            invoice_number=invoice_number,

            invoice_date=invoice_date_obj,

            due_date=due_date_obj,

            quantity=quantity,

            unit_price=unit_price,

            gst=gst,

            total_amount=calculated_total,

            gst_amount=gst_amount,

            amount_paid=amount_paid,

            balance_amount=balance_amount,

            payment_status=payment_status,

            notes=notes,

        )

        # ------------------------------------------
        # SUCCESS MESSAGE
        # ------------------------------------------

        messages.success(
            request,
            f"Invoice {invoice.invoice_number} created successfully."
        )

        return redirect("invoice_list")

    # ------------------------------------------
    # GET REQUEST
    # ------------------------------------------

    context = {

        "customers": customers,

        "products": products,

        "theme": appearance.theme or "light",

        "accent_color": (
            appearance.accent_color
            or "#2563eb"
        ),

    }

    return render(
        request,
        "customers/invoice_form.html",
        context
    )

@login_required(login_url="login")
@company_type_required("customer")
def invoice_view(request, invoice_id):

    company = get_company(request)

    if company is None:
        messages.error(
            request,
            "Company not found."
        )

        return redirect("login")

    invoice = get_object_or_404(
        CustomerInvoice,
        id=invoice_id,
        company=company
    )

    appearance, created = (
        CustomerInvoiceAppearance.objects.get_or_create(
            company=company
        )
    )

    context = {
        "invoice": invoice,
        "theme": appearance.theme,
        "accent_color": appearance.accent_color,
    }

    return render(
        request,
        "customers/invoice_view.html",
        context
    )


@login_required(login_url="login")
@company_type_required("customer")
def invoice_edit(request, invoice_id):

    company = get_company(request)

    if company is None:
        messages.error(
            request,
            "Company not found."
        )

        return redirect("login")

    invoice = get_object_or_404(
        CustomerInvoice,
        id=invoice_id,
        company=company
    )

    customers = Customer.objects.filter(
        company=company
    ).order_by(
        "name"
    )

    appearance, created = (
        CustomerInvoiceAppearance.objects.get_or_create(
            company=company
        )
    )

    if request.method == "POST":

        invoice_number = request.POST.get(
            "invoice_number"
        )

        customer_id = request.POST.get(
            "customer"
        )

        invoice_date = request.POST.get(
            "invoice_date"
        )

        due_date = request.POST.get(
            "due_date"
        )

        total_amount = request.POST.get(
            "total_amount"
        )

        payment_status = request.POST.get(
            "payment_status"
        ) or "Pending"

        customer = Customer.objects.filter(
            id=customer_id,
            company=company
        ).first()

        if customer is None:

            messages.error(
                request,
                "Invalid customer selected."
            )

            return redirect(
                "invoice_edit",
                invoice_id=invoice.id
            )

        if not invoice_number:

            messages.error(
                request,
                "Invoice number is required."
            )

            return redirect(
                "invoice_edit",
                invoice_id=invoice.id
            )

        if not invoice_date:

            messages.error(
                request,
                "Invoice date is required."
            )

            return redirect(
                "invoice_edit",
                invoice_id=invoice.id
            )

        if not total_amount:

            messages.error(
                request,
                "Total amount is required."
            )

            return redirect(
                "invoice_edit",
                invoice_id=invoice.id
            )

        try:

            total_amount = Decimal(
                total_amount
            )

        except (
            InvalidOperation,
            ValueError,
            TypeError
        ):

            messages.error(
                request,
                "Please enter a valid total amount."
            )

            return redirect(
                "invoice_edit",
                invoice_id=invoice.id
            )

        if total_amount < 0:

            messages.error(
                request,
                "Total amount cannot be negative."
            )

            return redirect(
                "invoice_edit",
                invoice_id=invoice.id
            )

        invoice.invoice_number = invoice_number
        invoice.customer = customer
        invoice.invoice_date = invoice_date
        invoice.due_date = due_date
        invoice.total_amount = total_amount
        invoice.payment_status = payment_status

        invoice.save()

        messages.success(
            request,
            "Invoice updated successfully."
        )

        return redirect(
            "invoice_list"
        )

    context = {
        "invoice": invoice,
        "customers": customers,
        "theme": appearance.theme,
        "accent_color": appearance.accent_color,
    }

    return render(
        request,
        "customers/invoice_edit.html",
        context
    )


@login_required(login_url="login")
@company_type_required("customer")
def invoice_delete(request, invoice_id):

    company = get_company(request)

    if company is None:
        messages.error(
            request,
            "Company not found."
        )

        return redirect("login")

    invoice = get_object_or_404(
        CustomerInvoice,
        id=invoice_id,
        company=company
    )

    if request.method == "POST":

        invoice.delete()

        messages.success(
            request,
            "Invoice deleted successfully."
        )

        return redirect(
            "invoice_list"
        )

    context = {
        "invoice": invoice,
    }

    return render(
        request,
        "customers/invoice_delete.html",
        context
    )

@login_required(login_url="login")
@company_type_required("customer")
def invoice_print(request, invoice_id):

    company = get_company(request)

    if company is None:
        messages.error(request, "Company not found.")
        return redirect("login")

    invoice = get_object_or_404(
        CustomerInvoice.objects.select_related(
            "customer",
            "product"
        ),
        id=invoice_id,
        company=company
    )

    context = {
        "company": company,
        "invoice": invoice,
    }

    return render(
        request,
        "customers/invoice_print.html",
        context
    )

    
@login_required(login_url="login")
@company_type_required("customer")
def customer_payment_list(request):
 

    company = get_company(request)

    if company is None:

        return redirect("login")

 

    payments = CustomerPayment.objects.filter(

        customer__company=company

    ).order_by(

        "-payment_date"

    )

 

    total_payments = payments.count()


    paid_payments = payments.filter(

        status__iexact="Paid"

    ).count()


    pending_payments = payments.filter(

        status__iexact="Pending"

    ).count()

 

    total_revenue = payments.filter(

        status__iexact="Paid"

    ).aggregate(

        total=Sum("amount")

    )["total"] or Decimal("0.00")

 
    appearance_settings, created = (
        CustomerInvoiceAppearance.objects.get_or_create(

            company=company,

            defaults={

                "theme": "light",

                "accent_color": "#2563eb",

            }

        )
    )

    theme = appearance_settings.theme or "light"


    accent_color = (

        appearance_settings.accent_color

        or "#2563eb"

    )


    context = {

        "payments": payments,

        "total_payments": total_payments,

        "paid_payments": paid_payments,

        "pending_payments": pending_payments,

        "total_revenue": total_revenue,

        "theme": theme,

        "accent_color": accent_color,

    }


    return render(

        request,

        "customers/customer_payment_list.html",

        context,

    )

@login_required(login_url="login")
@company_type_required("customer")
def customer_payment_form(request):

    company = get_company(request)

    if company is None:

        messages.error(
            request,
            "Company not found."
        )

        return redirect("login")

    customers = Customer.objects.filter(
        company=company
    ).order_by(
        "name"
    )

    appearance, created = (
        CustomerInvoiceAppearance.objects.get_or_create(
            company=company
        )
    )

    theme = appearance.theme or "light"

    accent_color = (
        appearance.accent_color
        or "#2563eb"
    )

    if request.method == "POST":

        payment_number = (
            request.POST.get(
                "payment_number"
            )
            or ""
        ).strip()

        customer_id = request.POST.get(
            "customer"
        )

        payment_date = request.POST.get(
            "payment_date"
        )

        amount = request.POST.get(
            "amount"
        )

        payment_method = request.POST.get(
            "payment_method"
        )

        status = request.POST.get(
            "status"
        )

        notes = request.POST.get(
            "notes"
        )

        if not customer_id:

            messages.error(
                request,
                "Please select a customer."
            )

        elif not Customer.objects.filter(
            id=customer_id,
            company=company
        ).exists():

            messages.error(
                request,
                "Invalid customer selected."
            )

        elif not payment_number:

            messages.error(
                request,
                "Payment number is required."
            )

        else:

            CustomerPayment.objects.create(

                company=company,

                receipt_number=payment_number,

                customer_id=customer_id,

                payment_date=payment_date,

                amount=amount,

                payment_method=payment_method,

                status=status,

                notes=notes,

            )

            messages.success(
                request,
                "Payment recorded successfully."
            )

            return redirect(
                "customer_payment_list"
            )

    context = {

        "customers": customers,

        "theme": theme,

        "accent_color": accent_color,

    }

    return render(

        request,

        "customers/customer_payment_form.html",

        context,

    )


@login_required
@company_type_required("customer")
def payment_create(request):

    if request.method == "POST":
        # save payment
        messages.success(
            request,
            "Payment received successfully."
        )
        return redirect("customer_payment_list")

    return render(
        request,
        "customers/payment_create.html",
    )

@login_required(login_url="login")
@company_type_required("customer")
def payment_print(request, pk):

    company = get_company(request)

    if company is None:
        messages.error(
            request,
            "Company not found."
        )
        return redirect("login")

    payment = get_object_or_404(
        CustomerPayment.objects.select_related(
            "customer",
            "invoice"
        ),
        pk=pk,
        company=company
    )

    appearance, created = (
        CustomerInvoiceAppearance.objects.get_or_create(
            company=company
        )
    )

    context = {
        "payment": payment,
        "appearance": appearance,
        "company": company,
    }

    return render(
        request,
        "customers/payment_print.html",
        context
    )

@login_required(login_url="login")
@company_type_required("customer")
def payment_update(request, pk):

    company = get_company(request)

    if company is None:
        messages.error(
            request,
            "Company not found."
        )
        return redirect("login")

    payment = get_object_or_404(
        CustomerPayment,
        pk=pk,
        company=company
    )

    customers = Customer.objects.filter(
        company=company
    ).order_by(
        "name"
    )

    appearance, created = (
        CustomerInvoiceAppearance.objects.get_or_create(
            company=company
        )
    )

    theme = appearance.theme or "light"

    accent_color = (
        appearance.accent_color
        or "#2563eb"
    )

    if request.method == "POST":

        receipt_number = (
            request.POST.get(
                "receipt_number"
            )
            or ""
        ).strip()

        customer_id = request.POST.get(
            "customer"
        )

        payment_date = request.POST.get(
            "payment_date"
        )

        amount = request.POST.get(
            "amount"
        )

        payment_method = request.POST.get(
            "payment_method"
        )

        status = request.POST.get(
            "status"
        )

        notes = (
            request.POST.get(
                "notes"
            )
            or ""
        ).strip()

        if not receipt_number:

            messages.error(
                request,
                "Receipt number is required."
            )

        else:

            customer = Customer.objects.filter(
                id=customer_id,
                company=company
            ).first()

            if customer is None:

                messages.error(
                    request,
                    "Invalid customer selected."
                )

            else:

                try:

                    amount = Decimal(
                        amount
                    )

                    if amount <= 0:
                        raise ValueError

                except (
                    InvalidOperation,
                    ValueError,
                    TypeError
                ):

                    messages.error(
                        request,
                        "Please enter a valid amount."
                    )

                else:

                    duplicate = (
                        CustomerPayment.objects.filter(
                            company=company,
                            receipt_number=receipt_number
                        )
                        .exclude(
                            pk=payment.pk
                        )
                        .exists()
                    )

                    if duplicate:

                        messages.error(
                            request,
                            "This receipt number already exists."
                        )

                    else:

                        payment.receipt_number = (
                            receipt_number
                        )

                        payment.customer = (
                            customer
                        )

                        payment.payment_date = (
                            payment_date
                        )

                        payment.amount = (
                            amount
                        )

                        payment.payment_method = (
                            payment_method
                        )

                        payment.status = (
                            status or "Pending"
                        )

                        payment.notes = (
                            notes
                        )

                        payment.save()

                        messages.success(
                            request,
                            "Payment updated successfully."
                        )

                        return redirect(
                            "customer_payment_list"
                        )

    context = {

        "payment": payment,

        "customers": customers,

        "theme": theme,

        "accent_color": accent_color,

    }

    return render(
        request,
        "customers/payment_update.html",
        context
    )

@login_required(login_url="login")
@company_type_required("customer")
def payment_print(request, pk):

    company = get_company(request)

    if company is None:
        messages.error(
            request,
            "Company not found."
        )
        return redirect("login")

    payment = get_object_or_404(
        CustomerPayment.objects.select_related(
            "customer",
            "invoice"
        ),
        pk=pk,
        company=company
    )

    appearance, created = (
        CustomerInvoiceAppearance.objects.get_or_create(
            company=company
        )
    )

    context = {
        "payment": payment,
        "appearance": appearance,
        "company": company,
    }

    return render(
        request,
        "customers/payment_print.html",
        context
    )

@login_required(login_url="login")
@company_type_required("customer")
def payment_delete(request, pk):

    company = get_company(request)

    if company is None:
        messages.error(
            request,
            "Company not found."
        )
        return redirect("login")

    payment = get_object_or_404(
        CustomerPayment,
        pk=pk,
        company=company
    )

    if request.method == "POST":

        payment.delete()

        messages.success(
            request,
            "Payment deleted successfully."
        )

        return redirect(
            "customer_payment_list"
        )

    return render(
        request,
        "customers/payment_delete.html",
        {
            "payment": payment,
        }
    )

@login_required(login_url="login")
@company_type_required("customer")
def reports(request):

    # Get logged-in user's company
    company = get_company(request)

    # Safety check
    if company is None:

        return render(
            request,
            "customers/reports.html",
            {
                "company": None,
                "products": [],
                "invoices": [],
                "total_products": 0,
                "total_sales": 0,
                "total_invoices": 0,
                "total_collection": 0,
                "pending_amount": 0,
                "paid_invoice": 0,
                "pending_invoice": 0,
                "overdue_invoice": 0,
                "total_cgst": 0,
                "total_sgst": 0,
                "total_tax": 0,
                "theme": "light",
                "accent_color": "#2563eb",
            }
        )



    appearance, created = (
        CustomerInvoiceAppearance.objects
        .get_or_create(
            company=company
        )
    )



    products = Product.objects.filter(
        company=company
    )


    invoices = CustomerInvoice.objects.filter(
        company=company
    )


    payments = CustomerPayment.objects.filter(
        company=company
    )

    total_products = products.count()


    total_sales = (
        invoices.aggregate(
            total=Sum("total_amount")
        )["total"]
        or Decimal("0.00")
    )


    total_invoices = invoices.count()


    total_collection = (
        payments.aggregate(
            total=Sum("amount")
        )["total"]
        or Decimal("0.00")
    )


    pending_amount = (
        invoices.aggregate(
            total=Sum("balance_amount")
        )["total"]
        or Decimal("0.00")
    )


    paid_invoice = invoices.filter(
        payment_status="Paid"
    ).count()


    pending_invoice = invoices.filter(
        payment_status="Pending"
    ).count()


    overdue_invoice = invoices.filter(
        payment_status="Overdue"
    ).count()


    total_tax = (
        invoices.aggregate(
            total=Sum("gst_amount")
        )["total"]
        or Decimal("0.00")
    )


    total_cgst = total_tax / Decimal("2")


    total_sgst = total_tax / Decimal("2")


    return render(
        request,
        "customers/reports.html",
        {

            # Company
            "company": company,


            # Data
            "products": products,


            "invoices":
                invoices.order_by(
                    "-invoice_date"
                )[:10],


            # Dashboard
            "total_products":
                total_products,


            "total_sales":
                total_sales,


            "total_invoices":
                total_invoices,


            "total_collection":
                total_collection,


            "pending_amount":
                pending_amount,


            # Invoice Status
            "paid_invoice":
                paid_invoice,


            "pending_invoice":
                pending_invoice,


            "overdue_invoice":
                overdue_invoice,


            # GST
            "total_cgst":
                total_cgst,


            "total_sgst":
                total_sgst,


            "total_tax":
                total_tax,



            "theme":
                appearance.theme
                or "light",


            "accent_color":
                appearance.accent_color
                or "#2563eb",

        }
    )

@login_required(login_url="login")
@company_type_required("customer")
def settings(request):

    # Get logged-in user's company
    company = get_company(request)

    # Safety check
    if company is None:

        messages.error(
            request,
            "Company not found."
        )

        return redirect("login")


    # Create or get GST settings
    gst, created = CustomerGSTSettings.objects.get_or_create(

        company=company,

        defaults={

            "company_name": company.company_name,

            "gst_number": "",

            "pan_number": "",

            "state": "",

            "state_code": "",

            "cgst": 9,

            "sgst": 9,

            "igst": 18,

            "is_active": False,

        }

    )


    # Save GST settings
    if request.method == "POST":

        gst.company_name = request.POST.get(
            "company_name",
            ""
        ).strip()

        gst.gst_number = request.POST.get(
            "gst_number",
            ""
        ).strip()

        gst.pan_number = request.POST.get(
            "pan_number",
            ""
        ).strip()

        gst.business_type = request.POST.get(
            "business_type",
            ""
        ).strip()

        gst.state = request.POST.get(
            "state",
            ""
        ).strip()

        gst.state_code = request.POST.get(
            "state_code",
            ""
        ).strip()


        # GST percentages

        gst.cgst = request.POST.get(
            "cgst"
        ) or 9

        gst.sgst = request.POST.get(
            "sgst"
        ) or 9

        gst.igst = request.POST.get(
            "igst"
        ) or 18


        # Tax type

        gst.default_tax_type = request.POST.get(
            "default_tax_type",
            "Intrastate"
        ).strip()


        # Contact details

        gst.contact_person = request.POST.get(
            "contact_person",
            ""
        ).strip()

        gst.email = request.POST.get(
            "email",
            ""
        ).strip()

        gst.phone = request.POST.get(
            "phone",
            ""
        ).strip()

        gst.city = request.POST.get(
            "city",
            ""
        ).strip()

        gst.pincode = request.POST.get(
            "pincode",
            ""
        ).strip()

        gst.address = request.POST.get(
            "address",
            ""
        ).strip()


        # Checkbox
        gst.is_active = "is_active" in request.POST


        # Save
        gst.save()


        messages.success(
            request,
            "GST Settings Saved Successfully."
        )


        return redirect(
            "gst_settings_list"
        )

    theme = "light"

    accent_color = "#2563eb"


    appearance = CustomerInvoiceAppearance.objects.filter(

        company=company

    ).first()


    if appearance:

        if appearance.theme:

            theme = appearance.theme


        if appearance.accent_color:

            accent_color = appearance.accent_color

    context = {

        "gst": gst,

        "theme": theme,

        "accent_color": accent_color,

    }


    return render(

        request,

        "customers/gst_settings.html",

        context

    )


@login_required(login_url="login")
@company_type_required("customer")
def gst_settings_list(request):

    # Get logged-in user's company
    company = get_company(request)

    # Safety check
    if company is None:
        return redirect("login")

    # Get GST settings only for this company
    settings = CustomerGSTSettings.objects.filter(
        company=company
    )

    # Default appearance values
    theme = "light"
    accent_color = "#2563eb"

    # Load saved billing appearance settings
    appearance = CustomerInvoiceAppearance.objects.filter(
        company=company
    ).first()

    if appearance:

        if appearance.theme:
            theme = appearance.theme

        if appearance.accent_color:
            accent_color = appearance.accent_color

    context = {

        "settings": settings,

        # Theme appearance
        "theme": theme,
        "accent_color": accent_color,

    }

    return render(
        request,
        "customers/gst_settings_list.html",
        context
    )
@login_required
@company_type_required("customer")
def delete_gst(request, pk):

    company = get_object_or_404(
        Company,
        user=request.user
    )

    gst = get_object_or_404(
        CustomerGSTSettings,
        id=pk,
        company=company
    )

    gst.delete()

    messages.success(
        request,
        "GST Settings Deleted Successfully."
    )

    return redirect("gst_settings_list")

@login_required
@company_type_required("customer")
def customer_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is not None:
            login(request, user)

            return redirect("product_dashboard")

        return render(
            request,
            "customer_login.html",
            {
                "error": "Invalid username or password."
            }
        )

    return render(request, "customer_login.html")

def register_customer(request):

    if request.method == "POST":

        company_name = request.POST.get("company_name")
        full_name = request.POST.get("full_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get(
            "confirm_password"
        )

        if password != confirm_password:
            messages.error(
                request,
                "Passwords do not match."
            )
            return redirect("customer_register.html")

        if User.objects.filter(
            username=username
        ).exists():

            messages.error(
                request,
                "Username already exists."
            )
            return redirect("customer_register.html")

        if User.objects.filter(
            email=email
        ).exists():

            messages.error(
                request,
                "Email already exists."
            )
            return redirect("customer_register.html")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=full_name
        )

        Company.objects.create(
    user=user,
    company_name=company_name,  
    full_name=full_name,
    phone=""
)

        messages.success(
            request,
            "Registration Successful."
        )

        return redirect("customer_login.html")

    return render(
        request,
        "customer_register.html"
    )


def product_portal(request):
    """
    Product Billing Portal
    """
    return render(request, "customers/Customer_billing_portal.html")

@login_required(login_url="login")
@company_type_required("customer")
def customer_admin_login(request):
    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is not None and user.is_superuser:
            login(request, user)
            return redirect("/customer-admin/")

        return render(
            request,
            "customers/customer_admin_login.html",
            {"error": "Only Super Admin can login."},
        )

    return render(request, "customers/customer_admin_login.html")
@login_required(login_url="login")
@company_type_required("customer")
def customer_staff_login(request):
    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("product_dashboard")

        return render(
            request,
            "customers/customer_staff_login.html",
            {
                "error": "Invalid username or password."
            }
        )

    return render(request, "customers/customer_staff_login.html")

@login_required(login_url="login")
@company_type_required("customer")
def payment_print(request, pk):
    payment = get_object_or_404(
        CustomerPayment,
        pk=pk,
        company__user=request.user
    )

    return render(
        request,
        "customers/payment_print.html",
        {
            "payment": payment
        }
    )
@login_required(login_url="login")
@company_type_required("customer")
def customer_billing_settings(request):

    company = get_user_company(request.user)

    if company is None:
        return HttpResponseForbidden(
            "No company is associated with this account."
        )

    appearance_settings, created = CustomerInvoiceAppearance.objects.get_or_create(
        company=company
    )

    return render(
        request,
        "customers/customer_billing_settings.html",
        {
            "appearance_settings": appearance_settings,
        }
    )




def get_user_company(user):
    try:
        return Company.objects.get(user=user)
    except Company.DoesNotExist:
        return None

@login_required(login_url="login")
@company_type_required("customer")
def customer_company_profile(request):
    company = get_company(request)

    if company is None:
        return HttpResponseForbidden(
            "No company is associated with this account."
        )

    profile, created = CustomerCompanyProfile.objects.get_or_create(
        user=request.user,
        defaults={
            "company_name": company.company_name,
            "owner_name": request.user.get_full_name(),
            "email": request.user.email,
        }
    )

    appearance_settings, _ = CustomerInvoiceAppearance.objects.get_or_create(
        company=company,
        defaults={
            "theme": "light",
            "accent_color": "#2563eb",
        }
    )

    if request.method == "POST":
        form = CustomerCompanyProfileForm(
            request.POST,
            request.FILES,
            instance=profile,
        )

        if form.is_valid():
            company_profile = form.save(commit=False)
            company_profile.user = request.user
            company_profile.save()

            messages.success(
                request,
                "Company profile updated successfully."
            )
            return redirect("customer_company_profile")

    else:
        form = CustomerCompanyProfileForm(instance=profile)

    context = {
        "form": form,
        "profile": profile,
        "company": company,
        "appearance_settings": appearance_settings,
    }

    return render(
        request,
        "customers/customer_company_profile.html",
        context,
    )
@login_required(login_url="login")
@company_type_required("customer")
def customer_invoice_settings(request):

    if request.user.is_superuser:

        company = None

    else:

        company = get_company(request)

        if not company:
            return HttpResponseForbidden(
                "No company is associated with this account."
            )

        if company.company_type != "customer":
            return HttpResponseForbidden(
                "Access Denied! Your company is not authorized "
                "to access customer billing settings."
            )


    if request.user.is_superuser:

        return render(
            request,
            "customers/customer_invoice_settings.html",
            {
                "company": None,
                "form": None,
                "settings": None,
                "appearance_settings": None,
                "is_superuser": True,
            }
        )


    settings_obj, created = (
        CustomerInvoiceSettings.objects.get_or_create(
            company=company
        )
    )


    appearance_settings, appearance_created = (
        CustomerInvoiceAppearance.objects.get_or_create(
            company=company,
            defaults={
                "theme": "light",
                "accent_color": "#2563eb",
            }
        )
    )


    if request.method == "POST":

        form = CustomerInvoiceSettingsForm(
            request.POST,
            instance=settings_obj
        )

        if form.is_valid():

            settings_obj = form.save(commit=False)

            settings_obj.company = company

            settings_obj.save()

            messages.success(
                request,
                "Invoice settings updated successfully."
            )

            return redirect(
                "customer_invoice_settings"
            )


    else:

        form = CustomerInvoiceSettingsForm(
            instance=settings_obj
        )

    return render(
        request,
        "customers/customer_invoice_settings.html",
        {
            "company": company,
            "form": form,
            "settings": settings_obj,
            "appearance_settings": appearance_settings,
            "is_superuser": False,
        }
    )


@login_required(login_url="login")
@company_type_required("customer")
def customer_payment_settings(request):

    if request.user.is_superuser:

        company = None

    else:

        company = get_company(request)

        if not company:

            return HttpResponseForbidden(
                "No company is associated with this account."
            )

        if company.company_type != "customer":

            return HttpResponseForbidden(
                "Access Denied! Your company is not authorized "
                "to access customer billing settings."
            )

    if request.user.is_superuser:

        return render(
            request,
            "customers/customer_payment_settings.html",
            {
                "company": None,
                "form": None,
                "settings": None,
                "appearance_settings": None,
                "is_superuser": True,
            }
        )
    settings_obj, created = (
        CustomerPaymentSettings.objects.get_or_create(
            company=company
        )
    )


    appearance_settings, created = (
        CustomerInvoiceAppearance.objects.get_or_create(
            company=company,
            defaults={
                "theme": "light",
                "accent_color": "#2563eb",
            }
        )
    )

    if request.method == "POST":

        form = CustomerPaymentSettingsForm(
            request.POST,
            instance=settings_obj
        )

        if form.is_valid():

            payment_settings = form.save(
                commit=False
            )

            payment_settings.company = company

            payment_settings.save()

            messages.success(
                request,
                "Payment settings saved successfully."
            )

            return redirect(
                "customer_payment_settings"
            )

    else:

        form = CustomerPaymentSettingsForm(
            instance=settings_obj
        )



    context = {

        "company": company,

        "form": form,

        "settings": settings_obj,

        "appearance_settings": appearance_settings,

        "is_superuser": False,

    }



    return render(
        request,
        "customers/customer_payment_settings.html",
        context
    )

@login_required(login_url="login")
@company_type_required("customer")
def customer_tax_gst_settings(request):


    if request.user.is_superuser:

        company = None

    else:
        company = get_company(request)

        if not company:

            return HttpResponseForbidden(
                "No company is associated with this account."
            )

        if company.company_type != "customer":

            return HttpResponseForbidden(
                "Access Denied! Your company is not authorized "
                "to access customer billing settings."
            )


    if request.user.is_superuser:

        return render(
            request,
            "customers/customer_tax_gst_settings.html",
            {
                "company": None,
                "form": None,
                "settings": None,
                "appearance_settings": None,
                "is_superuser": True,
            }
        )

    settings_obj, created = (
        CustomerTaxGSTSettings.objects.get_or_create(
            company=company
        )
    )


    appearance_settings, created = (
        CustomerInvoiceAppearance.objects.get_or_create(
            company=company,
            defaults={
                "theme": "light",
                "accent_color": "#2563eb",
            }
        )
    )


    if request.method == "POST":

        form = CustomerTaxGSTSettingsForm(
            request.POST,
            instance=settings_obj
        )

        if form.is_valid():

            tax_settings = form.save(
                commit=False
            )

            tax_settings.company = company

            tax_settings.save()

            messages.success(
                request,
                "Tax & GST settings saved successfully."
            )

            return redirect(
                "customer_tax_gst_settings"
            )


    else:

        form = CustomerTaxGSTSettingsForm(
            instance=settings_obj
        )
    context = {
        "company": company,
        "form": form,
        "settings": settings_obj,
        "appearance_settings": appearance_settings,
        "is_superuser": False,
    }

    return render(
        request,
        "customers/customer_tax_gst_settings.html",
        context
    )
@login_required(login_url="login")
@company_type_required("customer")
def customer_discount_settings(request):


    if request.user.is_superuser:

        company = None

    else:

        company = get_company(request)

        if not company:

            return HttpResponseForbidden(
                "No company is associated with this account."
            )

        if company.company_type != "customer":

            return HttpResponseForbidden(
                "Access Denied! Your company is not authorized "
                "to access customer billing settings."
            )


    if request.user.is_superuser:

        return render(
            request,
            "customers/customer_discount_settings.html",
            {
                "company": None,
                "form": None,
                "settings": None,
                "appearance_settings": None,
                "is_superuser": True,
            }
        )

    settings_obj, created = (
        CustomerDiscountSettings.objects.get_or_create(
            company=company
        )
    )


    appearance_settings, created = (
        CustomerInvoiceAppearance.objects.get_or_create(
            company=company,
            defaults={
                "theme": "light",
                "accent_color": "#2563eb",
            }
        )
    )


    if request.method == "POST":

        form = CustomerDiscountSettingsForm(
            request.POST,
            instance=settings_obj
        )

        if form.is_valid():

            discount_settings = form.save(
                commit=False
            )

            discount_settings.company = company

            discount_settings.save()

            messages.success(
                request,
                "Discount settings saved successfully."
            )

            return redirect(
                "customer_discount_settings"
            )

    else:

        form = CustomerDiscountSettingsForm(
            instance=settings_obj
        )
    context = {
        "company": company,
        "form": form,
        "settings": settings_obj,
        "appearance_settings": appearance_settings,
        "is_superuser": False,
    }

    return render(
        request,
        "customers/customer_discount_settings.html",
        context
    )

@login_required(login_url="login")
@company_type_required("customer")
def customer_notification_settings(request):


    if request.user.is_superuser:

        company = None

    else:

        company = get_company(request)

        if not company:

            return HttpResponseForbidden(
                "No company is associated with this account."
            )

        if company.company_type != "customer":

            return HttpResponseForbidden(
                "Access Denied! Your company is not authorized "
                "to access customer billing settings."
            )


    if request.user.is_superuser:

        return render(
            request,
            "customers/customer_notification_settings.html",
            {
                "company": None,
                "form": None,
                "settings": None,
                "appearance_settings": None,
                "is_superuser": True,
            }
        )

    notification_settings, created = (
        CustomerNotificationSettings.objects.get_or_create(
            company=company
        )
    )
    appearance_settings, created = (
        CustomerInvoiceAppearance.objects.get_or_create(
            company=company,
            defaults={
                "theme": "light",
                "accent_color": "#2563eb",
            }
        )
    )

    if request.method == "POST":

        form = CustomerNotificationSettingsForm(
            request.POST,
            instance=notification_settings
        )

        if form.is_valid():

            settings = form.save(
                commit=False
            )

            settings.company = company

            settings.save()

            messages.success(
                request,
                "Notification settings saved successfully."
            )

            return redirect(
                "customer_notification_settings"
            )


    else:

        form = CustomerNotificationSettingsForm(
            instance=notification_settings
        )


    context = {
        "company": company,
        "form": form,
        "settings": notification_settings,
        "appearance_settings": appearance_settings,
        "is_superuser": False,
    }

    return render(
        request,
        "customers/customer_notification_settings.html",
        context
    )

@login_required(login_url="login")
@company_type_required("customer")
def customer_invoice_appearance(request):

    company = get_user_company(request.user)

    if company is None:
        return HttpResponseForbidden(
            "No company is associated with this account."
        )

    if company.company_type != "customer":
        return HttpResponseForbidden(
            "Access denied. Your company is not authorized "
            "to access Customer Invoice Appearance Settings."
        )

    appearance_settings, created = (
        CustomerInvoiceAppearance.objects.get_or_create(
            company=company,
            defaults={
                "theme": "light",
                "accent_color": "#2563eb",
                "layout": "standard",

                "show_logo": True,
                "logo_position": "left",

                "show_company_name": True,
                "show_company_address": True,
                "show_company_phone": True,
                "show_company_email": True,
                "show_company_website": False,

                "show_customer_address": True,
                "show_customer_phone": True,
                "show_customer_email": True,

                "show_tax_details": True,
                "show_payment_details": True,
                "show_bank_details": False,

                "show_footer": True,
                "footer_text": "Thank you for your business.",

                "terms_text": "",
                "is_active": True,
            }
        )
    )

    if request.method == "POST":

        form = CustomerInvoiceAppearanceForm(
            request.POST,
            request.FILES,
            instance=appearance_settings
        )

        if form.is_valid():

            appearance_settings = form.save(commit=False)

            # Make sure this record always belongs
            # to the logged-in customer's company.
            appearance_settings.company = company

            appearance_settings.save()

            messages.success(
                request,
                "Customer invoice appearance settings saved successfully."
            )

            return redirect("customer_invoice_appearance")

        else:

            messages.error(
                request,
                "Please correct the errors below."

            )

    else:

        form = CustomerInvoiceAppearanceForm(
            instance=appearance_settings
        )

    return render(
        request,
        "customers/customer_invoice_appearance.html",
        {
            "form": form,
            "appearance_settings": appearance_settings,
            "company": company,
        }
    )
@login_required(login_url="login")
@company_type_required("customer")
def customer_password_settings(request):
    return render(
        request,
        "customers/customer_password_settings.html"
    )
@login_required(login_url="login")
@company_type_required("customer")
def customer_bank_payment_settings(request):


    if request.user.is_superuser:

        company = None

    else:

        company = get_company(request)

        if not company:

            return HttpResponseForbidden(
                "No company is associated with this account."
            )

        if company.company_type != "customer":

            return HttpResponseForbidden(
                "Access Denied! Your company is not authorized "
                "to access customer billing settings."
            )
    if request.user.is_superuser:

        return render(
            request,
            "customers/customer_bank_payment_settings.html",
            {
                "company": None,
                "form": None,
                "bank_settings": None,
                "appearance_settings": None,
                "is_superuser": True,
            }
        )

    settings_obj, created = (
        CustomerBankPaymentSettings.objects.get_or_create(
            company=company
        )
    )

    appearance_settings, created = (
        CustomerInvoiceAppearance.objects.get_or_create(
            company=company,
            defaults={
                "theme": "light",
                "accent_color": "#2563eb",
            }
        )
    )

    if request.method == "POST":

        form = CustomerBankPaymentSettingsForm(
            request.POST,
            instance=settings_obj
        )

        if form.is_valid():

            bank_settings = form.save(
                commit=False
            )

            bank_settings.company = company

            bank_settings.save()

            messages.success(
                request,
                "Bank & Payment settings saved successfully."
            )

            return redirect(
                "customer_bank_payment_settings"
            )


    else:

        form = CustomerBankPaymentSettingsForm(
            instance=settings_obj
        )


    context = {

        "company": company,

        "form": form,

        "bank_settings": settings_obj,

        "appearance_settings": appearance_settings,

        "is_superuser": False,
    }

    return render(
        request,
        "customers/customer_bank_payment_settings.html",
        context
    )
@login_required(login_url="login")
@company_type_required("customer")
def customer_security_settings(request):

    if request.user.is_superuser:

        return render(
            request,
            "customers/customer_security_settings.html",
            {
                "form": None,
                "security_settings": None,
                "appearance_settings": None,
                "company": None,
                "is_superuser": True,
            }
        )
    company = getattr(request.user, "company", None)

    if not company:

        return HttpResponseForbidden(
            "No company is associated with this account."
        )

    if company.company_type != "customer":

        return HttpResponseForbidden(
            "Access Denied! Your company is not authorized "
            "to access customer billing settings."
        )

    settings, created = (
        CustomerSecuritySettings.objects.get_or_create(
            company=company
        )
    )

    appearance_settings, appearance_created = (
        CustomerInvoiceAppearance.objects.get_or_create(
            company=company,
            defaults={
                "theme": "light",
                "accent_color": "#2563eb",
            }
        )
    )

    if request.method == "POST":

        form = CustomerSecuritySettingsForm(
            request.POST,
            instance=settings
        )

        if form.is_valid():

            security_settings = form.save(
                commit=False
            )

            security_settings.company = company

            security_settings.save()

            messages.success(
                request,
                "Security settings saved successfully."
            )

            return redirect(
                "customer_security_settings"
            )

    else:

        form = CustomerSecuritySettingsForm(
            instance=settings
        )

    context = {

        "form": form,

        "security_settings": settings,

        "settings": settings,

        "appearance_settings": appearance_settings,

        "company": company,

        "is_superuser": False,

    }

    return render(
        request,
        "customers/customer_security_settings.html",
        context
    )

@login_required(login_url="login")
@company_type_required("customer")
def logout_customer(request):

    company = Company.objects.filter(
        user=request.user,
        company_type="customer"
    ).first()

    appearance = None

    if company:
        appearance, created = CustomerInvoiceAppearance.objects.get_or_create(
            company=company,
            defaults={
                "theme": "light",
                "accent_color": "#2563eb",
                "layout": "standard",
                "logo_position": "left",
            }
        )

    if request.method == "POST":

        logout(request)

        messages.success(
            request,
            "You have been logged out successfully."
        )

        return redirect("login")

    return render(
        request,
        "customers/logout_customer.html",
        {
            "customer_appearance": appearance,
        }
    )