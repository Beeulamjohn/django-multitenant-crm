from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib import messages
from django.contrib.auth import (
    logout,
    update_session_auth_hash
)
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session

from django.db.models import Sum, Q
from django.http import HttpResponseForbidden
from django.utils import timezone

import re

from students.decorators import company_type_required

from app.models import Company
from app.utils import get_company

from employees.models import Staff

from billing.models import Invoice

from .models import (
    Student,
    StudentDocument,
    StudentStaff,
    Course,
    CompanyProfile,
    UserProfile,
    LoginHistory,
    ActiveDevice,
    NotificationSettings,
    AppearanceSettings,
    ReportSettings,
    UserSession,
    EmployeeSettings,
    StudentSettings,
)

from .forms import (
    StudentForm,
    StudentDocumentForm,
    StudentStaffForm,
    CompanyProfileForm,
    AccountProfileForm,
    CustomPasswordChangeForm,
    ReportSettingsForm,
    EmployeeSettingsForm,
    StudentSettingsForm,
)



@login_required
@company_type_required("education")
def student_list(request):
    company = get_company(request)

    # Get only students belonging to the logged-in education company
    students = Student.objects.filter(
        company=company
    )

    # Search
    query = request.GET.get("q", "").strip()

    if query:
        students = students.filter(
            Q(admission_number__icontains=query)
            | Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(email__icontains=query)
            | Q(mobile__icontains=query)
            | Q(course__icontains=query)
        )

    # Latest students first
    students = students.order_by("-id")

    # Appearance settings
    appearance, created = AppearanceSettings.objects.get_or_create(
        company=company
    )

    return render(
        request,
        "students/student_list.html",
        {
            "company": company,
            "students": students,
            "appearance": appearance,
            "query": query,
        },
    )




@login_required
@company_type_required("education")
def student_create(request):
    company = get_company(request)

    appearance, created = AppearanceSettings.objects.get_or_create(
        company=company
    )

    if request.method == "POST":
        form = StudentForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            student = form.save(commit=False)

            # Assign student to the logged-in education company
            student.company = company

            student.save()

            messages.success(
                request,
                "Student Added Successfully."
            )

            return redirect("student_list")

    else:
        form = StudentForm()

    return render(
        request,
        "students/student_create.html",
        {
            "company": company,
            "form": form,
            "appearance": appearance,
        },
    )

@login_required
@company_type_required("education")
def student_detail(request, pk):

    company = get_company(request)

    student = get_object_or_404(
        Student,
        id=pk,
        company=company
    )

    documents = StudentDocument.objects.filter(
        student=student
    )

    appearance, created = AppearanceSettings.objects.get_or_create(
        company=company
    )

    return render(
        request,
        "students/student_detail.html",
        {
            "student": student,
            "documents": documents,
            "company": company,
            "appearance": appearance,
        }
    )


@login_required(login_url="login")
@company_type_required("education")
def student_update(request, pk):

    company = get_company(request)

    if company is None:

        messages.error(
            request,
            "Company not found."
        )

        return redirect("login")

    appearance, created = AppearanceSettings.objects.get_or_create(
        company=company
    )

    student = get_object_or_404(
        Student,
        id=pk,
        company=company
    )

    if request.method == "POST":

        form = StudentForm(
            request.POST,
            request.FILES,
            instance=student
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Student Updated Successfully."
            )

            return redirect(
                "student_list"
            )

    else:

        form = StudentForm(
            instance=student
        )

    return render(
        request,
        "students/student_update.html",
        {
            "form": form,
            "student": student,
            "company": company,
            "appearance": appearance,
        }
    )


@login_required
@company_type_required("education")
def student_delete(request, pk):

    company = get_company(request)

    student = get_object_or_404(
        Student,
        id=pk,
        company=company
    )

    appearance, created = AppearanceSettings.objects.get_or_create(
        company=company
    )

    if request.method == "POST":

        student.delete()

        messages.success(
            request,
            "Student Deleted Successfully."
        )

        return redirect(
            "student_list"
        )

    return render(
        request,
        "students/student_delete.html",
        {
            "student": student,
            "company": company,
            "appearance": appearance,
        }
    )

