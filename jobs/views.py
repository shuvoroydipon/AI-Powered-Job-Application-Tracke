import json

from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from django.db.models import Q
from django.core.paginator import Paginator
from django.utils import timezone
from django.conf import settings

from .models import (
    JobApplication,
    Interview,
    AIAnalysis,
)

from .forms import (
    RegisterForm,
    JobApplicationForm,
    InterviewForm,
)


# =========================================================
# DASHBOARD
# =========================================================

@login_required
def dashboard(request):

    applications = JobApplication.objects.filter(
        user=request.user
    )

    total_applications = applications.count()

    wishlist_count = applications.filter(
        status="wishlist"
    ).count()

    applied_count = applications.filter(
        status="applied"
    ).count()

    screening_count = applications.filter(
        status="screening"
    ).count()

    interview_count = applications.filter(
        status="interview"
    ).count()

    selected_count = applications.filter(
        status="selected"
    ).count()

    rejected_count = applications.filter(
        status="rejected"
    ).count()

    # -----------------------------------------------------
    # Selection Percentage
    # -----------------------------------------------------

    selected_percentage = 0

    if total_applications > 0:

        selected_percentage = round(
            (
                selected_count
                / total_applications
            ) * 100,
            1
        )

    # -----------------------------------------------------
    # Recent Applications
    # -----------------------------------------------------

    recent_applications = applications.order_by(
        "-created_at"
    )[:5]

    # -----------------------------------------------------
    # Upcoming Interviews
    # -----------------------------------------------------

    upcoming_interviews = Interview.objects.filter(
        application__user=request.user,
        interview_date__gte=timezone.now()
    ).order_by(
        "interview_date"
    )[:5]

    context = {

        "applications": applications,

        "total_applications": total_applications,

        "wishlist_count": wishlist_count,

        "applied_count": applied_count,

        "screening_count": screening_count,

        "interview_count": interview_count,

        "selected_count": selected_count,

        "rejected_count": rejected_count,

        "selected_percentage": selected_percentage,

        "recent_applications": recent_applications,

        "upcoming_interviews": upcoming_interviews,

    }

    return render(
        request,
        "jobs/dashboard.html",
        context
    )


# =========================================================
# REGISTER
# =========================================================

def register(request):

    if request.user.is_authenticated:

        return redirect(
            "dashboard"
        )

    if request.method == "POST":

        form = RegisterForm(
            request.POST
        )

        if form.is_valid():

            user = form.save()

            login(
                request,
                user
            )

            messages.success(
                request,
                "Registration successful! Welcome!"
            )

            return redirect(
                "dashboard"
            )

    else:

        form = RegisterForm()

    context = {
        "form": form,
    }

    return render(
        request,
        "registration/register.html",
        context
    )


# =========================================================
# APPLICATION LIST
# =========================================================

@login_required
def application_list(request):

    applications = JobApplication.objects.filter(
        user=request.user
    )

    # -----------------------------------------------------
    # Search
    # -----------------------------------------------------

    search_query = request.GET.get(
        "q",
        ""
    ).strip()

    if search_query:

        applications = applications.filter(

            Q(
                job_title__icontains=search_query
            )

            |

            Q(
                company_name__icontains=search_query
            )

            |

            Q(
                location__icontains=search_query
            )

            |

            Q(
                category__icontains=search_query
            )

            |

            Q(
                tags__icontains=search_query
            )

        )

    # -----------------------------------------------------
    # Status Filter
    # -----------------------------------------------------

    status_filter = request.GET.get(
        "status",
        ""
    ).strip()

    if status_filter:

        applications = applications.filter(
            status=status_filter
        )

    # -----------------------------------------------------
    # Location Filter
    # -----------------------------------------------------

    location_filter = request.GET.get(
        "location",
        ""
    ).strip()

    if location_filter:

        applications = applications.filter(
            location__icontains=location_filter
        )

    # -----------------------------------------------------
    # Category Filter
    # -----------------------------------------------------

    category_filter = request.GET.get(
        "category",
        ""
    ).strip()

    if category_filter:

        applications = applications.filter(
            category__icontains=category_filter
        )

    # -----------------------------------------------------
    # Sorting
    # -----------------------------------------------------

    sort_by = request.GET.get(
        "sort",
        "-created_at"
    )

    allowed_sorting = [

        "job_title",
        "-job_title",

        "company_name",
        "-company_name",

        "application_date",
        "-application_date",

        "created_at",
        "-created_at",

    ]

    if sort_by not in allowed_sorting:

        sort_by = "-created_at"

    applications = applications.order_by(
        sort_by
    )

    # -----------------------------------------------------
    # Pagination
    # -----------------------------------------------------

    paginator = Paginator(
        applications,
        10
    )

    page_number = request.GET.get(
        "page"
    )

    page_obj = paginator.get_page(
        page_number
    )

    context = {

        "applications": page_obj,

        "page_obj": page_obj,

        "search_query": search_query,

        "status_filter": status_filter,

        "location_filter": location_filter,

        "category_filter": category_filter,

        "sort_by": sort_by,

    }

    return render(
        request,
        "jobs/application_list.html",
        context
    )


