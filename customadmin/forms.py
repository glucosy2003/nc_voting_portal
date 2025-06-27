from django import forms
from vote.models import ValidStudent
from vote.models import CountdownTimer

class ValidStudentForm(forms.ModelForm):
    class Meta:
        model = ValidStudent
        fields = ['full_name', 'student_id', 'program', 'year']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'student_id': forms.TextInput(attrs={'class': 'form-control'}),
            'program': forms.Select(attrs={'class': 'form-control'}),  # ✅ use Select, not TextInput
            'year': forms.Select(attrs={'class': 'form-control'}),
        }


class VotingTimerForm(forms.Form):
    start_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    end_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
