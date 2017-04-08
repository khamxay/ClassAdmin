from base64 import b64encode
import os
import classadmin
import unittest
import tempfile
import sample_data
import config
import json

mock_student_1 = {
	"fee" : 6000,
	"name" : "Mycroft Holmes",
	"grade" : "6th",
	"batch" : "B-2",
	"installments" : [
		{
			"date" : "2nd March 2017",
			"fee_paid" : 3000
		},
		{
			"date" : "2nd Feb 2017",
			"fee_paid" : 3000
		}
	],
	"roll_no" : 601
}

class ClassadminTestCase(unittest.TestCase):

	def setUp(self):
		config.mongo_config.MONGO_URI = 'mongodb://localhost:27017/classadmin_test'
		config.mongo_config.MONGO_DBNAME = 'classadmin_test'
		classadmin.app.config['TESTING'] = True
		sample_data.add_data()
		self.app = classadmin.app.test_client()

	def login(self):
		b_auth_token = "Basic " + b64encode(sample_data.sample_user_1["username"] + ":" + sample_data.sample_user_1["password"])
		headers = {"Authorization": b_auth_token}
		rv = self.app.post("/classadmin/api/login", headers = headers)
		rv = json.loads(rv.get_data())
		return rv["token"]

	def test_get_students(self):
		token = self.login()
		headers = {"Authorization": "Bearer " + token}
		rv = self.app.get("/classadmin/api/students", headers = headers)
		data = rv.get_data()
		assert "Sherlock Holmes" in data
		assert "James Moriarty" in data
		assert "John Watson" in data

	# Test case to GET a single student

	def test_add_student(self):
		token = self.login()
		headers = {"Authorization": "Bearer " + token}
		rv = self.app.post("/classadmin/api/students", data = json.dumps(mock_student_1), headers = headers, content_type='application/json')
		assert rv.status_code == 201
		rv = self.app.get("/classadmin/api/students", headers = headers).get_data()
		assert mock_student_1["name"] in rv

	def test_delete_student(self):
		token = self.login()
		headers = {"Authorization": "Bearer " + token}
		rv = self.app.get("/classadmin/api/students/801", headers = headers)
		data = rv.get_data()
		assert "Sherlock Holmes" in data
		rv = self.app.delete("/classadmin/api/students/801", headers = headers)
		assert rv.status_code == 200
		rv = self.app.get("/classadmin/api/students", headers = headers)
		data = rv.get_data()
		assert "Sherlock Holmes" not in data

	def test_update_student(self):
		token = self.login()
		headers = {"Authorization": "Bearer " + token}
		rv = self.app.get("/classadmin/api/students/801", headers = headers)
		data = rv.get_data()
		assert "Sherlock Holmes" in data
		assert "8th" in data
		assert "B-1" in data
		data = json.loads(data)
		data["name"] = "Mycroft Holmes"
		data["grade"] = "100th"
		data["batch"] = "B-99"
		rv = self.app.put("/classadmin/api/students/801", data = json.dumps(data), headers = headers, content_type = 'application/json')
		data = rv.get_data()
		assert "Mycroft Holmes" in data
		assert "Sherlock Holmes" not in data
		assert "100th" in data
		assert "8th" not in data
		assert "B-1" not in data
		assert "B-99" in data


	def tearDown(self):
		sample_data.delete_data()

if __name__ == '__main__':
	unittest.main()