# =========================================================
# CREATE APPLICATION
# =========================================================

@login_required
def application_create(request):

    if request.method == "POST":

        form = JobApplicationForm(
            request.POST
        )

        if form.is_valid():

            application = form.save(
                commit=False
            )

            application.user = request.user

            application.save()

            messages.success(
                request,
                "Job application created successfully!"
            )

            return redirect(
                "application_detail",
                pk=application.pk
            )

    else:

        form = JobApplicationForm()

    context = {

        "form": form,

        "title": "Add Job Application",

        "button_text": "Create Application",

    }

    return render(
        request,
        "jobs/application_form.html",
        context
    )


# =========================================================
# APPLICATION DETAIL
# =========================================================

@login_required
def application_detail(
    request,
    pk
):

    application = get_object_or_404(
        JobApplication,
        pk=pk,
        user=request.user
    )

    interviews = application.interviews.all()

    ai_analysis = AIAnalysis.objects.filter(
        application=application
    ).first()

    context = {

        "application": application,

        "interviews": interviews,

        "ai_analysis": ai_analysis,

    }

    return render(
        request,
        "jobs/application_detail.html",
        context
    )


# =========================================================
# UPDATE APPLICATION
# =========================================================

@login_required
def application_update(
    request,
    pk
):

    application = get_object_or_404(
        JobApplication,
        pk=pk,
        user=request.user
    )

    if request.method == "POST":

        form = JobApplicationForm(
            request.POST,
            instance=application
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Job application updated successfully!"
            )

            return redirect(
                "application_detail",
                pk=application.pk
            )

    else:

        form = JobApplicationForm(
            instance=application
        )

    context = {

        "form": form,

        "application": application,

        "title": "Edit Job Application",

        "button_text": "Update Application",

    }

    return render(
        request,
        "jobs/application_form.html",
        context
    )


# =========================================================
# DELETE APPLICATION
# =========================================================

@login_required
def application_delete(
    request,
    pk
):

    application = get_object_or_404(
        JobApplication,
        pk=pk,
        user=request.user
    )

    if request.method == "POST":

        application.delete()

        messages.success(
            request,
            "Job application deleted successfully!"
        )

        return redirect(
            "application_list"
        )

    context = {
        "application": application,
    }

    return render(
        request,
        "jobs/application_confirm_delete.html",
        context
    )


# =========================================================
# CREATE INTERVIEW
# =========================================================

@login_required
def interview_create(
    request,
    application_id
):

    application = get_object_or_404(
        JobApplication,
        pk=application_id,
        user=request.user
    )

    if request.method == "POST":

        form = InterviewForm(
            request.POST
        )

        if form.is_valid():

            interview = form.save(
                commit=False
            )

            interview.application = application

            interview.save()

            messages.success(
                request,
                "Interview added successfully!"
            )

            return redirect(
                "application_detail",
                pk=application.pk
            )

    else:

        form = InterviewForm()

    context = {

        "form": form,

        "application": application,

        "title": "Add Interview",

    }

    return render(
        request,
        "jobs/interview_form.html",
        context
    )


# =========================================================
# UPDATE INTERVIEW
# =========================================================

@login_required
def interview_update(
    request,
    pk
):

    interview = get_object_or_404(
        Interview,
        pk=pk,
        application__user=request.user
    )

    if request.method == "POST":

        form = InterviewForm(
            request.POST,
            instance=interview
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Interview updated successfully!"
            )

            return redirect(
                "application_detail",
                pk=interview.application.pk
            )

    else:

        form = InterviewForm(
            instance=interview
        )

    context = {

        "form": form,

        "interview": interview,

        "application": interview.application,

        "title": "Edit Interview",

    }

    return render(
        request,
        "jobs/interview_form.html",
        context
    )


# =========================================================
# DELETE INTERVIEW
# =========================================================

