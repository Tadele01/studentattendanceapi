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
studentDB = [{'id':'1', 'name':'tade'},{'id':'2', 
             'name':'jo_the_tall'},{'id':'3', 'name':'tiny_jo'}]
studentDBR = '''select first_name, last_name, course, section, department, password from student '''

@app.route('/')
def index():
    return "hello world"

@app.route('/stddb/student', methods=['GET'])
def get_all_student():
    with useDatabase(app.config['dbconfig']) as cursor :
        cursor.execute(studentDBR)
        contents = cursor.fetchall()  
    return jsonify(contents)

@app.route('/stddb/student/<stdid>', methods= ['GET'])
def get_student(stdid):
    std = [std for std in studentDB if (std['id'] == stdid)]
    return jsonify({'std': std})


@app.route('/stddb/student/<stdid>',methods=['PUT'])
def update_std(stdid): 
    std = [ std for std in studentDB if (std['id'] == stdid) ] 
    if 'name' in request.json : 
        std[0]['name'] = request.json['name'] 
    return jsonify({'std':std[0]})

@app.route('/stddb/student',methods=['POST'])
def create_student():
    with useDatabase(app.config['dbconfig']) as cursor :
        _SQL = '''insert into student (first_name, last_name, course, section, department, password) values (%s,%s,%s,%s,%s,%s) '''
        cursor.execute(_SQL,(str(request.json['first_name']), str(request.json['last_name']), str(request.json['course']), str(request.json['section']), str(request.json['department']), str(request.json['password'] )))
        studentDBR = '''select first_name, last_name, course, section, department, password from student '''
        cursor.execute(studentDBR)
        contents = cursor.fetchall()  
    return jsonify(contents)
    


@app.route('/stddb/student/<stdid>',methods=['DELETE'])
def delete_student(stdid): 
    std = [ std for std in studentDB if (std['id'] == stdid) ] 
    if len(std) == 0:
        return 'no element found to delete'
    studentDB.remove(std[0])
    return jsonify({'response':'Success'})

if __name__ == '__main__':
    app.run(debug=True)