@login_required
@company_type_required("education")
def upload_document(request, pk):

    company = get_company(request)

    student = get_object_or_404(
        Student,
        id=pk,
        company=company
    )

    appearance, created = AppearanceSettings.objects.get_or_create(
        company=company
    )

    if request.method == "POST":

        form = StudentDocumentForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            document = form.save(
                commit=False
            )

            document.student = student
            document.uploaded_by = request.user
            document.save()

            messages.success(
                request,
                "Document Uploaded Successfully."
            )

            return redirect(
                "student_detail",
                pk=student.id
            )

    else:

        form = StudentDocumentForm()

    return render(
        request,
        "students/upload_document.html",
        {
            "form": form,
            "student": student,
            "company": company,
            "appearance": appearance,
        }
    )


@login_required
@company_type_required("education")
def student_documents(request):

    company = get_company(request)

    students = Student.objects.filter(
        company=company
    )

    appearance, created = AppearanceSettings.objects.get_or_create(
        company=company
    )

    return render(
        request,
        "students/upload_document.html",
        {
            "students": students,
            "company": company,
            "appearance": appearance,
        }
    )


@login_required
@company_type_required("education")
def academic_details(request):

    company = get_company(request)

    students = Student.objects.filter(
        company=company
    ).order_by("-id")

    appearance, created = AppearanceSettings.objects.get_or_create(
        company=company
    )

    return render(
        request,
        "students/student_details.html",
        {
            "students": students,
            "company": company,
            "appearance": appearance,
        }
    )


@login_required
@company_type_required("education")
def student_management(request):

    is_super_admin = request.user.is_superuser

    company = Company.objects.filter(
        user=request.user
    ).first()

    appearance = None

    if company:
        appearance, created = AppearanceSettings.objects.get_or_create(
            company=company
        )

    context = {
        "is_super_admin": is_super_admin,
        "is_company_admin": company is not None,
        "company": company,
        "appearance": appearance,
    }

    return render(
        request,
        "students/student_management.html",
        context
    )


@login_required(login_url="login")
@company_type_required("education")
def company_dashboard(request):

    company = Company.objects.filter(
        user=request.user
    ).first()

    if not company:

        messages.error(
            request,
            "No company is linked to your account."
        )

        return redirect("login")

    if company.company_type != "education":

        return HttpResponseForbidden(
            "Access Denied! Your company is not authorized "
            "to access the Student dashboard."
        )

    company_profile = CompanyProfile.objects.filter(
        company=company
    ).first()

    appearance_settings, created = (
        AppearanceSettings.objects.get_or_create(
            company=company
        )
    )

    students = Student.objects.filter(
        company=company
    )

    staffs = Staff.objects.filter(
        company=company
    )

    query = request.GET.get(
        "q",
        ""
    ).strip()

    if query:

        students = students.filter(
            Q(admission_number__icontains=query)
            | Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(email__icontains=query)
            | Q(mobile__icontains=query)
            | Q(course__icontains=query)
        )

        staffs = staffs.filter(
            Q(staff_id__icontains=query)
            | Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(email__icontains=query)
            | Q(designation__icontains=query)
        )

    total_students = Student.objects.filter(
        company=company
    ).count()

    active_students = Student.objects.filter(
        company=company,
        status="Active"
    ).count()

    total_staff = Staff.objects.filter(
        company=company
    ).count()

    context = {
        "company": company,
        "company_profile": company_profile,
        "appearance": appearance_settings,
        "appearance_settings": appearance_settings,
        "query": query,
        "total_students": total_students,
        "active_students": active_students,
        "total_staff": total_staff,
        "recent_students": students.order_by("-id")[:5],
        "search_staffs": staffs.order_by("-id")[:5],
    }

    return render(
        request,
        "students/dashboard.html",
        context
    )


