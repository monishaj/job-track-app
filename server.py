""" Server for Job Track App """
from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db , User
import crud
# from flask_login import LoginManager
from jinja2 import StrictUndefined

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
            flash('Sucessfully Logged In.')
            return render_template('view.html')
            

    else:
        new_user = crud.create_user(fname, lname, email, password, phone_number)
        flash('Account created! Logged In.')
        
        #saving the user to the session
        session['new_user_id'] = new_user.user_id
        session['first_name'] = new_user.fname

        return render_template('view.html')





# @app.route('/view')
    


@app.route('/view/view-job-application')
def job_application():
    """View All Job Application of a user """
    # user_id = crud.get_user_by_email(email).user_id
    pass


# @app.route('/view/create-job-application', methods=['POST'])
# def create_job_application():
#     """Create a job application """
#     render_template('view_job_application.html')



        








if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True, port = 5002)