from django.urls import path
from . import views


urlpatterns = [

    # =====================================================
    # HOME / DASHBOARD
    # =====================================================

    path(
        "",
        views.dashboard,
        name="home"
    ),

    path(
        "dashboard/",
        views.dashboard,
        name="dashboard"
    ),


    # =====================================================
    # AUTHENTICATION
    # =====================================================

    path(
        "register/",
        views.register,
        name="register"
    ),


    # =====================================================
    # JOB APPLICATIONS
    # =====================================================

    # /applications/
    path(
        "applications/",
        views.application_list,
        name="application_list"
    ),

    # /jobs/  → Same Application List
    path(
        "jobs/",
        views.application_list,
        name="jobs"
    ),

    # /applications/create/
    path(
        "applications/create/",
        views.application_create,
        name="application_create"
    ),

    # /applications/<id>/
    path(
        "applications/<int:pk>/",
        views.application_detail,
        name="application_detail"
    ),

    # /applications/<id>/edit/
    path(
        "applications/<int:pk>/edit/",
        views.application_update,
        name="application_update"
    ),

    # /applications/<id>/delete/
    path(
        "applications/<int:pk>/delete/",
        views.application_delete,
        name="application_delete"
    ),


    # =====================================================
    # INTERVIEW MANAGEMENT
    # =====================================================

    # Add Interview
    path(
        "applications/<int:application_id>/interview/add/",
        views.interview_create,
        name="interview_create"
    ),

    # Edit Interview
    path(
        "interviews/<int:pk>/edit/",
        views.interview_update,
        name="interview_update"
    ),

    # Delete Interview
    path(
        "interviews/<int:pk>/delete/",
        views.interview_delete,
        name="interview_delete"
    ),


    # =====================================================
    # AI JOB DESCRIPTION ANALYSIS
    # =====================================================

    path(
        "applications/<int:pk>/ai-analyze/",
        views.ai_analyze,
        name="ai_analyze"
    ),

]