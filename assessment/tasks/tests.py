from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
import time
from django.utils import timezone
from datetime import datetime, timedelta
import json



def register_and_login(client,payload ):

        resp_register =client.post('/auth/register/', payload) 
        assert resp_register.status_code == 201

        
        resp_login =client.post('/auth/login/', 
            payload) 
        assert resp_login.status_code == 200
        response= resp_login.json()
        assert response['success'] is True
        assert response['token']
        return response['token']



class TestCRUDTasks(TestCase):
    def setUp(self):
        self.client = Client()
        self.payload={"email":"papa@papa.com", "password":"papa@papa", "username":"papa"}
        print("SETTED UP")
    
    def test_task_creation(self):
        token=register_and_login(self.client,self.payload)

        headers= {"HTTP_AUTHORIZATION": "Token "+token}
        
        resp_task_creation =self.client.post('/tasks/tasks/' , {'title':"Do the Testing", 
            "description":"You need to learn testing so we can move it to deployment testing",
            "due":(timezone.now()+ timedelta(days=2)).strftime("%Y-%m-%dT%H:%M:%S")},**headers)

        assert resp_task_creation.status_code == 201

        resp_task_get =self.client.get('/tasks/tasks/', **headers)

        assert resp_task_get.status_code == 200


    def test_task_updation(self):
        '''
        token=register_and_login(self.client,self.payload)

        headers= {"HTTP_AUTHORIZATION": "Token "+token}
        
        resp_task_creation =self.client.post('/tasks/tasks/' , {'title':"Do the Testing", 
            "description":"You need to learn testing so we can move it to deployment testing",
            "due":(timezone.now()+ timedelta(days=2)).strftime("%Y-%m-%dT%H:%M:%S")},**headers)

        assert resp_task_creation.status_code == 201

        resp_task_get =self.client.get('/tasks/tasks/', **headers)

        assert resp_task_get.status_code == 200
        '''
        pass

    
    
    def test_task_deletion(self):

        token=register_and_login(self.client,self.payload)

        headers= {"HTTP_AUTHORIZATION": "Token "+token}

        resp_task_creation =self.client.post('/tasks/tasks/' , {'title':"Do the Testing", 
            "description":"You need to learn testing so we can move it to deployment testing",
            "due":(timezone.now()+ timedelta(days=2)).strftime("%Y-%m-%dT%H:%M:%S")},**headers)

        assert resp_task_creation.status_code == 201

        resp_task_get =self.client.get('/tasks/tasks/', **headers)

        assert resp_task_get.status_code == 200

        alltasks=resp_task_get.json()
        alltasks= alltasks['tasks']
        task_to_delete=alltasks[0]
        id_of_task = task_to_delete['id']


        resp_task_deletion =self.client.delete('/tasks/tasks/', {'task_id':id_of_task},
                content_type="application/json",**headers)
        
        assert resp_task_deletion.status_code == 204


        resp_task_deletion_404 =self.client.delete('/tasks/tasks/', {'task_id':50},
                content_type="application/json",**headers)
        
        assert resp_task_deletion_404.status_code == 404

    




class TestBulkTasks(TestCase):
    def setUp(self):
        self.client = Client()
        self.payload={"email":"papa@papa.com", "password":"papa@papa", "username":"papa"}
        print("SETTED UP")    

    def test_bulk_task_creation(self):
        token=register_and_login(self.client,self.payload)

        headers= {"HTTP_AUTHORIZATION": "Token "+token}


        resp_bulk_creation =self.client.post('/tasks/bulk/' ,{'file':open('try.csv','rb')},**headers)
        assert resp_bulk_creation.status_code == 202






        

