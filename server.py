""" Server for Job Track App """
from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db , User
import crud
# from flask_login import LoginManager
from jinja2 import StrictUndefined
from datetime import datetime
from twilio.rest import Client
import os
import requests

app = Flask(__name__)
# login = LoginManager(app)
app.secret_key = "job_track_app"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """Show homepage"""

    return render_template('homepage.html')

@app.route('/about')
def about():
    """Show About page"""

    return render_template('about.html')

@app.route('/demo')
def demo():
    """Show Demo page"""

    return render_template('demo.html')    

@app.route('/sign-in')
def signin():
    return render_template('sign-in.html')

@app.route('/', methods=['POST'])
def set_user():
    """Create a new user and save to Db as well as initiate setting sessions ."""

    fname = request.form.get('fname')
    lname = request.form.get('lname')
    email = request.form.get('email')
    password = request.form.get('password')
    phone_number = request.form.get('phone_number')

    user = crud.get_user_by_email(email)

    if user:
        
        if user.check_password(password) == False:
            flash('Incorrect Password. Try again.')
            return redirect('/')
        else:
            session['user_id'] = user.user_id
            session['first_name'] = user.fname
            session['email'] = user.email
            flash('Sucessfully Logged In.')
            return render_template('view.html')
            
    else:
        new_user = crud.create_user(fname, lname, email, password, phone_number)
        flash('Account created! Logged In.')
        
        #saving the user to the session
        session['user_id'] = new_user.user_id
        session['first_name'] = new_user.fname
        session['email'] = new_user.email

        return render_template('view.html')


@app.route('/profile')
def user_profile():
    """Return the users profile """
    user_id = session.get('user_id', None)
    user = crud.get_user_by_email(session['email'])
    if user_id == None:
        user_details = {'logged_in': 'no'}
    else:    
        user_details = {
            'user_id': user_id,
            'first_name':user.fname,
            'lname':user.lname,
            'logged_in': 'yes',
    }
    return user_details

@app.route('/logout')
def logout():
    """User log-out"""  

    session.pop('user_id', None)
    session.pop('first_name', None)
    session.pop('email', None)
    flash('Logged Out')
    return redirect('/')



@app.route('/view' , methods = ['GET', 'POST'])
def view_page():
    """Show view page"""  

    view_job_app = request.form['job-application']
    print('************************************')
    print("view_job_app is ****************",view_job_app)
    if view_job_app == 'view-job-application':
        return redirect('/view-job-application')
    elif view_job_app == 'view-interview-questions':
        return redirect('/all-interview-questions')    
    else:
        return redirect('/render-create-job-application-form')


@app.route('/view-job-application')
def job_application():
    """View All Job Application of a user """

    user = crud.get_user_by_email(session['email'])
    user_id = user.user_id
    job_detail = crud.get_user_job_detail(user_id)
    dictionary_jobs = {}
    for index,job in enumerate(job_detail): 
        dictionary_jobs[index] = {}
        dictionary_jobs[index]['job_id'] = job.job_id,
        dictionary_jobs[index]['company_name'] = job.company_name,
        dictionary_jobs[index]['job_title'] = job.job_title,
        dictionary_jobs[index]['application_deadline'] = job.application_deadline,
        dictionary_jobs[index]['job_listing_url'] = job.job_listing_url ,
        dictionary_jobs[index]['state'] = job.state,
        dictionary_jobs[index]['app_state'] = crud.get_application_state_by_applied(job.job_completed_applications[0].job_applied_id).application_state
        # job_description['app_state'] = job.job_completed_applications[0].job_application_progress[-1].application_state

    return render_template('view-job-application.html', dictionary_jobs=dictionary_jobs)


@app.route('/job-application/<job_id>')
def render_job_application(job_id):
    session['job_id'] = job_id
    return render_template('job-application.html')