@login_required
@company_type_required("education")
def logout_view(request):

    if request.method == "POST":

        logout(request)

        messages.success(
            request,
            "You have been logged out successfully."
        )

        return redirect("login")

    return render(
        request,
        "students/logout_confirm.html"
    )


@login_required
@company_type_required("education")
def staff_list(request):

    company = get_object_or_404(
        Company,
        user=request.user
    )

    staffs = StudentStaff.objects.filter(
        company=company
    ).order_by("-created_at")

    query = request.GET.get(
        "q",
        ""
    ).strip()

    if query:

        staffs = staffs.filter(
            Q(staff_id__icontains=query)
            | Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(email__icontains=query)
            | Q(phone__icontains=query)
            | Q(department__icontains=query)
            | Q(designation__icontains=query)
            | Q(status__icontains=query)
        )

    appearance, created = AppearanceSettings.objects.get_or_create(
        company=company
    )

    return render(
        request,
        "students/staff_list.html",
        {
            "staffs": staffs,
            "query": query,
            "company": company,
            "appearance": appearance,
        }
    )


@login_required
@company_type_required("education")
def add_staff(request):

    company = get_object_or_404(
        Company,
        user=request.user
    )

    appearance, created = AppearanceSettings.objects.get_or_create(
        company=company
    )

    if request.method == "POST":

        form = StudentStaffForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            staff = form.save(
                commit=False
            )

            staff.company = company

            if StudentStaff.objects.filter(
                company=company,
                staff_id=staff.staff_id
            ).exists():

                form.add_error(
                    "staff_id",
                    "This Staff ID already exists."
                )

            else:

                staff.save()

                messages.success(
                    request,
                    "Staff added successfully."
                )

                return redirect(
                    "staff_list"
                )

    else:

        form = StudentStaffForm()

    return render(
        request,
        "students/add_staff.html",
        {
            "form": form,
            "company": company,
            "appearance": appearance,
        }
    )


@login_required(login_url="login")
@company_type_required("education")
def edit_staff(request, pk):

    company = get_object_or_404(
        Company,
        user=request.user
    )

    staff = get_object_or_404(
        Staff,
        id=pk,
        company=company
    )

    appearance, created = AppearanceSettings.objects.get_or_create(
        company=company
    )

    if request.method == "POST":

        form = StudentStaffForm(
            request.POST,
            request.FILES,
            instance=staff
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Staff updated successfully."
            )

            return redirect(
                "staff_list"
            )

        messages.error(
            request,
            "Please correct the errors below."
        )

    else:

        form = StudentStaffForm(
            instance=staff
        )

    return render(
        request,
        "students/edit_staff.html",
        {
            "staff": staff,
            "form": form,
            "company": company,
            "appearance": appearance,
        }
    )


@login_required
@company_type_required("education")
def delete_staff(request, pk):

    company = get_object_or_404(
        Company,
        user=request.user
    )

    staff = get_object_or_404(
        StudentStaff,
        id=pk,
        company=company
    )

    appearance, created = AppearanceSettings.objects.get_or_create(
        company=company
    )

    if request.method == "POST":

        staff.delete()

        messages.success(
            request,
            "Staff deleted successfully."
        )

        return redirect(
            "staff_list"
        )

    return render(
        request,
        "students/delete_staff.html",
        {
            "staff": staff,
            "company": company,
            "appearance": appearance,
        }
    )



@login_required
@company_type_required("education")
def course_list(request):

    company = get_object_or_404(
        Company,
        user=request.user
    )

    courses = Course.objects.filter(
        company=company
    )

    query = request.GET.get(
        "q",
        ""
    ).strip()

    if query:

        courses = courses.filter(
            Q(course_name__icontains=query)
            | Q(course_code__icontains=query)
            | Q(description__icontains=query)
        )

    appearance, created = AppearanceSettings.objects.get_or_create(
        company=company
    )

    return render(
        request,
        "students/course_list.html",
        {
            "courses": courses,
            "query": query,
            "company": company,
            "appearance": appearance,
        }
    )


