from django.test import TestCase
from django.test import TestCase
from rest_framework.test import APIRequestFactory
import requests
import json


class UnitTestCase(TestCase):

def test_api_create(self):
    #right case
    myobj = {'email': 'test01@outlook.com', 'password': 'abc12345'}
    r = requests.post('http://127.0.0.1:8000/api/auth/sign_in',data=myobj)
    access_token=r.headers.get('access-token')
    client_key= r.headers.get('client')



    headers = {'uid': 'test01@outlook.com', 'access-token': access_token, 'client': client_key}
    myobj = {'comment': 'Hello Everyone', 'user_id': '335'}
    response=requests.post('http://127.0.0.1:8000/api/user/reports',headers=headers, data=myobj)
    responseBody = json.loads(response.text)

    self.assertEqual(responseBody['code'], 0)
    self.assertEqual(responseBody['success'], True)

def test_api_reports_get(self):
    myobj = {'email': 'test01@outlook.com', 'password': 'abc12345'}
    r = requests.post('http://127.0.0.1:8000/api/auth/sign_in',data=myobj)
    access_token=r.headers.get('access-token')
    client_key= r.headers.get('client')

    headers = {'uid': 'test01@outlook.com', 'access-token': access_token, 'client': client_key}
    myobj = {'assignee_id': '2', 'user_id': '335', 'status':0}

    # correct parameter
    payload = {'page': '1', 'per_page': '1', 'user_id':'335'}

    
    response=requests.post('http://127.0.0.1:8000/api/user/reports',params=payload,headers=headers, data=myobj)
    responseBody = json.loads(response.text)

    self.assertEqual(responseBody['code'], 0)
    self.assertEqual(responseBody['success'], True)

def test_api_reports_delete(self):
    myobj = {'email': 'test01@outlook.com', 'password': 'abc12345'}
    r = requests.post('http://127.0.0.1:8000/api/auth/sign_in',data=myobj)
    access_token=r.headers.get('access-token')
    client_key= r.headers.get('client')
    id = '251'

    headers = {'uid': 'test01@outlook.com', 'access-token': access_token, 'client': client_key}

    response=requests.post('http://127.0.0.1:8000/api/user/reports/' + id,headers=headers)
    self.assertEqual(responseBody['code'], 0)
    self.assertEqual(responseBody['success'], True)

