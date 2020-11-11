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
    job_title_id = db.Column(db.Integer, db.ForeignKey('job_titles.job_title_id'),nullable=False)
    application_deadline = db.Column(db.DateTime)
    job_listing_url = db.Column(db.Text)
    application_state_id = db.Column(db.Integer,db.ForeignKey('application_states.application_state_id') )
    location_id = db.Column(db.Integer, db.ForeignKey('locations.location_id'))
    application_listed = db.Column(db.DateTime)
    salary = db.Column(db.String(25))


    job_completed_applications = db.relationship("JobCompletedApplication")

    job_title = db.relationship("JobTitle")
    application_state =db.relationship("ApplicationState")
    location = db.relationship("Location")


    def __repr__(self):
        return f'<JobDetail job_id = {self.job_id} || company_name = {self.company_name} || job_title_id = {self.job_title_id} >'



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


    def __repr__(self):
        return f'<JobCompletedApplication job_applied_id = {self.job_applied_id}|| user_id = {self.user_id} || job_id = {self.job_id} ||application_date_submitted = {self.application_date_submitted} >'

    

class ApplicationState(db.Model):
    """ Job Application Status """
    __tablename__ = 'application_states'

    application_state_id = db.Column(db.Integer,
                        primary_key = True, 
                        autoincrement = True)
    state_name = db.Column(db.String(25), unique = True)

    app_state_job_details = db.relationship("JobDetail")                    



    def __repr__(self):
        return f'<ApplicationState application_state_id = {self.application_state_id} state_name = {self.state_name}>'



class JobTitle(db.Model):
    """ Job Application Positions"""
    __tablename__ = 'job_titles'

    job_title_id = db.Column(db.Integer,
                        primary_key = True, 
                        autoincrement = True)
    job_title = db.Column(db.String(100))

    position_job_details = db.relationship("JobDetail")


    def __repr__(self):
        return f'<JobPosition job_title_id = {self.job_title_id} job_title = {self.job_title}>'



class Location(db.Model):
    """ Job Application Location"""
    __tablename__ = 'locations'

    location_id = db.Column(db.Integer,
                        primary_key = True, 
                        autoincrement = True)
    state = db.Column(db.String(100),unique = True ,nullable=False)
    city = db.Column(db.String(100),unique = True)

    location_job_details = db.relationship("JobDetail")


    def __repr__(self):
        return f'<Location location_id = {self.location_id} || state = {self.state} || city = {self.city} >'

class ApplicationProgress(db.Model):
    """ Job Application state progress"""

    __tablename__ = 'application_progress'
    app_progress_id = db.Column(db.Integer,
                        primary_key = True, 
                        autoincrement = True)
    application_state_id = db.Column(db.Integer,db.ForeignKey('application_states.application_state_id') )
    job_applied_id = db.Column(db.Integer , db.ForeignKey('job_completed_applications.job_applied_id'))
    created_at = db.Column(db.DateTime)

    application_state_progress =db.relationship("ApplicationState")
    progress_job_completed_application = db.relationship("JobCompletedApplication")



# class JobDescription(db.Model):
#     """ Job Description Details"""
#     __tablename__ = 'job_descriptions'

#     job_description_id = db.Column(db.Integer,
#                         primary_key = True, 
#                         autoincrement = True)
#     job_applied_id = db.Column(db.Integer)
#     user_id = db.Column(db.Integer)
#     job_description_text = db.Column(db.Text)


#     def __repr__(self):
#         return f'<JobDescription job_description_id = {self.job_description_id} || user_id = {self.user_id} ||job_applied_id = {self.job_applied_id} ||job_description_text = {self.job_description_text} >'


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