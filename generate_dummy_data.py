import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "votingsite.settings")

import django
from django.contrib.auth import get_user_model

django.setup()

# THE ORDER OF THE LINES FROM ABOVE MATTERS!

from voting.models import Voter, Candidate  
from faker import Faker

faker = Faker()

User = get_user_model()

def create_users_and_voters(num_users):
    users_and_voters = []
    for _ in range(num_users):
        username = faker.user_name()
        email = faker.email()
        password = "password1234"
        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_active = True
        user.is_email_verified = True
        user.save()
        first_name = faker.first_name()
        last_name = faker.last_name()
        ssn = faker.unique.random_int(min=10000000000, max=99999999999)
        date_of_birth = faker.date_of_birth(minimum_age=18, maximum_age=70)  
        voter = Voter.objects.create(user=user, first_name=first_name, last_name=last_name, social_security_number=ssn, date_of_birth=date_of_birth)
        users_and_voters.append((user, voter))

    return users_and_voters

def create_candidates(num_candidates):
    candidates = []
    for _ in range(num_candidates):
        candidate_first_name = faker.first_name()
        candidate_last_name = faker.last_name()
        candidate_ssn = faker.unique.random_int(min=10000000000, max=99999999999)
        candidate_date_of_birth = faker.date_of_birth(minimum_age=25, maximum_age=70) 
        candidate = Candidate.objects.create(first_name=candidate_first_name, last_name=candidate_last_name, social_security_number=candidate_ssn, date_of_birth=candidate_date_of_birth)
        candidates.append(candidate)

    return candidates

def generate_dummy_data():
    num_users = 50
    num_candidates = 10 
    users_and_voters = create_users_and_voters(num_users)
    candidates = create_candidates(num_candidates)

if __name__ == "__main__":
    generate_dummy_data()