@login_required
def interview_delete(
    request,
    pk
):

    interview = get_object_or_404(
        Interview,
        pk=pk,
        application__user=request.user
    )

    application_id = interview.application.pk

    if request.method == "POST":

        interview.delete()

        messages.success(
            request,
            "Interview deleted successfully!"
        )

        return redirect(
            "application_detail",
            pk=application_id
        )

    context = {
        "interview": interview,
    }

    return render(
        request,
        "jobs/interview_confirm_delete.html",
        context
    )


# =========================================================
# AI JOB DESCRIPTION ANALYSIS
# =========================================================

@login_required
def ai_analyze(
    request,
    pk
):

    application = get_object_or_404(
        JobApplication,
        pk=pk,
        user=request.user
    )

    # -----------------------------------------------------
    # Check Job Description
    # -----------------------------------------------------

    if not application.job_description:

        messages.error(
            request,
            "Please add a job description before using AI analysis."
        )

        return redirect(
            "application_detail",
            pk=application.pk
        )

    # -----------------------------------------------------
    # Check API Key
    # -----------------------------------------------------

    api_key = getattr(
        settings,
        "OPENAI_API_KEY",
        ""
    )

    if not api_key:

        messages.error(
            request,
            "OpenAI API key is not configured."
        )

        return redirect(
            "application_detail",
            pk=application.pk
        )

    try:

        from openai import OpenAI

        client = OpenAI(
            api_key=api_key
        )

        # -------------------------------------------------
        # AI Prompt
        # -------------------------------------------------

        prompt = f"""
You are an expert recruitment assistant.

Analyze this job posting and return ONLY valid JSON.

Job Title:
{application.job_title}

Company:
{application.company_name}

Job Description:
{application.job_description}

Return exactly this JSON structure:

{{
    "job_summary": "Short summary of the job",
    "required_skills": "List the important required skills",
    "required_experience": "Required experience",
    "important_technologies": "Important technologies",
    "interview_suggestions": "Interview preparation suggestions",
    "match_score": 0
}}

The match_score must be an integer from 0 to 100.

Do not use markdown.
Do not add ```json.
Return only JSON.
"""

        # -------------------------------------------------
        # OpenAI Request
        # -------------------------------------------------

        response = client.responses.create(

            model="gpt-5.6",

            input=prompt

        )

        ai_text = response.output_text.strip()

        # -------------------------------------------------
        # Parse JSON
        # -------------------------------------------------

        try:

            result = json.loads(
                ai_text
            )

        except json.JSONDecodeError:

            # Try removing markdown fences
            cleaned_text = ai_text.replace(
                "```json",
                ""
            ).replace(
                "```",
                ""
            ).strip()

            result = json.loads(
                cleaned_text
            )

        # -------------------------------------------------
        # Get AI Values
        # -------------------------------------------------

        job_summary = result.get(
            "job_summary",
            ""
        )

        required_skills = result.get(
            "required_skills",
            ""
        )

        required_experience = result.get(
            "required_experience",
            ""
        )

        important_technologies = result.get(
            "important_technologies",
            ""
        )

        interview_suggestions = result.get(
            "interview_suggestions",
            ""
        )

        match_score = result.get(
            "match_score",
            0
        )

        # -------------------------------------------------
        # Validate Match Score
        # -------------------------------------------------

        try:

            match_score = int(
                match_score
            )

        except (TypeError, ValueError):

            match_score = 0

        match_score = max(
            0,
            min(
                100,
                match_score
            )
        )

        # -------------------------------------------------
        # Save AI Analysis
        # -------------------------------------------------

        AIAnalysis.objects.update_or_create(

            application=application,

            defaults={

                "job_summary": job_summary,

                "required_skills": required_skills,

                "required_experience": required_experience,

                "important_technologies":
                    important_technologies,

                "interview_suggestions":
                    interview_suggestions,

                "match_score": match_score,

            }

        )

        messages.success(
            request,
            "AI job analysis completed successfully!"
        )

    except Exception as e:

        print(
            "AI ANALYSIS ERROR:",
            e
        )

        error_text = str(e).lower()

        if (
            "quota" in error_text
            or "insufficient_quota" in error_text
            or "429" in error_text
        ):

            messages.error(
                request,
                "AI analysis is unavailable because the API quota "
                "or billing limit has been reached."
            )

        else:

            messages.error(
                request,
                "AI analysis failed. Please check your API "
                "configuration and try again."
            )

    return redirect(
        "application_detail",
        pk=application.pk
    )