from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date, timedelta
from django.utils import timezone

# Create your models here.
class CustomUser(AbstractUser):
    student_number = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.username

class Assignment(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    reminder_date = models.DateField(null=True, blank=True)
    completed_date = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.reminder_date:
            self.reminder_date = self.due_date - timedelta(days=2)  # Set a default reminder 2 days before
        if self.completed and not self.completed_date:
            self.completed_date = date.today()

        super().save(*args, **kwargs)

    def is_due_soon(self):
        return (self.due_date - date.today()).days <= 2 and self.due_date >= date.today()

    def is_overdue(self):
        return self.due_date < date.today() and not self.completed

    def is_completed_before_due(self):
        return self.completed and self.due_date > self.completed_date

    def is_completed_after_due(self):
        return self.completed and self.due_date < self.completed_date

    def reminder_text(self):
        # Check for different conditions and return appropriate reminder message
        if self.is_completed_before_due():
            return "Completed before due date"
        elif self.is_completed_after_due():
            return "Completed after due date"
        elif self.is_overdue():
            return "Overdue"
        elif self.is_due_soon():
            return "Due Soon"
        else:
            return "Pending"

    def __str__(self):
        return self.title 
    
    class Meta:
        ordering = ['due_date']


MOOD_CHOICES = [
    ('happy', '😊 Happy'),
    ('okay', '😐 Okay'),
    ('stressed', '😰 Stressed'),
    ('sad', '😢 Sad'),
    ('motivated', '💪 Motivated'),
    ('tired', '😴 Tired'),
]

class MoodCheckin(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    mood = models.CharField(max_length=20, choices=MOOD_CHOICES)
    note = models.TextField(blank=True, null=True)
    checkin_date = models.DateTimeField(default=timezone.now)

    def motivation_message(self):
        mood_motivations = {
            'happy': (
                "Keep up the positive energy! Stay focused and keep winning! "
                "Maintain this momentum and tackle your assignments with the same enthusiasm!"
            ),
            'okay': (
                "You're doing fine. Small steps every day lead to success. "
                "Try reviewing one subject at a time to ensure steady progress. Stay consistent!"
            ),
            'stressed': (
                "Take a deep breath. Break your work into smaller pieces. You've got this. "
                "Try creating a study plan, prioritize assignments, and take regular breaks to recharge!"
            ),
            'sad': (
                "It's okay to have off days. Reach out to a friend or mentor and take care of yourself. "
                "Remember, your well-being is just as important as your studies. Don’t hesitate to ask for support!"
            ),
            'motivated': (
                "Now's the time to push your limits! Keep going strong! "
                "Stay focused on your goals. Review your tasks and prioritize the most important ones to stay ahead."
            ),
            'tired': (
                "Rest is part of the process. Recharge and come back stronger. "
                "Plan your study sessions effectively—balance work with rest for better retention and productivity."
            ),
        }
        return mood_motivations.get(self.mood, "Keep going, one step at a time.")

    def __str__(self):
        return f"{self.user.username} - {self.get_mood_display()} on {self.checkin_date.strftime('%Y-%m-%d')}"

    class Meta:
        ordering = ['-checkin_date']