from django.contrib import admin
from .models import (
    Student,
    StudentDocument,
    Course,
)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "admission_number",
        "first_name",
        "last_name",
        "course",
        "department",
        "mobile",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "course",
        "department",
        "created_at",
    )

    search_fields = (
        "admission_number",
        "first_name",
        "last_name",
        "mobile",
        "email",
    )

    ordering = (
        "-created_at",
    )

    list_per_page = 20


@admin.register(StudentDocument)
class StudentDocumentAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "document_type",
        "uploaded_by",
        "uploaded_at",
    )

    list_filter = (
        "document_type",
        "uploaded_at",
    )

    search_fields = (
        "student__first_name",
        "student__admission_number",
    )

    ordering = (
        "-uploaded_at",
    )

    list_per_page = 20


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "course_code",
        "course_name",
        "duration",
        "fees",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "course_code",
        "course_name",
    )

    ordering = (
        "course_code",
    )

    list_per_page = 20