from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from students.decorators import company_type_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.db.models import Sum
from django.db import IntegrityError
from .models import EmployeeAttendanceSettings
from .forms import EmployeeAttendanceSettingsForm
from .models import EmployeeLeaveSettings
from .forms import EmployeeLeaveSettingsForm
from .models import EmployeePayrollSettings
from .forms import EmployeePayrollSettingsForm
from .models import EmployeeTaxSettings
from .forms import EmployeeTaxSettingsForm
from .models import EmployeeNotificationSettings
from .forms import EmployeeNotificationSettingsForm
from .models import EmployeeDocumentSettings
from .forms import EmployeeDocumentSettingsForm
from .models import EmployeeReportSettings
from .forms import EmployeeReportSettingsForm
from .models import EmployeeSecuritySettings
from .forms import EmployeeSecuritySettingsForm
from .models import EmployeeThemeSettings
from .forms import EmployeeThemeSettingsForm
from app.models import Company
from decimal import Decimal, InvalidOperation
from django.contrib.auth import logout
from .forms import EmployeeCompanyProfileForm
from .models import EmployeeCompanyProfile
from .models import (
    Employee,
    Attendance,
    Payroll,
    EmployeeDataSettings,
    EmployeeDepartmentSettings,
    EmployeeRoleData,
)

from .forms import (
    EmployeeDataSettingsForm,
    EmployeeDepartmentForm,
    EmployeeRoleForm,
)


from app.utils import get_company

def get_company(request):
    if not request.user.is_authenticated:
        return None

    return get_object_or_404(
        Company,
        user=request.user
    )
@login_required(login_url="login")
@company_type_required("employee")
def employee_dashboard(request):

    company = None
    company_profile = None
    appearance = None

    # ---------------- SUPER ADMIN ---------------- #

    if request.user.is_superuser:
        employees = Employee.objects.all()

    else:
        company = get_company(request)

        if not company:
            return HttpResponseForbidden(
                "No company profile is associated with this account."
            )

        employees = Employee.objects.filter(company=company)

        # Company Profile
        company_profile, _ = EmployeeCompanyProfile.objects.get_or_create(
            company=company,
            defaults={
                "company_name": company.company_name,
            }
        )

        # Theme Settings
        appearance, _ = EmployeeThemeSettings.objects.get_or_create(
            company=company
        )

    # ---------------- APPEARANCE ---------------- #

    theme = getattr(appearance, "theme", "light")
    accent_color = getattr(appearance, "accent_color", "#2563eb")
    font_size = getattr(appearance, "font_size", "medium")
    dashboard_layout = getattr(
        appearance,
        "dashboard_layout",
        "comfortable",
    )
    sidebar_style = getattr(
        appearance,
        "sidebar_style",
        "expanded",
    )

    # Remove time_zone (your model doesn't have it)
    time_zone = "Asia/Kolkata"

    # ---------------- STATISTICS ---------------- #

    total_employees = employees.count()

    active_employees = employees.filter(
        employment_status="Active"
    ).count()

    inactive_employees = employees.filter(
        employment_status="Inactive"
    ).count()

    departments = (
        employees.values("department")
        .distinct()
        .count()
    )

    new_employees = employees.count()

    total_salary = sum(
        (emp.salary or 0)
        for emp in employees
    )

    recent_employees = employees.order_by("-id")[:5]

    # ---------------- CONTEXT ---------------- #

    context = {
        "company": company,
        "company_profile": company_profile,

        "total": total_employees,
        "active": active_employees,
        "inactive": inactive_employees,
        "departments": departments,
        "new_employees": new_employees,
        "total_salary": total_salary,
        "recent_employees": recent_employees,

        "appearance": appearance,
        "theme": theme,
        "accent_color": accent_color,
        "font_size": font_size,
        "dashboard_layout": dashboard_layout,
        "sidebar_style": sidebar_style,
        "time_zone": time_zone,
    }

    return render(
        request,
        "employees/dashboard_employee.html",
        context,
    )


@login_required(login_url="login")
@company_type_required("employee")
def employee_list(request):

    company = get_company(request)

    if company is None:

        messages.error(
            request,
            "Company not found."
        )

        return redirect("login")

    employees = Employee.objects.filter(
        company=company
    ).order_by("first_name")

    print("CURRENT COMPANY ID:", company.id)
    print("CURRENT COMPANY NAME:", company.company_name)
    print("EMPLOYEE COUNT:", employees.count())

    for employee in employees:

        print(
            "EMPLOYEE:",
            employee.id,
            employee.employee_id,
            employee.first_name,
            "COMPANY:",
            employee.company_id
        )

    total_employees = employees.count()

    active_employees = employees.filter(
        employment_status="Active"
    ).count()

    appearance, created = EmployeeThemeSettings.objects.get_or_create(
        company=company
    )

    context = {
        "company": company,
        "employees": employees,
        "total": total_employees,
        "active_employees": active_employees,
        "appearance": appearance,
    }

    return render(
        request,
        "employees/employee_list.html",
        context
    )
