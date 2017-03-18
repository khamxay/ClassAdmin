from flask import Flask, request, jsonify, make_response, render_template, flash, redirect, g
from flask_httpauth import HTTPTokenAuth, HTTPBasicAuth

from mongo_config import setup_mongo_connection
from common.common_error_codes import *
from common.common_util import JSONEncode
from common import http_codes
from handlers import student_handler
from handlers import user_handler
from handlers import security_handler
from forms import LoginForm

project_name = "classadmin"

# Project initialization and configuration
app = Flask(__name__)
auth = HTTPTokenAuth('Bearer')
bauth = HTTPBasicAuth()

setup_mongo_connection(app)
app.config.from_object('config')
security_handler.initialize_token_serializer(app.config)


# User authentication related functions
@bauth.verify_password
def authenticate(username, password):
	user = security_handler.verify_credentials(username, password)
	g.username = user['username']
	return True

@auth.verify_token
def verify_token(token):
	g.user = None
	token_data = security_handler.validate_token(token)
	if 'username' in token_data:
		g.username = token_data['username']
		return True
	return False


# Initialize authentication related error handlers
@auth.error_handler
@bauth.error_handler
def unauthorized():
	return make_response(jsonify({'error': 'Unauthorized access'}), http_codes.HTTP_UNAUTHORIZED)


# Initialize rest of the error handlers
@app.errorhandler(NotFoundError)
@app.errorhandler(BadInputError)
@app.errorhandler(AlreadyExistsError)
@app.errorhandler(ServerSideError)
@app.errorhandler(BadCredentialsError)
@app.errorhandler(TokenExpiredError)
def handle_application_error(error):
	return make_response(jsonify({'error': error.error_message}), error.error_code)


#----- REST APIs---------------
# POST /classadmin/api/login
@app.route("/" + project_name + "/api/login", methods=["POST"])
@bauth.login_required
def api_login():
	token = security_handler.generate_token({'username': g.username})
	return jsonify({'token': token})

# GET /classadmin/api/students
@app.route("/" + project_name + "/api/students", methods=["GET"])
@auth.login_required
def read_students():
	students = student_handler.get_students(request.args)
	return JSONEncode.encode({"students:": students})


# GET /classadmin/api/students/<id>
@app.route("/" + project_name + "/api/students/<int:roll_no>", methods=["GET"])
@auth.login_required
def read_student(roll_no):
	student = student_handler.get_student(roll_no)
	return JSONEncode.encode({'student': student})


# POST /classadmin/api/students
@app.route("/" + project_name + "/api/students", methods=["POST"])
@auth.login_required
def create_student():
	student = student_handler.add_student(request.json)
	return JSONEncode.encode(student), http_codes.HTTP_CREATED


# PUT /classadmin/api/students/<id>
@app.route("/" + project_name + "/api/students/<int:roll_no>", methods=["PUT"])
@auth.login_required
def update_student(roll_no):
	student = student_handler.update_student(roll_no, request.json)
	return JSONEncode.encode({'student': student})


# DELETE /classadmin/api/students/<id>
@app.route("/" + project_name + "/api/students/<int:roll_no>", methods=["DELETE"])
@auth.login_required
def delete_student(roll_no):
	student_handler.delete_student(roll_no)
	return jsonify({'result': True})


# POST /classadmin/api/students/<id>/installments
@app.route("/" + project_name + "/api/students/<int:roll_no>/installments", methods=["POST"])
@auth.login_required
def create_installment(roll_no):
	student = student_handler.add_installment(roll_no, request.json)
	return JSONEncode.encode({'student': student})


# PUT /classadmin/api/students/<id>/installments/<id>
@app.route("/" + project_name + "/api/students/<int:roll_no>/installments/<int:installment_id>", methods=["PUT"])
@auth.login_required
def update_installment(roll_no, installment_id):
	student = student_handler.update_installment(roll_no, installment_id, request.json)
	return JSONEncode.encode({'student': student})


# DELETE /classadmin/api/students/<id>/installments/<id>
@app.route("/" + project_name + "/api/students/<int:roll_no>/installments/<int:installment_id>", methods=["DELETE"])
@auth.login_required
def delete_installment(roll_no, installment_id):
	student_handler.delete_installment(roll_no, installment_id)
	return jsonify({'result': True})


#----- WEB Interfaces (for debugging purposes) ------------

# http://<ip>:<port>/classadmin
@app.route("/" + project_name)
def index():
	students = student_handler.get_students({})
	return render_template('index.html', students = students)

'''# GET/POST /classadmin/login
@app.route("/" + project_name + "/login", methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		flash('Login requested for username="%s", password="%s", remember_me=%s' %
			  (form.username.data, form.password.data, str(form.remember_me.data)))
		return redirect('/classadmin')
	return render_template('login.html', title='Sign In', form=form)'''


if __name__ == "__main__":
	app.run(debug=app.config['DEBUG_MODE'])
