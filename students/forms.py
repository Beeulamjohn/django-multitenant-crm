from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from .models import (
    EmployeeSettings,
    StudentSettings,
    NotificationSettings,
    ReportSettings,
    AppearanceSettings,
    UserProfile,
    Student,
    StudentDocument,
    StudentStaff,
    CompanyProfile,
)

class StudentForm(forms.ModelForm):
    admission_date = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "form-control",
            }
        ),
    )

    dob = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "form-control",
            }
        ),
    )

    class Meta:
        model = Student
        exclude = ("company", "created_at")

        widgets = {
            "student_id": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Student ID",
            }),
            "admission_number": forms.TextInput(attrs={
                "class": "form-control",
            }),
            "first_name": forms.TextInput(attrs={
                "class": "form-control",
            }),
            "last_name": forms.TextInput(attrs={
                "class": "form-control",
            }),
            "gender": forms.Select(attrs={
                "class": "form-control",
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
            }),
            "mobile": forms.TextInput(attrs={
                "class": "form-control",
            }),
            "father_name": forms.TextInput(attrs={
                "class": "form-control",
            }),
            "mother_name": forms.TextInput(attrs={
                "class": "form-control",
            }),
            "parent_mobile": forms.TextInput(attrs={
                "class": "form-control",
            }),
            "address": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
            }),
            "city": forms.TextInput(attrs={
                "class": "form-control",
            }),
            "state": forms.TextInput(attrs={
                "class": "form-control",
            }),
            "country": forms.TextInput(attrs={
                "class": "form-control",
            }),
            "pincode": forms.TextInput(attrs={
                "class": "form-control",
            }),
            "course": forms.TextInput(attrs={
                "class": "form-control",
            }),
            "department": forms.TextInput(attrs={
                "class": "form-control",
            }),
            "batch": forms.TextInput(attrs={
                "class": "form-control",
            }),
            "semester": forms.TextInput(attrs={
                "class": "form-control",
            }),
            "roll_number": forms.TextInput(attrs={
                "class": "form-control",
            }),
            "status": forms.Select(attrs={
                "class": "form-control",
            }),
            "photo": forms.FileInput(attrs={
                "class": "form-control",
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs["autocomplete"] = "off"

            if field.required:
                field.widget.attrs["required"] = True


class StudentDocumentForm(forms.ModelForm):

    class Meta:
        model = StudentDocument
        exclude = ("student", "uploaded_by", "uploaded_at")

        widgets = {
            "document_type": forms.Select(attrs={
                "class": "form-control",
            }),
            "file": forms.FileInput(attrs={
                "class": "form-control",
            }),
        }


class StudentStaffForm(forms.ModelForm):
    joining_date = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "form-control",
            }
        ),
    )

    class Meta:
        model = StudentStaff
        exclude = ("company", "created_at")

        widgets = {
            "staff_id": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Staff ID",
            }),
            "first_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter First Name",
            }),
            "last_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Last Name",
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Email Address",
            }),
            "phone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Phone Number",
            }),
            "department": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Department",
            }),
            "designation": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Designation",
            }),
            "address": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Enter Address",
            }),
            "qualification": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Qualification",
            }),
            "salary": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Salary",
            }),
            "status": forms.Select(attrs={
                "class": "form-control",
            }),
            "profile": forms.FileInput(attrs={
                "class": "form-control",
            }),
            "certification": forms.FileInput(attrs={
                "class": "form-control",
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs["autocomplete"] = "off"

            if field.required:
                field.widget.attrs["required"] = True



class CompanyProfileForm(forms.ModelForm):

    class Meta:
        model = CompanyProfile

        fields = [
            "company_name",
            "company_logo",
            "company_type",
            "owner_name",
            "email",
            "phone",
            "website",
            "address",
            "city",
            "state",
            "country",
            "pin_code",
            "description",
        ]

        widgets = {

            "company_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter company name",
                }
            ),

            "company_logo": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/png,image/jpeg,image/jpg,image/svg+xml",
                }
            ),

            "company_type": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "owner_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter owner or manager name",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter company email",
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter phone number",
                }
            ),

            "website": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://example.com",
                }
            ),

            "address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter complete company address",
                    "rows": 4,
                }
            ),

            "city": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter city",
                }
            ),

            "state": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter state",
                }
            ),

            "country": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter country",
                }
            ),

            "pin_code": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter PIN code",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter company description",
                    "rows": 5,
                }
            ),
        }

    def clean_company_name(self):
        company_name = self.cleaned_data.get("company_name")

        if not company_name:
            raise forms.ValidationError(
                "Company name is required."
            )

        return company_name.strip()

    def clean_owner_name(self):
        owner_name = self.cleaned_data.get("owner_name")

        if not owner_name:
            raise forms.ValidationError(
                "Owner / Manager name is required."
            )

        return owner_name.strip()

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")

        if not phone:
            raise forms.ValidationError(
                "Phone number is required."
            )

        phone = phone.strip()

        if not phone.replace("+", "").replace(" ", "").isdigit():
            raise forms.ValidationError(
                "Enter a valid phone number."
            )

        return phone

    def clean_pin_code(self):
        pin_code = self.cleaned_data.get("pin_code")

        if not pin_code:
            raise forms.ValidationError(
                "PIN code is required."
            )

        return pin_code.strip()

    def clean_company_logo(self):
        logo = self.cleaned_data.get("company_logo")

        if logo:
            allowed_types = [
                "image/jpeg",
                "image/png",
                "image/jpg",
                "image/svg+xml",
            ]

            if logo.content_type not in allowed_types:
                raise forms.ValidationError(
                    "Only PNG, JPG, JPEG, or SVG images are allowed."
                )

            # 2 MB maximum
            if logo.size > 2 * 1024 * 1024:
                raise forms.ValidationError(
                    "Company logo must be smaller than 2 MB."
                )

        return logo

