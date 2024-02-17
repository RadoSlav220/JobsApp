from flask import Request, Response, redirect, render_template, make_response, request, url_for
from enums.user_type import UserType
from exceptions.UnauthorisedOperationError import UnauthorisedOperationError
from exceptions.UserNotFoundError import UserNotFoundError
from helper_functions import consistent_hash
from setup import Application, Job, User, app, db
from globals import LOGGED_USER
from validators.job_validators import validate_job_elements
from validators.user_validators import validate_password, validate_user_elements, validate_username

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET' and LOGGED_USER:
        return make_response("You must logout first.", 400)
    elif request.method == 'GET':
        return make_response(render_template('login.html', title='Login'))
    elif request.method == 'POST':
        try:
            login_user(request)
            return redirect(url_for('home'))
        except ValueError as error:
            return make_response(render_template('login.html', title='Login', message=str(error)), 400)
        except UserNotFoundError as error:
            return make_response(render_template('login.html', title='Login', message=str(error)), 404)


@app.route("/logout", methods=['GET'])
def logout():
    global LOGGED_USER
    if LOGGED_USER:
        LOGGED_USER = None
        return redirect(url_for('home'))
    else:
        return make_response("You are not logged in.", 400)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET' and LOGGED_USER:
        return make_response("You must logout first.", 400)
    
    if request.method == 'GET':
        return make_response(render_template('register.html', title='Register'))
    elif request.method == 'POST':
        try:
            register_user(request)
            return make_response(render_template('register.html', title='Register', message='Registered successfully!'))
        except ValueError as error:
            return make_response(render_template('register.html', title='Register', message=str(error)), 400)


def login_user(request: Request) -> User:
    global LOGGED_USER 
    requestUsername = request.form.get('username')
    requestPassword = request.form.get('password')

    validate_username(requestUsername)
    validate_password(requestPassword)
    
    user = User.query.filter_by(username=requestUsername, password=consistent_hash(requestPassword)).first()
    if user:
        LOGGED_USER = user
        return user
    else:
        raise UserNotFoundError('Wrong username or password')


def is_user_registered(username):
    return User.query.filter_by(username=username).first()


def register_user(request: Request):
    requestName = request.form.get('name')
    requestUsername = request.form.get('username')
    requestPassword = request.form.get('password')
    requestEmail = request.form.get('email')
    requestUserType = request.form.get('user_type')

    validate_user_elements(requestName, requestUsername, requestPassword, requestEmail, requestUserType)

    if is_user_registered(requestUsername):
        raise ValueError("Username is already taken")

    new_user = User(name=requestName, username=requestUsername, password=consistent_hash(requestPassword), 
                    email=requestEmail, user_type=UserType(requestUserType))
    db.session.add(new_user)
    db.session.commit()



########################################################################################################################


@app.route('/apply/<job_id>', methods=['POST'])
def apply(job_id):
    if not LOGGED_USER or LOGGED_USER.user_type == UserType.RECRUITER:
        return make_response('You are not logged as applicant. You cannot apply to a job.', 403)
    
    if has_already_applied(LOGGED_USER.id, job_id):
        return make_response('You have already applied for this job', 400)
    
    new_application = Application(applicant_id = LOGGED_USER.id, job_id=job_id)
    db.session.add(new_application)
    db.session.commit()
    return make_response('Successfully applied for this job', 200)


@app.route('/createJobPage', methods=['GET'])
def create_job_page():
    if LOGGED_USER and LOGGED_USER.user_type == UserType.RECRUITER:
        return make_response(render_template('create_job.html', title='Create Job', user=LOGGED_USER))
    else:
        return make_response('You are not logged as a Recruiter. You cannot create Jobs.', 400)


@app.route("/jobs", methods=['GET', 'POST'])
def jobs():
    if request.method == 'GET':
        jobs = get_jobs(LOGGED_USER)
        return make_response(render_template('jobs.html', title='Jobs', user=LOGGED_USER, jobs=jobs)) 
    elif request.method == 'POST':
        try:
            job = postJob(LOGGED_USER, request)
            return make_response(render_template('create_job.html', title='Create Job', user=LOGGED_USER, message=f'Job ({job.title}) created successfully'))
        except UnauthorisedOperationError as error:
            return make_response(str(error), 401)
        except ValueError as error:
            return make_response(str(error), 400)


