""" Server for Job Track App """
from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db , User
import crud
# from flask_login import LoginManager
from jinja2 import StrictUndefined
from datetime import datetime

app = Flask(__name__)
# login = LoginManager(app)
app.secret_key = "job_track_app"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """Show homepage"""

    return render_template('homepage.html')


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
        session['new_user_id'] = new_user.user_id
        session['first_name'] = new_user.fname
        session['email'] = new_user.email

        return render_template('view.html')


@app.route('/view')
def view_page():
    """Show view page"""  

    view_job_app = request.args.get('view-job-application')
    if view_job_app:
        return redirect('/view-job-application')
    else:
        return render_template('create-job-application.html')


@app.route('/view-job-application')
def job_application():
    """View All Job Application of a user """

    user = crud.get_user_by_email(session['email'])
    user_id = user.user_id
    job_detail = crud.get_user_job_detail(user_id)
    dictionary_jobs = {}
    for index,job in enumerate(job_detail): 
        dictionary_jobs[index] = {}
        dictionary_jobs[index]['company_name'] = job.company_name,
        dictionary_jobs[index]['job_title'] = job.job_title,
        dictionary_jobs[index]['application_deadline'] = job.application_deadline,
        dictionary_jobs[index]['job_listing_url'] = job.job_listing_url ,
        dictionary_jobs[index]['state'] = job.state,
        dictionary_jobs[index]['app_state'] = crud.get_application_state_by_applied(job.job_completed_applications[0].job_applied_id).application_state
        # job_description['app_state'] = job.job_completed_applications[0].job_application_progress[-1].application_state

    return render_template('view-job-application.html', dictionary_jobs=dictionary_jobs)


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
    listing_date = request.form.get('listing_date')
    salary = request.form.get('salary')
    application_state = request.form.get('application_state')
    state = request.form.get('state')
    city = request.form.get('city')
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

    note = crud.create_note(job_applied_id, user_id, note_title, note_text, note_date_created)

    created_at = datetime.now()

    application_progress = crud.create_application_progress(application_state, job_applied_id , created_at)

    return redirect('/view-job-application')
    
    # else:
    #     return render_template('create-job-application.html')


@app.route('/render-create-job-application-form')
def render_create_job():
    
    return render_template('create-job-application.html')


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True, port = 5002)