class AccountProfileForm(forms.ModelForm):

    username = forms.CharField(
        required=True,
        max_length=150
    )

    email = forms.EmailField(
        required=True
    )

    class Meta:
        model = UserProfile
        fields = [
            "full_name",
            "mobile_number",
            "profile_picture",
            "two_factor_enabled",
        ]

    def __init__(self, *args, user=None, **kwargs):

        super().__init__(*args, **kwargs)

        self.user = user

        if user:

            self.fields["username"].initial = user.username
            self.fields["email"].initial = user.email

    def save(self, commit=True):

        profile = super().save(commit=commit)

        if self.user:

            self.user.username = self.cleaned_data["username"]
            self.user.email = self.cleaned_data["email"]

            if commit:
                self.user.save()

        return profile


class CustomPasswordChangeForm(PasswordChangeForm):

    old_password = forms.CharField(
        label="Current Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter current password"
            }
        )
    )

    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter new password"
            }
        )
    )

    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Confirm new password"
            }
        )
    )


class EmployeeSettingsForm(forms.ModelForm):

    class Meta:
        model = EmployeeSettings

        fields = [
            "working_hours",
            "office_start",
            "office_end",
            "attendance_method",

            "salary_cycle",
            "overtime_calculation",
            "overtime_rate",

            "annual_leave",
            "sick_leave",
            "leave_carry_forward",

            "employee_prefix",
            "auto_employee_id",
            "starting_number",

            "probation_period",
            "probation_tracking",
        ]

        widgets = {
            "working_hours": forms.NumberInput(
                attrs={
                    "min": 1,
                    "max": 24,
                    "step": "0.5",
                }
            ),

            "office_start": forms.TimeInput(
                attrs={
                    "type": "time",
                }
            ),

            "office_end": forms.TimeInput(
                attrs={
                    "type": "time",
                }
            ),

            "overtime_rate": forms.NumberInput(
                attrs={
                    "min": 0,
                    "step": "0.01",
                }
            ),

            "annual_leave": forms.NumberInput(
                attrs={
                    "min": 0,
                    "max": 365,
                }
            ),

            "sick_leave": forms.NumberInput(
                attrs={
                    "min": 0,
                    "max": 365,
                }
            ),

            "employee_prefix": forms.TextInput(
                attrs={
                    "maxlength": 10,
                    "placeholder": "EMP",
                }
            ),

            "starting_number": forms.NumberInput(
                attrs={
                    "min": 1,
                }
            ),

            "probation_period": forms.NumberInput(
                attrs={
                    "min": 0,
                    "max": 60,
                }
            ),
        }

    def clean_employee_prefix(self):

        prefix = self.cleaned_data["employee_prefix"]

        prefix = prefix.strip().upper()

        if not prefix:
            raise forms.ValidationError(
                "Employee ID prefix is required."
            )

        return prefix

    def clean(self):

        cleaned_data = super().clean()

        office_start = cleaned_data.get("office_start")
        office_end = cleaned_data.get("office_end")

        if office_start and office_end:

            if office_end <= office_start:

                raise forms.ValidationError(
                    "Office end time must be later than "
                    "office start time."
                )

        return cleaned_data





