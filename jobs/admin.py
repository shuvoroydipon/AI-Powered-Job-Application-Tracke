from django.contrib import admin

from .models import (
    JobApplication,
    Interview,
    AIAnalysis,
)


# =========================================================
# JOB APPLICATION ADMIN
# =========================================================

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):

    list_display = (
        'job_title',
        'company_name',
        'user',
        'location',
        'status',
        'application_date',
        'created_at',
    )

    list_filter = (
        'status',
        'category',
        'application_date',
        'created_at',
    )

    search_fields = (
        'job_title',
        'company_name',
        'location',
        'category',
        'tags',
        'user__username',
        'user__email',
    )

    ordering = (
        '-created_at',
    )

    list_per_page = 20

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    fieldsets = (

        (
            'User Information',
            {
                'fields': (
                    'user',
                )
            }
        ),

        (
            'Job Information',
            {
                'fields': (
                    'job_title',
                    'company_name',
                    'job_description',
                    'location',
                    'salary',
                    'job_url',
                )
            }
        ),

        (
            'Application Information',
            {
                'fields': (
                    'application_date',
                    'status',
                    'category',
                    'tags',
                    'notes',
                )
            }
        ),

        (
            'Timestamps',
            {
                'fields': (
                    'created_at',
                    'updated_at',
                )
            }
        ),
    )


# =========================================================
# INTERVIEW ADMIN
# =========================================================

@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):

    list_display = (
        'application',
        'get_company',
        'interview_date',
        'interview_type',
        'created_at',
    )

    list_filter = (
        'interview_type',
        'interview_date',
        'created_at',
    )

    search_fields = (
        'application__job_title',
        'application__company_name',
        'application__user__username',
        'interview_notes',
    )

    ordering = (
        'interview_date',
    )

    list_per_page = 20

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    fieldsets = (

        (
            'Application',
            {
                'fields': (
                    'application',
                )
            }
        ),

        (
            'Interview Information',
            {
                'fields': (
                    'interview_date',
                    'interview_type',
                    'meeting_link',
                    'interview_notes',
                )
            }
        ),

        (
            'Timestamps',
            {
                'fields': (
                    'created_at',
                    'updated_at',
                )
            }
        ),
    )

    @admin.display(
        description='Company'
    )
    def get_company(self, obj):

        return obj.application.company_name


# =========================================================
# AI ANALYSIS ADMIN
# =========================================================

@admin.register(AIAnalysis)
class AIAnalysisAdmin(admin.ModelAdmin):

    list_display = (
        'get_job_title',
        'get_company',
        'match_score',
        'created_at',
        'updated_at',
    )

    list_filter = (
        'match_score',
        'created_at',
        'updated_at',
    )

    search_fields = (
        'application__job_title',
        'application__company_name',
        'application__user__username',
        'job_summary',
        'required_skills',
        'important_technologies',
    )

    ordering = (
        '-created_at',
    )

    list_per_page = 20

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    fieldsets = (

        (
            'Application',
            {
                'fields': (
                    'application',
                )
            }
        ),

        (
            'AI Match',
            {
                'fields': (
                    'match_score',
                )
            }
        ),

        (
            'AI Job Analysis',
            {
                'fields': (
                    'job_summary',
                    'required_skills',
                    'required_experience',
                    'important_technologies',
                    'interview_suggestions',
                )
            }
        ),

        (
            'Timestamps',
            {
                'fields': (
                    'created_at',
                    'updated_at',
                )
            }
        ),
    )

    @admin.display(
        description='Job Title'
    )
    def get_job_title(self, obj):

        return obj.application.job_title

    @admin.display(
        description='Company'
    )
    def get_company(self, obj):

        return obj.application.company_name