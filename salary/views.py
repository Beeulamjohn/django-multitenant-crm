from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from students.decorators import company_type_required
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Employee
from django.contrib.auth import authenticate, login
from .forms import EmployeeForm
from app.models import Company
from .models import Salary
from .models import SalaryStructure
from .forms import SalaryStructureForm
from .models import Payroll
from django.shortcuts import render,redirect,get_object_or_404
from .models import Payslip
from .models import Bonus
from .models import Deduction
from .models import Attendance
from django.http import HttpResponse, request
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from django.http import HttpResponseForbidden
from .models import SalaryPayrollSettings, SalaryPayroll
from .forms import PayrollSettingsForm, SalaryPayrollForm
from .models import SalaryPayslipSettings
from .forms import SalaryPayslipSettingsForm
from .models import SalaryTaxDeductionSettings
from .forms import SalaryTaxDeductionSettingsForm
from .models import SalaryBonusSettings
from .forms import SalaryBonusSettingsForm
from .models import EmployeeSalarySettings
from .forms import EmployeeSalarySettingsForm
from .models import SalaryNotificationSettings
from .forms import SalaryNotificationSettingsForm
from .models import SalaryThemeSettings
from .forms import SalaryThemeSettingsForm
from decimal import Decimal, InvalidOperation
from django.contrib.auth import logout
from app.utils import get_company
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph
)

from .models import (
    Attendance,
    SalaryAttendanceSettings,
)

from .forms import (
    SalaryAttendanceSettingsForm,
    AttendanceForm,
)




@login_required(login_url="login")
@company_type_required("salary")
def salary_dashboard(request):
 

    if request.user.is_superuser:

        company = None

        employees = Employee.objects.all()

        salaries = Salary.objects.all()

        # No company-specific appearance for super admin
        appearance = None
 

    else:

        company = get_company(request)

        # Company validation
        if company is None:

            return HttpResponseForbidden(
                "Access Denied! Company not found."
            )

        # Allow only Salary companies
        if company.company_type != "salary":

            return HttpResponseForbidden(
                "Access Denied! Your company is not authorized "
                "to access the Salary dashboard."
            )
 

        employees = Employee.objects.filter(
            company=company
        )

        salaries = Salary.objects.filter(
            company=company
        )
 

        appearance, created = SalaryThemeSettings.objects.get_or_create(
            company=company
        )
 

    total_salary = salaries.aggregate(
        total=Sum("net_salary")
    )["total"] or 0


    paid_salary = salaries.filter(
        paid=True
    ).aggregate(
        total=Sum("net_salary")
    )["total"] or 0


    pending_salary = salaries.filter(
        paid=False
    ).aggregate(
        total=Sum("net_salary")
    )["total"] or 0
 

    context = {

        "company": company,

        "appearance": appearance,

        "employees": employees,

        "salaries": salaries,

        "employee_count": employees.count(),

        "total_salary": total_salary,

        "paid_salary": paid_salary,

        "pending_salary": pending_salary,

    }


    return render(
        request,
        "salary/dashboard_salary.html",
        context,
    )

@login_required(login_url="login")
@company_type_required("salary")
def employee_salary_list(request):

    # Super Admin
    if request.user.is_superuser:

        company = None

        employees = Employee.objects.all()

        appearance = None


    else:

        # Get logged-in user's company
        company = get_company(request)


        if company is None:

            messages.error(
                request,
                "Company not found."
            )

            return redirect("login")


        # Allow only salary companies
        if company.company_type != "salary":

            return HttpResponseForbidden(
                "Access Denied! Your company is not authorized to access the Salary module."
            )


        # Get employees only for this company
        employees = Employee.objects.filter(
            company=company
        )


        # Get appearance settings
        appearance, created = SalaryThemeSettings.objects.get_or_create(
            company=company
        )


    context = {

        "employees": employees,

        "company": company,

        "appearance": appearance,

    }


    return render(
        request,
        "salary/employee_salary_list.html",
        context
    )

@login_required(login_url="login")
@company_type_required("salary")
def salary_edit_employee(request, employee_id):

    company = get_company(request)

    if company is None:

        messages.error(
            request,
            "Company not found."
        )

        return redirect("login")


    # Get employee only from the logged-in company's employees
    employee = get_object_or_404(
        Employee,
        id=employee_id,
        company=company
    )


    # ==========================
    # UPDATE EMPLOYEE
    # ==========================

    if request.method == "POST":

        employee.name = request.POST.get(
            "name",
            ""
        ).strip()


        employee.department = request.POST.get(
            "department",
            ""
        ).strip()


        employee.designation = request.POST.get(
            "designation",
            ""
        ).strip()


        employee.basic_salary = request.POST.get(
            "basic_salary",
            employee.basic_salary
        )


        employee.status = request.POST.get(
            "status",
            employee.status
        )


        employee.joined_date = request.POST.get(
            "joined_date",
            employee.joined_date
        )


        employee.save()


        messages.success(
            request,
            "Employee details updated successfully."
        )


        return redirect(
            "salary_dashboard"
        )


    # ==========================
    # THEME / APPEARANCE
    # ==========================

    appearance, created = SalaryThemeSettings.objects.get_or_create(
        company=company
    )


    # ==========================
    # CONTEXT
    # ==========================

    context = {

        "company": company,

        "employee": employee,

        "appearance": appearance,

    }


    # ==========================
    # EDIT TEMPLATE
    # ==========================

    return render(
        request,
        "salary/salary_edit_employee.html",
        context
    )

@login_required(login_url="login")
@company_type_required("salary")
def salary_delete_employee(request, employee_id):

    # ==========================
    # GET COMPANY
    # ==========================

    company = get_company(request)

    if company is None:

        messages.error(
            request,
            "Company not found."
        )

        return redirect("login")


    # ==========================
    # GET EMPLOYEE
    # ==========================

    employee = get_object_or_404(
        Employee,
        id=employee_id,
        company=company
    )


    # ==========================
    # DELETE EMPLOYEE
    # ==========================

    if request.method == "POST":

        employee.delete()


        messages.success(
            request,
            "Employee deleted successfully."
        )


        return redirect(
            "employee_salary_list"
        )


    # ==========================
    # THEME SETTINGS
    # ==========================

    appearance, created = SalaryThemeSettings.objects.get_or_create(
        company=company
    )


    # ==========================
    # CONTEXT
    # ==========================

    context = {

        "company": company,

        "employee": employee,

        "appearance": appearance,

    }


    # ==========================
    # DELETE TEMPLATE
    # ==========================

    return render(
        request,
        "salary/salary_delete_employee.html",
        context
    )


