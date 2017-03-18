from common_error_codes import *
import mongo_config

def get_students(qargs):
	filterr = {}
	if qargs.get('name'):
		nameregex = '.*' + qargs.get('name') + '.*'
		namefilter = {'name': {'$regex': nameregex}}
		filterr.update(namefilter)
	if qargs.get('grade'):
		gradefilter = {'grade': qargs.get('grade')}
		filterr.update(gradefilter)
	if qargs.get('batch'):
		batchfilter = {'batch': qargs.get('batch')}
		filterr.update(batchfilter)

	students = mongo_config.mongo.db.students.find(filterr)
	if students.count() == 0:
		raise NotFoundError("No student found for the given filter")
	output = []
	for s in students:
		output.append(s)
	return output


def get_student(roll_no):
	student = mongo_config.mongo.db.students.find_one({'roll_no': roll_no})
	if len(student) != 0:
		return student
	raise NotFoundError("Student with that roll number does not exist.")


def add_student(request):
	students = mongo_config.mongo.db.students.find({'roll_no': request["roll_no"]})
	if students.count() != 0:
		raise AlreadyExistsError("Student with that roll number is already present")
	student = {
		"roll_no": request["roll_no"],
		"name": request["name"],
		"grade": request["grade"],
		"batch": request["batch"],
		"fee": request["fee"],
		"installments": []
	}

	result = mongo_config.mongo.db.students.insert_one(student)
	if not result.inserted_id:
		raise ServerSideError("There was some error adding the student. Please try again.")
	return student


def update_student(roll_no, request):
	student = mongo_config.mongo.db.students.find_one({'roll_no': roll_no})
	if not student or len(student) == 0:
		raise NotFoundError("Student with that roll number not found.")

	if 'name' in request and type(request['name']) != unicode:
		raise BadInputError("Bad name")
	if 'grade' in request and type(request['grade']) is not unicode:
		raise BadInputError("Bad grade")
	if 'batch' in request and type(request['batch']) is not unicode:
		raise BadInputError("Bad batch")
	if 'fee' in request and type(request['fee']) is not int:
		raise BadInputError("Bad fee")

	new_student = {}
	new_student['name'] = request.get('name', student['name'])
	new_student['grade'] = request.get('grade', student['grade'])
	new_student['batch'] = request.get('batch', student['batch'])
	new_student['fee'] = request.get('fee', student['fee'])

	result = mongo_config.mongo.db.students.update_one(
		{"roll_no": roll_no},
		{
			"$set": new_student,
		})

	if result.matched_count == 1 and result.modified_count == 0:
		raise BadInputError("You did not change any information!")
	if result.modified_count != 1:
		raise ServerSideError("There was some error updating the student. Please try again.")

	student = mongo_config.mongo.db.students.find_one({'roll_no': roll_no})
	if not student or len(student) != 0:
		return student
	raise ServerSideError("Student successfully updated but can't display right now.")


def delete_student(roll_no):
	result = mongo_config.mongo.db.students.delete_one({'roll_no': roll_no})
	if result.deleted_count != 1:
		raise NotFoundError("Student with that roll number not found.")
	return True


def add_installment(roll_no, request):
	student = mongo_config.mongo.db.students.find_one({'roll_no': roll_no})
	if len(student) == 0:
		raise NotFoundError("Student with that roll number does not exist.")

	if len(student["installments"]) == 0:
		installment_id = 1
	else:
		installment_id = student["installments"][-1]["id"] + 1

	installment = {
		"id": installment_id,
		"date": request["date"],
		"fee_paid": request["fee_paid"]
	}
	student["installments"].append(installment)
	
	result = mongo_config.mongo.db.students.update_one(
	{"roll_no": roll_no},
	{
		"$set": student,
	})

	if result.matched_count != 1 or result.modified_count != 1:
		raise ServerSideError("There was some error adding the installment. Please try again.")

	return student


def update_installment(roll_no, installment_id, request):
	student = mongo_config.mongo.db.students.find_one({'roll_no': roll_no})
	if len(student) == 0:
		raise NotFoundError("Student with that roll number does not exist.")

	if len(student["installments"]) == 0:
		raise NotFoundError("No installments exist to edit.")

	installment = [installment for installment in student["installments"] if installment["id"] == installment_id]
	if len(installment) == 0:
		raise NotFoundError("Installment with that ID for the student not found.")

	installment = installment[0]

	if 'date' in request and type(request['date']) != unicode:
		raise BadInputError("Bad date provided.")
	if 'fee_paid' in request and type(request['fee_paid']) != int:
		raise BadInputError("Bad fee amount provided.")

	installment['date'] = request.get('date', installment['date'])
	installment['fee_paid'] = request.get('fee_paid', installment['fee_paid'])

	result = mongo_config.mongo.db.students.update_one(
	{"roll_no": roll_no},
	{
		"$set": student,
	})

	if result.matched_count != 1 or result.modified_count != 1:
		raise ServerSideError("There was some error updating the installment. Please try again.")

	return student


def delete_installment(roll_no, installment_id):
	student = mongo_config.mongo.db.students.find_one({'roll_no': roll_no})
	if len(student) == 0:
		raise NotFoundError("Student with that roll number does not exist.")

	if len(student["installments"]) == 0:
		raise NotFoundError("No installments exist to delete.")

	installment = [installment for installment in student["installments"] if installment["id"] == installment_id]
	if len(installment) == 0:
		raise NotFoundError("Installment with that ID for the student not found.")

	installment = installment[0]

	student["installments"].remove(installment)

	result = mongo_config.mongo.db.students.update_one(
	{"roll_no": roll_no},
	{
		"$set": student,
	})

	if result.matched_count != 1 or result.modified_count != 1:
		raise ServerSideError("There was some error deleting the installment. Please try again.")

	return True
