from django import forms
from django.core.exceptions import ValidationError
from .models import ValidStudent, Candidate, Voter, PROGRAM_CHOICES

POSITION_CHOICES = [
    ('', '------ (Optional) ------'),
    ('President', 'President'),
    ('Vice President', 'Vice President'),
    ('Treasurer', 'Treasurer'),
    ('Secretary', 'Secretary'),
    ('Speaker', 'Speaker'),
    ('Sanitation', 'Sanitation'),
    ('Social Welfare', 'Social Welfare'),
    ('Sports Director', 'Sports Director'),
    ('Spiritual Director', 'Spiritual Director'),
    ('Entertainment Director', 'Entertainment Director'),
    ('Nursing Representative', 'Nursing Representative'),
    ('ICT Representative', 'ICT Representative'),
    ('BBA Representative', 'BBA Representative'),
]

YEAR_CHOICES = [
    ('', '-- Select Year --'),
    ('1', '1st Year'),
    ('2', '2nd Year'),
    ('3', '3rd Year'),
    ('4', '4th Year'),
]


class CandidateApplicationForm(forms.ModelForm):
    position = forms.ChoiceField(
        choices=POSITION_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Candidate
        fields = ['position', 'manifesto', 'photo']
        widgets = {
            'manifesto': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4, 
                'placeholder': 'Your Manifesto'
            }),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class VoterRegistrationForm(forms.Form):
    student_id = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 2210001'}),
        label="Student ID"
    )
    program = forms.ChoiceField(
        choices=PROGRAM_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Program"
    )
    year = forms.ChoiceField(
        choices=YEAR_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Year of Study"
    )

    def clean(self):
        cleaned_data = super().clean()
        student_id = cleaned_data.get('student_id', '').upper().strip()
        program = cleaned_data.get('program', '').strip()
        year = cleaned_data.get('year', '').strip()

        if not year.isdigit():
            raise ValidationError("❌ Please select a valid year.")

        try:
            valid_student = ValidStudent.objects.get(
                student_id=student_id,
                program=program,
                year=int(year)  # Ensure matching integer field
            )
        except ValidStudent.DoesNotExist:
            raise ValidationError("❌ Student ID, program, or year do not match any valid student record.")


        cleaned_data['valid_student'] = valid_student
        return cleaned_data