@login_required(login_url="login")
@company_type_required("salary")
def salary_structure_list(request):

    # Get logged-in user's company
    company = get_object_or_404(
        Company,
        user=request.user
    )

    # Get salary structures belonging only to this company
    structures = SalaryStructure.objects.filter(
        company=company
    ).order_by("-id")

    # Get appearance settings for this company
    appearance, created = SalaryThemeSettings.objects.get_or_create(
        company=company
    )

    context = {
        "company": company,
        "structures": structures,
        "appearance": appearance,
    }

    return render(
        request,
        "salary/salary_structure_list.html",
        context
    )






@login_required(login_url="login")
@company_type_required("salary")
def add_salary_structure(request):

    # Get logged-in user's company
    company = get_object_or_404(
        Company,
        user=request.user
    )

    # Get/create appearance settings for this company
    appearance, created = SalaryThemeSettings.objects.get_or_create(
        company=company
    )

    if request.method == "POST":

        form = SalaryStructureForm(
            request.POST
        )

        if form.is_valid():

            salary = form.save(
                commit=False
            )

            # Important for multi-tenant security
            salary.company = company

            salary.save()

            messages.success(
                request,
                "Salary Structure Added Successfully"
            )

            return redirect(
                "salary_structure_list"
            )

    else:

        form = SalaryStructureForm()

    context = {
        "form": form,
        "company": company,
        "appearance": appearance,
    }

    return render(
        request,
        "salary/add_salary_structure.html",
        context
    )


@login_required(login_url="login")
def edit_salary_structure(request, id):

    company = request.user.company

    salary = get_object_or_404(
        SalaryStructure,
        id=id,
        company=company
    )

    if request.method == "POST":

        salary.basic_salary = request.POST.get(
            "basic_salary"
        ) or 0

        salary.hra = request.POST.get(
            "hra"
        ) or 0

        salary.allowance = request.POST.get(
            "allowance"
        ) or 0

        salary.deduction = request.POST.get(
            "deduction"
        ) or 0

        salary.save()

        messages.success(
            request,
            "Salary structure updated successfully."
        )

        return redirect("salary_structure_list")

    context = {
        "salary": salary
    }

    return render(
        request,
        "salary/edit_salary_structure.html",
        context
    )


@login_required(login_url="login")
def delete_salary_structure(request, id):

    company = request.user.company

    salary = get_object_or_404(
        SalaryStructure,
        id=id,
        company=company
    )

    if request.method == "POST":

        salary.delete()

        messages.success(
            request,
            "Salary structure deleted successfully."
        )

        return redirect("salary_structure_list")

    context = {
        "salary": salary
    }

    return render(
        request,
        "salary/delete_salary_structure.html",
        context
    )
@login_required(login_url="login")
@company_type_required("salary")
def salary_payroll_list(request):

    # Get logged-in user's company
    company = Company.objects.filter(
        user=request.user
    ).first()

    # Company validation
    if company is None:

        messages.error(
            request,
            "Company not found."
        )

        return redirect("login")


    # Get or create appearance settings
    appearance, created = SalaryThemeSettings.objects.get_or_create(
        company=company
    )


    # Get payroll records ONLY for this company
    payrolls = (
        SalaryPayroll.objects
        .filter(company=company)
        .select_related("employee")
        .order_by("-year", "-month", "-id")
    )


    # Paid payroll count
    paid_count = payrolls.filter(
        payment_status="Paid"
    ).count()


    # Pending payroll count
    pending_count = payrolls.filter(
        payment_status="Pending"
    ).count()


    # Total net salary
    total_salary = (
        payrolls.aggregate(
            total=Sum("net_salary")
        )["total"]
        or 0
    )


    context = {

        "company": company,

        "appearance": appearance,

        "payrolls": payrolls,

        "paid_count": paid_count,

        "pending_count": pending_count,

        "total_salary": total_salary,

    }


    return render(
        request,
        "salary/salary_payroll_list.html",
        context
    )


# ============================================================
# GENERATE PAYROLL
# ============================================================

@login_required(login_url="login")
@company_type_required("salary")
def salary_payroll_create(request):

    # Get logged-in user's company
    company = Company.objects.filter(
        user=request.user
    ).first()


    # Company validation
    if company is None:

        messages.error(
            request,
            "Company not found."
        )

        return redirect("login")


    # Get or create appearance settings
    appearance, created = SalaryThemeSettings.objects.get_or_create(
        company=company
    )


    # Get ONLY employees belonging to this company
    employees = (
        Employee.objects
        .filter(company=company)
        .order_by("name")
    )


    # ========================================================
    # POST
    # ========================================================

    if request.method == "POST":

        form = SalaryPayrollForm(
            request.POST
        )


        # Important:
        # Employee dropdown should contain only this company's
        # employees.

        form.fields["employee"].queryset = employees


        if form.is_valid():

            # Create object without saving first
            payroll = form.save(
                commit=False
            )


            # Assign company
            payroll.company = company


            # Calculate net salary on the server
            payroll.net_salary = (
                payroll.basic_salary
                + payroll.allowance
                - payroll.deduction
            )


            # Save payroll
            payroll.save()


            # Success message
            messages.success(
                request,
                "Payroll generated successfully."
            )


            # Go to payroll list
            return redirect(
                "salary_payroll_list"
            )


    # ========================================================
    # GET
    # ========================================================

    else:

        form = SalaryPayrollForm()

        form.fields["employee"].queryset = employees


    # ========================================================
    # CONTEXT
    # ========================================================

    context = {

        "form": form,

        "employees": employees,

        "company": company,

        "appearance": appearance,

    }


    return render(
        request,
        "salary/salary_payroll_create.html",
        context
    )

