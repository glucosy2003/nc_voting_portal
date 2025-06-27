from collections import OrderedDict
from collections import defaultdict

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.db import models
from django.db.models import Q
import csv
from io import StringIO
from django.http import HttpResponse
from django.contrib.auth import update_session_auth_hash

from vote.models import Candidate, ValidStudent, Vote, Voter
from .forms import ValidStudentForm
from vote.forms import VoterRegistrationForm

from vote.models import CountdownTimer
from .forms import VotingTimerForm
from django.utils import timezone
from datetime import datetime
from django.utils.timezone import localtime



# --- Admin check -------------------------------------------------------------
def is_admin(user):
    return user.is_staff

# --- Admin login/logout ------------------------------------------------------
@csrf_protect
def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect("customadmin:admin_dashboard")
        else:
            return render(request, "customadmin/login.html", {
                "error": "Invalid credentials or not an admin."
            })
    return render(request, "customadmin/login.html")

@login_required
def admin_logout(request):
    logout(request)
    return redirect("customadmin:admin_login")

# --- Admin dashboard with statistics ----------------------------------------


@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    total_candidates = Candidate.objects.count()
    approved_candidates = Candidate.objects.filter(approved=True).count()
    rejected_candidates = Candidate.objects.filter(approved=False).count()
    pending_candidates = Candidate.objects.filter(approved__isnull=True).count()

    total_voters = ValidStudent.objects.count()
    total_votes = Vote.objects.count()
    distinct_voters = Vote.objects.values('voter_id').distinct().count()
    positions_count = Candidate.objects.values_list('position', flat=True).distinct().count()

    # Use Django's localtime
    now = localtime(timezone.now())

    app_timer = CountdownTimer.objects.filter(timer_type='application').first()
    vote_timer = CountdownTimer.objects.filter(timer_type='voting').first()

    app_remaining = 0
    vote_remaining = 0

    if app_timer and app_timer.start_time <= now <= app_timer.end_time:
        app_remaining = int((app_timer.end_time - now).total_seconds())

    if vote_timer and vote_timer.start_time <= now <= vote_timer.end_time:
        vote_remaining = int((vote_timer.end_time - now).total_seconds())

    context = {
        'total_candidates': total_candidates,
        'approved_candidates': approved_candidates,
        'rejected_candidates': rejected_candidates,
        'pending_candidates': pending_candidates,
        'total_voters': total_voters,
        'total_votes': total_votes,
        'distinct_voters': distinct_voters,
        'positions_count': positions_count,
        'app_remaining': app_remaining,
        'vote_remaining': vote_remaining,
    }

    return render(request, "customadmin/dashboard.html", context)


# --- Manage Candidates -------------------------------------------------------
@login_required
@user_passes_test(is_admin)
def manage_candidates(request):
    positions_order = [
        'President', 'Vice President', 'Treasurer', 'Secretary', 'Speaker',
        'Sanitation', 'Social Welfare', 'Sports Director', 'Spiritual Director',
        'Entertainment Director', 'Nursing Representative', 'ICT Representative',
        'BBA Representative',
    ]

    candidates = Candidate.objects.select_related('valid_student').all()
    grouped = OrderedDict((pos, []) for pos in positions_order)

    for cand in candidates:
        grouped.setdefault(cand.position if cand.position in grouped else 'Others', []).append(cand)

    return render(request, 'customadmin/manage_candidates.html', {
        'grouped_candidates': grouped
    })

# --- Candidate actions -------------------------------------------------------
@csrf_protect
@login_required
@user_passes_test(is_admin)
def approve_candidate(request, candidate_id):
    cand = get_object_or_404(Candidate, id=candidate_id)
    cand.approved = True
    cand.save()
    messages.success(request, f"✅ Candidate '{cand.valid_student.full_name}' approved.")
    return redirect('customadmin:manage_candidates')

@csrf_protect
@login_required
@user_passes_test(is_admin)
def reject_candidate(request, candidate_id):
    cand = get_object_or_404(Candidate, id=candidate_id)
    cand.approved = False
    cand.save()
    messages.warning(request, f"⚠️ Candidate '{cand.valid_student.full_name}' rejected.")
    return redirect('customadmin:manage_candidates')

@csrf_protect
@login_required
@user_passes_test(is_admin)
def delete_candidate(request, candidate_id):
    cand = get_object_or_404(Candidate, id=candidate_id)
    if request.method == 'POST':
        cand.delete()
        messages.error(request, f"🗑️ Candidate '{cand.valid_student.full_name}' deleted.")
    return redirect('customadmin:manage_candidates')

# --- View results ------------------------------------------------------------
@login_required
@user_passes_test(is_admin)
def view_results(request):
    if request.GET.get("download") == "csv":
        return export_results_csv()  # 🔁 Route to the CSV export logic

    positions_order = [
        'President', 'Vice President', 'Treasurer', 'Secretary', 'Speaker', 'Sanitation',
        'Social Welfare', 'Sports Director', 'Spiritual Director', 'Entertainment Director',
        'Nursing Representative', 'ICT Representative', 'BBA Representative',
    ]

    results = OrderedDict((pos, []) for pos in positions_order)

    for cand in Candidate.objects.select_related('valid_student').all():
        count = Vote.objects.filter(candidate=cand).count()
        key = cand.position if cand.position in results else 'Others'
        results.setdefault(key, []).append({'candidate': cand, 'count': count})

    for pos, entries in results.items():
        total_votes = sum(entry['count'] for entry in entries) or 1
        for entry in entries:
            entry['percentage'] = round((entry['count'] / total_votes) * 100, 2)
        entries.sort(key=lambda e: e['count'], reverse=True)

    return render(request, 'customadmin/results.html', {
        'results': results,
    })