@login_required(login_url="login")
@company_type_required("employee")
def employee_added(request):

    company = get_company(request)

    if company is None:

        messages.error(
            request,
            "Company not found."
        )

        return redirect("login")

    appearance, created = EmployeeThemeSettings.objects.get_or_create(
        company=company
    )

    if request.method == "POST":

        try:

            employee_id = request.POST.get("employee_id", "").strip()
            first_name = request.POST.get("first_name", "").strip()
            last_name = request.POST.get("last_name", "").strip()
            email = request.POST.get("email", "").strip()
            phone = request.POST.get("phone", "").strip()
            gender = request.POST.get("gender", "").strip()
            dob = request.POST.get("dob") or None
            address = request.POST.get("address", "").strip()
            role = request.POST.get("role", "").strip()
            department = request.POST.get("department", "").strip()
            designation = request.POST.get("designation", "").strip()
            joining_date = request.POST.get("joining_date") or None
            salary = request.POST.get("salary") or 0
            employment_status = request.POST.get(
                "employment_status",
                "Active"
            )

            employee = Employee.objects.create(

                company=company,

                employee_id=employee_id,

                first_name=first_name,

                last_name=last_name,

                email=email,

                phone=phone,

                gender=gender,

                dob=dob,

                address=address,

                role=role,

                department=department,

                designation=designation,

                joining_date=joining_date,

                salary=salary,

                employment_status=employment_status

            )

            print("EMPLOYEE SAVED:")
            print("Employee ID:", employee.id)
            print("Employee Code:", employee.employee_id)
            print("Company ID:", employee.company_id)

            messages.success(
                request,
                "Employee added successfully."
            )

            return redirect("employee_list")

        except Exception as e:

            print("EMPLOYEE SAVE ERROR:", e)

            messages.error(
                request,
                f"Employee could not be saved: {e}"
            )

    return render(
        request,
        "employees/employee_form.html",
        {
            "company": company,
            "appearance": appearance,
        }
    )

@login_required(login_url="login")
@company_type_required("employee")
def edit_employee(request, pk):

    company = get_company(request)

    employee = get_object_or_404(
        Employee,
        pk=pk,
        company=company
    )

    if request.method == "POST":

        employee.employee_id = request.POST["employee_id"]
        employee.first_name = request.POST["first_name"]
        employee.last_name = request.POST["last_name"]
        employee.email = request.POST["email"]
        employee.phone = request.POST["phone"]
        employee.gender = request.POST["gender"]
        employee.dob = request.POST["dob"]
        employee.address = request.POST["address"]
        employee.role = request.POST["role"]
        employee.department = request.POST["department"]
        employee.designation = request.POST["designation"]
        employee.joining_date = request.POST["joining_date"]
        employee.salary = request.POST["salary"]
        employee.employment_status = request.POST["employment_status"]

        employee.save()

        return redirect("employee_list")

    return render(
        request,
        "employees/employee_form.html",
        {"employee": employee}
    )



@login_required(login_url="login")
@company_type_required("employee")
def delete_employee(request, pk):

    company = get_company(request)

    employee = get_object_or_404(
        Employee,
        pk=pk,
        company=company
    )

    employee.delete()

    return redirect("employee_list")


@login_required(login_url="login")
@company_type_required("employee")
def employee_attendance_list(request):

    company = get_company(request)

    if company is None:
        messages.error(request, "Company not found.")
        return redirect("login")

    # Get company-specific appearance settings
    appearance = EmployeeThemeSettings.objects.filter(
        company=company
    ).first()

    # Get only this company's attendance records
    records = Attendance.objects.filter(
        company=company
    ).select_related(
        "employee"
    ).order_by(
        "-date"
    )

    # Correct attendance counts
    total_records = records.count()

    present_count = records.filter(
        status="Present"
    ).count()

    absent_count = records.filter(
        status="Absent"
    ).count()

    late_count = records.filter(
        status="Late"
    ).count()

    leave_count = records.filter(
        status="Leave"
    ).count()

    context = {
        "company": company,

        "appearance": appearance,

        "attendance": records,

        "total_records": total_records,

        "present_count": present_count,

        "absent_count": absent_count,

        "late_count": late_count,

        "leave_count": leave_count,
    }

    return render(
        request,
        "employees/employee_attendance_list.html",
        context
    )



@login_required(login_url="login")
@company_type_required("employee")
def employee_mark_attendance(request):

    company = get_company(request)

    if company is None:
        messages.error(
            request,
            "Company not found."
        )
        return redirect("login")

    # Get employees only from the logged-in company
    employees = Employee.objects.filter(
        company=company
    ).order_by(
        "first_name",
        "last_name"
    )

    # Get saved appearance settings
    appearance, created = EmployeeThemeSettings.objects.get_or_create(
        company=company
    )

    if request.method == "POST":

        employee_id = request.POST.get("employee")
        attendance_date = request.POST.get("date")
        status = request.POST.get("status")

        # Validation
        if not employee_id or not attendance_date or not status:

            messages.error(
                request,
                "Please fill in all required fields."
            )

            return render(
                request,
                "employees/employee_attendance_form.html",
                {
                    "employees": employees,
                    "company": company,
                    "appearance": appearance,
                }
            )

        # Make sure employee belongs to current company
        employee = Employee.objects.filter(
            id=employee_id,
            company=company
        ).first()

        if employee is None:

            messages.error(
                request,
                "Invalid employee selected."
            )

            return redirect(
                "employee_mark_attendance"
            )

        # Prevent duplicate attendance for same employee and date
        existing_attendance = Attendance.objects.filter(
            company=company,
            employee=employee,
            date=attendance_date
        ).first()

        if existing_attendance:

            # Update existing attendance
            existing_attendance.status = status
            existing_attendance.save()

            messages.success(
                request,
                "Attendance updated successfully."
            )

        else:

            # Create attendance
            Attendance.objects.create(
                company=company,
                employee=employee,
                date=attendance_date,
                status=status
            )

            messages.success(
                request,
                "Attendance marked successfully."
            )

        return redirect(
            "employee_attendance_list"
        )

    return render(
        request,
        "employees/employee_attendance_form.html",
        {
            "employees": employees,
            "company": company,
            "appearance": appearance,
        }
    )