@app.route('/view-job-application/<job_id>')
def get_job_details(job_id):
    """ Display extended job details"""
    print("job_id:",job_id)
    user = crud.get_user_by_email(session['email'])
    user_id = user.user_id
    print("user_id:",user_id)
    # user_id = 11
    job_detail = crud.get_user_job_detail(user_id)
    job_applied_id = crud.get_job_applied_by_job_id(job_id)
    dictionary_jobs = {}
    for job in job_detail:
        print("job:",job) 
        if job.job_id == int(job_id): 
            print("entered if")
            dictionary_jobs['company_name'] = job.company_name,
            dictionary_jobs['job_title'] = job.job_title,
            dictionary_jobs['application_deadline'] = job.application_deadline,
            dictionary_jobs['job_listing_url'] = job.job_listing_url ,
            dictionary_jobs['state'] = job.state,
            dictionary_jobs['city'] = job.city,
            dictionary_jobs['salary'] = job.salary,
            dictionary_jobs['application_listed'] = job.application_listed,
            dictionary_jobs['app_state'] = crud.get_application_state_by_applied(job.job_completed_applications[0].job_applied_id).application_state
    
    notes_list = crud.all_note_by_job_applied_id(job_applied_id)
    
    note_dictionary = {}
    
    for index, note in enumerate(notes_list):
        note_dictionary[index] = {}
        # note_dictionary[index]['note_category'] = note.note_category,
        note_dictionary[index]['note_title'] = note.note_title,
        note_dictionary[index]['note_text'] = note.note_text
    # print("dictionary_jobs::",dictionary_jobs)
    # print(note_dictionary)
    note_job_description = crud.all_jd_by_job_applied_id(job_applied_id)
    note_jd = {}
    for index, note in enumerate(note_job_description):
        note_jd[index] = {}
        note_jd[index]['note_title'] = note.note_title,
        note_jd[index]['note_text'] = note.note_text
    note_recruit = crud.all_recruiter_by_job_applied_id(job_applied_id)
    note_recruiter = {}
    for index, note in enumerate(note_recruit):
        note_recruiter[index] = {}
        note_recruiter[index]['note_title'] = note.note_title,
        note_recruiter[index]['note_text'] = note.note_text
    

    
    return render_template('view-application-details.html', dictionary_jobs = dictionary_jobs ,note_dictionary = note_dictionary, note_jd= note_jd, note_recruiter = note_recruiter )


@app.route('/resources/<job_id>')
def get_resources(job_id):
    """ get resources of a particular job application"""
    job_applied_id = crud.get_job_applied_by_job_id(job_id)
    note_resumes = crud.all_resume_by_job_applied_id(job_applied_id)
    note_resume = {}
    for index, note in enumerate(note_resumes):
        note_resume[index] = {}
        note_resume[index]['note_title'] = note.note_title,
        note_resume[index]['note_text'] = note.note_text
    
    note_followups = crud.all_followup_by_job_applied_id(job_applied_id)
    note_followup = {}

    for index, note in enumerate(note_followups):
        note_followup[index] = {}
        note_followup[index]['note_title'] = note.note_title,
        note_followup[index]['note_text'] = note.note_text
    
    return render_template('resources.html' , note_resume =note_resume , note_followup=note_followup)

 
@app.route('/interview-questions/<job_id>')
def get_interview_questions(job_id):
    """ get interview questions of a particular job application"""
    """ get resources of a particular job application"""
    job_applied_id = crud.get_job_applied_by_job_id(job_id)
    note_interviewqs = crud.all_interview_by_job_applied_id(job_applied_id)
    note_interview_question = {}
    for index, note in enumerate(note_interviewqs):
        note_interview_question[index] = {}
        note_interview_question[index]['note_category'] = note.note_category,
        note_interview_question[index]['note_title'] = note.note_title,
        note_interview_question[index]['note_text'] = note.note_text
    
    return render_template('interview-questions.html' , note_interview_question =note_interview_question )
   

@app.route('/update-fields/<job_id>' , methods=['POST', 'GET'])
def update_fileds(job_id):
    """ Update Fields of a particular job application"""
    job_applied_id = crud.get_job_applied_by_job_id(job_id)
    created_at = datetime.now()
    user_id = session['user_id']
    note_date_created = datetime.now()
    if request.method == 'GET':
        return render_template('update-fields.html')
    else:
        application_state = request.form.get('application_state')
        note_category = request.form.get('note_category')
        note_title = request.form.get('note_title')
        note_text = request.form.get('note_text')

        if application_state:
            application_progress = crud.create_application_progress(application_state, job_applied_id , created_at)
        if note_category:
            note = crud.create_note(job_applied_id, user_id, note_title, note_text, note_category, note_date_created)
    template =  f'/view-job-application/{job_id}'       
    return redirect(template)





    

