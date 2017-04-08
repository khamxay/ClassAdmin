from base64 import b64encode
import os
import classadmin
import unittest
import tempfile
import sample_data
import config
import json

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

    def tearDown(self):
        sample_data.delete_data()

if __name__ == '__main__':
    unittest.main()