@app.route('/delete_job/<job_id>', methods=['POST'])
def delete_job(job_id):
    delete_job_by_id(job_id)
    return redirect(url_for('jobs'))


@app.route("/jobs/<job_id>", methods=['GET', 'DELETE'])
def job_action(job_id):
    if LOGGED_USER is None:
        return make_response('You must log first.', 401)

    if LOGGED_USER and request.method == 'GET':
        return display_job_for_user(LOGGED_USER, job_id)
    elif LOGGED_USER.user_type == UserType.RECRUITER and request.method == 'DELETE':
        delete_job_by_id(job_id)
        return make_response('Successfully deleted', 200)
    else:
        return make_response('Bad request', 400)


def has_already_applied(applicant_id, job_id) -> bool:
    return Application.query.filter_by(applicant_id=applicant_id, job_id=job_id).first() is not None


def postJob(user: User, request: Request) -> Job:
    if user is None or user.user_type != UserType.RECRUITER:
        raise UnauthorisedOperationError('You are not logged as a Recruiter. You cannot create Jobs.')

    job_title = request.form.get('title')
    job_company_name = request.form.get('company_name')
    job_desription = request.form.get('description')
    job_salary_lower = request.form.get('salary_lower_bound')
    job_salary_upper = request.form.get('salary_upper_bound')

    validate_job_elements(job_title, job_company_name, job_desription, job_salary_lower, job_salary_upper)

    new_job = Job(title=job_title, company_name=job_company_name, recruiter_id=user.id, description=job_desription, 
                  salary_lower_bound=job_salary_lower, salary_upper_bound=job_salary_upper)
    db.session.add(new_job)
    db.session.commit()
    return new_job


def get_jobs(user: User) -> list[Job]:
    if user.user_type == UserType.RECRUITER:
        jobs = Job.query.filter_by(recruiter_id=user.id).all()
    elif user.user_type == UserType.APPLICANT:
        jobs = Job.query.all()
    return jobs


def delete_job_by_id(job_id):
    job = Job.query.get_or_404(job_id)
    Application.query.filter_by(job_id=job_id).delete()
    db.session.delete(job)
    db.session.commit()


def display_job_for_user(user: User, job_id) -> Response:
    job = Job.query.get_or_404(job_id)
    if user.user_type == UserType.APPLICANT:
        recruiter_data = db.session.query(User.name, User.email).join(Job, Job.recruiter_id==User.id)\
                                    .filter_by(recruiter_id=job_id).first()
        return make_response(render_template('job_info.html', title='Job Details', user=user, job=job, recruiter_data=recruiter_data))
    elif user.user_type == UserType.RECRUITER:
        applications = db.session.query(User.name, User.email).join(Application, Application.applicant_id==User.id)\
                                    .join(Job, Job.id==Application.job_id)\
                                    .filter_by(recruiter_id=user.id, id=job_id).all()
        return make_response(render_template('job_info.html', title='Job Details', user=user, job=job, applications=applications))




@app.route("/")
def home():
    if LOGGED_USER:
        return make_response(render_template('index.html', title='Home', user=LOGGED_USER))
    else:
        return make_response(render_template('index.html', title='Home', message='Login first!'))


@app.route("/magic")
def read_data():
    users = User.query.all()
    result = ''
    
    for user in users:
        result += f'<h3>{user.id} {user.name} {user.username} {user.password} {user.email} {user.user_type}</h3>'
    
    result += '<br>'
    jobs = Job.query.all()
    for job in jobs:
        result += f'<h3>{job.id} {job.title} {job.company_name} {job.recruiter_id} {job.description} {job.salary_lower_bound} {job.salary_upper_bound}</h3>'
    
    result += '<br>'
    applications = Application.query.all()
    for application in applications:
        result += f'<h3>{application.id} {application.applicant_id} {application.job_id}</h3>'
  
    return result


if __name__ == "__main__":
    app.run(debug=True)