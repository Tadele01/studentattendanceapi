# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 09:36:55 2019

@author: Tadele Y
"""

from DBcm import useDatabase, ConnectionError, CredentialsError
from flask import Flask, request, jsonify
from flask import copy_current_request_context
from threading import Thread
from time import sleep 
app = Flask(__name__)
app.config['dbconfig'] = {'host':'127.0.0.1', 'user':'root', 'database':'android',}


@app.route('/')
def index():
    return "hello world"

@app.route('/stddb/student', methods=['GET'])
def get_all_student():
    with useDatabase(app.config['dbconfig']) as cursor :
        _SQL = '''select first_name, last_name, course, section, department, password from student '''
        cursor.execute(_SQL)
        contents = cursor.fetchall()  
    return jsonify(contents)

@app.route('/stddb/student/<course>', methods= ['GET'])
def get_student(course):
    with useDatabase(app.config['dbconfig']) as cursor :
        _SQL = '''select first_name, last_name from student where course = %s '''
        cursor.execute(_SQL, (course,))
        contents = cursor.fetchall()
    return jsonify(contents)

@app.route('/stddb/student/<id>', methods= ['GET'])
def get_student_by_course(id):
    with useDatabase(app.config['dbconfig']) as cursor :
        _SQL = '''select first_name, last_name, course, section, department from student where id = %s '''
        cursor.execute(_SQL, (id,))
        contents = cursor.fetchall()
    return jsonify(contents)


@app.route('/stddb/student/<id>',methods=['PUT'])
def update_std(id): 
    with useDatabase(app.config['dbconfig']) as cursor :
        if 'first_name' in request.json:
            _SQL = '''update student set first_name = %s where id = %s '''
            cursor.execute(_SQL, (request.json['first_name'],id))
        if 'last_name' in request.json:
            _SQL = '''update student set last_name = %s where id = %s '''
            cursor.execute(_SQL, (request.json['last_name'],id))
        if 'section' in request.json:
            _SQL = '''update student set section = %s where id = %s '''
            cursor.execute(_SQL, (request.json['section'],id))
        if 'department' in request.json:
            _SQL = '''update student set department = %s where id = %s '''
            cursor.execute(_SQL, (request.json['first_name'],id))
        if 'course' in request.json:
            _SQL = '''update student set course = %s where id = %s '''
            cursor.execute(_SQL, (request.json['course'],id))
        _SQL = '''select first_name, last_name, course, section, department from student where id = %s '''
        cursor.execute(_SQL, (id,))
        contents = cursor.fetchall() 
    return jsonify(contents)
@app.route('/stddb/student',methods=['POST'])
def create_student():
    with useDatabase(app.config['dbconfig']) as cursor :
        _SQL = '''insert into student (first_name, last_name, course, section, department, password) values (%s,%s,%s,%s,%s,%s) '''
        cursor.execute(_SQL,(str(request.json['first_name']), str(request.json['last_name']), str(request.json['course']), str(request.json['section']), str(request.json['department']), str(request.json['password'] )))
        studentDBR = '''select first_name, last_name, course, section, department, password from student '''
        cursor.execute(studentDBR)
        contents = cursor.fetchall()  
    return jsonify(contents)
    


@app.route('/stddb/student/<id>',methods=['DELETE'])
def delete_student(id): 
    with useDatabase(app.config['dbconfig']) as cursor :
        _SQL = '''delete from student where id = %s '''
        cursor.execute(_SQL,(id,))
    return jsonify({'response':'Success'})

'''
operations for taking attendace
'''
@app.route('/stddb/attendance', methods=['POST'])
def add_attend_student():
    with useDatabase(app.config['dbconfig']) as cursor :
        _SQL = '''insert into attendance (first_name,last_name, status, date) values (%s,%s,%s,%s) '''
        cursor.execute(_SQL,(str(request.json['first_name']), str(request.json['last_name']), request.json['status'], str(request.json['date'])))
        _SQL = '''select first_name, last_name, status, date from attendance '''
        cursor.execute(_SQL)
        contents = cursor.fetchall()  
    return jsonify(contents)

@app.route('/stddb/attendance', methods=['GET'])
def get_attendance():
    with useDatabase(app.config['dbconfig']) as cursor :
        _SQL = '''select first_name, last_name, status, date from attendance '''
        cursor.execute(_SQL)
        contents = cursor.fetchall()  
    return jsonify(contents)

'''
Operations for teachers
'''
@app.route('/stddb/teacher', methods=['GET'])
def get_teacher():
    with useDatabase(app.config['dbconfig']) as cursor :
        _SQL = '''select name, course from teacher '''
        cursor.execute(_SQL)
        contents = cursor.fetchall()  
    return jsonify(contents)

@app.route('/stddb/teacher', methods=['POST'])
def add_teacher():
    with useDatabase(app.config['dbconfig']) as cursor :
        _SQL = '''insert into teacher (name,password, course) values (%s,%s,%s) '''
        cursor.execute(_SQL,(str(request.json['name']), str(request.json['password']), str(request.json['course'])))
        _SQL = '''select name, course from teacher '''
        cursor.execute(_SQL)
        contents = cursor.fetchall()  
    return jsonify(contents)

@app.route('/stddb/teacher/login', methods=['POST'])
def login_teacher():
    with useDatabase(app.config['dbconfig']) as cursor :
        _SQL = '''select name from  teacher where (name = %s and password = %s) '''
        cursor.execute(_SQL,(str(request.json['name']), str(request.json['password'])))
        contents = cursor.fetchall()  
    return jsonify(contents)

if __name__ == '__main__':
    app.run(debug=True)


