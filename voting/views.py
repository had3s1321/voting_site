from django.shortcuts import render, redirect
from django.contrib.auth.decorators import  login_required 
from django.contrib import messages
from .models import Poll, Voter, Vote
from .forms import CreatePollForm, VoterRegistrationForm
from .models import Poll




def index(request):
    polls = Poll.objects.all()
    context = {
        'polls' : polls
    }
    return render(request, 'voting/index.html', context)


def create_poll(request):
    if request.method == 'POST':
        form = CreatePollForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CreatePollForm()
    context = {
        'form' : form
    }
    return render(request, 'voting/create.html', context)


@login_required
def vote(request, poll_id):
    user = request.user
    poll = Poll.objects.get(pk=poll_id)

    try:
        voter = user.voter
    except Voter.DoesNotExist:
        return redirect('voter-registration')

    if not poll:
        messages.add_message(request, messages.ERROR, 'No poll is open')
        context = {'has_error': True}
        return render(request, 'voting/vote.html', context)

    if Vote.objects.filter(voter=voter, poll=poll).exists():
        messages.add_message(request, messages.ERROR, 'You have already voted in this poll.')
        context = {'has_error': True}
        return redirect('home')  # Redirect to the home page

    if request.method == 'POST':
        selected_candidate = request.POST.get('poll')

        try:
            poll = Poll.objects.get(id=poll_id)
            candidate = None

            if selected_candidate == 'candidate_one':
                candidate = poll.candidate_one
            elif selected_candidate == 'candidate_two':
                candidate = poll.candidate_two
            elif selected_candidate == 'candidate_three':
                candidate = poll.candidate_three

            if candidate:
                candidate.vote_count += 1
                candidate.save()

                Vote.objects.create(voter=voter, poll=poll, candidate=candidate)

                messages.add_message(request, messages.SUCCESS, 'Your vote has been recorded successfully.')
                return redirect('home')
            else:
                messages.add_message(request, messages.ERROR, 'Invalid candidate selection.')
        except Poll.DoesNotExist:
            messages.add_message(request, messages.ERROR, 'Selected poll does not exist.')

    context = {
        'poll': poll
    }
    return render(request, 'voting/vote.html', context)



def results(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)
    context = {
        'poll' : poll
    }
    return render(request, 'voting/results.html', context)


@login_required
def voter_registration(request):
    user = request.user
    if request.method == 'POST':
        form = VoterRegistrationForm(request.POST)
        if form.is_valid():
            voter = form.save(commit=False)
            voter.user = user
            voter.save()
            return redirect('home')
    else:
        form = VoterRegistrationForm()
    return render(request, 'voting/voter-registration.html', {'form': form})


