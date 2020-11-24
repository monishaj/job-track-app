import os
import json
from random import choice, randint
import datetime
from faker import Faker

import crud
import model
import server

os.system('dropdb job-track-app')
os.system('createdb job-track-app')

model.connect_to_db(server.app)
model.db.create_all()

fake = Faker()

# create 10 job position
job_list = ["Software apprentice","Software engineer","Junior developer","Senior developer","Junior software engineer","Sw engineer", "Software Cloud Engineer", "Devops Engineer", "Devops Cloud Engineer","Data Science Engineer"]


# create Application state
app_state = ["Applied","Phone-Interview","Onsite-Interview","Rejected","Offer"]


# create 10 fake users each creating their job entry
for user in range(10):
    fname = fake.first_name() 
    lname = fake.last_name() #fake.name().split(" ")
    email = f"{fname}{lname}@gmail.com"
    password = f"{fname}{lname}123" #fake.password(length=12)
    phone_number = f"+1669247609{user}" 
    users = crud.create_user(fname, lname, email, password, phone_number)

    #create job details entry of each user 

    for job in range(5):
        rand_month = randint(1,12)
        date1 = datetime.date(year = 2020, month = rand_month, day = randint(1,14))
        date2 = datetime.date(year = 2020, month = rand_month, day = randint(15,29))

        company_name = fake.company()
        job_title = choice(job_list)
        application_deadline = date2
        job_listing_url = fake.url()
        state = fake.state()
        city = fake.city()
        application_listed = date1
        salary = randint(70000 , 90000)

        job_detail = crud.create_job_detail(company_name, job_title, application_deadline, job_listing_url, state, city, application_listed, salary)

        #create 5 job application per user

        user_id = user + 1
        job_id = job +(5 * user)+ 1
        application_date_submitted = date2
        job_applied = crud.create_job_applied(user_id, job_id, application_date_submitted)

        #create job application progress
        app_state = choice(["applied","phone interview","onsite interview","rejected","offer"])
        job_applied_id = user + 1 
        created_at = date1 
        application_progress = crud.create_application_progress(app_state, job_applied_id, created_at)

        #create upto 5 notes per user

        job_applied_id = job +(5 * user)+ 1
        user_id = user + 1
        note_category = choice(["Job Description","Follow-up","Note","Interview Question Behavioral","Interview Question Informational","Interview Question Technical","Recruiter Contact", "Resume"])
        note_title = f" {note_category} {job}"
        note_text = f" This is Note {note_category} of {company_name}."
        note_date_created = date1

        note = crud.create_note(job_applied_id, user_id, note_title, note_text,note_category, note_date_created)

    