@login_required
@company_type_required("education")
def add_course(request):

    company = get_object_or_404(
        Company,
        user=request.user
    )

    appearance, created = AppearanceSettings.objects.get_or_create(
        company=company
    )

    if request.method == "POST":

        course_code = request.POST.get(
            "course_code",
            ""
        ).strip()

        if Course.objects.filter(
            company=company,
            course_code=course_code
        ).exists():

            messages.error(
                request,
                "Course code already exists for your company."
            )

            return render(
                request,
                "students/add_course.html",
                {
                    "company": company,
                    "appearance": appearance,
                }
            )

        Course.objects.create(
            company=company,
            course_code=course_code,
            course_name=request.POST.get(
                "course_name"
            ),
            duration=request.POST.get(
                "duration"
            ),
            fees=request.POST.get(
                "fees"
            ),
        )

        messages.success(
            request,
            "Course Added Successfully."
        )

        return redirect(
            "course_list"
        )

    return render(
        request,
        "students/add_course.html",
        {
            "company": company,
            "appearance": appearance,
        }
    )


@login_required
@company_type_required("education")
def edit_course(request, pk):

    company = get_object_or_404(
        Company,
        user=request.user
    )

    course = get_object_or_404(
        Course,
        id=pk,
        company=company
    )

    appearance, created = AppearanceSettings.objects.get_or_create(
        company=company
    )

    if request.method == "POST":

        course.course_code = request.POST.get(
            "course_code"
        )

        course.course_name = request.POST.get(
            "course_name"
        )

        course.duration = request.POST.get(
            "duration"
        )

        course.fees = request.POST.get(
            "fees"
        )

        course.status = request.POST.get(
            "status"
        )

        course.save()

        messages.success(
            request,
            "Course updated successfully."
        )

        return redirect(
            "course_list"
        )

    return render(
        request,
        "students/edit_course.html",
        {
            "course": course,
            "company": company,
            "appearance": appearance,
        }
    )


@login_required
@company_type_required("education")
def delete_course(request, pk):

    company = get_object_or_404(
        Company,
        user=request.user
    )

    course = get_object_or_404(
        Course,
        id=pk,
        company=company
    )

    appearance, created = AppearanceSettings.objects.get_or_create(
        company=company
    )

    if request.method == "POST":

        course.delete()

        messages.success(
            request,
            "Course deleted successfully."
        )

        return redirect(
            "course_list"
        )

    return render(
        request,
        "students/delete_course.html",
        {
            "course": course,
            "company": company,
            "appearance": appearance,
        }
    )


@login_required
@company_type_required("education")
def student_report(request):

    company = get_object_or_404(
        Company,
        user=request.user
    )

    students = Student.objects.filter(
        company=company
    )

    staff = Staff.objects.filter(
        company=company
    )

    invoices = Invoice.objects.filter(
        company=company
    )

    appearance, created = AppearanceSettings.objects.get_or_create(
        company=company
    )

    total_revenue = invoices.aggregate(
        total=Sum("total_amount")
    )["total"] or 0

    paid_amount = invoices.aggregate(
        total=Sum("amount_paid")
    )["total"] or 0

    pending_amount = invoices.aggregate(
        total=Sum("balance_amount")
    )["total"] or 0

    context = {
        "company": company,
        "appearance": appearance,
        "total_students": students.count(),
        "active_students": students.filter(
            status="Active"
        ).count(),
        "inactive_students": students.filter(
            status="Inactive"
        ).count(),
        "total_staff": staff.count(),
        "total_revenue": total_revenue,
        "paid_amount": paid_amount,
        "pending_amount": pending_amount,
        "recent_students": students.order_by("-id")[:10],
        "recent_invoices": invoices.order_by("-created_at")[:10],
    }

    return render(
        request,
        "students/student_report.html",
        context
    )



def company_settings(request):

    if request.user.is_authenticated:

        company = Company.objects.filter(
            user=request.user
        ).first()

    else:

        company = Company.objects.first()

    appearance = None

    if company:

        appearance, created = (
            AppearanceSettings.objects.get_or_create(
                company=company
            )
        )

    return render(
        request,
        "students/company_settings.html",
        {
            "company": company,
            "appearance": appearance,
        }
    )



