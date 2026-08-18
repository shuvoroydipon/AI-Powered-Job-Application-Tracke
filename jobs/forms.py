from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import JobApplication, Interview


# =========================================================
# User Registration Form
# =========================================================

class RegisterForm(UserCreationForm):

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email'
            }
        )
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]

        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter username'
                }
            ),
        }

    def save(self, commit=True):

        user = super().save(commit=False)

        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


# =========================================================
# Job Application Form
# =========================================================

class JobApplicationForm(forms.ModelForm):

    class Meta:

        model = JobApplication

        fields = [
            'job_title',
            'company_name',
            'job_description',
            'location',
            'salary',
            'job_url',
            'application_date',
            'status',
            'category',
            'tags',
            'notes',
        ]

        widgets = {

            # Job Title
            'job_title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'e.g. Django Developer'
                }
            ),

            # Company Name
            'company_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'e.g. ABC Technologies'
                }
            ),

            # Job Description
            'job_description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 7,
                    'placeholder': (
                        'Paste the complete job description here...'
                    )
                }
            ),

            # Location
            'location': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'e.g. Dhaka, Bangladesh'
                }
            ),

            # Salary
            'salary': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'e.g. 50000',
                    'step': '0.01'
                }
            ),

            # Job URL
            'job_url': forms.URLInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'https://example.com/job'
                }
            ),

            # Application Date
            'application_date': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            ),

            # Status
            'status': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            # Category
            'category': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'e.g. Software Development'
                }
            ),

            # Tags
            'tags': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': (
                        'e.g. Python, Django, React, REST API'
                    )
                }
            ),

            # Notes
            'notes': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 5,
                    'placeholder': (
                        'Write any additional notes here...'
                    )
                }
            ),
        }

    # -----------------------------------------------------
    # Job Title Validation
    # -----------------------------------------------------

    def clean_job_title(self):

        job_title = self.cleaned_data['job_title']

        if len(job_title.strip()) < 2:

            raise forms.ValidationError(
                'Job title must contain at least 2 characters.'
            )

        return job_title.strip()

    # -----------------------------------------------------
    # Company Name Validation
    # -----------------------------------------------------

    def clean_company_name(self):

        company_name = self.cleaned_data['company_name']

        if len(company_name.strip()) < 2:

            raise forms.ValidationError(
                'Company name must contain at least 2 characters.'
            )

        return company_name.strip()

    # -----------------------------------------------------
    # Location Validation
    # -----------------------------------------------------

    def clean_location(self):

        location = self.cleaned_data['location']

        if len(location.strip()) < 2:

            raise forms.ValidationError(
                'Location must contain at least 2 characters.'
            )

        return location.strip()


# =========================================================
# Interview Form
# =========================================================

class InterviewForm(forms.ModelForm):

    class Meta:

        model = Interview

        fields = [
            'interview_date',
            'interview_type',
            'meeting_link',
            'interview_notes',
        ]

        widgets = {

            # Interview Date & Time
            'interview_date': forms.DateTimeInput(
                attrs={
                    'class': 'form-control',
                    'type': 'datetime-local'
                }
            ),

            # Interview Type
            'interview_type': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            # Meeting Link
            'meeting_link': forms.URLInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': (
                        'https://meet.google.com/...'
                    )
                }
            ),

            # Interview Notes
            'interview_notes': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 5,
                    'placeholder': (
                        'Write interview preparation notes...'
                    )
                }
            ),
        }

    # -----------------------------------------------------
    # Interview Date Validation
    # -----------------------------------------------------

    def clean_interview_date(self):

        interview_date = self.cleaned_data.get(
            'interview_date'
        )

        if not interview_date:
            raise forms.ValidationError(
                'Interview date and time is required.'
            )

        return interview_date

    # -----------------------------------------------------
    # Meeting Link Validation
    # -----------------------------------------------------

    def clean_meeting_link(self):

        meeting_link = self.cleaned_data.get(
            'meeting_link'
        )

        # Meeting link is optional
        if meeting_link:
            return meeting_link.strip()

        return meeting_link