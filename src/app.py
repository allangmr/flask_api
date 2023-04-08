from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from config import config
from validations import *

app = Flask(__name__)
conn = MySQL(app)

@app.route('/courses', methods=['GET'])
def list_courses():
    try:
        cursor=conn.connection.cursor()
        sql = "SELECT id, name FROM courses"
        cursor.execute(sql)
        data = cursor.fetchall()
        courses = []
        for row in data:
            course={'id': row[0], 'name': row[1]}
            courses.append(course)
        return jsonify({'courses': courses, 'message': 'Listado de Materias'})
    except Exception as ex:
        return jsonify({'message': 'Error: No se encontraron materias'})
    
@app.route('/course/<id>', methods=['GET'])
def read_course(id):
    try:
        course = find_course(id)
        if course != None:
            return jsonify({'courses': course, 'message': 'Informacion de Materia'})
        else:
            return jsonify({'message': 'Materia no encontrada'})
    except Exception as ex:
        return jsonify({'message': 'Error: No se pudieron encontrar las materias por un error en el sistema.'})

@app.route('/courses', methods=['POST'])
def create_course():
    if(validate_course_name(request.json['name'])):
        try:
            duplicated = course_duplicated(request.json['name'])
            if duplicated != None:
                return jsonify({'message': 'La materia ya existe, no se puede duplicar.'})
            else:
                cursor=conn.connection.cursor()
                sql = """INSERT INTO courses (name) 
                VALUES ('{0}')""".format(request.json['name'])
                cursor.execute(sql)
                conn.connection.commit() #confirm action insert
                return jsonify({'message': 'Materia registrada'})
        except Exception as ex:
            return jsonify({'message': 'Error: No se pudo crear la materia.'})
    else:
        return jsonify({'message': "Parámetros inválidos..."})

@app.route('/course/<id>', methods=['DELETE'])
def delete_course(id):
    try:
        course = find_course(id)
        if course != None:
            cursor=conn.connection.cursor()
            sql = "DELETE FROM courses where id = {0}".format(id)
            cursor.execute(sql)
            conn.connection.commit() #confirm action delete
            return jsonify({'message': 'Materia eliminada'})
        else:
            return jsonify({'message': 'La Materia con ese codigo no existe, por lo cual no es posible eliminarlo.'})
    except Exception as ex:
        return jsonify({'message': 'Error: No se pudo eliminar la materia.'})
    
@app.route('/course/<id>', methods=['PUT'])
def update_course(id):
    if(validate_course_name(request.json['name'])):
        try:
            course = find_course(id)
            if course != None:
                cursor=conn.connection.cursor()
                sql = """UPDATE courses 
                SET name='{0}' WHERE id= {1}""".format(request.json['name'], id)
                cursor.execute(sql)
                conn.connection.commit() #confirm action update
                return jsonify({'message': 'Materia actualizada'})
            else:
                return jsonify({'message': 'No se puede actualizar los datos de la materia, ya que la misma no existe.'})
        except Exception as ex:
            return jsonify({'message': 'Error: No se pudo editar la materia.'})
    else:
        return jsonify({'message': "Parámetros inválidos..."})
    
def course_duplicated(name):
    try:
        cursor=conn.connection.cursor()
        sql = "SELECT id, name FROM courses where name = '{0}'".format(name)
        cursor.execute(sql)
        data = cursor.fetchone()
        if data != None:
            course={'id': data[0], 'name': data[1]}
            return course
        else:
            return None
    except Exception as ex:
        raise ex
    
def find_course(id):
    try:
        cursor=conn.connection.cursor()
        sql = "SELECT id, name FROM courses where id = '{0}'".format(id)
        cursor.execute(sql)
        data = cursor.fetchone()
        if data != None:
            course={'id': data[0], 'name': data[1]}
            return course
        else:
            return None
    except Exception as ex:
        raise ex
    
def page_not_found(error):
    return jsonify({'message': 'La ruta a la que desea acceder no existe'})

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, page_not_found)
    app.run()