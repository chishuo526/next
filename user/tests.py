# from datetime import datetime
# from datetime import timedelta
# from django.test import TestCase
# result=datetime.now() + timedelta(days=3)
# print(result)
import hashlib
import time
import uuid

Nonce = str(uuid.uuid4()).replace('-', '')
print(len(Nonce))
CurTime = str(int(time.time()))
print(CurTime)
Nonce = str(uuid.uuid4()).replace('-', '')
headers={}
headers['Nonce'] = Nonce
CurTime = str(int(time.time()))
headers['CurTime'] = CurTime
AppSecret = '7413b1296a89'
headers = hashlib.sha1((AppSecret + Nonce + CurTime).encode('utf-8')).hexdigest()
print(headers)