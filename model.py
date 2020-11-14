from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()
class User(db.Model):
    """A user."""
    __tablename__ = 'users'

    user_id = db.Column(db.Integer,
                        primary_key = True, 
                        autoincrement = True)

    fname = db.Column(db.String(50),nullable=False)
    lname = db.Column(db.String(50))
    email = db.Column(db.Text, unique = True,nullable=False)
    password = db.Column(db.String(200),nullable=False)
    phone_number = db.Column(db.BigInteger ,nullable=False)
    # to set any default parameters put default = xyz

    user_notes = db.relationship("Note")
    user_job_completed_applications = db.relationship("JobCompletedApplication")


    def set_password(self, password):
        self.password = generate_password_hash(password)


    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User user_id = {self.user_id} || email = {self.email} || Name = {self.fname} {self.lname}>'

class JobDetail(db.Model):
    """ Job Application Details"""
    __tablename__ = 'job_details'

    job_id = db.Column(db.Integer,
                        primary_key = True, 
                        autoincrement = True)
    company_name = db.Column(db.String(50),nullable=False)
    job_title = db.Column(db.String,nullable=False)
    application_deadline = db.Column(db.DateTime)
    job_listing_url = db.Column(db.Text)
    state = db.Column(db.String,nullable=False)
    city = db.Column(db.String)
    application_listed = db.Column(db.DateTime)
    salary = db.Column(db.String(25))

    job_completed_applications = db.relationship("JobCompletedApplication")

    def __repr__(self):
        return f'<JobDetail job_id = {self.job_id} || company_name = {self.company_name} || job_title = {self.job_title} >'


class Note(db.Model):
    """ Job Application Notes"""
    __tablename__ = 'notes'

    note_id = db.Column(db.Integer,
                        primary_key = True, 
                        autoincrement = True)
    job_applied_id = db.Column(db.Integer , db.ForeignKey('job_completed_applications.job_applied_id'))
    user_id = db.Column(db.Integer,db.ForeignKey('users.user_id'))
    note_title = db.Column(db.String(100))
    note_text = db.Column(db.Text)
    note_date_created = db.Column(db.DateTime)

    note_job_completed_application = db.relationship("JobCompletedApplication")
    note_user = db.relationship("User")

    def __repr__(self):
        return f'< Notes notes_id = {self.note_id}|| User user_id = {self.user_id} || job_applied_id = {self.job_applied_id} || notes_title = {self.note_title} || notes_text = {self.note_text} >'


class JobCompletedApplication(db.Model):
    """ Job Application Completed Details"""
    __tablename__ = 'job_completed_applications'

    job_applied_id = db.Column(db.Integer,
                        primary_key = True, 
                        autoincrement = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    job_id = db.Column(db.Integer,db.ForeignKey('job_details.job_id') ,unique = True)
    application_date_submitted = db.Column(db.DateTime ,nullable=False)

    job_completed_notes = db.relationship("Note")

    job_completed_user = db.relationship("User")
    job_completed_detail = db.relationship("JobDetail")
    job_application_progress = db.relationship("ApplicationProgress")

    def __repr__(self):
        return f'<JobCompletedApplication job_applied_id = {self.job_applied_id}|| user_id = {self.user_id} || job_id = {self.job_id} ||application_date_submitted = {self.application_date_submitted} >'


class ApplicationProgress(db.Model):
    """ Job Application state progress"""

    __tablename__ = 'application_progress'
    app_progress_id = db.Column(db.Integer,
                        primary_key = True, 
                        autoincrement = True)
    application_state = db.Column(db.String)
    job_applied_id = db.Column(db.Integer , db.ForeignKey('job_completed_applications.job_applied_id'))
    created_at = db.Column(db.DateTime)

    progress_job_completed_application = db.relationship("JobCompletedApplication")

    def __repr__(self):
        return f'<ApplicationProgress app_progress_id = {self.app_progress_id} || application_state= {self.application_state} || job_applied_id = {self.job_applied_id} ||created_at = {self.created_at} >'


def connect_to_db(app, db_uri='postgresql:///job-track-app', echo=True):
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_ECHO'] = echo
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = app
    db.init_app(app)

    print('Connected to the db!')


if __name__ == '__main__':
    from server import app

    # Call connect_to_db(app, echo=False) if program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
    db.create_all()