@app.route('/create-job-application', methods=['POST'])
def create_job_application():
    """Create a job application """

    # if request.method == 'POST':
    user = crud.get_user_by_email(session['email'])
    user_id = user.user_id

    company_name = request.form.get('company_name')
    job_title = request.form.get('job_title')
    deadline = request.form.get('deadline')
    job_listing_url = request.form.get('company_name')
    listing_date = request.form.get('application_listed')
    salary = request.form.get('salary')
    application_state = request.form.get('application_state')
    state = request.form.get('state')
    city = request.form.get('city')
    note_category = request.form.get('note_category')
    note_title = request.form.get('note_title')
    note_text = request.form.get('note_text')
    
    formatted_listing_date = datetime.strptime(listing_date , "%Y-%m-%dT%H:%M")
    formatted_deadline = datetime.strptime(deadline , "%Y-%m-%dT%H:%M")

    job_detail = crud.create_job_detail(company_name, job_title, formatted_deadline, job_listing_url, state, city, formatted_listing_date, salary)

    job_id = crud.get_last_job_id()
    application_date_submitted = datetime.now()

    job_applied = crud.create_job_applied(user_id, job_id, application_date_submitted)

    job_applied_id = crud.get_last_job_applied_id()
    note_date_created = datetime.now()

    note = crud.create_note(job_applied_id, user_id, note_title, note_text, note_category, note_date_created)

    created_at = datetime.now()

    application_progress = crud.create_application_progress(application_state, job_applied_id , created_at)

    return redirect('/view-job-application')
    
    # else:
    #     return render_template('create-job-application.html')


@app.route('/render-create-job-application-form')
def render_create_job():
    """Rendering create job application template """
    return render_template('create-job-application.html')

@app.route('/all-interview-questions')
def all_interview_questions():
    """ Return all the Interview questions of every job the user applied"""
    # user_id = 11
    user_id = session['user_id']
    interview_objects = crud.all_interview_by_user_id(user_id)
    behavioral = {}
    technical = {}
    informational = {}

    for index, note in enumerate(interview_objects):
        if note.note_category == 'Interview Question Behavioral':
            behavioral[index] = {}
            behavioral[index]['note_title'] = note.note_title,
            behavioral[index]['note_text'] = note.note_text
            

        elif note.note_category == 'Interview Question Technical':
            technical[index] = {}
            technical[index]['note_title'] = note.note_title,
            technical[index]['note_text'] = note.note_text

        else:
            informational[index] = {}
            informational[index]['note_title'] = note.note_title,
            informational[index]['note_text'] = note.note_text
    print ('behavioral',behavioral)
    print ('technical',technical)
    print ('informational',informational)

    return render_template('all-interview-questions.html',behavioral=behavioral, technical = technical,informational=informational  )

@app.route('/events' , methods = ['GET','POST'])
def events():
    """Rendering event template """
    # if request.method == 'GET':
    #     return render_template('events.html',event_dict=event_dict)
    # else:
    user = crud.get_user_by_email(session['email'])
    user_id = user.user_id 
    phone = user.phone_number

    event_title = request.form.get('event_title')
    event_text = request.form.get('reminder_text')
    event_time = request.form.get('event-time')
    reminder_status = request.form.get('reminder')
    print('reminder_status',reminder_status)

    if event_time:
        created_at = datetime.strptime(event_time, "%Y-%m-%dT%H:%M")
        event = crud.create_event(user_id,event_title,event_text,reminder_status, created_at)

    if reminder_status == 'Yes':
        print('yes************************************')
        # twilio(phone,event_text)

    event_dict = {}

    event_objects = crud.get_event_by_user_id(user_id)
    for index, obj in enumerate(event_objects):
        event_dict[index] = {}
        event_dict[index]['event_title'] = obj.event_title,
        event_dict[index]['reminder_status'] = obj.reminder_status
        event_dict[index]['created_at'] = obj.created_at
    print(event_dict)

    return render_template('events.html', event_dict=event_dict)


def twilio(to_number,body_content):
    # run source secrets.sh per terminal window
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    phone = os.getenv('TWILIO_PHONE_NUMBER')
    client = Client(account_sid, auth_token)

    # phone number should be as string
    message = client.messages.create(
    to=to_number, 
    from_=phone,
    body=body_content)

    print(message.sid)


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True, port = 5002)