@login_required
@company_type_required("education")
def company_profile(request):

    company = get_object_or_404(
        Company,
        user=request.user
    )

    profile, created = CompanyProfile.objects.get_or_create(
        company=company,
        defaults={
            "company_name": company.company_name,
            "owner_name": company.full_name,
            "email": request.user.email,
            "phone": company.phone,
            "company_type": "education",
            "country": "India",
            "address": "",
            "city": "",
            "state": "Kerala",
            "pin_code": "",
            "description": "",
        }
    )

    appearance, created = AppearanceSettings.objects.get_or_create(
        company=company
    )

    if request.method == "POST":

        form = CompanyProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():

            profile = form.save(
                commit=False
            )

            profile.company = company
            profile.save()

            messages.success(
                request,
                "Company profile updated successfully."
            )

            return redirect(
                "company_profile"
            )

    else:

        form = CompanyProfileForm(
            instance=profile
        )

    return render(
        request,
        "students/company_profile.html",
        {
            "form": form,
            "company": company,
            "profile": profile,
            "appearance": appearance,
        }
    )


@login_required
@company_type_required("education")
def account_settings(request):

    profile, created = UserProfile.objects.get_or_create(
        user=request.user,
        defaults={
            "full_name": (
                request.user.get_full_name()
                or request.user.username
            )
        }
    )

    company = Company.objects.filter(
        user=request.user
    ).first()

    appearance = None

    if company:

        appearance, created = (
            AppearanceSettings.objects.get_or_create(
                company=company
            )
        )

    if request.method == "POST":

        form = AccountProfileForm(
            request.POST,
            request.FILES,
            instance=profile,
            user=request.user
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Account settings updated successfully."
            )

            return redirect(
                "account_settings"
            )

    else:

        form = AccountProfileForm(
            instance=profile,
            user=request.user
        )

    login_history = LoginHistory.objects.filter(
        user=request.user
    ).order_by("-login_time")

    active_devices = ActiveDevice.objects.filter(
        user=request.user
    ).order_by("-last_activity")

    return render(
        request,
        "students/account_settings.html",
        {
            "profile": profile,
            "form": form,
            "login_history": login_history,
            "active_devices": active_devices,
            "company": company,
            "appearance": appearance,
        }
    )


@login_required(login_url="login")
@company_type_required("education")
def change_password(request):

    if request.method == "POST":

        form = CustomPasswordChangeForm(
            user=request.user,
            data=request.POST
        )

        if form.is_valid():

            user = form.save()

            update_session_auth_hash(
                request,
                user
            )

            messages.success(
                request,
                "Your password has been changed successfully."
            )

            return redirect(
                "account_settings"
            )

        messages.error(
            request,
            "Please correct the errors below."
        )

    else:

        form = CustomPasswordChangeForm(
            user=request.user
        )

    return render(
        request,
        "students/change_password.html",
        {
            "form": form
        }
    )


@login_required
@company_type_required("education")
def login_history(request):

    history = LoginHistory.objects.filter(
        user=request.user
    ).order_by("-login_time")

    company = Company.objects.filter(
        user=request.user
    ).first()

    appearance = None

    if company:

        appearance, created = (
            AppearanceSettings.objects.get_or_create(
                company=company
            )
        )

    return render(
        request,
        "students/login_history.html",
        {
            "login_history": history,
            "company": company,
            "appearance": appearance,
        }
    )


@login_required(login_url="login")
@company_type_required("education")
def active_devices(request):

    devices = ActiveDevice.objects.filter(
        user=request.user
    ).order_by("-last_activity")

    company = Company.objects.filter(
        user=request.user
    ).first()

    appearance = None

    if company:

        appearance, created = (
            AppearanceSettings.objects.get_or_create(
                company=company
            )
        )

    return render(
        request,
        "students/active_devices.html",
        {
            "active_devices": devices,
            "company": company,
            "appearance": appearance,
        }
    )


