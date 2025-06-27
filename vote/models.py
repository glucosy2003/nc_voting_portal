from django.db import models
import uuid
from django.contrib.auth.models import User

# ========================
# Program Choices Constant
# ========================
PROGRAM_CHOICES = [
    ('Human Resource Management', 'Human Resource Management'),
    ('Business Administration', 'Business Administration'),
    ('Accountancy', 'Accountancy'),
    ('Nursing and Midwifery', 'Nursing and Midwifery'),
    ('Information and Communication Technology', 'Information and Communication Technology'),
]

# ======================
# Valid Student Database
# ======================
class ValidStudent(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='valid_student')  # Optional connection to Django auth
    full_name = models.CharField(max_length=100, verbose_name="Full Name")
    student_id = models.CharField(max_length=20, unique=True, verbose_name="Student ID")

    program = models.CharField(max_length=45, choices=PROGRAM_CHOICES, verbose_name="Program")
    year = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4')], verbose_name="Year of Study")

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.student_id})"

    def get_voter(self):
        return getattr(self, 'voter', None)

    def get_candidate(self):
        return getattr(self, 'candidate', None)


# ================
# Registered Voter
# ================
class Voter(models.Model):
    valid_student = models.OneToOneField(ValidStudent, on_delete=models.CASCADE, related_name='voter')
    voter_id = models.CharField(max_length=10, unique=True)
    voted = models.BooleanField(default=False, verbose_name="Has Voted?")

    def __str__(self):
        return f"Voter: {self.valid_student.student_id} ({self.valid_student.full_name})"


# ==============
# Candidate Info
# ==============
class Candidate(models.Model):
    valid_student = models.OneToOneField(ValidStudent, on_delete=models.CASCADE, related_name='candidate')
    position = models.CharField(max_length=100, verbose_name="Position")
    manifesto = models.TextField(verbose_name="Manifesto")
    photo = models.ImageField(upload_to='candidate_photos/%Y/%m/', verbose_name="Candidate Photo")
    approved = models.BooleanField(null=True, default=None, verbose_name="Approval Status")
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.valid_student.full_name} - {self.position}"


# ===========
# Vote Record
# ===========
class Vote(models.Model):
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE, related_name='votes')
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='received_votes')
    position = models.CharField(max_length=100)  # store position name here
    voted_at = models.DateTimeField(auto_now_add=True)
    voter_ip = models.GenericIPAddressField(null=True, blank=True)
    device_info = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.voter.valid_student.student_id} voted for {self.candidate.valid_student.full_name} as {self.position}"

    class Meta:
        unique_together = ('voter', 'position')  # Prevent multiple votes per position


# ===========
# countdown
# ===========
class CountdownTimer(models.Model):
    TIMER_TYPE_CHOICES = [
        ('application', 'Candidate Application'),
        ('voting', 'Voting'),
    ]

    timer_type = models.CharField(max_length=20, choices=TIMER_TYPE_CHOICES, unique=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"{self.get_timer_type_display()} Countdown"