@login_required(login_url="login")
@company_type_required("employee")
def employee_payroll(request):

    company = get_company(request)

    if company is None:
        return redirect("login")

    appearance, created = EmployeeThemeSettings.objects.get_or_create(
        company=company
    )

    payrolls = (
        Payroll.objects
        .filter(company=company)
        .select_related("employee")
        .order_by("-year", "-month")
    )

    return render(
        request,
        "employees/employee_payroll_list.html",
        {
            "payrolls": payrolls,
            "company": company,
            "appearance": appearance,
        }
    )


@login_required(login_url="login")
@company_type_required("employee")
def add_employee_payroll(request):

    # Get logged-in user's company
    company = get_company(request)

    if company is None:
        messages.error(
            request,
            "Company not found."
        )

        return redirect("login")


    # Get employees belonging only to this company
    employees = Employee.objects.filter(
        company=company
    ).order_by(
        "first_name",
        "last_name"
    )


    # Get company appearance settings
    appearance, created = EmployeeThemeSettings.objects.get_or_create(
        company=company
    )


    if request.method == "POST":

        employee_id = request.POST.get("employee")
        month = request.POST.get("month")
        year = request.POST.get("year")
        payment_status = request.POST.get(
            "payment_status",
            "Pending"
        )

        try:

            basic = Decimal(
                request.POST.get(
                    "basic_salary",
                    "0"
                )
            )

            bonus = Decimal(
                request.POST.get(
                    "bonus",
                    "0"
                )
            )

            deduction = Decimal(
                request.POST.get(
                    "deduction",
                    "0"
                )
            )

            year = int(year)

        except (
            InvalidOperation,
            TypeError,
            ValueError
        ):

            messages.error(
                request,
                "Please enter valid payroll details."
            )

            return render(
                request,
                "employees/employee_payroll_form.html",
                {
                    "employees": employees,
                    "company": company,
                    "appearance": appearance,
                }
            )


        # Validate employee belongs to this company
        try:

            employee = Employee.objects.get(
                id=employee_id,
                company=company
            )

        except Employee.DoesNotExist:

            messages.error(
                request,
                "Selected employee does not belong to your company."
            )

            return redirect(
                "add_employee_payroll"
            )


        # Calculate net salary
        net_salary = (
            basic
            + bonus
            - deduction
        )


        # Prevent negative salary
        if net_salary < 0:

            messages.error(
                request,
                "Net salary cannot be negative."
            )

            return render(
                request,
                "employees/employee_payroll_form.html",
                {
                    "employees": employees,
                    "company": company,
                    "appearance": appearance,
                }
            )


        # Create payroll record
        Payroll.objects.create(

            company=company,

            employee=employee,

            month=month,

            year=year,

            basic_salary=basic,

            bonus=bonus,

            deduction=deduction,

            net_salary=net_salary,

            payment_status=payment_status

        )


        messages.success(
            request,
            "Payroll added successfully."
        )


        return redirect(
            "employee_payroll"
        )


    return render(
        request,
        "employees/employee_payroll_form.html",
        {
            "employees": employees,
            "company": company,
            "appearance": appearance,
        }
    )
@login_required(login_url="login")
@company_type_required("employee")
def edit_employee_payroll(request, pk):

    company = get_company(request)

    if company is None:
        messages.error(request, "Company not found.")
        return redirect("login")

    appearance, created = EmployeeThemeSettings.objects.get_or_create(
        company=company
    )

    payroll = get_object_or_404(
        Payroll,
        id=pk,
        company=company
    )

    employees = Employee.objects.filter(company=company).order_by(
        "first_name", "last_name"
    )

    if request.method == "POST":

        employee_id = request.POST.get("employee")
        month = request.POST.get("month")
        year = request.POST.get("year")
        payment_status = request.POST.get("payment_status", "Pending")

        try:
            basic = Decimal(request.POST.get("basic_salary", "0"))
            bonus = Decimal(request.POST.get("bonus", "0"))
            deduction = Decimal(request.POST.get("deduction", "0"))
            year = int(year)
        except (InvalidOperation, TypeError, ValueError):
            messages.error(request, "Please enter valid payroll details.")
            return render(
                request,
                "employees/employee_payroll_form.html",
                {
                    "employees": employees,
                    "payroll": payroll,
                    "appearance": appearance,
                    "edit_mode": True,
                },
            )

        employee = get_object_or_404(
            Employee,
            id=employee_id,
            company=company
        )

        net_salary = basic + bonus - deduction

        if net_salary < 0:
            messages.error(request, "Net salary cannot be negative.")
            return render(
                request,
                "employees/employee_payroll_form.html",
                {
                    "employees": employees,
                    "payroll": payroll,
                    "appearance": appearance,
                    "edit_mode": True,
                },
            )

        payroll.employee = employee
        payroll.month = month
        payroll.year = year
        payroll.basic_salary = basic
        payroll.bonus = bonus
        payroll.deduction = deduction
        payroll.net_salary = net_salary
        payroll.payment_status = payment_status
        payroll.save()

        messages.success(request, "Payroll updated successfully.")
        return redirect("employee_payroll")

    return render(
        request,
        "employees/employee_payroll_form.html",
        {
            "employees": employees,
            "payroll": payroll,
            "appearance": appearance,
            "edit_mode": True,
        },
    )