@login_required(login_url="login")
@company_type_required("salary")
def salary_payroll_edit(request, id):

    # Get logged-in user's company

    company = Company.objects.filter(
        user=request.user
    ).first()


    if company is None:

        messages.error(
            request,
            "Company not found."
        )

        return redirect("login")


    # Get appearance settings

    appearance, created = SalaryThemeSettings.objects.get_or_create(
        company=company
    )


    # IMPORTANT:
    # Only get payroll belonging to this company

    payroll = get_object_or_404(
        SalaryPayroll,
        id=id,
        company=company
    )


    if request.method == "POST":

        employee_id = request.POST.get(
            "employee"
        )

        month = request.POST.get(
            "month"
        )

        year = request.POST.get(
            "year"
        )

        basic_salary = request.POST.get(
            "basic_salary"
        )

        allowance = request.POST.get(
            "allowance"
        )

        deduction = request.POST.get(
            "deduction"
        )


        # Update employee only if supplied

        if employee_id:

            from .models import Employee

            employee = get_object_or_404(
                Employee,
                id=employee_id,
                company=company
            )

            payroll.employee = employee


        payroll.month = month

        payroll.year = year

        payroll.basic_salary = (
            Decimal(basic_salary or "0")
        )

        payroll.allowance = (
            Decimal(allowance or "0")
        )

        payroll.deduction = (
            Decimal(deduction or "0")
        )


        # Calculate Net Salary

        payroll.net_salary = (
            payroll.basic_salary
            + payroll.allowance
            - payroll.deduction
        )


        payroll.save()


        messages.success(
            request,
            "Payroll updated successfully."
        )


        return redirect(
            "salary_payroll_list"
        )


    context = {

        "payroll": payroll,

        "appearance": appearance,

    }


    return render(
        request,
        "salary/salary_payroll_edit.html",
        context
    )
@login_required(login_url="login")
@company_type_required("salary")
def salary_payroll_delete(request, id):

    # Get logged-in user's company

    company = Company.objects.filter(
        user=request.user
    ).first()


    if company is None:

        messages.error(
            request,
            "Company not found."
        )

        return redirect("login")


    # Appearance settings

    appearance, created = SalaryThemeSettings.objects.get_or_create(
        company=company
    )


    # IMPORTANT:
    # Payroll must belong to logged-in company

    payroll = get_object_or_404(
        SalaryPayroll,
        id=id,
        company=company
    )


    if request.method == "POST":

        payroll.delete()


        messages.success(
            request,
            "Payroll deleted successfully."
        )


        return redirect(
            "salary_payroll_list"
        )


    context = {

        "payroll": payroll,

        "appearance": appearance,

    }


    return render(
        request,
        "salary/salary_payroll_delete.html",
        context
    )

@login_required(login_url="login")
@company_type_required("salary")
def attendance_dashboard(request): 

    company = get_object_or_404(
        Company,
        user=request.user
    )
 

    attendance = (
        Attendance.objects
        .filter(
            employee__company=company
        )
        .select_related(
            "employee"
        )
        .order_by(
            "-date",
            "-id"
        )
    )

 

    present_count = attendance.filter(
        status="Present"
    ).count()


    absent_count = attendance.filter(
        status="Absent"
    ).count()


    leave_count = attendance.filter(
        status="Leave"
    ).count()


    half_day_count = attendance.filter(
        status="Half Day"
    ).count()

 
    appearance, created = SalaryThemeSettings.objects.get_or_create(
        company=company
    )

 
    return render(
        request,
        "salary/attendance_dashboard.html",
        {
            "attendance": attendance,

            "present_count": present_count,

            "absent_count": absent_count,

            "leave_count": leave_count,

            "half_day_count": half_day_count,

            "company": company,

            "appearance": appearance,
        }
    )

@login_required(login_url="login")
@company_type_required("salary")
def mark_attendance(request):

    company = get_object_or_404(
        Company,
        user=request.user
    )

    appearance, created = SalaryThemeSettings.objects.get_or_create(
        company=company
    )

    employees = Employee.objects.filter(
        company=company
    ).order_by("name")

    if request.method == "POST":

        form = AttendanceForm(request.POST)

        form.fields["employee"].queryset = employees

        if form.is_valid():

            attendance = form.save(
                commit=False
            )

            employee = form.cleaned_data["employee"]

            # Security check
            if employee.company_id != company.id:

                messages.error(
                    request,
                    "Invalid employee selected."
                )

                return redirect(
                    "mark_attendance"
                )

            attendance.employee = employee

            attendance.save()

            messages.success(
                request,
                "Attendance saved successfully."
            )

            return redirect(
                "attendance_dashboard"
            )

    else:

        form = AttendanceForm()

        form.fields["employee"].queryset = employees

    return render(
        request,
        "salary/mark_attendance.html",
        {
            "form": form,
            "employees": employees,
            "company": company,
            "appearance": appearance,
        }
    )


@login_required(login_url="login")
@company_type_required("salary")
def edit_attendance(request, id):

    company = get_company(request)

    attendance = get_object_or_404(
        Attendance.objects.select_related("employee"),
        id=id,
        employee__company=company
    )

    employees = Employee.objects.filter(
        company=company,
        status="Active"
    ).order_by("name")

    appearance, created = SalaryThemeSettings.objects.get_or_create(
        company=company
    )

    if request.method == "POST":

        employee_id = request.POST.get("employee")
        date = request.POST.get("date")
        status = request.POST.get("status")
        check_in = request.POST.get("check_in")
        check_out = request.POST.get("check_out")
        remarks = request.POST.get("remarks")

        # Make sure selected employee belongs to this company
        employee = get_object_or_404(
            Employee,
            id=employee_id,
            company=company
        )

        attendance.employee = employee
        attendance.date = date
        attendance.status = status
        attendance.check_in = check_in or None
        attendance.check_out = check_out or None
        attendance.remarks = remarks or ""

        attendance.save()

        messages.success(
            request,
            "Attendance updated successfully."
        )

        return redirect("attendance_dashboard")

    return render(
        request,
        "salary/edit_attendance.html",
        {
            "attendance": attendance,
            "employees": employees,
            "company": company,
            "appearance": appearance,
        }
    )