class StudentSettingsForm(forms.ModelForm):

    class Meta:

        model = StudentSettings

        fields = [
            "admission_prefix",
            "student_id_format",
            "auto_generate_student_id",
            "default_student_status",

            "course_duration",
            "course_duration_unit",
            "default_course",

            "attendance_tracking",
            "attendance_alerts",

            "fee_reminders",
            "fee_reminder_schedule",

            "certificate_number_format",
            "certificate_prefix",

            "parent_notifications",
            "notify_fee",
            "notify_attendance",
            "notify_certificate",
            "notify_general",
        ]

        widgets = {

            "admission_prefix": forms.TextInput(
                attrs={
                    "placeholder": "Example: ADM",
                    "maxlength": "20",
                }
            ),

            "student_id_format": forms.Select(),

            "auto_generate_student_id": forms.CheckboxInput(),

            "default_student_status": forms.Select(),

            "course_duration": forms.NumberInput(
                attrs={
                    "min": 1,
                }
            ),

            "course_duration_unit": forms.Select(),

            "default_course": forms.TextInput(
                attrs={
                    "placeholder": "Example: Computer Science",
                    "maxlength": "150",
                }
            ),

            "attendance_tracking": forms.CheckboxInput(),

            "attendance_alerts": forms.CheckboxInput(),

            "fee_reminders": forms.CheckboxInput(),

            "fee_reminder_schedule": forms.Select(),

            "certificate_number_format": forms.Select(),

            "certificate_prefix": forms.TextInput(
                attrs={
                    "placeholder": "Example: CERT",
                    "maxlength": "20",
                }
            ),

            "parent_notifications": forms.CheckboxInput(),

            "notify_fee": forms.CheckboxInput(),

            "notify_attendance": forms.CheckboxInput(),

            "notify_certificate": forms.CheckboxInput(),

            "notify_general": forms.CheckboxInput(),
        }



class NotificationSettingsForm(forms.ModelForm):

    class Meta:
        model = NotificationSettings

        fields = [
            "email_notifications",
            "sms_notifications",
            "whatsapp_notifications",

            "fee_due_reminders",
            "salary_payment_notifications",
            "attendance_alerts",
            "student_admission_alerts",
            "employee_joining_alerts",
            "invoice_payment_reminders",
            "monthly_summary_reports",

            "fee_reminder_days",
            "invoice_reminder_days",
            "summary_day",
            "notification_time",
        ]

        widgets = {
            "fee_reminder_days": forms.NumberInput(
                attrs={
                    "min": 1,
                    "max": 30,
                }
            ),

            "invoice_reminder_days": forms.NumberInput(
                attrs={
                    "min": 1,
                    "max": 30,
                }
            ),

            "summary_day": forms.NumberInput(
                attrs={
                    "min": 1,
                    "max": 28,
                }
            ),

            "notification_time": forms.TimeInput(
                format="%H:%M",
                attrs={
                    "type": "time",
                }
            ),
        }




class AppearanceSettingsForm(forms.ModelForm):

    class Meta:
        model = AppearanceSettings

        fields = [
            "theme",
            "accent_color",
            "font_size",
            "dashboard_layout",
            "sidebar_style",
            "language",
            "date_format",
            "time_format",
            "timezone",
        ]

        widgets = {

            "theme": forms.RadioSelect(),

            "accent_color": forms.TextInput(
                attrs={
                    "type": "color",
                    "class": "color-picker",
                }
            ),

            "font_size": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "dashboard_layout": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "sidebar_style": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "language": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "date_format": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "time_format": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "timezone": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
        }

