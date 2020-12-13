from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.generic import View
from .forms import TaskCalendarForm
from .models import TaskCalendar
from datetime import date, timedelta, datetime
from django.core.exceptions import ObjectDoesNotExist
from abc import abstractmethod
import json


class PublicTask(LoginRequiredMixin, View):
    def __init__(self):

        self.help_message = { 
                'id':     'Введите ID сообщения',
                'button': 'Изменить'
            }

        self.inputs_status = { 
                'title':       '',   
                'description': '',
                'date':        '',
                'select':      '',

        }

        self.for_dashboard ={
            'title': 'Панель управления календарем'
        }

        self.ready_check_modify = False  #готовность формы на изменение

        LoginRequiredMixin.__init__(self) 
        View.__init__(self)


class CalendarView(PublicTask):

    redirect_field_name = None

    def get(self,request):

       ''' Первоночальный вариант 
       js_data = [
                  {
                      'title': 'Shooting',
                      'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras eu pellentesque nibh. In nisl nulla, convallis ac nulla eget, pellentesque pellentesque magna.',
                      'start': '2020-08-25',
                      'end': '2020-08-25',
                      'className': 'fc-bg-blue',
                      'icon' : "camera"
                  },
                  {
                      'title': 'Go Space :)',
                      'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras eu pellentesque nibh. In nisl nulla, convallis ac nulla eget, pellentesque pellentesque magna.',
                      'start': '2020-12-27',
                      'end': '2020-12-27',
                      'className': 'fc-bg-default',
                      'icon' : "rocket"
                  },
              ]
        '''
       user_name = request.user
       curent_user = User.objects.get(username=user_name)
       tasks = TaskCalendar.objects.filter(user=curent_user)
       tasks_list = []
       for task in tasks:
           cur_task = {"title": task.title,
           "description": task.description,
           "date": str(task.date)
           }
           tasks_list.append(cur_task)

       tasks_json_list = json.dumps(tasks_list)
       self.for_dashboard['title'] = f'Hi, {user_name}! {self.for_dashboard["title"]}'
       return render(request, 'app_calendar/calendar.html',
             {'tasks': tasks_json_list,
              'for_dashboard': self.for_dashboard,
             }
            )


    def post(self,request):
       user_name = request.user
       curent_user = User.objects.get(username=user_name)
       task_form = TaskCalendarForm(data=request.POST)
       if task_form.is_valid():
           new_task = task_form.save(commit=False)
           new_task.user = curent_user
           new_task.save()
       else:
           task_form = TaskCalendarForm()
       
       tasks = TaskCalendar.objects.filter(user=curent_user)
       tasks_list = []
       for task in tasks:
           cur_task = {"title": task.title,
           "description": task.description,
           "date": str(task.date)
           }
           tasks_list.append(cur_task)

       self.for_dashboard['title'] = f'Hi, {user_name}! {self.for_dashboard["title"]}' 
       tasks_json_list = json.dumps(tasks_list)
       return render(request, 'app_calendar/calendar.html', 
            {"tasks": tasks_json_list,
            'for_dashboard': self.for_dashboard,
            }
           )



class DisplayTasks(PublicTask):

    def __init__(self):
        PublicTask.__init__(self)
        self.for_dashboard['title'] = 'Список задач.'

    redirect_field_name = None
    def get(self, request):
        user_name = request.user
        curent_user = User.objects.get(username=user_name)
        tasks_list = TaskCalendar.objects.filter(user=curent_user)
        selected_task = []
        for task in tasks_list:
            if date.today() == task.date.date():
                selected_task.append(task)
        return render(request, 'app_calendar/display_tasks.html', 
                {'tasks': selected_task,
                'for_dashboard': self.for_dashboard,
                }
                )


    def post(self, request):
        user_name = request.user
        curent_user = User.objects.get(username=user_name)
        tasks_list = TaskCalendar.objects.filter(user=curent_user)
        selected_task = []
        try:
            date_sel = datetime.strptime(request.POST['date'], '%m/%d/%y %H:%M').date()
        except ValueError:
            date_sel = date.today()
        
        print(date.today)
        for task in tasks_list:
            if  date_sel == task.date.date():
                selected_task.append(task)
           
        return render(request, 'app_calendar/display_tasks.html', 
                {'tasks': selected_task,
                'for_dashboard': self.for_dashboard,
                }
                )

        