@login_required(login_url="login")
@company_type_required("education")
def two_factor_settings(request):

    profile, created = UserProfile.objects.get_or_create(
        user=request.user,
        defaults={
            "full_name": (
                request.user.get_full_name()
                or request.user.username
            )
        }
    )

    if request.method == "POST":

        profile.two_factor_enabled = (
            not profile.two_factor_enabled
        )

        profile.save(
            update_fields=[
                "two_factor_enabled"
            ]
        )

        messages.success(
            request,
            "Two-Factor Authentication settings updated."
        )

        return redirect(
            "two_factor_settings"
        )

    return render(
        request,
        "students/two_factor.html",
        {
            "profile": profile
        }
    )


@login_required
@company_type_required("education")
def logout_all_devices(request):

    if request.method != "POST":

        return redirect(
            "account_settings"
        )

    current_session_key = request.session.session_key

    sessions = Session.objects.filter(
        expire_date__gte=timezone.now()
    )

    for session in sessions:

        try:

            session_data = session.get_decoded()

            if str(
                session_data.get("_auth_user_id")
            ) == str(request.user.id):

                if (
                    session.session_key
                    != current_session_key
                ):

                    session.delete()

        except Exception:

            continue

    UserSession.objects.filter(
        user=request.user
    ).exclude(
        session_key=current_session_key
    ).update(
        is_active=False
    )

    messages.success(
        request,
        "You have been logged out from all other devices."
    )

    return redirect(
        "account_settings"
    )



@login_required
@company_type_required("education")
def dashboard(request):

    company = Company.objects.filter(
        user=request.user
    ).first()

    appearance = None

    if company:

        appearance, created = (
            AppearanceSettings.objects.get_or_create(
                company=company
            )
        )

    return render(
        request,
        "dashboard.html",
        {
            "company": company,
            "appearance": appearance,
        }
    )


@login_required
@company_type_required("education")
def account_profile(request):

    profile = UserProfile.objects.get(
        user=request.user
    )

    return render(
        request,
        "account_profile.html",
        {
            "profile": profile
        }
    )



@login_required
@company_type_required("education")
def student_employee_settings(request):

    company = Company.objects.filter(
        user=request.user
    ).first()

    if not company:

        messages.error(
            request,
            "Company profile not found."
        )

        return redirect(
            "company_settings"
        )

    settings, created = (
        EmployeeSettings.objects.get_or_create(
            company=company
        )
    )

    appearance, created = (
        AppearanceSettings.objects.get_or_create(
            company=company
        )
    )

    if request.method == "POST":

        form = EmployeeSettingsForm(
            request.POST,
            instance=settings
        )

        if form.is_valid():

            employee_settings = form.save(
                commit=False
            )

            employee_settings.company = company
            employee_settings.save()

            messages.success(
                request,
                "Employee settings saved successfully."
            )

            return redirect(
                "student_employee_settings"
            )

        messages.error(
            request,
            "Please correct the errors in the form."
        )

    else:

        form = EmployeeSettingsForm(
            instance=settings
        )

    return render(
        request,
        "students/student_employee_settings.html",
        {
            "form": form,
            "employee_settings": settings,
            "company": company,
            "appearance": appearance,
        }
    )

@login_required
@company_type_required("education")
def student_settings(request):

    company = Company.objects.filter(
        user=request.user
    ).first()

    if not company:

        messages.error(
            request,
            "Company profile not found."
        )

        return redirect(
            "company_settings"
        )

    settings, created = (
        StudentSettings.objects.get_or_create(
            company=company
        )
    )

    appearance, created = (
        AppearanceSettings.objects.get_or_create(
            company=company
        )
    )

    if request.method == "POST":

        form = StudentSettingsForm(
            request.POST,
            instance=settings
        )

        if form.is_valid():

            student_settings = form.save(
                commit=False
            )

            student_settings.company = company
            student_settings.save()

            messages.success(
                request,
                "Student settings saved successfully."
            )

            return redirect(
                "student_settings"
            )

    else:

        form = StudentSettingsForm(
            instance=settings
        )

    return render(
        request,
        "students/student_settings.html",
        {
            "form": form,
            "settings": settings,
            "company": company,
            "appearance": appearance,
        }
    )



