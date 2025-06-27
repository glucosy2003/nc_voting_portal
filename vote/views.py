import random  # 1
import string  # 2
from datetime import datetime  # 3
from django.utils import timezone  # 4
from django.utils.timezone import localtime  # 5
from django.conf import settings  # 6

from django.shortcuts import render, get_object_or_404, redirect  # 8
from django.contrib import messages  # 9
from django.views import View  # 10
from django.http import HttpResponse  # 11
from django.contrib.auth import logout  # 12
from django.db.models import Count  # 13
from collections import defaultdict, OrderedDict  # 14-15

from .forms import VoterRegistrationForm, CandidateApplicationForm  # 17
from .models import ValidStudent, Voter, Candidate, CountdownTimer, Vote  # 18

from django.db import IntegrityError  # 20


# === Voter ID Generator ===
def generate_voter_id(length=7):  # 23
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))  # 24


def home(request):  # 27
    return render(request, 'vote/home.html')  # 28

def help_page(request):
    return render(request, 'vote/help.html')

def student_login(request):  # 31
    if request.method == 'POST':  # 32
        student_id = request.POST.get('student_id', '').strip()  # 33
        voter_id = request.POST.get('voter_id', '').strip()  # 34

        try:  # 36
            student = ValidStudent.objects.get(student_id=student_id)  # 37
            voter = Voter.objects.get(valid_student=student, voter_id=voter_id)  # 38

            request.session.flush()  # 🔐 Secure session rotation (prevents fixation) — 40
            request.session['student_id'] = student.student_id  # 41
            request.session['voter_id'] = voter.voter_id  # 42

            messages.info(request, f"👋 Welcome, {student.full_name}!")  # 44
            return redirect('dashboard')  # 45

        except (ValidStudent.DoesNotExist, Voter.DoesNotExist):  # 47
            messages.error(request, "Invalid Student ID or Voter ID. Please try again.", extra_tags='login')  # 48

    return render(request, 'vote/login.html')  # 50


def voter_register(request):  # 53
    if request.method == 'POST':  # 54
        form = VoterRegistrationForm(request.POST)  # 55
        if form.is_valid():  # 56
            valid_student = form.cleaned_data['valid_student']  # 57
            try:  # 59
                existing = Voter.objects.get(valid_student=valid_student)  # 60
                return render(request, 'vote/voter_register.html', {  # 62
                    'form': VoterRegistrationForm(),  # 63
                    'voter_id': existing.voter_id,  # 64
                    'already_registered': True,  # 65
                })
            except Voter.DoesNotExist:  # 66
                voter_id = generate_voter_id()  # 67
                while Voter.objects.filter(voter_id=voter_id).exists():  # 68
                    voter_id = generate_voter_id()  # 69

                Voter.objects.create(valid_student=valid_student, voter_id=voter_id)  # 71
                return render(request, 'vote/voter_register.html', {  # 73
                    'form': VoterRegistrationForm(),  # 74
                    'voter_id': voter_id,  # 75
                })
    else:  # 77
        form = VoterRegistrationForm()  # 78

    return render(request, 'vote/voter_register.html', {'form': form})  # 80