# --- Export results to CSV ---------------------------------------------------
def export_results_csv():
    candidates = Candidate.objects.select_related('valid_student').all()
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Position', 'Candidate Name', 'Vote Count', 'Vote Percentage'])

    positions = {}
    for cand in candidates:
        pos = cand.position or 'Others'
        count = Vote.objects.filter(candidate=cand).count()
        positions.setdefault(pos, []).append((cand, count))

    for pos, items in positions.items():
        total = sum(i[1] for i in items) or 1
        sorted_items = sorted(items, key=lambda x: x[1], reverse=True)
        for cand, count in sorted_items:
            percentage = round((count / total) * 100, 2)
            writer.writerow([
                pos,
                cand.valid_student.full_name,
                count,
                f"{percentage}%",
            ])

    response = HttpResponse(output.getvalue(), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="election_results.csv"'
    return response

# --- View voters -------------------------------------------------------------
@login_required
@user_passes_test(is_admin)
def registered_voters(request):
    query = request.GET.get('q', '')
    
    if query:
        voters = Voter.objects.select_related('valid_student').filter(
            Q(valid_student__student_id__icontains=query) |
            Q(valid_student__full_name__icontains=query)
        ).order_by('valid_student__student_id')
    else:
        voters = Voter.objects.select_related('valid_student').all().order_by('valid_student__student_id')

    # Grouping voters by their program
    grouped_voters = defaultdict(list)
    for voter in voters:
        program = voter.valid_student.program
        grouped_voters[program].append(voter)

    return render(request, 'customadmin/registered_voters.html', {
        'grouped_voters': dict(grouped_voters),
        'search_query': query,
    })

# --- Valid Student Management ------------------------------------------------
@login_required
@user_passes_test(is_admin)
def list_valid_students(request):
    q = request.GET.get('q', '')
    students = ValidStudent.objects.filter(
        Q(full_name__icontains=q) | Q(student_id__icontains=q)
    ).order_by('program', 'full_name') if q else ValidStudent.objects.all().order_by('program', 'full_name')

    # ✅ Group students by program
    grouped_students = {}
    for student in students:
        grouped_students.setdefault(student.program, []).append(student)

    return render(request, 'customadmin/valid_students_list.html', {
        'grouped_students': grouped_students,
        'query': q,
    })

@login_required
@user_passes_test(is_admin)
def add_valid_student(request):
    if request.method == 'POST':
        form = ValidStudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Valid student added successfully.')
            return redirect('customadmin:list_valid_students')
    else:
        form = ValidStudentForm()
    return render(request, 'customadmin/valid_student_form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def delete_valid_student(request, pk):
    student = get_object_or_404(ValidStudent, pk=pk)
    if request.method == 'POST':
        student.delete()
        messages.success(request, f'🗑️ Student {student.student_id} deleted successfully.')
        return redirect('customadmin:list_valid_students')
    return render(request, 'customadmin/valid_student_confirm_delete.html', {'student': student})


@login_required
@user_passes_test(is_admin)
def change_admin_password(request):
    if request.method == 'POST':
        current = request.POST.get('current_password')
        new1 = request.POST.get('new_password1')
        new2 = request.POST.get('new_password2')

        if not request.user.check_password(current):
            messages.error(request, 'Current password is incorrect.')
        elif new1 != new2:
            messages.error(request, 'New passwords do not match.')
        elif len(new1) < 8:
            messages.error(request, 'New password must be at least 8 characters.')
        else:
            request.user.set_password(new1)
            request.user.save()
            update_session_auth_hash(request, request.user)  # Keep user logged in
            messages.success(request, 'Password changed successfully!')
            return redirect('customadmin:change_admin_password')

    return render(request, 'customadmin/change_password.html')

@login_required
@user_passes_test(is_admin)
def countdown_timer_control(request):
    timer_types = ['application', 'voting']
    timers = {t.timer_type: t for t in CountdownTimer.objects.all()}
    timer_labels = [('application', 'Application'), ('voting', 'Voting')]

    if request.method == 'POST':
        for timer_type in timer_types:
            start_time_str = request.POST.get(f'{timer_type}_start')
            end_time_str = request.POST.get(f'{timer_type}_end')

            if start_time_str and end_time_str:
                try:
                    start_time = datetime.strptime(start_time_str, '%Y-%m-%dT%H:%M')
                    end_time = datetime.strptime(end_time_str, '%Y-%m-%dT%H:%M')

                    timer = CountdownTimer.objects.filter(timer_type=timer_type).first()
                    if timer:
                        timer.start_time = start_time
                        timer.end_time = end_time
                        timer.save()
                    else:
                        CountdownTimer.objects.create(
                            timer_type=timer_type,
                            start_time=start_time,
                            end_time=end_time
                        )
                except ValueError:
                    messages.error(request, f"Invalid date/time format for {timer_type} timer.")
                    return redirect('customadmin:countdown_timer_control')

            else:
                messages.error(request, f"Both start and end times are required for {timer_type} timer.")
                return redirect('customadmin:countdown_timer_control')


        messages.success(request, "Countdown timers updated successfully.")
        return redirect('customadmin:countdown_timer_control')


    context = {
        'timers': timers,
        'timer_labels': timer_labels,
    }
    return render(request, 'customadmin/countdown_timer_control.html', context)



@login_required
@user_passes_test(is_admin)
def clear_votes(request):
    if request.method == 'POST':
        Vote.objects.all().delete()
        messages.success(request, "✅ All votes cleared successfully.")
        return render(request, 'customadmin/clear_votes.html')
    else:
        return render(request, 'customadmin/clear_votes.html')