@login_required
@company_type_required("education")
def notification_settings(request):

    company = Company.objects.filter(
        user=request.user
    ).first()

    if not company:

        messages.error(
            request,
            "Company profile not found."
        )

        return redirect(
            "company_settings"
        )

    settings, created = (
        NotificationSettings.objects.get_or_create(
            company=company
        )
    )

    appearance, created = (
        AppearanceSettings.objects.get_or_create(
            company=company
        )
    )

    if request.method == "POST":

        settings.email_notifications = (
            "email_notifications"
            in request.POST
        )

        settings.sms_notifications = (
            "sms_notifications"
            in request.POST
        )

        settings.whatsapp_notifications = (
            "whatsapp_notifications"
            in request.POST
        )

        settings.fee_due_reminders = (
            "fee_due_reminders"
            in request.POST
        )

        settings.salary_payment_notifications = (
            "salary_payment_notifications"
            in request.POST
        )

        settings.attendance_alerts = (
            "attendance_alerts"
            in request.POST
        )

        settings.student_admission_alerts = (
            "student_admission_alerts"
            in request.POST
        )

        settings.employee_joining_alerts = (
            "employee_joining_alerts"
            in request.POST
        )

        settings.invoice_payment_reminders = (
            "invoice_payment_reminders"
            in request.POST
        )

        settings.monthly_summary_reports = (
            "monthly_summary_reports"
            in request.POST
        )

        try:

            settings.fee_reminder_days = int(
                request.POST.get(
                    "fee_reminder_days",
                    7
                )
            )

        except (
            ValueError,
            TypeError
        ):

            settings.fee_reminder_days = 7

        try:

            settings.invoice_reminder_days = int(
                request.POST.get(
                    "invoice_reminder_days",
                    7
                )
            )

        except (
            ValueError,
            TypeError
        ):

            settings.invoice_reminder_days = 7

        try:

            settings.summary_day = int(
                request.POST.get(
                    "summary_day",
                    1
                )
            )

        except (
            ValueError,
            TypeError
        ):

            settings.summary_day = 1

        notification_time = request.POST.get(
            "notification_time",
            "09:00"
        )

        if notification_time:

            settings.notification_time = (
                notification_time
            )

        if not (
            settings.email_notifications
            or settings.sms_notifications
            or settings.whatsapp_notifications
        ):

            messages.error(
                request,
                "Please enable at least one notification channel."
            )

            return render(
                request,
                "students/notification_settings.html",
                {
                    "settings": settings,
                    "company": company,
                    "appearance": appearance,
                }
            )

        settings.save()

        messages.success(
            request,
            "Notification preferences saved successfully."
        )

        return redirect(
            "notification_settings"
        )

    return render(
        request,
        "students/notification_settings.html",
        {
            "settings": settings,
            "company": company,
            "appearance": appearance,
        }
    )


# ============================================================
# APPEARANCE SETTINGS
# ============================================================
import re

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Company, AppearanceSettings


