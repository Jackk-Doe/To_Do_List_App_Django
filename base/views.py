from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin   #User login required for inherited classes
from django.urls import reverse_lazy
from .models import Task

# Logout function in urls.py

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True     #Prevent User to re-login

    def get_success_url(self):
        return reverse_lazy('tasks')    #Once logined, redirect to this url

class TaskList(LoginRequiredMixin, ListView):   #Auto look for html (template) file with same class name (task_list.html)
    model = Task
    context_object_name = 'tasks'   #How class's obj is called in html

class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'    #Rewrite Auto template file seeking function

class TaskCreate(LoginRequiredMixin, CreateView):   #The CreateView auto create form field inside it
    model = Task
    fields = '__all__'      #Use all fields in assigned [model]
    success_url = reverse_lazy('tasks') #If all went successfully, go to 'tasks' in urlpatterns

class TaskUpdate(LoginRequiredMixin, UpdateView):   #Auto fill form field, with given fields var
    model = Task 
    fields = '__all__'
    success_url = reverse_lazy('tasks')

class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
