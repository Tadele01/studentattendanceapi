
from flask import Flask, request, jsonify
app = Flask(__name__)
studentDB = [{'id':'1', 'name':'tade'},{'id':'2', 
             'name':'jo_the_tall'},{'id':'3', 'name':'tiny_jo'}]

@app.route('/')
def index():
    return "hello world"

@app.route('/stddb/student', methods=['GET'])
def get_all_student():
    return jsonify({'std': studentDB})

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
    dat = {
    'id' : request.json['id'], 
    'name' :  request.json['name']
    }
    studentDB.append(dat)
    return jsonify(dat)


@app.route('/stddb/student/<stdid>',methods=['DELETE'])
def delete_student(stdid): 
    std = [ std for std in studentDB if (std['id'] == stdid) ] 
    if len(std) == 0:
        return 'no element found to delete'
    studentDB.remove(std[0])
    return jsonify({'response':'Success'})

if __name__ == '__main__':
    app.run(debug=True)


