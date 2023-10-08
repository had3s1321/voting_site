from django import forms
from django.core.validators import RegexValidator
from .models import Voter, Candidate, Poll



class VoterRegistrationForm(forms.ModelForm):
    social_security_number = forms.CharField(
        max_length=11,
        validators=[RegexValidator(
            regex=r'^\d{11}$',
            message='Social security number must be 11 digits.',
            code='invalid_ssn'
        )],
    )

    class Meta:
        model = Voter
        fields = ['first_name', 'last_name', 'date_of_birth', 'social_security_number']



class CreatePollForm(forms.ModelForm):
    candidate_one = forms.ModelChoiceField(
        queryset=Candidate.objects.all(),
        label='Option 1 (Choose a Candidate)',
    )
    candidate_two = forms.ModelChoiceField(
        queryset=Candidate.objects.all(),
        label='Option 2 (Choose a Candidate)',
    )
    candidate_three = forms.ModelChoiceField(
        queryset=Candidate.objects.all(),
        label='Option 3 (Choose a Candidate)',
    )

    class Meta:
        model = Poll
        fields = ['name', 'candidate_one', 'candidate_two', 'candidate_three']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
