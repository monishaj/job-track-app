from model import db, User, ApplicationState, Location, JobTitle, JobDetail, JobCompletedApplication, Note, connect_to_db, ApplicationProgress

def create_user(fname, lname, email, password, phone_number):
    """Create and return a new user"""
    user = User(fname = fname, lname = lname , email = email ,password = password, phone_number = phone_number)
    #setting password hash
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return user


def get_users():
    """Return all users."""

    return User.query.all()


def get_user_by_id(user_id):
    """Return a user by primary key."""

    return User.query.get(user_id)

def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()

def create_application_state(state_name):
    """Create and return Application State """
    app_state = ApplicationState(state_name = state_name)
    db.session.add(app_state)
    db.session.commit()

    return app_state

def get_application_state():
    """Return all application state."""

    return ApplicationState.query.all()


def get_application_state_by_id(application_state_id):
    """Return a application state by primary key."""

    return ApplicationState.query.get(application_state_id)


def create_location(state, city):
    """Create and return location """
    location = Location(state = state , city = city)
    db.session.add(location)
    db.session.commit()

    return location

def get_location():
    """Return all location."""

    return Location.query.all()


def get_location_by_id(location_id):
    """Return a location by primary key."""

    return Location.query.get(location_id)    

def create_job_title(job_title):
    """Create and return Job Title """
    job_role = JobTitle(job_title = job_title)
    db.session.add(job_role)
    db.session.commit()

    return job_role

def get_job_title():
    """Return all job title."""

    return JobTitle.query.all()


def get_job_title_by_id(job_title_id):
    """Return a job title by primary key."""

    return JobTitle.query.get(job_title_id)    


def create_job_detail(company_name, job_title_id, application_deadline, job_listing_url, application_state_id, location_id, application_listed, salary):
    """Create and return Job Details """
    job_detail = JobDetail(company_name = company_name, job_title_id = job_title_id, application_deadline = application_deadline, job_listing_url = job_listing_url, application_state_id = application_state_id, location_id = location_id, application_listed = application_listed, salary = salary)
    db.session.add(job_detail)
    db.session.commit()

    return job_detail

def get_job_detail():
    """Return all job detail."""

    return JobDetail.query.all()


def get_job_detail_by_id(job_detail_id):
    """Return a job detail by primary key."""

    return JobDetail.query.get(job_detail_id)


def create_job_applied(user_id, job_id, application_date_submitted):
    """Create and return job application completed """
    job_applied = JobCompletedApplication( user_id = user_id, job_id = job_id, application_date_submitted = application_date_submitted)
    db.session.add(job_applied)
    db.session.commit()

    return job_applied

def get_job_applied():
    """Return all job applied."""

    return JobCompletedApplication.query.all()


def get_job_applied_by_id(job_applied_id):
    """Return a job applied by primary key."""

    return JobCompletedApplication.query.get(job_applied_id)



def create_note(job_applied_id, user_id, note_title, note_text, note_date_created):
    """create and return note """
    note = Note(job_applied_id =job_applied_id, user_id = user_id , note_title = note_title , note_text = note_text, note_date_created = note_date_created)
    db.session.add(note)
    db.session.commit()

    return note 

def get_note():
    """Return all note created."""

    return Note.query.all()


def get_note_by_id(note_id):
    """Return a note by primary key."""

    return Note.query.get(note_id)

def create_application_progress(application_state_id, job_applied_id , created_at):
    """create and return Application Progress """
    app_progress = ApplicationProgress(application_state_id = application_state_id, job_applied_id = job_applied_id, created_at = created_at)
    db.session.add(app_progress)
    db.session.commit()

    return app_progress 

def get_application_progress():
    """Return all Application Progress created."""

    return ApplicationProgress.query.all()


def get_application_progress_by_id(app_progress_id):
    """Return a Application Progress by primary key."""

    return ApplicationProgress.query.get(app_progress_id)

# def get_user_job_detail(user_id):
#     JobDetail.



######
# def function (monisha userid= 5)

# current_users_applied_jobs = JobCompletedApplication.query.filter(JobCompletedApplication.userId == monisha_userid).all() --> return list of monisha's job application

# in jinja,forloop or iterate through this list (current_users_applied_jobs)
# job.job_completed_user.fname --> firstname
# job.job_completed_detail.company_name 



if __name__ == '__main__':
    from server import app
    connect_to_db(app)