from flask import Flask, request, Response # Se importan las librerías del framework para peticionoes y respuestas del servidor
from flask_pymongo import pymongo # Librería para la conexión con la base de datos MongoDB 
import hashlib # Librería para hacer un Hash de contraseñas en la base de datos al momento de crear una cuenta o iniciar sesión
import os # Librería para obtener variables de entorno de otros archivos
from  dotenv import load_dotenv # Librería para cargar las variables de entorno existentes
from flask.json import jsonify # Librería para convertir nuestras respuestas en un Json
from bson import json_util # Convierte los objetos de MongoDb en json para poder ser utilizados en una respuesta del servidor
from bson.objectid import ObjectId # Para poder utilizar los objetos de mongo cuando son obtenidos a través de queries en otras funciones
import dbconfig as db # importamos los datos de conexión de las base de datos del arcihivvo dbcocnfig y le asignamos un alias 
from flask_cors import CORS, cross_origin # Para especificar que el Backend pueda recibir peticicones desde otros origenes
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from binascii import hexlify, unhexlify

load_dotenv()# Se llama a la función para cargar las variables de entorno

salt = os.getenv('SALT').encode() # Obtenemos la variable SALT del archivo .env para poder utilizarlo en la función para Hash,y ya que viene como String, es convertido en Bytes

app = Flask(__name__) # Se define el nombre de la aplicación con la variable __name__ que se le asignó antes a Flask
app.config['CORS_HEADERS'] = 'Content-Type' #Le decimos a Cors en qué formato va a recibir los headers (datos de las peticiones)
CORS(app) #Se define el nombre de la App que utilizará cors el cual es otro objeto de flask
cors = CORS(app, resources = {r"*":{"origins":"http://localhost:4200"}}) #Permitimos el orgien de nuestro servidor local de Frontend para que pueda recibir peticiones y datos desde ahí
db1 = db.c_users.users #Users database using the users collecion variable
db2 = db.c_pvkpbk.keys #Users database using the users collecion variable


@app.route('/users/<id>', methods=['GET']) #Definimos la ruta para ver un usuario específico por medio del ID
def get_user(id): #La función recibe el parámetro ID
        user = db1.find_one({'_id': ObjectId(id)}) # Hacemos una consulta a mongo para encontrar por medio de la Id proporcionada y luego es almacenada dentro de la variable user, esto es un objeto de Mongo DB que en caso de que la consulta devuelva algo tiene los datos de ese usuario, y en caso contrario el valor es None o Undefined en el caso del Frontend
        response = json_util.dumps(user) #Definimos la variable response en donde convertimos el objeto de mongo en un Json 
        return Response(response, mimetype= 'application/json') # Definimos el tipo de datos por el cuál se enviará la respuesta del servidor
        

@app.route('/users/<username>', methods=['DELETE']) # Definimos la función de eliminar usuario a través de su Username el cual es único así que no deberia haber problema al utilizarlo en lugar del ID
def delete_user(username): #La función recibe como parámetro el nombre del usuario 
        db1.delete_one({'username': username}) #Se elimina al usuario por medio del username en mongodb
        response = jsonify({'message': 'User: '+ username + ' was deleted successfully'}) #Se define una variable con un valor en formato json para que el usuario sepa qué dato fue eliminado 
        return response # Se retorna la respuesta anteriormente definida


@app.route('/users/<id>', methods=['PUT']) #Definimos la función para actualizar a través del id del usuario a través del método PUT
def update_user(id): #La función recibe el Id como parámetro
        username = request.json['username'] #Definimos el usuario por lo que está recibiendo en formato json en la petición, la cual es un objeto con los datos que envia el usuario y en este caso obtenemos en esta variable unicamente el nombre de usuario
        user = db1.find_one({'_id': ObjectId(id)}) # se Define una variable con la consulta para ver si el usiario que se quiere actualizar existe buscandolo por medio del ID
        # password = request.json['password'].encode()
        if user != None: #En caso de que no se encuentre el nombre de usuario de ese ID el valor de user es None, por lo tanto, lo siguiente solo podrá continuar si el dato no es None
                if username: #Si está definido el usuario, es decir que si se ha enviado el dato Username a través de Json
                        # hashed_password = hashlib.pbkdf2_hmac('sha512', password, salt, 100000).hex()
                        usernameold = user['username'] #Guardamos en una variable el nombre que actualmente tiene el usuario en la base de datos (antes de actualizar)
                        db1.update_one({'_id': ObjectId(id)}, {'$set':{
                        'username': username}}) #Actualizamos el lcampo username del usuario que coicida con la id que le llega como parámemtro y se define el nombre de usuario que llega por Json
                        response =  jsonify({'message': 'User: '+ usernameold + ' was updated successfully to '+ username}) #Se define la respuesta del servidor para que muestre al usuario el antiguo y el nuevo nombre de usuario después de haber actualizado
                        return response #Se envia la respuesta
        else:
                return {'alert': 'Username do not match with any username account'} #Esta respuesta se da en caso de que on se encuentre el nombre de usuario de la ID que le llega como parámetro, es decir, si el objeto de la consulta user está vacío o la consulta no fue exitosa


@app.route('/users', methods=['GET']) #Definimos la ruta para obtener todos los usuarios registrados en la base de datos
def get_users():
        users = db1.find() #Hacemos una consulta sin argumentos a la colección de los usuario en la base de datos
        response = json_util.dumps(users) #Y la respuesta es el objeto de Mongo pero convertido en Json
        return Response(response, mimetype='application/json') #Definimos el tipo de respuesta que se está enviando