@login_required(login_url="login")
@company_type_required("salary")
def delete_attendance(request, id):

    company = get_company(request)

    attendance = get_object_or_404(
        Attendance.objects.select_related("employee"),
        id=id,
        employee__company=company
    )

    appearance, created = SalaryThemeSettings.objects.get_or_create(
        company=company
    )

    if request.method == "POST":

        attendance.delete()

        messages.success(
            request,
            "Attendance deleted successfully."
        )

        return redirect("attendance_dashboard")

    return render(
        request,
        "salary/delete_attendance.html",
        {
            "attendance": attendance,
            "company": company,
            "appearance": appearance,
        }
    )

@login_required(login_url="login")
@company_type_required("salary")
def payslip_list(request): 

    company = get_company(request)

    if company is None:

        messages.error(
            request,
            "Company not found."
        )

        return redirect("login")

 

    appearance = SalaryThemeSettings.objects.filter(
        company=company
    ).first()

 
    payslips = (
        Payslip.objects
        .filter(company=company)
        .select_related("employee")
        .order_by("-created_at")
    )

 

    search = request.GET.get(
        "search",
        ""
    ).strip()


    if search:

        payslips = payslips.filter(
            employee__name__icontains=search
        )

 

    month = request.GET.get(
        "month",
        ""
    ).strip()


    if month and month != "All Months":

        payslips = payslips.filter(
            month=month
        )
 

    status = request.GET.get(
        "status",
        ""
    ).strip()


    if status and status != "All Status":

        payslips = payslips.filter(
            payment_status=status
        ) 
    total_payslips = payslips.count()


    paid_count = payslips.filter(
        payment_status="Paid"
    ).count()


    pending_count = payslips.filter(
        payment_status="Pending"
    ).count()

 

    from django.db.models import Sum

    total_salary = (
        payslips.aggregate(
            total=Sum("net_salary")
        )["total"]
        or 0
    )

 

    context = {

        "payslips": payslips,

        "paid_count": paid_count,

        "pending_count": pending_count,

        "total_salary": total_salary,

        "total_payslips": total_payslips,

        "company": company,

        "appearance": appearance,

    }

 

    return render(

        request,

        "salary/payslip_list.html",

        context

    )





@login_required(login_url="login")
@company_type_required("salary")
def payslip_create(request):
 

    company = get_object_or_404(
        Company,
        user=request.user
    )

 

    appearance, created = SalaryThemeSettings.objects.get_or_create(
        company=company
    )

 

    employees = Employee.objects.filter(
        company=company,
        status="Active"
    ).order_by("name")
 

    if request.method == "POST":

        employee_id = request.POST.get("employee")
        month = request.POST.get("month")
        year = request.POST.get("year")

        basic_salary = request.POST.get("basic_salary")
        allowance = request.POST.get("allowance") or "0"
        deduction = request.POST.get("deduction") or "0"

        payment_status = request.POST.get(
            "payment_status",
            "Pending"
        )

 

        employee = get_object_or_404(
            Employee,
            id=employee_id,
            company=company,
            status="Active"
        )

 

        try:

            basic_salary = Decimal(basic_salary)
            allowance = Decimal(allowance)
            deduction = Decimal(deduction)

        except (InvalidOperation, TypeError):

            messages.error(
                request,
                "Please enter valid salary amounts."
            )

            return render(
                request,
                "salary/payslip_create.html",
                {
                    "employees": employees,
                    "appearance": appearance,
                }
            )


        if basic_salary < 0 or allowance < 0 or deduction < 0:

            messages.error(
                request,
                "Salary amounts cannot be negative."
            )

            return render(
                request,
                "salary/payslip_create.html",
                {
                    "employees": employees,
                    "appearance": appearance,
                }
            )

 
        net_salary = (
            basic_salary
            + allowance
            - deduction
        )

 
        Payslip.objects.create(

            company=company,

            employee=employee,

            month=month,

            year=year,

            basic_salary=basic_salary,

            allowance=allowance,

            deduction=deduction,

            net_salary=net_salary,

            payment_status=payment_status
        )


        messages.success(
            request,
            "Payslip generated successfully."
        )


        return redirect(
            "payslip_list"
        )

 

    return render(
        request,
        "salary/payslip_create.html",
        {
            "employees": employees,
            "company": company,
            "appearance": appearance,
        }
    )

@login_required(login_url="login")
def payslip_edit(request, pk):

    payslip = get_object_or_404(
        Payslip,
        id=pk
    )

    if request.method == "POST":

        payslip.month = request.POST.get("month")
        payslip.year = request.POST.get("year")

        payslip.basic_salary = request.POST.get(
            "basic_salary"
        ) or 0

        payslip.allowance = request.POST.get(
            "allowance"
        ) or 0

        payslip.deduction = request.POST.get(
            "deduction"
        ) or 0

        payslip.payment_status = request.POST.get(
            "payment_status"
        )

        # Calculate net salary
        payslip.net_salary = (
            float(payslip.basic_salary)
            + float(payslip.allowance)
            - float(payslip.deduction)
        )

        payslip.save()

        messages.success(
            request,
            "Payslip updated successfully."
        )

        return redirect("payslip_list")

    return render(
        request,
        "salary/payslip_edit.html",
        {
            "payslip": payslip,
        }
    )

@login_required(login_url="login")
def payslip_delete(request, pk):

    payslip = get_object_or_404(
        Payslip,
        id=pk
    )

    if request.method == "POST":

        payslip.delete()

        messages.success(
            request,
            "Payslip deleted successfully."
        )

        return redirect("payslip_list")

    return render(
        request,
        "salary/payslip_delete.html",
        {
            "payslip": payslip,
        }
    )