class AddTask(PublicTask):

    def __init__(self):
        PublicTask.__init__(self)
        self.for_dashboard['title'] = 'Добавить задачу.'

    redirect_field_name = None
    def get(self, request):
        task_form = {}
        return render(request, 'app_calendar/add_task.html',
                {'task_form': task_form,
                 'for_dashboard': self.for_dashboard,
                }
                )

    def post(self, request):
        user_name = request.user
        curent_user = User.objects.get(username=user_name)
        task_form = TaskCalendarForm(data=request.POST)
        if task_form.is_valid():
            new_task = task_form.save(commit=False)
            new_task.user = curent_user
            new_task.save()
        else:
            task_form = TaskCalendarForm()
        return render(request, 'app_calendar/add_task.html', 
                {'task_form': task_form,
                 'for_dashboard': self.for_dashboard,
                }
                )



class GetAboutTask(PublicTask):

    def __init__(self):
        PublicTask.__init__(self)
        self.for_dashboard['title'] = 'Полная информация по задаче.'

    def get(self, request):
        return render(request, 'app_calendar/get_about_task.html', 
                {'task': None,
                'for_dashboard': self.for_dashboard,
                }
                )

    
    def post(self, request):
        user_name = request.user
        try:
            task_id = request.POST['id']
            curent_user = User.objects.get(username=user_name)
            task = TaskCalendar.objects.get(user=curent_user, id=int(task_id))
            return render(request, 'app_calendar/get_about_task.html', 
                    {'task': task,
                    'for_dashboard': self.for_dashboard,
                    }
                    )
        except ObjectDoesNotExist:
            task = {'description': 'Такой задачи не существует',
                    'id': task_id
            }
            return render(request, 'app_calendar/get_about_task.html', 
                    {'task': task,
                    'for_dashboard': self.for_dashboard,
                    }
                    )
        except ValueError:
            task = {'description': 'Введите корректный id. Должны быть цифры.',
                    'id': task_id
                    }
            return render(request, 'app_calendar/get_about_task.html', 
                    {'task': task,
                    'for_dashboard': self.for_dashboard,
                    }
                    )


class ChangetTask(PublicTask):

    def __init__(self):
        PublicTask.__init__(self)
        self.for_dashboard['title'] = 'Изменить задачу.'

    def get(self, request):
        self.help_message['button'] = "Найти"
        return render(request, 'app_calendar/change_task.html', 
            {'task': None, 
             'help_message': self.help_message, 
             'inputs_status': self.inputs_status,
             'ready_check_modify': self.ready_check_modify,
             'for_dashboard': self.for_dashboard,
             }
        )

    
    def post(self, request):
        '''
        Поведение зависит от  колличества заполненых полей.
        Если любое поле заполнено и id указан верно - обновляем данные.
        Если же чего-то не хватает, обноляем форму либо выдаем ошибку
        '''

        task = {}
        user_name = request.user
        try:
            task_id = request.POST['id']
            curent_user = User.objects.get(username=user_name)
            task = TaskCalendar.objects.get(user=curent_user, id=int(task_id))
            
            change = {'title': False,
                'description': False,
                'status':      False,
                'date':        False}
            
            if request.POST['title']:
               if not request.POST['title'] == task.title:
                   task.title = request.POST['title']
                   change['title'] = True

            if request.POST['description']:
               if not request.POST['description'] == task.description:
                   task.description = request.POST['description']
                   change['description'] = True
            
            if request.POST['status']:
               if not int(request.POST['status']) == int(task.status):
                   task.status = int(request.POST['status'])
                   change['status'] = True
            
            if request.POST['date']:
               if not request.POST['date'] == task.date:
                   task.date = datetime.strptime(request.POST['date'], '%m/%d/%y %H:%M')
                   change['date'] = True

            if not change['title'] and not change['description'] and not change['date'] and not change['status']:
                return render(request, 'app_calendar/change_task.html', 
                        {'task': task, 
                        'help_message':self.help_message,
                        'inputs_status': self.inputs_status,
                        'ready_check_modify': self.ready_check_modify,
                        'for_dashboard': self.for_dashboard,
                        }
                    )

            task.save()
            task = {}
            self.help_message['id'] = "Задание успешно изменено."
            self.help_message['button'] = "Найти"
            return render(request, 'app_calendar/change_task.html',
                         {'task': task, 
                          'help_message':self.help_message,
                          'inputs_status': self.inputs_status,
                          'ready_check_modify': self.ready_check_modify,
                          'for_dashboard': self.for_dashboard,
                          }
                         )            

        except ObjectDoesNotExist:
            self.help_message['id'] = "Объект не найден. Введите корректный ID"
            self.help_message['button'] = "Найти"
            return render(request, 'app_calendar/change_task.html',
                    {'task': task, 
                     'help_message':self.help_message,
                     'inputs_status':self.inputs_status,
                     'ready_check_modify': self.ready_check_modify,
                     'for_dashboard': self.for_dashboard,
                     }
                    )

        except ValueError:
            self.help_message['id'] = "Объект не найден. Введите корректный ID. Должный быть цифры."
            self.help_message['button'] = "Найти"
            return render(request, 'app_calendar/change_task.html', 
                       {'task': task,
                        'help_message':self.help_message,
                        'inputs_status':self.inputs_status,
                        'ready_check_modify': self.ready_check_modify,
                        'for_dashboard': self.for_dashboard, 
                        }
                       )


