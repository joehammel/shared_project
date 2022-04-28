from json import dumps
from logging import info
from tornado.escape import json_decode, utf8
from tornado.gen import coroutine

#create code for encryption of data at rest 
from .base import BaseHandler
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms
key = "thebestsecretkeyintheentireworld"
key_bytes = bytes(key, "utf-8")
nonce_bytes = os.urandom(16)
nonce=nonce_bytes.hex()
chacha20_cipher = Cipher(algorithms.ChaCha20(key_bytes, nonce_bytes),
                         mode=None)
chacha20_encryptor = chacha20_cipher.encryptor()


#create code to hash password
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
salt = os.urandom(16)
kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)

class RegistrationHandler(BaseHandler):

    @coroutine
    def post(self):
        try:
            body = json_decode(self.request.body)
            email = body['email'].lower().strip()
            if not isinstance(email, str):
                raise Exception()
            password = body['password']
            if not isinstance(password, str):
                raise Exception()
            pw =body.get('password')
            password_bytes = bytes(pw, "utf-8")
            kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)
            hashed_password = kdf.derive(password_bytes)
            if pw is None:
                pw = email
            if not isinstance(pw, str):
                raise Exception()
            display_name =body.get('displayName')
            if display_name is None:
                display_name = email
            if not isinstance(display_name, str):
                raise Exception()
            display_name_bytes = bytes(display_name, "utf-8")
            display_namex = chacha20_encryptor.update(display_name_bytes)
            address =body.get('address')
            if address is None:
                address = email
            if not isinstance(address, str):
                raise Exception()
            address_bytes = bytes(address, "utf-8")
            addressx = chacha20_encryptor.update(address_bytes)
            phone =body.get('phone')
            if phone is None:
                phone = email
            if not isinstance(phone, str):
                raise Exception()
            phone_bytes = bytes(phone, "utf-8")
            phonex = chacha20_encryptor.update(phone_bytes)
            medical_condition =body.get('medical condition')
            if medical_condition is None:
                medical_condition = email
            if not isinstance(medical_condition, str):
                raise Exception()
            medical_condition_bytes = bytes(medical_condition, "utf-8")
            medical_conditionx = chacha20_encryptor.update(medical_condition_bytes)

        except Exception as e:
            self.send_error(400, message='**You must provide an email address, password and display name!**')
            return

        if not email:
            self.send_error(400, message='**The email address is invalid!**')
            return

        if not password:
            self.send_error(400, message='**The password is invalid!**')
            return

        if not display_name:
            self.send_error(400, message='**The display name is invalid!**')
            return
        user = yield self.db.users.find_one({
          'email': email
        }, {})

        if user is not None:
            self.send_error(409, message='**A user with the given email address already exists!**')
            return



        yield self.db.users.insert_one({
            'email': email,
            'password': hashed_password,
            'displayName': display_namex,
            'address': addressx,
            'phone': phonex,
            'medical condition': medical_conditionx,
            'nonce': nonce,
            'salt': salt,
            'hash': 'hash'
        })


        self.set_status(200)
        self.response['email'] = email
        self.response['displayName'] = display_name
        self.response['nonce'] = nonce

        self.write_json()

