from django.core.management.base import BaseCommand
from tasks.models import Task
from django.utils import timezone
from datetime import datetime , timedelta
from django.contrib.auth.models import User
import pandas as pd
from django.conf import settings
import os


class Command(BaseCommand):
    def add_arguments(self, parser):
        
        pass

    def send_email(self, user,path):
        pass
        return False
        # send true on sending of email
    
    def compile_tasks(self,user, now,next_date):
        all_tasks= Task.objects.filter(due__gte=now, due__lt=next_date,
        status__in=[Task.STATUS_TYPE_PENDING, Task.STATUS_TYPE_OVERDUE], user=user)

        response=[]
        
        for  task in all_tasks:
            response.append({'status':task.status, 'title':task.title,'description':task.description,
            'due':task.due.strftime('%Y-%m-%dT%H:%M:%S')})  

        df=pd.DataFrame(response)
        path=os.path.join(settings.BASE_DIR,'daily_reports',
            user.username+now.strftime('%Y-%m-%dT%H:%M:%S')+'.csv')
        df.to_csv(path)

        if self.send_email(user, path):
            os.remove(path)



    
    
    def handle(self, *args, **options):
        now = timezone.now()
        next_date= now+timedelta(days=1)

        upcoming_tasks_user= Task.objects.filter(due__gte=now, due__lt=next_date,
        status__in=[Task.STATUS_TYPE_PENDING, Task.STATUS_TYPE_OVERDUE]
        ).values('user').distinct()
        

        for us in upcoming_tasks_user:
            id = us['user']
            user=User.objects.get(id=id)
            self.compile_tasks(user, now,next_date)