@login_required(login_url="login")
@company_type_required("employee")
def delete_employee_payroll(request, pk):

    company = get_company(request)

    if company is None:
        messages.error(request, "Company not found.")
        return redirect("login")

    payroll = get_object_or_404(
        Payroll,
        id=pk,
        company=company
    )

    if request.method == "POST":
        payroll.delete()
        messages.success(request, "Payroll deleted successfully.")
        return redirect("employee_payroll")

    return render(
        request,
        "employees/delete_payroll.html",
        {
            "payroll": payroll,
        },
    )


@login_required(login_url="login")
@company_type_required("employee")
def department_list(request):

    # Get logged-in user's company
    company = get_company(request)


    # Validate company
    if company is None:

        messages.error(
            request,
            "Company not found."
        )

        return redirect("login")


    # Get departments belonging only to this company
    departments = EmployeeDepartmentSettings.objects.filter(
        company=company
    ).prefetch_related(
        "roles"
    )


    # Get or create Appearance Settings for this company
    appearance, created = EmployeeThemeSettings.objects.get_or_create(
        company=company
    )


    # Render department page
    return render(
        request,
        "employees/department_list.html",
        {
            "departments": departments,
            "company": company,
            "appearance": appearance,
        }
    )



@login_required(login_url="login")
@company_type_required("employee")
def add_department(request):

    company = get_company(request)

    if company is None:

        messages.error(
            request,
            "Company not found."
        )

        return redirect("login")


    # Get appearance settings for the current company
    appearance, created = EmployeeThemeSettings.objects.get_or_create(
        company=company
    )


    if request.method == "POST":

        form = EmployeeDepartmentForm(
            request.POST
        )

        if form.is_valid():

            department = form.save(
                commit=False
            )

            department.company = company

            try:

                department.save()

                messages.success(
                    request,
                    "Department created successfully."
                )

                return redirect(
                    "department_list"
                )

            except IntegrityError:

                form.add_error(
                    "name",
                    "This department already exists."
                )

    else:

        form = EmployeeDepartmentForm()


    return render(
        request,
        "employees/department_form.html",
        {
            "form": form,
            "company": company,
            "appearance": appearance,
        }
    )

@login_required(login_url="login")
@company_type_required("employee")
def edit_department(request, pk):

    company = get_company(request)

    if company is None:
        messages.error(request, "Company not found.")
        return redirect("login")

    # Department belongs only to this company
    department = get_object_or_404(
        EmployeeDepartmentSettings,
        id=pk,
        company=company
    )

    appearance, created = EmployeeThemeSettings.objects.get_or_create(
        company=company
    )

    if request.method == "POST":

        form = EmployeeDepartmentForm(
            request.POST,
            instance=department
        )

        if form.is_valid():

            updated_department = form.save(commit=False)
            updated_department.company = company

            try:
                updated_department.save()

                messages.success(
                    request,
                    "Department updated successfully."
                )

                return redirect("department_list")

            except IntegrityError:
                form.add_error(
                    "name",
                    "This department already exists."
                )

    else:

        form = EmployeeDepartmentForm(instance=department)

    return render(
        request,
        "employees/department_form.html",
        {
            "form": form,
            "company": company,
            "appearance": appearance,
            "edit_mode": True,
            "department": department,
        }
    )

@login_required(login_url="login")
@company_type_required("employee")
def delete_department(request, pk):

    company = get_company(request)

    if company is None:
        messages.error(request, "Company not found.")
        return redirect("login")

    department = get_object_or_404(
        EmployeeDepartmentSettings,
        id=pk,
        company=company
    )

    appearance, created = EmployeeThemeSettings.objects.get_or_create(
        company=company
    )

    if request.method == "POST":

        department.delete()

        messages.success(
            request,
            "Department deleted successfully."
        )

        return redirect("department_list")

    return render(
        request,
        "employees/delete_department.html",
        {
            "department": department,
            "company": company,
            "appearance": appearance,
        }
    )