class ChangeStatusTaskAbstract(PublicTask):
    def __init__(self):
        PublicTask.__init__(self)
        self.help_message['button'] = 'Завершить'
        
        self.inputs_status['title'] = 'disabled'
        self.inputs_status['description'] = 'disabled'
        self.inputs_status['date'] = 'disabled'
        self.inputs_status['select'] = 'disabled'

    @abstractmethod
    def modify_status(self, task):
        pass
        

    def get(self, request):
        self.help_message['button'] = 'Найти'
        return render(request, 'app_calendar/change_task.html',
                 {'task': None, 
                  'help_message': self.help_message,
                  'inputs_status': self.inputs_status,
                  'ready_check_modify': self.ready_check_modify,
                  'for_dashboard': self.for_dashboard,
                 }
                )

    def post(self, request):
        '''
        Поведение зависит от правильного введеного id.
        Сначала ищем объект, затем меняем ему статус.
        Если ID найдено, то меняем статус на завершить.
        Если ID не корректно выдаем ошибку.
        '''
        task = {}
        user_name = request.user
        try:
            task_id = request.POST['id']
            curent_user = User.objects.get(username=user_name)
            task = TaskCalendar.objects.get(user=curent_user, id=int(task_id))

            if int(request.POST['modify'] == 'False'):
                self.ready_check_modify = True
                return render(request, 'app_calendar/change_task.html', 
                          {'task': task, 
                          'help_message':self.help_message,
                          'inputs_status': self.inputs_status,
                          'ready_check_modify': self.ready_check_modify,
                          'for_dashboard': self.for_dashboard,
                          }
                         )             
            
            self.modify_status(task)

            task = {}
            self.help_message['button'] = "Найти"
            self.ready_check_modify = False
            return render(request, 'app_calendar/change_task.html', 
                          {'task': task, 
                          'help_message':self.help_message,
                          'inputs_status': self.inputs_status,
                          'ready_check_modify': self.ready_check_modify,
                          'for_dashboard': self.for_dashboard,
                          }
                         )               

        except ObjectDoesNotExist:
            self.help_message['id'] = "Объект не найден. Введите корректный ID"
            self.help_message['button'] = "Найти"
            return render(request, 'app_calendar/change_task.html', 
                          {'task': task, 
                          'help_message':self.help_message,
                          'inputs_status': self.inputs_status,
                          'ready_check_modify': self.ready_check_modify,
                          'for_dashboard': self.for_dashboard,
                          }
                         )    

        except ValueError:
            self.help_message['id'] = "Объект не найден. Введите корректный ID. Должны быть цифры."
            self.help_message['button'] = "Найти"
            return render(request, 'app_calendar/change_task.html', 
                          {'task': task, 
                          'help_message':self.help_message,
                          'inputs_status': self.inputs_status,
                          'ready_check_modify': self.ready_check_modify,
                          'for_dashboard': self.for_dashboard,
                          }
                         )    

            
class ChangeStatusTaskToFinish(ChangeStatusTaskAbstract):

    def __init__(self):
        ChangeStatusTaskAbstract.__init__(self)
        self.for_dashboard['title'] = 'Завершить задачу.'

    def modify_status(self, task):
        if not task.status:
            task.status = True
            task.save()
            self.help_message['id'] = "Задание успешно изменено."


class ChangeStatusTaskToStart(ChangeStatusTaskAbstract):

    def __init__(self):
        ChangeStatusTaskAbstract.__init__(self)
        self.for_dashboard['title'] = 'Начать задачу заново.'

    def modify_status(self, task):
        if task.status:
            task.status = False
            task.save()
            self.help_message['id'] = "Задание успешно изменено."