def voting_dashboard(request):  # 83
    student_id = request.session.get('student_id', None)  # 84
    voter_id = request.session.get('voter_id', None)  # 85

    if not student_id or not voter_id:  # 87
        return redirect('student_login')  # 88

    try:  # 90
        voter = Voter.objects.get(valid_student__student_id=student_id, voter_id=voter_id)  # 91
    except Voter.DoesNotExist:  # 92
        messages.error(request, "Voter record not found. Please login again.", extra_tags='voter')  # 93
        return redirect('student_login')  # 94

    total_students = ValidStudent.objects.count()  # 97
    total_voters = Voter.objects.count()  # 98
    total_positions = Candidate.objects.values('position').distinct().count()  # 99
    total_votes_cast = Vote.objects.count()  # 100

    voting_percentage = (total_votes_cast / (total_voters * total_positions) * 100) if total_voters and total_positions else 0  # 102

    voted_positions = Vote.objects.filter(voter=voter).values_list('position', flat=True).distinct()  # 105

    POSITION_ORDER = [  # 107
        'President', 'Vice President', 'Treasurer', 'Secretary', 'Speaker',
        'Sanitation', 'Social Welfare', 'Sports Director', 'Spiritual Director',
        'Entertainment Director', 'Nursing Representative', 'ICT Representative', 'BBA Representative',
    ]

    candidates = Candidate.objects.filter(approved=True).annotate(  # 114
        vote_count=Count('received_votes')  # 115
    )

    grouped_candidates = {}  # 117
    for c in candidates:  # 118
        grouped_candidates.setdefault(c.position, []).append(c)  # 119

    for cand_list in grouped_candidates.values():  # 121
        total_votes = sum(c.vote_count for c in cand_list)  # 122
        for c in cand_list:  # 123
            c.vote_percentage = round((c.vote_count / total_votes * 100), 1) if total_votes else 0  # 124
        cand_list.sort(key=lambda x: -x.vote_count)  # 125

    positions = OrderedDict()  # 127
    for pos in POSITION_ORDER:  # 128
        if pos in grouped_candidates:  # 129
            positions[pos] = grouped_candidates[pos]  # 130

    now = localtime(timezone.now())  # 133
    voting_timer = CountdownTimer.objects.filter(timer_type='voting').first()  # 134
    voting_status = "closed"  # 135
    time_remaining = 0  # 136

    application_timer = CountdownTimer.objects.filter(timer_type='application').first()  # 138
    application_status = "closed"  # 139
    application_time_remaining = 0  # 140

    if voting_timer and voting_timer.start_time and voting_timer.end_time:  # 142
        if now < voting_timer.start_time:  # 143
            voting_status = "not_started"  # 144
            time_remaining = int((voting_timer.start_time - now).total_seconds())  # 145
        elif voting_timer.start_time <= now <= voting_timer.end_time:  # 146
            voting_status = "open"  # 147
            time_remaining = int((voting_timer.end_time - now).total_seconds())  # 148

    if application_timer and application_timer.start_time and application_timer.end_time:  # 152
        if now < application_timer.start_time:  # 153
            application_status = "not_started"  # 154
            application_time_remaining = int((application_timer.start_time - now).total_seconds())  # 155
        elif application_timer.start_time <= now <= application_timer.end_time:  # 156
            application_status = "open"  # 157
            application_time_remaining = int((application_timer.end_time - now).total_seconds())  # 158

    return render(request, 'vote/dashboard.html', {  # 161
        'stats': {
            'total_students': total_students,
            'total_voters': total_voters,
            'votes_cast': total_votes_cast,
            'voting_percentage': round(voting_percentage, 1),
        },
        'positions': positions,
        'voted_positions': voted_positions,
        'voting_timer': voting_timer,
        'voting_status': voting_status,
        'time_remaining': time_remaining,
        'voting_end_time': voting_timer.end_time if voting_timer else None,
        'application_timer': application_timer,
        'application_status': application_status,
        'application_time_remaining': application_time_remaining,
    })


def vote(request, candidate_id):  # 181
    if request.method == 'POST':  # 182
        now = timezone.now()  # 183
        voting_timer = CountdownTimer.objects.filter(timer_type='voting').first()  # 184

        if not voting_timer or not (voting_timer.start_time <= now <= voting_timer.end_time):  # 186
            messages.error(request, "Voting is currently closed.", extra_tags='voter')  # 187
            return redirect('dashboard')  # 188

        student_id = request.session.get('student_id', None)  # 190
        voter_id = request.session.get('voter_id', None)  # 191

        try:
            voter = Voter.objects.get(valid_student__student_id=student_id, voter_id=voter_id)  # 193
        except Voter.DoesNotExist:
            messages.error(request, "Voter record not found.", extra_tags='voter')  # 195
            return redirect('dashboard')

        candidate = get_object_or_404(Candidate, pk=candidate_id, approved=True)  # 198
        position = candidate.position  # 199

        if Vote.objects.filter(voter=voter, position=position).exists():  # 201
            messages.error(request, f"You have already voted for the position '{position.title()}'.", extra_tags='voter')  # 202
            return redirect('dashboard')

        try:
            Vote.objects.create(voter=voter, candidate=candidate, position=position)  # 206
            messages.success(request, f"You have voted for {candidate.valid_student.full_name} as {position.title()}.", extra_tags='voter')  # 207
        except IntegrityError:
            messages.error(request, "You have already voted for this position.", extra_tags='voter')  # 210

        return redirect('dashboard')  # 212