@login_required(login_url="login")
@company_type_required("employee")
def employee_reports(request):

    # Get logged-in company
    company = get_company(request)

    # Get appearance settings for this company
    appearance, created = EmployeeThemeSettings.objects.get_or_create(
        company=company
    )

    # Get company employees
    employees = Employee.objects.filter(
        company=company
    )

    # Get company attendance
    attendance = Attendance.objects.filter(
        company=company
    )

    # Get company payroll
    payroll = Payroll.objects.filter(
        company=company
    )

    # Get company departments
    departments = EmployeeDepartmentSettings.objects.filter(
        company=company
    )

    context = {

        # Appearance settings
        "appearance": appearance,

        # Company
        "company": company,

        # Employee statistics
        "total_employees":
            employees.count(),

        "active_employees":
            employees.filter(
                employment_status="Active"
            ).count(),

        "inactive_employees":
            employees.filter(
                employment_status="Inactive"
            ).count(),

        # Department statistics
        "department_count":
            departments.count(),

        # Attendance statistics
        "attendance_count":
            attendance.count(),

        "present_count":
            attendance.filter(
                status="Present"
            ).count(),

        "leave_count":
            attendance.filter(
                status="Leave"
            ).count(),

        # Payroll statistics
        "payroll_count":
            payroll.count(),

        "total_salary":
            payroll.aggregate(
                total=Sum("net_salary")
            )["total"] or 0,

        # Recent employees
        "recent_employees":
            employees.order_by("-id")[:5],
    }

    return render(
        request,
        "employees/reports_employee.html",
        context
    )






@login_required(login_url="login")
@company_type_required("employee")
def employee_portal(request):
    return render(request, "employees/employee_portal.html")


@login_required(login_url="login")
@company_type_required("employee")
def employee_admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        print("Username:", username)

        user = authenticate(
            request,
            username=username,
            password=password
        )

        print("Authenticated:", user)

        if user:
            print("is_staff:", user.is_staff)
            print("is_superuser:", user.is_superuser)

        if user is not None and user.is_superuser:
            login(request, user)
            print("Employee Admin Login Success")
            return redirect("/employee-admin/")

        print("Employee Admin Login Failed")

        return render(
            request,
            "employees/employee_admin_login.html",
            {
                "error": "Invalid username or password."
            }
        )

    return render(request, "employees/employee_admin_login.html")

@login_required(login_url="login")
@company_type_required("employee")
def employee_staff_login(request):
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
            return redirect("employee_dashboard")

        return render(
            request,
            "employees/employee_staff_login.html",
            {
                "error": "Invalid username or password."
            }
        )

    return render(
        request,
        "employees/employee_staff_login.html"
    )


@login_required(login_url="login")
@company_type_required("employee")
def employee_settings(request):

    # Get logged-in user's company
    company = Company.objects.filter(
        user=request.user
    ).first()

    if not company:
        return render(
            request,
            "employees/employees_settings_data.html",
            {
                "error": "Company profile was not found.",
                "appearance": None,
            }
        )

    # Get or create appearance settings for this company
    appearance, created =  EmployeeThemeSettings.objects.get_or_create(
        company=company
    )

    return render(
        request,
        "employees/employees_settings_data.html",
        {
            "company": company,
            "appearance": appearance,
        }
    )




@login_required(login_url="login")
@company_type_required("employee")
def employee_general_settings(request):


    company = Company.objects.filter(
        user=request.user
    ).first()


    if not company:

        return render(
            request,
            "employees/general.html",
            {
                "error": "Company profile was not found."
            }
        )

    employee_settings, created = (
        EmployeeDataSettings.objects.get_or_create(
            company=company
        )
    )


    appearance, appearance_created = (
        EmployeeThemeSettings.objects.get_or_create(
            company=company
        )
    )

    if request.method == "POST":

        form = EmployeeDataSettingsForm(
            request.POST,
            instance=employee_settings
        )

        if form.is_valid():

            employee_settings = form.save(
                commit=False
            )

            employee_settings.company = company

            employee_settings.save()

            return redirect(
                "employee_general_settings"
            )


    else:

        form = EmployeeDataSettingsForm(
            instance=employee_settings
        )


    return render(
        request,
        "employees/general.html",
        {
            "company": company,

            "employee_settings": employee_settings,

            "form": form,

            # Theme & Appearance
            "appearance": appearance,
        }
    )
@login_required(login_url="login")
@company_type_required("employee")
def employee_profile_settings(request):

    company = getattr(request.user, "company", None)

    if company is None:
        return render(
            request,
            "employees/employee_profile.html",
            {"error": "Company profile could not be found."}
        )

    profile, created = EmployeeCompanyProfile.objects.get_or_create(
        company=company,
        defaults={
            "company_name": company.company_name,
        }
    )

    appearance, _ = EmployeeThemeSettings.objects.get_or_create(
        company=company
    )

    if request.method == "POST":
        form = EmployeeCompanyProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():
            employee_profile = form.save(commit=False)
            employee_profile.company = company
            employee_profile.save()

            messages.success(
                request,
                "Company profile updated successfully."
            )
            return redirect("employee_profile_settings")

    else:
        form = EmployeeCompanyProfileForm(instance=profile)

    return render(
        request,
        "employees/employee_profile.html",
        {
            "form": form,
            "company": company,
            "profile": profile,
            "appearance": appearance,
        }
    )