@login_required(login_url="login")
@company_type_required("salary")
def bonus_list(request):
 

    company = get_company(request)

    if company is None:
        return render(
            request,
            "salary/bonus_list.html",
            {
                "bonuses": Bonus.objects.none(),
                "total_bonus": Decimal("0.00"),
                "paid_bonus": 0,
                "pending_bonus": 0,
                "appearance": None,
            }
        )
 

    appearance, created = SalaryThemeSettings.objects.get_or_create(
        company=company
    )
 

    bonuses = Bonus.objects.filter(
        company=company
    ).select_related(
        "employee"
    ).order_by(
        "-bonus_date",
        "-id"
    )
 
    search = request.GET.get(
        "search",
        ""
    ).strip()

    if search:

        bonuses = bonuses.filter(
            employee__name__icontains=search
        ) | bonuses.filter(
            bonus_title__icontains=search
        )

        bonuses = bonuses.distinct()
 

    bonus_type = request.GET.get(
        "bonus_type",
        ""
    ).strip()

    if bonus_type and bonus_type != "All":

        bonuses = bonuses.filter(
            bonus_type=bonus_type
        )
 
    payment_status = request.GET.get(
        "status",
        ""
    ).strip()

    if payment_status and payment_status != "All":

        bonuses = bonuses.filter(
            payment_status=payment_status
        ) 

    total_bonus = sum(
        (bonus.amount or Decimal("0.00"))
        for bonus in bonuses
    )

    paid_bonus = bonuses.filter(
        payment_status="Paid"
    ).count()

    pending_bonus = bonuses.filter(
        payment_status="Pending"
    ).count()
 
    bonus_types = (
        Bonus.objects
        .filter(company=company)
        .exclude(bonus_type__isnull=True)
        .exclude(bonus_type="")
        .values_list(
            "bonus_type",
            flat=True
        )
        .distinct()
        .order_by("bonus_type")
    )
 
    context = {

        "bonuses": bonuses,

        "total_bonus": total_bonus,

        "paid_bonus": paid_bonus,

        "pending_bonus": pending_bonus,

        "bonus_types": bonus_types,

        "appearance": appearance,

        "selected_search": search,

        "selected_bonus_type": bonus_type,

        "selected_status": payment_status,
    }

    return render(
        request,
        "salary/bonus_list.html",
        context
    )


@login_required(login_url="login")
@company_type_required("salary")
def bonus_create(request):
 
    company = get_company(request)

    if company is None:
        messages.error(request, "Company not found.")
        return redirect("login")
 
    appearance, created = SalaryThemeSettings.objects.get_or_create(
        company=company
    )
 
    employees = Employee.objects.filter(
        company=company,
        status="Active"
    ).order_by("name")
 
    if request.method == "POST":

        employee_id = request.POST.get("employee")
        bonus_title = request.POST.get("bonus_title", "").strip()
        bonus_type = request.POST.get("bonus_type", "Performance")
        amount = request.POST.get("amount")
        bonus_date = request.POST.get("bonus_date")
        description = request.POST.get("description", "").strip()
        payment_status = request.POST.get(
            "payment_status",
            "Pending"
        )
 
        if not employee_id:
            messages.error(
                request,
                "Please select an employee."
            )

        elif not bonus_title:
            messages.error(
                request,
                "Please enter a bonus title."
            )

        elif not amount:
            messages.error(
                request,
                "Please enter the bonus amount."
            )

        elif not bonus_date:
            messages.error(
                request,
                "Please select the bonus date."
            )

        else:

            # Important:
            # Employee must belong to logged-in company.
            employee = get_object_or_404(
                Employee,
                id=employee_id,
                company=company,
                status="Active"
            )

            try:
                Bonus.objects.create(
                    company=company,
                    employee=employee,
                    bonus_title=bonus_title,
                    bonus_type=bonus_type,
                    amount=amount,
                    bonus_date=bonus_date,
                    description=description,
                    payment_status=payment_status
                )

                messages.success(
                    request,
                    "Employee bonus saved successfully."
                )

                return redirect("bonus_list")

            except Exception as e:

                messages.error(
                    request,
                    f"Unable to save bonus: {str(e)}"
                )
 
    return render(
        request,
        "salary/bonus_create.html",
        {
            "employees": employees,
            "appearance": appearance,
            "company": company,
        }
    )





@login_required(login_url="login")
@company_type_required("salary")
def bonus_delete(request,id):

    company=get_company(request)

    bonus=get_object_or_404(
        Bonus,
        id=id,
        company=company
    )


    if request.method=="POST":

        bonus.delete()

        return redirect("bonus_list")


    return render(
        request,
        "salary/bonus_delete.html",
        {
            "bonus":bonus
        }
    )



@login_required(login_url="login")
@company_type_required("salary")
def deduction_list(request):
 

    company = get_company(request)
 

    if company is None:
        return render(
            request,
            "salary/deduction_list.html",
            {
                "deductions": Deduction.objects.none(),
                "total_amount": 0,
                "total_records": 0,
                "completed": 0,
                "pending": 0,
                "appearance": {
                    "theme": "light",
                    "accent_color": "#2563eb",
                    "font_size": "medium",
                    "dashboard_layout": "grid",
                    "sidebar_style": "expanded",
                    "language": "en",
                },
            }
        )
 
    appearance, created = SalaryThemeSettings.objects.get_or_create(
        company=company
    )
 
    deductions = (
        Deduction.objects
        .filter(company=company)
        .select_related("employee")
        .order_by("-deduction_date")
    )
 
    search = request.GET.get("search", "").strip()

    if search:

        deductions = deductions.filter(
            employee__name__icontains=search
        )
 

    deduction_type = request.GET.get(
        "deduction_type",
        ""
    ).strip()

    if deduction_type and deduction_type != "All Types":

        deductions = deductions.filter(
            deduction_type=deduction_type
        )
 

    status = request.GET.get(
        "status",
        ""
    ).strip()

    if status and status != "All Status":

        deductions = deductions.filter(
            status=status
        )
 

    total_records = deductions.count()

    total_amount = sum(
        deduction.amount or 0
        for deduction in deductions
    )

    completed = deductions.filter(
        status="Completed"
    ).count()

    pending = deductions.filter(
        status="Applied"
    ).count()
 

    context = {

        "company": company,

        "appearance": appearance,

        "deductions": deductions,

        "total_amount": total_amount,

        "total_records": total_records,

        "completed": completed,

        "pending": pending,

        # Keep current filter values
        "search": search,

        "selected_type": deduction_type,

        "selected_status": status,
    } 

    return render(
        request,
        "salary/deduction_list.html",
        context
    )