class ReportSettingsForm(forms.ModelForm):

    class Meta:
        model = ReportSettings

        fields = [
            "default_report_format",
            "default_date_range",

            "include_company_logo",
            "show_gst_details",
            "include_signature",
            "report_header_footer",

            "report_watermark",
            "enable_watermark",
            "watermark_position",

            "automatic_monthly_reports",
            "email_reports_to_admin",
            "monthly_report_day",
            "monthly_report_time",
        ]

        widgets = {

            "default_report_format": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "default_date_range": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "include_company_logo": forms.CheckboxInput(
                attrs={
                    "class": "toggle-input",
                }
            ),

            "show_gst_details": forms.CheckboxInput(
                attrs={
                    "class": "toggle-input",
                }
            ),

            "include_signature": forms.CheckboxInput(
                attrs={
                    "class": "toggle-input",
                }
            ),

            "report_header_footer": forms.CheckboxInput(
                attrs={
                    "class": "toggle-input",
                }
            ),

            "report_watermark": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter watermark text",
                    "maxlength": "200",
                }
            ),

            "enable_watermark": forms.CheckboxInput(
                attrs={
                    "class": "toggle-input",
                }
            ),

            "watermark_position": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "automatic_monthly_reports": forms.CheckboxInput(
                attrs={
                    "class": "toggle-input",
                }
            ),

            "email_reports_to_admin": forms.CheckboxInput(
                attrs={
                    "class": "toggle-input",
                }
            ),

            "monthly_report_day": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "monthly_report_time": forms.TimeInput(
                attrs={
                    "class": "form-control",
                    "type": "time",
                },
                format="%H:%M",
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["monthly_report_day"].choices = [
            (1, "1st Day"),
            (5, "5th Day"),
            (10, "10th Day"),
            (15, "15th Day"),
            (20, "20th Day"),
            (25, "25th Day"),
        ]

    def clean_monthly_report_day(self):

        day = self.cleaned_data.get(
            "monthly_report_day"
        )

        if day not in [1, 5, 10, 15, 20, 25]:
            raise forms.ValidationError(
                "Please select a valid report day."
            )

        return day


class UserCreateForm(forms.Form):

    first_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter first name"
            }
        )
    )

    last_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter last name"
            }
        )
    )

    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter username"
            }
        )
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter email address"
            }
        )
    )

    role = forms.ChoiceField(
        choices=UserProfile.ROLE_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "form-control"
            }
        )
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter password"
            }
        )
    )

    confirm_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Confirm password"
            }
        )
    )

    def clean_username(self):

        username = self.cleaned_data["username"]

        if User.objects.filter(
            username__iexact=username
        ).exists():

            raise forms.ValidationError(
                "This username is already in use."
            )

        return username

    def clean_password(self):

        password = self.cleaned_data["password"]

        validate_password(password)

        return password

    def clean(self):

        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get(
            "confirm_password"
        )

        if password and confirm_password:

            if password != confirm_password:

                raise forms.ValidationError(
                    "Passwords do not match."
                )

        return cleaned_data

class UserUpdateForm(forms.Form):

    first_name = forms.CharField(
        max_length=150,
        required=True
    )

    last_name = forms.CharField(
        max_length=150,
        required=False
    )

    email = forms.EmailField(
        required=True
    )

    role = forms.ChoiceField(
        choices=UserProfile.ROLE_CHOICES
    )

    is_active = forms.BooleanField(
        required=False
    )

class UserPasswordResetForm(forms.Form):

    password = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput,
        label="New Password"
    )

    confirm_password = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput,
        label="Confirm Password"
    )

    def clean(self):

        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get(
            "confirm_password"
        )

        if password != confirm_password:

            raise forms.ValidationError(
                "Passwords do not match."
            )

        validate_password(password)

        return cleaned_data

class AccountProfileForm(forms.ModelForm):

    username = forms.CharField(
        required=True,
        max_length=150
    )

    email = forms.EmailField(
        required=True
    )

    class Meta:
        model = UserProfile
        fields = [
            "full_name",
            "mobile_number",
            "profile_picture",
            "two_factor_enabled",
        ]

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.user = user

        if user:
            self.fields["username"].initial = user.username
            self.fields["email"].initial = user.email

    def save(self, commit=True):
        profile = super().save(commit=False)

        if self.user:
            self.user.username = self.cleaned_data["username"]
            self.user.email = self.cleaned_data["email"]

            if commit:
                self.user.save()

        if commit:
            profile.save()

        return profile