@login_required(login_url="login")
@company_type_required("employee")
def employee_departments_roles_settings(request):

    company = get_object_or_404(
        Company,
        user=request.user
    )



    appearance, created = (
        EmployeeThemeSettings.objects.get_or_create(
            company=company
        )
    )


    if request.method == "POST":

        form_type = request.POST.get(
            "form_type"
        )



        if form_type == "department":

            department_form = EmployeeDepartmentForm(
                request.POST
            )

            role_form = EmployeeRoleForm()

            role_form.fields["department"].queryset = (
                EmployeeDepartmentSettings.objects
                .filter(
                    company=company,
                    is_active=True
                )
                .order_by("name")
            )


            if department_form.is_valid():

                department = department_form.save(
                    commit=False
                )

                department.company = company

                department.save()


                messages.success(
                    request,
                    "Department added successfully."
                )


                return redirect(
                    "employee_departments_roles_settings"
                )



        elif form_type == "role":

            department_form = EmployeeDepartmentForm()

            role_form = EmployeeRoleForm(
                request.POST
            )
            role_form.fields["department"].queryset = (
                EmployeeDepartmentSettings.objects
                .filter(
                    company=company,
                    is_active=True
                )
                .order_by("name")
            )


            if role_form.is_valid():

                role = role_form.save(
                    commit=False
                )

                role.company = company

                role.save()


                messages.success(
                    request,
                    "Role added successfully."
                )


                return redirect(
                    "employee_departments_roles_settings"
                )



    else:

        department_form = EmployeeDepartmentForm()

        role_form = EmployeeRoleForm()


        role_form.fields["department"].queryset = (
            EmployeeDepartmentSettings.objects
            .filter(
                company=company,
                is_active=True
            )
            .order_by("name")
        )



    departments = (
        EmployeeDepartmentSettings.objects
        .filter(
            company=company
        )
        .prefetch_related("roles")
        .order_by("name")
    )



    roles = (
        EmployeeRoleData.objects
        .filter(
            company=company
        )
        .select_related("department")
        .order_by(
            "department__name",
            "name"
        )
    )


    context = {

        "company": company,

        "departments": departments,

        "roles": roles,

        "department_count": departments.count(),

        "role_count": roles.count(),

        "department_form": department_form,

        "role_form": role_form,

        # IMPORTANT:
        # This is what your HTML uses.
        "appearance": appearance,

    }



    return render(
        request,
        "employees/departments_roles.html",
        context
    )

@login_required(login_url="login")
@company_type_required("employee")
def employee_department_delete(request, pk):

    company = get_object_or_404(
        Company,
        user=request.user
    )

    department = get_object_or_404(
        EmployeeDepartmentSettings,
        pk=pk,
        company=company
    )

    if request.method == "POST":

        department.delete()

        messages.success(
            request,
            "Department deleted successfully."
        )

    return redirect(
        "employee_departments_roles_settings"
    )

@login_required(login_url="login")
@company_type_required("employee")
def employee_department_edit(request, pk):

    company = get_object_or_404(
        Company,
        user=request.user
    )

    department = get_object_or_404(
        EmployeeDepartmentSettings,
        pk=pk,
        company=company
    )

    if request.method == "POST":

        form = EmployeeDepartmentForm(
            request.POST,
            instance=department
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Department updated successfully."
            )

            return redirect(
                "employee_departments_roles_settings"
            )

    else:

        form = EmployeeDepartmentForm(
            instance=department
        )

    return render(
        request,
        "employees/department_edit.html",
        {
            "form": form,
            "department": department,
            "company": company,
        }
    )

@login_required(login_url="login")
@company_type_required("employee")
def employee_role_edit(request, pk):

    company = get_object_or_404(
        Company,
        user=request.user
    )

    role = get_object_or_404(
        EmployeeRoleData,
        pk=pk,
        company=company
    )

    if request.method == "POST":

        form = EmployeeRoleForm(
            request.POST,
            instance=role
        )

        form.fields["department"].queryset = (
            EmployeeDepartmentSettings.objects
            .filter(
                company=company,
                is_active=True
            )
            .order_by("name")
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Role updated successfully."
            )

            return redirect(
                "employee_departments_roles_settings"
            )

    else:

        form = EmployeeRoleForm(
            instance=role
        )

        form.fields["department"].queryset = (
            EmployeeDepartmentSettings.objects
            .filter(
                company=company,
                is_active=True
            )
            .order_by("name")
        )

    return render(
        request,
        "employees/role_edit.html",
        {
            "form": form,
            "role": role,
            "company": company,
        }
    )

@login_required(login_url="login")
@company_type_required("employee")
def employee_role_delete(request, pk):

    company = get_object_or_404(
        Company,
        user=request.user
    )

    role = get_object_or_404(
        EmployeeRoleData,
        pk=pk,
        company=company
    )

    if request.method == "POST":

        role.delete()

        messages.success(
            request,
            "Role deleted successfully."
        )

    return redirect(
        "employee_departments_roles_settings"
    )

@login_required(login_url="login")
@company_type_required("employee")
def employee_attendance_settings(request):


    company = Company.objects.filter(
        user=request.user
    ).first()

    if company is None:

        return render(
            request,
            "employees/attendance_settings.html",
            {
                "error": "Company profile could not be found."
            }
        )



    attendance_settings, created = (
        EmployeeAttendanceSettings.objects.get_or_create(
            company=company
        )
    )


    appearance, appearance_created = (
        EmployeeThemeSettings.objects.get_or_create(
            company=company
        )
    )


    if request.method == "POST":

        form = EmployeeAttendanceSettingsForm(
            request.POST,
            instance=attendance_settings
        )

        if form.is_valid():

            settings = form.save(
                commit=False
            )

            settings.company = company

            settings.save()

            messages.success(
                request,
                "Attendance settings saved successfully."
            )

            return redirect(
                "employee_attendance_settings"
            )



    else:

        form = EmployeeAttendanceSettingsForm(
            instance=attendance_settings
        )



    context = {

        "company": company,

        "form": form,

        "attendance_settings":
            attendance_settings,

        # Theme / Appearance
        "appearance":
            appearance,
    }



    return render(
        request,
        "employees/attendance_settings.html",
        context
    )