@login_required(login_url="login")
@company_type_required("salary")
def deduction_create(request):
 
    company = get_company(request)

    if company is None:

        messages.error(
            request,
            "Company not found."
        )

        return redirect("login")

 

    appearance, created = SalaryThemeSettings.objects.get_or_create(
        company=company
    )

 
    employees = Employee.objects.filter(
        company=company,
        status="Active"
    ).order_by("name")

 
    if request.method == "POST":

        Deduction.objects.create(

            company=company,

            employee_id=request.POST.get(
                "employee"
            ),

            deduction_title=request.POST.get(
                "deduction_title"
            ),

            deduction_type=request.POST.get(
                "deduction_type"
            ),

            amount=request.POST.get(
                "amount"
            ),

            deduction_date=request.POST.get(
                "deduction_date"
            ),

            description=request.POST.get(
                "description"
            ),

            status=request.POST.get(
                "status"
            )

        )
 

        messages.success(
            request,
            "Employee deduction added successfully."
        )
 

        return redirect(
            "deduction_list"
        )
 
    return render(

        request,

        "salary/deduction_create.html",

        {
            "employees": employees,

            # Send theme settings to template
            "appearance": appearance,
        }

    )

@login_required(login_url="login")
@company_type_required("salary")
def deduction_delete(request,id):


    company=get_company(request)



    deduction=get_object_or_404(

        Deduction,

        id=id,

        company=company

    )



    deduction.delete()



    return redirect(
        "deduction_list"
    )

@login_required(login_url="login")
@company_type_required("salary")
def add_employee(request): 

    if request.user.is_superuser:

        return HttpResponseForbidden(
            "Super Admin cannot add employees without selecting a company."
        )


    company = get_company(request)


    if company is None:

        messages.error(
            request,
            "Company not found."
        )

        return redirect(
            "login"
        )
 

    if company.company_type != "salary":

        return HttpResponseForbidden(
            "Access Denied! Your company is not authorized "
            "to access Employee Salary Management."
        )
 

    appearance, created = SalaryThemeSettings.objects.get_or_create(

        company=company

    )
 

    if request.method == "POST":

        form = EmployeeForm(

            request.POST

        )


        if form.is_valid():

            employee = form.save(

                commit=False

            )


            # Assign current company automatically
            employee.company = company


            employee.save()


            messages.success(

                request,

                "Employee Added Successfully."

            )


            return redirect(

                "employee_salary_list"

            )
 

    else:

        form = EmployeeForm()

 
    context = {

        "form": form,

        "company": company,

        "appearance": appearance,

    }


    return render(

        request,

        "salary/add_employee.html",

        context

    )



@login_required(login_url="login")
@company_type_required("salary")
def salary_report(request): 
    company = get_company(request)

    if company is None:

        messages.error(
            request,
            "Company not found."
        )

        return redirect("login")

 

    appearance, created = SalaryThemeSettings.objects.get_or_create(
        company=company
    )
 
    payrolls = Payroll.objects.filter(
        company=company
    ).select_related(
        "employee"
    ).order_by(
        "-year",
        "-id"
    )

 
    search = request.GET.get(
        "search",
        ""
    ).strip()

    if search:

        payrolls = payrolls.filter(

            employee__name__icontains=search

        ) | payrolls.filter(

            employee__employee_id__icontains=search

        )

 
    month = request.GET.get(
        "month",
        ""
    ).strip()

    if month:

        payrolls = payrolls.filter(
            month=month
        )

 

    year = request.GET.get(
        "year",
        ""
    ).strip()

    if year:

        payrolls = payrolls.filter(
            year=year
        )

 

    status = request.GET.get(
        "status",
        ""
    ).strip()

    if status:

        payrolls = payrolls.filter(
            payment_status=status
        )

 

    total_employees = payrolls.values(
        "employee"
    ).distinct().count()


    total_salary = payrolls.aggregate(
        total=Sum("net_salary")
    )["total"] or 0


    total_bonus = Bonus.objects.filter(
        company=company
    ).aggregate(
        total=Sum("amount")
    )["total"] or 0


    total_deduction = Deduction.objects.filter(
        company=company
    ).aggregate(
        total=Sum("amount")
    )["total"] or 0


    paid = payrolls.filter(
        payment_status="Paid"
    ).count()


    pending = payrolls.filter(
        payment_status="Pending"
    ).count()

 

    context = {

        # Payroll
        "payrolls": payrolls,

        # Summary
        "total_employees": total_employees,
        "total_salary": total_salary,
        "total_bonus": total_bonus,
        "total_deduction": total_deduction,
        "paid": paid,
        "pending": pending,

        # Appearance / Theme
        "appearance": appearance,

    }

 
    return render(

        request,

        "salary/salary_report.html",

        context

    )