def about_page(request):  # 215
    return render(request, 'vote/about.html')  # 216


def results_view(request):  # 219
    try:
        voting_timer = CountdownTimer.objects.get(timer_type='voting')  # 221
        voting_ended = timezone.now() > voting_timer.end_time  # 222
    except CountdownTimer.DoesNotExist:
        voting_ended = True  # 224

    results = defaultdict(list)  # 226

    if voting_ended:
        candidates = Candidate.objects.filter(approved=True).annotate(vote_count=Count('received_votes'))  # 228
        grouped = defaultdict(list)  # 230
        for c in candidates:
            grouped[c.position].append(c)

        for position, cands in grouped.items():
            total_votes = sum(c.vote_count for c in cands)
            for c in cands:
                results[position].append({
                    'name': c.valid_student.full_name,
                    'votes': c.vote_count,
                    'percentage': round((c.vote_count / total_votes) * 100, 1) if total_votes else 0,
                    'photo_url': c.photo.url if c.photo else None,  # 🔁 Template will use default via {% static %}
                })
            results[position].sort(key=lambda x: -x['votes'])

    return render(request, 'vote/results.html', {
        'voting_ended': voting_ended,
        'results': dict(results),
    })


def custom_logout_view(request):  # 247
    logout(request)
    request.session.flush()
    return redirect('login')


class RegisterView(View):  # 252
    def get(self, request):  # 253
        if 'student_id' not in request.session:
            messages.warning(request, "⚠️ Please log in as a student to apply.", extra_tags='voter')
            return redirect('student_login')

        form = CandidateApplicationForm()
        return render(request, 'vote/apply.html', {'form': form})

    def post(self, request):  # 260
        if 'student_id' not in request.session:
            messages.warning(request, "⚠️ Session expired or unauthorized access.", extra_tags='voter')
            return redirect('student_login')

        form = CandidateApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            student_id = request.session.get('student_id')
            try:
                valid_student = ValidStudent.objects.get(student_id=student_id)
            except ValidStudent.DoesNotExist:
                messages.error(request, "❌ You are not recognized as a valid student.", extra_tags='voter')
                return redirect('student_login')

            if Candidate.objects.filter(valid_student=valid_student).exists():
                messages.warning(request, "⚠️ You have already submitted an application.", extra_tags='voter')
                return redirect('dashboard')

            candidate = form.save(commit=False)
            candidate.valid_student = valid_student
            candidate.approved = None
            candidate.save()

            messages.success(request, "✅ Your application has been submitted.", extra_tags='voter')
            return redirect('dashboard')

        return render(request, 'vote/apply.html', {'form': form})


def candidate_apply(request):  # 288
    try:
        valid_student = ValidStudent.objects.get(user=request.user)
    except ValidStudent.DoesNotExist:
        messages.error(request, "❌ You are not a valid student.", extra_tags='apply')
        return redirect('home')

    if Candidate.objects.filter(valid_student=valid_student).exists():
        messages.warning(request, "🎯 You have already applied as a candidate.", extra_tags='apply')
        return redirect('dashboard')

    if request.method == 'POST':
        form = CandidateApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            candidate = form.save(commit=False)
            candidate.valid_student = valid_student
            candidate.approved = None 
            candidate.save()
            messages.success(request, "✅ Your application was submitted successfully.", extra_tags='apply')
            return redirect('dashboard')
    else:
        form = CandidateApplicationForm()

    return render(request, 'vote/apply.html', {'form': form})