@login_required(login_url="login")
@company_type_required("employee")
def employee_leave_settings(request):

    # Get logged-in user's company
    company = get_company(request)

    # Company validation
    if company is None:

        return HttpResponseForbidden(
            "Company profile not found."
        )

    # Get company appearance settings
    appearance, created = (
        EmployeeThemeSettings.objects.get_or_create(
            company=company
        )
    )

    # Get employee leave settings
    leave_settings, created = (
        EmployeeLeaveSettings.objects.get_or_create(
            company=company
        )
    )

    # Handle form submission
    if request.method == "POST":

        form = EmployeeLeaveSettingsForm(
            request.POST,
            instance=leave_settings
        )

        if form.is_valid():

            settings = form.save(
                commit=False
            )

            settings.company = company

            settings.save()

            messages.success(
                request,
                "Leave settings saved successfully."
            )

            return redirect(
                "employee_leave_settings"
            )

    else:

        form = EmployeeLeaveSettingsForm(
            instance=leave_settings
        )

    return render(
        request,
        "employees/leave.html",
        {
            "company": company,
            "appearance": appearance,
            "leave_settings": leave_settings,
            "form": form,
        }
    )

@login_required(login_url="login")
@company_type_required("employee")
def employee_payroll_settings(request):

    company = get_company(request)

    if company is None:
        return HttpResponseForbidden(
            "Company profile not found."
        )

    # Get Payroll Settings
    payroll_settings, created = (
        EmployeePayrollSettings.objects.get_or_create(
            company=company
        )
    )

    # Get Theme & Appearance Settings
    appearance, created = (
        EmployeeThemeSettings.objects.get_or_create(
            company=company
        )
    )

    if request.method == "POST":

        form = EmployeePayrollSettingsForm(
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
                "employee_payroll_settings"
            )

    else:

        form = EmployeePayrollSettingsForm(
            instance=payroll_settings
        )

    context = {
        "company": company,
        "form": form,
        "payroll_settings": payroll_settings,

        # Theme & Appearance
        "appearance": appearance,
    }

    return render(
        request,
        "employees/payroll_settings.html",
        context
    )

@login_required(login_url="login")
@company_type_required("employee")
def employee_tax_settings(request):

    # Get logged-in user's company
    company = get_company(request)

    if company is None:
        return HttpResponseForbidden(
            "Company profile not found."
        )

    # Tax settings
    tax_settings, created = (
        EmployeeTaxSettings.objects.get_or_create(
            company=company
        )
    )

    # Theme & Appearance settings
    appearance, created = (
        EmployeeThemeSettings.objects.get_or_create(
            company=company
        )
    )

    # Save tax settings
    if request.method == "POST":

        form = EmployeeTaxSettingsForm(
            request.POST,
            instance=tax_settings
        )

        if form.is_valid():

            tax_settings = form.save(
                commit=False
            )

            # Make sure settings belong to this company
            tax_settings.company = company

            tax_settings.save()

            messages.success(
                request,
                "Tax & Statutory settings saved successfully."
            )

            return redirect(
                "employee_tax_settings"
            )

    else:

        form = EmployeeTaxSettingsForm(
            instance=tax_settings
        )

    context = {
        "company": company,
        "tax_settings": tax_settings,
        "form": form,

        # Theme appearance data
        "appearance": appearance,
    }

    return render(
        request,
        "employees/tax_statutory.html",
        context
    )