@login_required(login_url="login")
@company_type_required("salary")
def salary_report_pdf(request):

    company = get_company(request)

    payrolls = Payroll.objects.filter(
        company=company
    )

    response = HttpResponse(
        content_type="application/pdf"
    )

    response["Content-Disposition"] = (
        'attachment; filename="Salary_Report.pdf"'
    )

    document = SimpleDocTemplate(response)

    styles = getSampleStyleSheet()

    elements = []

    title = Paragraph(
        "<b>Salary Report</b>",
        styles["Heading1"]
    )

    elements.append(title)

    elements.append(
        Paragraph("<br/>", styles["Normal"])
    )

    total_salary = payrolls.aggregate(
        Sum("net_salary")
    )["net_salary__sum"] or 0

    elements.append(

        Paragraph(
            f"<b>Total Employees :</b> {payrolls.count()}",
            styles["Normal"]
        )

    )

    elements.append(

        Paragraph(
            f"<b>Total Payroll :</b> ₹ {total_salary}",
            styles["Normal"]
        )

    )

    elements.append(
        Paragraph("<br/>", styles["Normal"])
    )

    data = [

        [

            "Employee",

            "Month",

            "Basic",

            "Allowance",

            "Deduction",

            "Net Salary",

            "Status"

        ]

    ]

    for item in payrolls:

        data.append([

            item.employee.name,

            f"{item.month} {item.year}",

            str(item.basic_salary),

            str(item.allowance),

            str(item.deduction),

            str(item.net_salary),

            item.payment_status

        ])

    table = Table(data)

    table.setStyle(

        TableStyle([

            ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#2563eb")),

            ("TEXTCOLOR",(0,0),(-1,0),colors.white),

            ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),

            ("GRID",(0,0),(-1,-1),0.5,colors.grey),

            ("BACKGROUND",(0,1),(-1,-1),colors.beige),

            ("ALIGN",(0,0),(-1,-1),"CENTER"),

            ("BOTTOMPADDING",(0,0),(-1,0),12),

        ])

    )

    elements.append(table)

    document.build(elements)

    return response


@login_required(login_url="login")
@company_type_required("salary")
def salary_portal(request):
    return render(
        request,
        "salary/salary_portal.html"
    )


@login_required(login_url="login")
@company_type_required("salary")
def salary_admin_login(request):
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
            return redirect("/salary-admin/")

        return render(
            request,
            "salary/salary_admin_login.html",
            {
                "error": "Invalid username or password.",
            },
        )

    return render(
        request,
        "salary/salary_admin_login.html",
    )


@login_required(login_url="login")
@company_type_required("salary")
def salary_staff_login(request):
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
            return redirect("salary_dashboard")

        return render(
            request,
            "salary/salary_staff_login.html",
            {
                "error": "Invalid username or password.",
            },
        )

    return render(
        request,
        "salary/salary_staff_login.html",
    )


@login_required(login_url="login")
@company_type_required("salary")
def salary_settings_page(request):

    company = request.user.company

    appearance, created = SalaryThemeSettings.objects.get_or_create(
        company=company,
        defaults={
            "theme": "light",
            "accent_color": "#2563eb",
            "font_size": "medium",
            "dashboard_layout": "grid",
            "sidebar_style": "expanded",
            "language": "en",
        }
    )

    return render(
        request,
        "salary/salary_settings_page.html",
        {
            "appearance": appearance,
        }
    )

@login_required(login_url="login")
@company_type_required("salary")
def salary_payroll_settings(request):

    company = request.user.company

    # Payroll Settings
    payroll_settings, created = SalaryPayrollSettings.objects.get_or_create(
        company=company
    )

    # Theme & Appearance Settings
    appearance, created = SalaryThemeSettings.objects.get_or_create(
        company=company
    )

    if request.method == "POST":

        form = PayrollSettingsForm(
            request.POST,
            instance=payroll_settings
        )

        if form.is_valid():

            payroll_settings = form.save(
                commit=False
            )

            payroll_settings.company = company

            payroll_settings.save()

            messages.success(
                request,
                "Payroll settings saved successfully."
            )

            return redirect(
                "salary_payroll_settings"
            )

    else:

        form = PayrollSettingsForm(
            instance=payroll_settings
        )

    return render(
        request,
        "salary/salary_payroll_settings.html",
        {
            "form": form,
            "payroll_settings": payroll_settings,
            "appearance": appearance,
        }
    )



@login_required(login_url="login")
@company_type_required("salary")
def salary_attendance_settings(request):
 
    company = getattr(
        request.user,
        "company",
        None
    )

    if company is None:

        messages.error(
            request,
            "Company profile not found."
        )

        return redirect("login")
 

    settings_obj, created = (
        SalaryAttendanceSettings.objects.get_or_create(
            company=company
        )
    )

 

    appearance, created = (
        SalaryThemeSettings.objects.get_or_create(
            company=company
        )
    )
 

    if request.method == "POST":

        form = SalaryAttendanceSettingsForm(
            request.POST,
            instance=settings_obj
        )

        if form.is_valid():

            attendance_settings = form.save(
                commit=False
            )

            attendance_settings.company = company

            attendance_settings.save()


            messages.success(
                request,
                "Attendance settings saved successfully."
            )


            return redirect(
                "salary_attendance_settings"
            )

    else:

        form = SalaryAttendanceSettingsForm(
            instance=settings_obj
        )
 

    return render(
        request,
        "salary/salary_attendance_settings.html",
        {
            "form": form,

            "attendance_settings": settings_obj,

            "appearance": appearance,
        }
    )


@login_required(login_url="login")
@company_type_required("salary")
def salary_payslip_settings(request):
 

    company = getattr(
        request.user,
        "company",
        None
    )

    if company is None:

        messages.error(
            request,
            "Company profile not found."
        )

        return redirect(
            "login"
        )

 
    settings_obj, created = (
        SalaryPayslipSettings.objects.get_or_create(
            company=company
        )
    )
 
    appearance, created = (
        SalaryThemeSettings.objects.get_or_create(
            company=company
        )
    )
 
    if request.method == "POST":

        form = SalaryPayslipSettingsForm(
            request.POST,
            instance=settings_obj
        )

        if form.is_valid():

            payslip_settings = form.save(
                commit=False
            )

            payslip_settings.company = company

            payslip_settings.save()


            messages.success(
                request,
                "Payslip settings saved successfully."
            )


            return redirect(
                "salary_payslip_settings"
            )

    else:

        form = SalaryPayslipSettingsForm(
            instance=settings_obj
        )
 
    return render(
        request,
        "salary/salary_payslip_settings.html",
        {
            "form": form,

            "payslip_settings": settings_obj,

            "appearance": appearance,
        }
    )


