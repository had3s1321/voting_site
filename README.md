# Online Voting Application

## Overview
The Online Voting Application is designed to allow users to vote online in the upcoming elections. The application is divided into two main parts: user registration and the voting process.

## Features
- User Registration: Users can register on the site using a valid email address.
- Personal Data Submission: Before voting, users are required to provide their personal data.
- Voting: Once personal data is verified, users can cast their votes.

## Installation
To run the project locally, follow these steps:

Clone the repository:
clone https://github.com/had3s1321/voting_site.git

Navigate to the project directory

Set up a Python virtual environment (recommended):
python -m venv venv

Activate the virtual environment:
On Windows:
venv\Scripts\activate
On macOS and Linux:
source venv/bin/activate

Install project dependencies:
pip install -r requirements.txt

Create a PostgreSQL database and configure the database settings in settings.py.
Apply database migrations:
python manage.py migrate

Run the development server:
python manage.py runserver

Access the application at http://127.0.0.1:8000/ in your web browser.



## To-Do
Implement tests for views and forms.
Improve the consistency of the frontend.
Deploy the application on a cloud platform.