@login_required(login_url="login")
@company_type_required("employee")
def employee_notification_settings(request):


    company = get_object_or_404(
        Company,
        user=request.user
    )


    notification_settings, created = (
        EmployeeNotificationSettings.objects
        .get_or_create(
            company=company
        )
    )


    appearance, appearance_created = (
        EmployeeThemeSettings.objects
        .get_or_create(
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
    )


    if request.method == "POST":

        form = EmployeeNotificationSettingsForm(
            request.POST,
            instance=notification_settings
        )


        if form.is_valid():

            notification_settings = form.save(
                commit=False
            )


            # Always connect settings
            # to the logged-in company
            notification_settings.company = company


            notification_settings.save()


            messages.success(
                request,
                "Employee notification settings saved successfully."
            )


            return redirect(
                "employee_notification_settings"
            )


    else:

        form = EmployeeNotificationSettingsForm(
            instance=notification_settings
        )



    context = {

        "company": company,

        "form": form,

        "notification_settings":
            notification_settings,

        # Theme & Appearance
        "appearance": appearance,

    }


    return render(
        request,
        "employees/employee_notifications_settings.html",
        context
    )


@login_required(login_url="login")
@company_type_required("employee")
def employee_document_settings(request):

    # Get logged-in user's company
    company = Company.objects.filter(
        user=request.user
    ).first()

    # Company validation
    if company is None:

        return render(
            request,
            "employees/documents.html",
            {
                "error": "Company profile could not be found."
            }
        )

    # Get or create document settings
    document_settings, created = (
        EmployeeDocumentSettings.objects.get_or_create(
            company=company
        )
    )

    # Get or create theme & appearance settings
    appearance, created = (
        EmployeeThemeSettings.objects.get_or_create(
            company=company
        )
    )

    # Handle form submission
    if request.method == "POST":

        form = EmployeeDocumentSettingsForm(
            request.POST,
            instance=document_settings
        )

        if form.is_valid():

            settings = form.save(
                commit=False
            )

            # Always attach settings
            # to the logged-in company
            settings.company = company

            settings.save()

            messages.success(
                request,
                "Employee document settings saved successfully."
            )

            return redirect(
                "employee_document_settings"
            )

    else:

        form = EmployeeDocumentSettingsForm(
            instance=document_settings
        )

    # Template context
    context = {
        "company": company,
        "form": form,
        "document_settings": document_settings,

        # Theme & Appearance
        "appearance": appearance,
    }

    return render(
        request,
        "employees/documents.html",
        context
    )


@login_required(login_url="login")
@company_type_required("employee")
def employee_report_settings(request):


    company = Company.objects.filter(
        user=request.user
    ).first()


    if company is None:

        return render(
            request,
            "employees/reports_settings.html",
            {
                "error": "Company profile could not be found."
            }
        )


    report_settings, created = (
        EmployeeReportSettings.objects.get_or_create(
            company=company
        )
    )


    appearance, created = (
        EmployeeThemeSettings.objects.get_or_create(
            company=company
        )
    )


    if request.method == "POST":

        form = EmployeeReportSettingsForm(
            request.POST,
            instance=report_settings
        )


        if form.is_valid():

            report_settings = form.save(
                commit=False
            )

            report_settings.company = company

            report_settings.save()


            messages.success(
                request,
                "Employee report settings saved successfully."
            )


            return redirect(
                "employee_report_settings"
            )



    else:

        form = EmployeeReportSettingsForm(
            instance=report_settings
        )


    context = {

        "company": company,

        "form": form,

        "report_settings": report_settings,

        # Theme & Appearance
        "appearance": appearance,

    }


    return render(
        request,
        "employees/reports_settings.html",
        context
    )
@login_required(login_url="login")
@company_type_required("employee")
def employee_security_settings(request):

    company = Company.objects.filter(
        user=request.user
    ).first()

    if company is None:
        return render(
            request,
            "employees/security_permissions.html",
            {
                "error": "Company profile could not be found.",
            }
        )

    # Security settings
    security_settings, _ = (
        EmployeeSecuritySettings.objects.get_or_create(
            company=company
        )
    )

    # Theme & Appearance settings
    theme_settings, _ = (
        EmployeeThemeSettings.objects.get_or_create(
            company=company,
            defaults={
                "theme": "light",
                "accent_color": "#2563eb",
                "font_size": "medium",
                "dashboard_layout": "grid",
                "sidebar_style": "expanded",
            }
        )
    )

    if request.method == "POST":

        form = EmployeeSecuritySettingsForm(
            request.POST,
            instance=security_settings
        )

        if form.is_valid():

            security_settings = form.save(
                commit=False
            )

            security_settings.company = company
            security_settings.save()

            messages.success(
                request,
                "Security & permissions settings saved successfully."
            )

            return redirect(
                "employee_security_settings"
            )

    else:

        form = EmployeeSecuritySettingsForm(
            instance=security_settings
        )

    context = {
        "company": company,
        "form": form,
        "security_settings": security_settings,

        # IMPORTANT
        # Security page uses theme_settings.xxx
        "theme_settings": theme_settings,
    }

    return render(
        request,
        "employees/security_permissions.html",
        context
    )
@login_required(login_url="login")
@company_type_required("employee")
def employee_theme_settings(request):

    company = Company.objects.filter(
        user=request.user
    ).first()

    if company is None:

        return render(
            request,
            "employees/theme_appearance.html",
            {
                "error": "Company profile could not be found."
            }
        )

    theme_settings, created = (
        EmployeeThemeSettings.objects.get_or_create(
            company=company
        )
    )

    if request.method == "POST":

        form = EmployeeThemeSettingsForm(
            request.POST,
            instance=theme_settings
        )

        if form.is_valid():

            settings = form.save(
                commit=False
            )

            settings.company = company

            settings.save()

            messages.success(
                request,
                "Theme and appearance settings saved successfully."
            )

            return redirect(
                "employee_theme_settings"
            )

    else:

        form = EmployeeThemeSettingsForm(
            instance=theme_settings
        )

    context = {
        "company": company,
        "form": form,
        "theme_settings": theme_settings,
    }

    return render(
        request,
        "employees/theme_appearance.html",
        context
    )

@login_required(login_url="login")
@company_type_required("employee")
def logout_employee(request):

    company = Company.objects.filter(
        user=request.user
    ).first()

    theme_settings = None

    if company:
        theme_settings = EmployeeThemeSettings.objects.filter(
            company=company
        ).first()

    if request.method == "POST":

        logout(request)

        messages.success(
            request,
            "You have been logged out successfully."
        )

        return redirect("login")

    context = {
        "theme_settings": theme_settings,
    }

    return render(
        request,
        "employees/logout_employee.html",
        context
    )