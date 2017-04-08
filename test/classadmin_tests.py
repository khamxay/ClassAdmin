import os
import classadmin
import unittest
import tempfile
import sample_data
import config

class ClassadminTestCase(unittest.TestCase):

    def setUp(self):
        config.mongo_config.MONGO_URI = 'mongodb://localhost:27017/classadmin_test'
        config.mongo_config.MONGO_DBNAME = 'classadmin_test'
        classadmin.app.config['TESTING'] = True
        sample_data.add_data()
        self.app = classadmin.app.test_client()
        #with classadmin.app.app_context():
        #    classadmin.setup_mongo_connection(self.app)

    def test_get_students(self):
        rv = self.app.get("/test")
        print(rv.get_data())

    def tearDown(self):
        sample_data.delete_data()
        #os.close(self.db_fd)
        #os.unlink(flaskr.app.config['DATABASE'])

if __name__ == '__main__':
    unittest.main()