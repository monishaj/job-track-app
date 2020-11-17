from model import db, User, JobDetail, JobCompletedApplication, Note, connect_to_db, ApplicationProgress


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


def create_job_detail(company_name, job_title, application_deadline, job_listing_url, state, city, application_listed, salary):
    """Create and return Job Details """

    job_detail = JobDetail(company_name = company_name, job_title = job_title, application_deadline = application_deadline, job_listing_url = job_listing_url, state = state , city = city, application_listed = application_listed, salary = salary)
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

def get_job_applied_by_job_id(job_id):
    """Return a job applied by job id."""

    return JobCompletedApplication.query.filter(JobCompletedApplication.job_id == job_id).first().job_applied_id


def create_note(job_applied_id, user_id, note_title, note_text, note_date_created):
    """create and return note """

    note = Note(job_applied_id =job_applied_id, user_id = user_id , note_title = note_title , note_text = note_text, note_date_created = note_date_created)
    db.session.add(note)
    db.session.commit()

    return note 


def get_note():
    """Return all note created."""

    return Note.query.all()


def all_note_by_job_applied_id(job_applied_id):
    """Return all notes for job applied id."""

    return Note.query.filter(Note.job_applied_id == job_applied_id).all()


def create_application_progress(application_state, job_applied_id , created_at):
    """create and return Application Progress """
    app_progress = ApplicationProgress(application_state = application_state, job_applied_id = job_applied_id, created_at = created_at)
    db.session.add(app_progress)
    db.session.commit()

    return app_progress 


def get_application_progress():
    """Return all Application Progress created."""

    return ApplicationProgress.query.all()


def get_application_progress_by_id(app_progress_id):
    """Return a Application Progress by primary key."""

    return ApplicationProgress.query.get(app_progress_id)


def get_user_job_detail(user_id):
    """ get a list of all the jobs a user applied"""

    return JobDetail.query.filter(JobCompletedApplication.user_id == user_id).join(JobCompletedApplication).all()


def update_application_progress_state(job_applied_id):
    """ Update the created_at and application state of Application progress table once the user updates"""
    pass

def update_job_detail(job_id):
    """ Update the application state in the job details table once the user updates"""
    pass


def get_application_state_by_applied(job_applied_id):
    """ Return the latest application state object """

    return ApplicationProgress.query.filter(JobCompletedApplication.job_applied_id == job_applied_id).join(JobCompletedApplication).order_by(ApplicationProgress.app_progress_id.desc()).first()


def get_last_job_id():
    """Get the last job_id record"""

    return JobDetail.query.with_entities(JobDetail.job_id).order_by(JobDetail.job_id.desc()).first()[0]


def get_last_job_applied_id():
    """Get the last job applied id record"""

    return JobCompletedApplication.query.with_entities(JobCompletedApplication.job_applied_id).order_by(JobCompletedApplication.job_applied_id.desc()).first()[0]


if __name__ == '__main__':
    from server import app
    connect_to_db(app)