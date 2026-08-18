from django.db import models
from django.contrib.auth.models import User


# =========================================================
# JOB APPLICATION MODEL
# =========================================================

class JobApplication(models.Model):

    STATUS_CHOICES = [
        ('wishlist', 'Wishlist'),
        ('applied', 'Applied'),
        ('screening', 'Screening'),
        ('interview', 'Interview'),
        ('selected', 'Selected'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='job_applications'
    )

    job_title = models.CharField(
        max_length=200
    )

    company_name = models.CharField(
        max_length=200
    )

    job_description = models.TextField(
        blank=True,
        null=True
    )

    location = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    salary = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True
    )

    job_url = models.URLField(
        blank=True,
        null=True
    )

    application_date = models.DateField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='wishlist'
    )

    category = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    tags = models.CharField(
        max_length=500,
        blank=True,
        null=True
    )

    notes = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        ordering = ['-created_at']

        verbose_name = 'Job Application'

        verbose_name_plural = 'Job Applications'

    def __str__(self):

        return f"{self.job_title} - {self.company_name}"


# =========================================================
# INTERVIEW MODEL
# =========================================================

class Interview(models.Model):

    INTERVIEW_TYPE_CHOICES = [
        ('online', 'Online'),
        ('phone', 'Phone'),
        ('onsite', 'On-site'),
        ('technical', 'Technical'),
        ('hr', 'HR'),
        ('other', 'Other'),
    ]

    application = models.ForeignKey(
        JobApplication,
        on_delete=models.CASCADE,
        related_name='interviews'
    )

    interview_date = models.DateTimeField()

    interview_type = models.CharField(
        max_length=20,
        choices=INTERVIEW_TYPE_CHOICES,
        default='online'
    )

    meeting_link = models.URLField(
        blank=True,
        null=True
    )

    interview_notes = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        ordering = ['interview_date']

        verbose_name = 'Interview'

        verbose_name_plural = 'Interviews'

    def __str__(self):

        return (
            f"{self.application.job_title} - "
            f"{self.interview_date}"
        )


# =========================================================
# AI ANALYSIS MODEL
# =========================================================

class AIAnalysis(models.Model):

    application = models.OneToOneField(
        JobApplication,
        on_delete=models.CASCADE,
        related_name='ai_analysis'
    )

    job_summary = models.TextField(
        blank=True,
        null=True
    )

    required_skills = models.TextField(
        blank=True,
        null=True
    )

    required_experience = models.TextField(
        blank=True,
        null=True
    )

    important_technologies = models.TextField(
        blank=True,
        null=True
    )

    interview_suggestions = models.TextField(
        blank=True,
        null=True
    )

    match_score = models.PositiveIntegerField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        ordering = ['-created_at']

        verbose_name = 'AI Analysis'

        verbose_name_plural = 'AI Analyses'

    def __str__(self):

        return (
            f"AI Analysis - "
            f"{self.application.job_title}"
        )