@app.route('/signup', methods = ['POST']) # Definimos la ruta para poder registrar usuarios a través del método POST
def create_user():
        # Receiving data
        username = request.json['username'] #Se define esta variable con lo que llega de la petición en formato json
        user = db1.find_one({'username':username}) # se Define una variable con la consulta para ver si el usiario que se quiere actualizar existe buscandolo por medio del username o nombre de usuario

        password = request.json['password'].encode()#Se define esta variable con lo que llega de la petición en formato json, pero en este caso al mismo tiempo la contraseña que envía el usuario desde su registro es convertida en Bytes para poder se operada por la función de Hash más adelante
        if user == None and password: #En caso de que el usuario que se quiere registrar ya exista, se envia una respuesta directamente para decirle al usuario que ese nombre de usuario ya está registrado
                pvk,pbk, cipher_password = Generate_keys(password) #Generacion de llave privada y pública para este usuario y al mismo tiempo se cifra la contraseña
                if cipher_password: #En caso de que el nombre de usuario y el password hayan sido recibidos, es decir que desde el request tengan un valor enviado por el usuario
                        idk = db2.insert({'public_key': pbk, 'private_key': pvk})

                        idu =  db1.insert(
                                {'username': username, 'password': cipher_password, 'key': str(idk)}
                        ) #Definimos la variable id por el objetod de mongo que es generado después de insertar la contraseña cifrada y el nombre de usuario en la base de datos en la colección de usuarios
                        response = {
                                'id': str(idu), #Es necesario hacer esto, ya que si estamos definiendo un json, no puede haber un objeto, es decir, todo debe estar en formato string
                                'username': username, #Guardamos en el json el nombre de usuario
                                'password': cipher_password #Guardamos en el json la contraseña cifradad
                        }
                        return response #Se devuelvee el json anterior
                else:
                        return not_found() #en caso de que no se envie alguno de los datos se llama a la función de not_found que le indicará al servidor como una respuesta el código de estado del error
                return {'message': 'Received'} #En caso de que todo haya salido bien, se envia una respuesta de recibido que indica que el usuario ha sido creado satisfactoriamente
        else:
                return {'alert': 'Username is already taken, try to login or choose another one'} #Esta respuesta se envía en caso de que el nombre de usuario que se quiere registrar ya se encuentre en la base de datos (esta respuesta será capturadad por el Frontend para mostrar alertas indicando al  usuario el motivo del error al registrar)


@app.route('/signin',methods=['POST']) #Definimos el método login a través de POST
def login():
        username = request.json['username'] #se define la variable username por el dato en json que llegue con la petición
        user = db1.find_one({'username':username})# se Define una variable con la consulta para ver si el usiario existe buscandolo por medio del username o nombre de usuario
        userkid = user['key']
        key = db2.find_one({'_id': ObjectId(userkid)})
        password = request.json['password']#Se define esta variable con lo que llega de la petición en formato json, pero en este caso al mismo tiempo la contraseña que envía el usuario desde su registro es convertida en Bytes para poder se operada por la función de Hash más adelante
        private_key = key['private_key']
        cipher_password = user['password']
        d_pwd = decipher_passwords(private_key,cipher_password)
        if user != None and d_pwd == password:
                return {'message': 'Login Success',
                        'response': 'welcome '+ username} #En caso de que la variable user no sea None, es decir, que la consulta haya sido un exito y ese usuario si exista dentro de la base de datos Y que  el resultado de cifrar la contaseña del usuario conincida con la cifrada dentro del objeto de la base de datos entonces le damos acceso y enviamos la respuesta de Login satisfactorio y le damos la bienvenia
        else:
                return {'message': 'Login failed',
                                'response': 'invalid username or pasword'} #Por motivos de seguridad no le indicamos que el nombre de usuario por el que quiere ingresar existe o no, y tampoco le decimos en qué se equivocó, para que no sepa cuáles usuarios hay dentro de la base de datos y no intente un ataque de fuerza bruta o algo parecido. por eso en caso de que alguna de las dos que el usuario no esté en la base de datos o que la contraseña no coincida no lo dejamos entrar al sistema


@app.errorhandler(404) #Esta ruta es llamada cuando ocurre un error 404 en nuestro servidor o simplemente cuando se llama la función directamente
def not_found(error=None):
        response = jsonify({
                'message': 'Resource Not Found',
                'status': 404
        }) #Se define una respuesta para decir el tipo de error que se capturó
        response.status_code = 404 #Definimos el mensaje del servidor de error 404 para que nos diga algo específico y no solo erro 505 o status 200
        return response #y se retorna la función
if __name__ == "__main__":
        app.run(load_dotenv=True) #Se ejecuta la aplicación flask, enviándole un parámetro el cual quiere decir que debe cargar su configuración de los archivos .env o .flaskenv, el cuál está en la raíz del proyecto, esto es útil para indicarle la ruta de la aplicación principal que va a ejecutar el comando Flask run el entorno de flask que puede ser Desarrollo o producción (development or production) el modo de debug que es para que nos muestre una definicón detallada de los errores en caso de que existan y el puerto en el que se va a establecer el servidor, por defecto flask utiliza el 5000, pero es posible cambiarlo directamente en el archivo .flaskenv
def Generate_keys(message):
        private_key = RSA.generate(1024)
        public_key = private_key.publickey()
        private_pem = private_key.export_key(format="DER").hex()
        public_pem = public_key.export_key(format="DER").hex()
        pu_key = RSA.import_key(unhexlify(public_pem))
        cipher = PKCS1_OAEP.new(key=pu_key)
        cipher_text = cipher.encrypt(message).hex()
        return (private_pem, public_pem, cipher_text)
def decipher_passwords(private_key, password):
        pr_key = RSA.import_key(unhexlify(private_key))
        msg_ = unhexlify(password)
        decrypt = PKCS1_OAEP.new(key=pr_key)
        decrypted_password = decrypt.decrypt(msg_).decode()
        return decrypted_password