from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model
from django.utils import timezone



User = get_user_model()



class PersonalDetails(models.Model):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    date_of_birth = models.DateField(default=timezone.now)
    social_security_number = models.CharField(
        max_length=11,
        validators=[RegexValidator(
            regex=r'^\d{11}$',  # Use regex to enforce 11 digits
            message='Social security number must be 11 digits.',
            code='invalid_ssn'
        )]
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.first_name} {self.last_name}'



class Voter(PersonalDetails):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    


class Candidate(PersonalDetails):
    vote_count = models.IntegerField(default=0)



class Poll(models.Model):
    name = models.CharField(default=None, max_length=50)
    
    candidate_one = models.ForeignKey(
        Candidate,
        on_delete=models.SET_NULL,
        null=True,
        related_name='option_one_polls',
    )
    candidate_two = models.ForeignKey(
        Candidate,
        on_delete=models.SET_NULL,
        null=True,
        related_name='option_two_polls',
    )
    candidate_three = models.ForeignKey(
        Candidate,
        on_delete=models.SET_NULL,
        null=True,
        related_name='option_three_polls',
    )

    def __str__(self):
        return self.name
    
    def total_votes(self):
        return (
            self.candidate_one.vote_count +
            self.candidate_two.vote_count +
            self.candidate_three.vote_count
        )
    



class Vote(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    voted_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.voter} voted in {self.poll} at {self.voted_at}'

 