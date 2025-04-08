from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Assignment, CustomUser, MoodCheckin

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'description', 'due_date', 'completed', 'reminder_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'reminder_date': forms.DateInput(attrs={'type': 'date'}),
        }

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    student_number = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Student Number'})
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'student_number', 'password1', 'password2']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")

        return password2  
    
class MoodCheckInForm(forms.ModelForm):
       class Meta:
         model = MoodCheckin
         fields = ['mood', 'note']
         widgets = {
            'note': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Optional: Write how you feel...'}),
        }