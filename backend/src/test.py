import hashlib
import os
from  dotenv import load_dotenv
from  Crypto.Random import get_random_bytes

load_dotenv()
message = b'El dios de la muerte solo come manzanas'
salt = os.getenv('SALT').encode()
# print("salt >", salt)
# hola  = str(get_random_bytes(1024)).replace('b','')
# print("hola >", hola)

# salt = b'80th9saon+fyzkyesrv$ov9gash*)48n07jp*5zx%di1j$inod'

hashed_message = hashlib.pbkdf2_hmac('sha512', message, salt, 1000000).hex()

print(str(hashed_message))
# hashed_message = hashlib.pbkdf2_hmac('sha512', message, salt, 1000000).hex()
# print(hashed_message)

message = input('Type a password: ').encode()
unhashed_message = hashlib.pbkdf2_hmac('sha512', message, salt, 1000000).hex()
# print(unhashed_message)


if unhashed_message == hashed_message:
    print('The password is correct')
# print(hashed_message)