@login_required(login_url="login")
@company_type_required("salary")
def salary_tax_deductions_settings(request):
 
    company = getattr(
        request.user,
        "company",
        None
    )

    if company is None:

        messages.error(
            request,
            "Company profile not found."
        )

        return redirect(
            "login"
        )

 
    settings_obj, created = (
        SalaryTaxDeductionSettings.objects.get_or_create(
            company=company
        )
    )
 

    appearance, created = (
        SalaryThemeSettings.objects.get_or_create(
            company=company
        )
    )

 

    if request.method == "POST":

        form = SalaryTaxDeductionSettingsForm(
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
                "Tax & deduction settings saved successfully."
            )


            return redirect(
                "salary_tax_deductions_settings"
            )

    else:

        form = SalaryTaxDeductionSettingsForm(
            instance=settings_obj
        )
 

    return render(
        request,
        "salary/salary_tax_deductions_settings.html",
        {
            "form": form,

            "tax_settings": settings_obj,

            "appearance": appearance,
        }
    )



@login_required(login_url="login")
@company_type_required("salary")
def salary_bonus_settings(request):
 
    company = getattr(
        request.user,
        "company",
        None
    )

    if company is None:

        messages.error(
            request,
            "Company profile not found."
        )

        return redirect("login")
 

    settings_obj, created = (
        SalaryBonusSettings.objects.get_or_create(
            company=company
        )
    )

 

    appearance, created = (
        SalaryThemeSettings.objects.get_or_create(
            company=company
        )
    )
 

    if request.method == "POST":

        form = SalaryBonusSettingsForm(
            request.POST,
            instance=settings_obj
        )

        if form.is_valid():

            bonus_settings = form.save(
                commit=False
            )

            bonus_settings.company = company

            bonus_settings.save()


            messages.success(
                request,
                "Bonus settings saved successfully."
            )


            return redirect(
                "salary_bonus_settings"
            )

    else:

        form = SalaryBonusSettingsForm(
            instance=settings_obj
        )
 
    return render(
        request,
        "salary/salary_bonus_settings.html",
        {
            "form": form,

            "bonus_settings": settings_obj,

            "appearance": appearance,
        }
    )

@login_required(login_url="login")
@company_type_required("salary")
def employee_salary_settings(request):
 
    company = request.user.company

 

    settings_obj, created = (
        EmployeeSalarySettings.objects.get_or_create(
            company=company
        )
    )

 
    appearance, created = (
        SalaryThemeSettings.objects.get_or_create(
            company=company
        )
    )

 
    if request.method == "POST":

        form = EmployeeSalarySettingsForm(
            request.POST,
            instance=settings_obj
        )


        if form.is_valid():

            salary_settings = form.save(
                commit=False
            )

            salary_settings.company = company

            salary_settings.save()


            messages.success(
                request,
                "Employee salary settings saved successfully."
            )


            return redirect(
                "employee_salary_settings"
            )


    else:

        form = EmployeeSalarySettingsForm(
            instance=settings_obj
        )

 
    return render(
        request,
        "salary/employee_salary_settings.html",
        {
            "form": form,

            "salary_settings": settings_obj,

            "appearance": appearance,
        }
    )

@login_required(login_url="login")
@company_type_required("salary")
def salary_notification_settings(request):

    company = getattr(request.user, "company", None)

    if company is None:

        messages.error(
            request,
            "Company profile was not found."
        )

        return redirect("salary_dashboard")


    # Salary notification settings
    settings_obj, created = (
        SalaryNotificationSettings.objects.get_or_create(
            company=company
        )
    )


    # Get saved theme & appearance settings
    appearance, created = (
        SalaryThemeSettings.objects.get_or_create(
            company=company
        )
    )


    if request.method == "POST":

        form = SalaryNotificationSettingsForm(
            request.POST,
            instance=settings_obj
        )

        if form.is_valid():

            notification_settings = form.save(
                commit=False
            )

            notification_settings.company = company

            notification_settings.save()


            messages.success(
                request,
                "Salary notification settings saved successfully."
            )

            return redirect(
                "salary_notification_settings"
            )

    else:

        form = SalaryNotificationSettingsForm(
            instance=settings_obj
        )


    context = {

        "form": form,

        "salary_notifications_settings":
            settings_obj,

        "appearance":
            appearance,

    }


    return render(
        request,
        "salary/salary_notifications.html",
        context
    )


@login_required(login_url="login")
@company_type_required("salary")
def salary_theme_settings(request):

    company = getattr(
        request.user,
        "company",
        None
    )
    if company is None:

        messages.error(
            request,
            "Company profile was not found."
        )

        return redirect(
            "salary_dashboard"
        )

    theme_settings, created = (
        SalaryThemeSettings.objects.get_or_create(
            company=company,
            defaults={
                "theme": "light",
                "accent_color": "#2563eb",
                "font_size": "medium",
                "dashboard_layout": "grid",
                "sidebar_style": "expanded",
                "language": "en",
                "time_zone": "Asia/Kolkata",
                "show_breadcrumbs": True,
                "show_page_description": True,
                "compact_cards": False,
                "animations_enabled": True,
            }
        )
    )
    if request.method == "POST":

        form = SalaryThemeSettingsForm(
            request.POST,
            instance=theme_settings
        )

        if form.is_valid():

            saved_settings = form.save(
                commit=False
            )

            saved_settings.company = company

            saved_settings.save()

            messages.success(
                request,
                "Salary theme and appearance settings saved successfully."
            )

            return redirect(
                "salary_theme_settings"
            )

        else:

            messages.error(
                request,
                "Please correct the errors below."
            )


    else:

        form = SalaryThemeSettingsForm(
            instance=theme_settings
        )


    return render(
        request,
        "salary/salary_theme_appearance.html",
        {
            "form": form,
            "appearance": theme_settings,
            "theme_settings": theme_settings,
        }
    )
@login_required(login_url="login")
@company_type_required("salary")
def logout_salary(request):

    company = Company.objects.filter(
        user=request.user
    ).first()

    theme_settings = None

    if company:
        theme_settings = SalaryThemeSettings.objects.filter(
            company=company
        ).first()

    if request.method == "POST":

        logout(request)

        messages.success(
            request,
            "You have been logged out successfully."
        )

        return redirect("login")

    return render(
        request,
        "salary/logout_salary.html",
        {
            "theme_settings": theme_settings,
        }
    )