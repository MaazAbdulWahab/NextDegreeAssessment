from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
import time

# Create your tests here.


class TestRegistration(TestCase):
    def setUp(self):
        self.client = Client()
        print("SETTED UP")
    
    def test_registration_correct(self):
        print("TESTING THE REGISTRATION API FOR THE CREATION OF ACCOUNT")
        resp =self.client.post('/auth/register/', 
            {"username":"papa", "email":"papa@papa.com", "password":"papa@papa"}) 
        assert resp.status_code == 201
        
    
    
    def test_registration_duplicate(self):
        User.objects.create(username="papa", email="papa@papa.com")
        print("TESTING REGISTRATION DUPLICATE ACCOUNT")
        resp =self.client.post('/auth/register/', 
            {"username":"papa", "email":"papa@papa.com", "password":"whatever@whatever"}) 
        assert resp.status_code == 400


    def tearDown(self):
        print(User.objects.get(username="papa").delete())



class TestLogin(TestCase):
    def setUp(self):
        self.client = Client()
        print("SETTED UP")
    
    def test_login_correct(self):
        print("TESTING THE CORRECT LOGIN FUNCTIONALITY")
        print("TESTING REGISTRATION FIRST")
        resp_register =self.client.post('/auth/register/', 
            {"username":"papa", "email":"papa@papa.com", "password":"papa@papa"}) 
        assert resp_register.status_code == 201

        print("TESTING LOGGING IN THEN")
        resp_login =self.client.post('/auth/login/', 
            {"email":"papa@papa.com", "password":"papa@papa"}) 
        assert resp_login.status_code == 200
        response= resp_login.json()
        assert response['success'] is True
        assert response['token']


    
    def test_login_incorrect(self):
        print("TESTING THE INCORRECT LOGIN FUNCTIONALITY")
        print("TESTING REGISTRATION FIRST")
        resp_register =self.client.post('/auth/register/', 
            {"username":"papa", "email":"papa@papa.com", "password":"papa@papa"}) 
        assert resp_register.status_code == 201

        print("TESTING LOGGING IN WITH WRONG EMAIL")
        resp_login_wrong_email =self.client.post('/auth/login/', 
            {"email":"papi@papa.com", "password":"papa@papa"}) 
        assert resp_login_wrong_email.status_code == 404


        print("TESTING LOGGING IN WITH WRONG PASSWORD")
        resp_login_wrong_email =self.client.post('/auth/login/', 
            {"email":"papa@papa.com", "password":"papi@papa"}) 
        assert resp_login_wrong_email.status_code == 400

    def tearDown(self):
        print(User.objects.get(username="papa").delete())



class TestLogout(TestCase):
    def setUp(self):
        self.client = Client()
        print("SETTED UP")
    
    def test_logout_correct(self):
        print("TESTING THE CORRECT LOGOUT FUNCTIONALITY")
        print("TESTING REGISTRATION FIRST")
        resp_register =self.client.post('/auth/register/', 
            {"username":"papa", "email":"papa@papa.com", "password":"papa@papa"}) 
        assert resp_register.status_code == 201

        print("TESTING LOGGING IN THEN")
        resp_login =self.client.post('/auth/login/', 
            {"email":"papa@papa.com", "password":"papa@papa"}) 
        assert resp_login.status_code == 200
        response= resp_login.json()
        assert response['success'] is True
        assert response['token']
        token = response["token"]


        print("NOW LOGGING OUT")
        headers_logout= {"HTTP_AUTHORIZATION": "Token "+token}
        
        resp_logout =self.client.post('/auth/logout/' , **headers_logout)
        assert resp_logout.status_code == 200 


    def test_logout_incorrect(self):
        print("TESTING THE INCORRECT LOGOUT FUNCTIONALITY")
        print("TESTING REGISTRATION FIRST")
        resp_register =self.client.post('/auth/register/', 
            {"username":"papa", "email":"papa@papa.com", "password":"papa@papa"}) 
        assert resp_register.status_code == 201

        print("TESTING LOGGING IN THEN")
        resp_login =self.client.post('/auth/login/', 
            {"email":"papa@papa.com", "password":"papa@papa"}) 
        assert resp_login.status_code == 200
        response= resp_login.json()
        assert response['success'] is True
        assert response['token']
        token = response["token"]


        print("NOW LOGGING OUT")
        
        resp_logout =self.client.post('/auth/logout/')#
        assert resp_logout.status_code == 401



    def tearDown(self):
        User.objects.get(username="papa").delete()





    