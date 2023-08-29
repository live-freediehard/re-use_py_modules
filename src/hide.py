from Crypto.PublicKey import RSA
from Crypto import Random
import ast
from Crypto.Cipher import PKCS1_OAEP

random_generator = Random.new().read
key = RSA.generate(2048, random_generator)  

publickey = key.publickey()  

encryptor = PKCS1_OAEP.new(publickey)
encrypted = encryptor.encrypt(b'iR7q%9iF666')

print('encrypted message:', encrypted)

f = open('encryption.txt', 'w')
f.write(str(encrypted))
f.close()

f = open('encryption.txt', 'r')
message = f.read()

decryptor = PKCS1_OAEP.new(key)

decrypted = decryptor.decrypt(ast.literal_eval(str(message)))

print('decrypted', decrypted)

str_val=str(decrypted)
splitted_str=str_val.split('\'')
strpwd=splitted_str[1]
print(strpwd)

f = open('dencryption.txt', 'w')
f.write(str(decrypted))
f.close()
