from pymongo import MongoClient
from config.mongo_config import MONGO_URI, MONGO_DBNAME
import sys

sample_student_1 = {
	"fee" : 7000,
	"name" : "John Watson",
	"grade" : "7th",
	"batch" : "B-1",
	"installments" : [
		{
			"date" : "23rd March 2017",
			"fee_paid" : 3000
		},
		{
			"date" : "2nd Feb 2017",
			"fee_paid" : 4000
		}
	],
	"roll_no" : 701
}

sample_student_2 = {
	"fee" : 7000,
	"name" : "Sherlock Holmes",
	"grade" : "8th",
	"batch" : "B-1",
	"installments" : [ ],
	"roll_no" : 801
}

sample_student_3 = {
	"fee" : 10000,
	"name" : "James Moriarty",
	"grade" : "10th",
	"batch" : "B-2",
	"installments" : [
		{
			"date" : "21st December 2016",
			"fee_paid" : 3000
		},
		{
			"date" : "14th December 2016",
			"fee_paid" : 4000
		},
		{
			"date" : "3rd November 2016",
			"fee_paid" : 2000
		}
	],
	"roll_no" : 901
}


sample_user_1 = {
	"username" : "sample_user",
	"name" : "John Smith",
	"email" : "john_smith@example.com",
	"password" : "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"
}

def setup_db_connection():
	client = MongoClient(MONGO_URI)
	db = client[MONGO_DBNAME]
	return db

def add_data():
	db = setup_db_connection()
	db.students.insert_one(sample_student_1)
	db.students.insert_one(sample_student_2)
	db.students.insert_one(sample_student_3)
	db.users.insert_one(sample_user_1)
	print "Sample records added successfully!"

def delete_data():
	db = setup_db_connection()
	db.students.remove({})
	db.users.remove({})
	print "Database cleared!"

def print_usage():
	print "Usage: sample_data.py [ add | delete ]"	

def main():
	if len(sys.argv) != 2:
		print_usage()
	else:
		if sys.argv[1] == "add":
			add_data()
		elif sys.argv[1] == "delete":
			delete_data()
		else:
			print "Unknown command line option provided!"
			print_usage()

if __name__ == '__main__':
	main()