@login_required
@company_type_required("education")
def appearance_settings(request):

    # Get the logged-in company's tenant
    company = get_object_or_404(
        Company,
        user=request.user
    )

    # Get or create appearance settings for this company
    settings, created = AppearanceSettings.objects.get_or_create(
        company=company,
        defaults={
            "theme": "light",
            "accent_color": "#2563eb",
            "font_size": "medium",
            "dashboard_layout": "grid",
            "sidebar_style": "expanded",
            "language": "en",
            "date_format": "DD/MM/YYYY",
            "time_format": "12",
            "timezone": "Asia/Kolkata",
        }
    )

    if request.method == "POST":


        theme = request.POST.get("theme", "light").strip()

        accent_color = request.POST.get(
            "accent_color",
            "#2563eb"
        ).strip()

        font_size = request.POST.get(
            "font_size",
            "medium"
        ).strip()

        dashboard_layout = request.POST.get(
            "dashboard_layout",
            "grid"
        ).strip()

        sidebar_style = request.POST.get(
            "sidebar_style",
            "expanded"
        ).strip()

        language = request.POST.get(
            "language",
            "en"
        ).strip()

        date_format = request.POST.get(
            "date_format",
            "DD/MM/YYYY"
        ).strip()

        time_format = request.POST.get(
            "time_format",
            "12"
        ).strip()

        timezone_value = request.POST.get(
            "timezone",
            "Asia/Kolkata"
        ).strip()

        valid_themes = dict(
            AppearanceSettings.THEME_CHOICES
        )

        valid_font_sizes = dict(
            AppearanceSettings.FONT_SIZE_CHOICES
        )

        valid_dashboard_layouts = dict(
            AppearanceSettings.DASHBOARD_LAYOUT_CHOICES
        )

        valid_sidebar_styles = dict(
            AppearanceSettings.SIDEBAR_STYLE_CHOICES
        )

        valid_languages = dict(
            AppearanceSettings.LANGUAGE_CHOICES
        )

        valid_date_formats = dict(
            AppearanceSettings.DATE_FORMAT_CHOICES
        )

        valid_time_formats = dict(
            AppearanceSettings.TIME_FORMAT_CHOICES
        )

        valid_timezones = dict(
            AppearanceSettings.TIMEZONE_CHOICES
        )

        # Theme
        if theme not in valid_themes:
            theme = "light"

        # Accent color
        if not re.fullmatch(
            r"#[0-9A-Fa-f]{6}",
            accent_color
        ):
            accent_color = "#2563eb"

        # Font size
        if font_size not in valid_font_sizes:
            font_size = "medium"

        # Dashboard layout
        if dashboard_layout not in valid_dashboard_layouts:
            dashboard_layout = "grid"

        # Sidebar
        if sidebar_style not in valid_sidebar_styles:
            sidebar_style = "expanded"

        # Language
        if language not in valid_languages:
            language = "en"

        # Date format
        if date_format not in valid_date_formats:
            date_format = "DD/MM/YYYY"

        # Time format
        if time_format not in valid_time_formats:
            time_format = "12"

        # Timezone
        if timezone_value not in valid_timezones:
            timezone_value = "Asia/Kolkata"


        settings.theme = theme
        settings.accent_color = accent_color
        settings.font_size = font_size
        settings.dashboard_layout = dashboard_layout
        settings.sidebar_style = sidebar_style
        settings.language = language
        settings.date_format = date_format
        settings.time_format = time_format
        settings.timezone = timezone_value

        settings.save()

        messages.success(
            request,
            "Appearance settings saved successfully."
        )

        return redirect("appearance_settings")

    # -----------------------------
    # GET
    # -----------------------------

    return render(
        request,
        "students/appearance_settings.html",
        {
            "company": company,
            "settings": settings,
            "appearance": settings,
        }
    )
# ============================================================
# REPORT SETTINGS
# ============================================================

@login_required
@company_type_required("education")
def report_settings(request):

    company = get_object_or_404(
        Company,
        user=request.user
    )

    settings, created = (
        ReportSettings.objects.get_or_create(
            company=company
        )
    )

    appearance, created = (
        AppearanceSettings.objects.get_or_create(
            company=company
        )
    )

    if request.method == "POST":

        form = ReportSettingsForm(
            request.POST,
            instance=settings
        )

        if form.is_valid():

            report_settings = form.save(
                commit=False
            )

            report_settings.company = company
            report_settings.save()

            messages.success(
                request,
                "Report settings saved successfully."
            )

            return redirect(
                "report_settings"
            )

        messages.error(
            request,
            "Please correct the errors below."
        )

    else:

        form = ReportSettingsForm(
            instance=settings
        )

    return render(
        request,
        "students/report_settings.html",
        {
            "company": company,
            "settings": settings,
            "form": form,
            "appearance": appearance,
        }
    )


# ============================================================
# COMMON COMPANY HELPER
# ============================================================

def get_user_company(user):

    return get_object_or_404(
        Company,
        user=user
    )