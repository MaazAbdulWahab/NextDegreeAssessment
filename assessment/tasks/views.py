from django.shortcuts import render

# Create your views here.

from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.permissions  import IsAuthenticated
from core.utils import CustomTokenAuth
from tasks.models import *
from datetime import datetime
import pandas as pd
import os


def create_task(user, title, description, due):
    t=Task.objects.create(user=user, title=title, description=description,
                    due=due, status= Task.STATUS_TYPE_PENDING)
    return t.id


class TasksCRUD(APIView):
    authentication_classes=[CustomTokenAuth]
    
    permission_classes=[IsAuthenticated]


    def get(self,request, *args, **kwargs):

        user=request.user
        related_tasks= user.created_tasks.all()
        response=[]
        for task in related_tasks:
            response.append({'id':task.id,'status':task.status, 'title':task.title,'description':task.description,
            'due':task.due.strftime('%Y-%m-%dT%H:%M:%S')})
        
        return Response({'success': True,'tasks':response}, status=200)


    def delete(self,request, *args, **kwargs):
        
        user=request.user
        task_id= request.data.get('task_id')
        related_task= user.created_tasks.filter(id=task_id)
        
        if not related_task.exists():
            return Response({'success': False,'message':"Task Not Found"}, status=404)

        else:
            related_task.delete()
            return Response({'success': True,}, status=204)

    def post(self,request,*args,**kwargs):

        user=request.user

        title=request.data.get('title')
        description=request.data.get('description')

        due=request.data.get('due')
        due=datetime.strptime(due,'%Y-%m-%dT%H:%M:%S')

        task_id= create_task(user,title,description,due)

        return Response({'success': True,'task_id':task_id}, status=201)

    
    
    def put(self,request,*args,**kwargs):
        user=request.user
        task_id= request.data.get('task_id')
        try:
            related_task= user.created_tasks.get(id=task_id)
        except:
            return Response({'success': False,'message':"Task Not Found"}, status=404)

        title=request.data.get('title')
        description=request.data.get('description')
        status= request.data.get('status')

        if title:
            related_task.title=title
        if description:
            related_task.description=description

        if status:
            
            allowed_status_types=list(map(lambda x : x[0],Task.STATUS_CHOICES))
            status= status.upper()

            if status not in allowed_status_types:
               return Response({'success': False,'message':"Task Status Not Allowed"}, status=400) 
            related_task.status=status
        
        due=request.data.get('due')
        if due:
            due=datetime.strptime(due,'%Y-%m-%dT%H:%M:%S')
            related_task.due=due



        related_task.save()

        return Response({'success': True,'task_id':related_task.id}, status=202)




class BulkTasks(APIView):
    authentication_classes=[CustomTokenAuth]
    
    permission_classes=[IsAuthenticated]

    def post(self,request,*args,**kwargs):
        
        user=request.user
        file= request.data.get('file')
        name=file.name
        
        data=pd.read_csv(file)

        
        task_ids=[]
        for row in data.to_dict(orient="records"):
            title=row['title']
            description=row['description']

            due=row['due']
            due=datetime.strptime(due,'%Y-%m-%dT%H:%M:%S')
           
            task_id= create_task(user,title,description,due) 
        task_ids.append(task_id)

        return Response({'success': True,'task_ids':task_ids}, status=202)


        
