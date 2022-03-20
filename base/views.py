from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin   #User login required for inherited classes

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from django.urls import reverse_lazy
from matplotlib.style import context
from .models import Task

# Logout function is in urls.py

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True     #Prevent User to re-login

    def get_success_url(self):
        return reverse_lazy('tasks')    #Once logined, redirect to this url


class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm       #User Django built-in to create Form
    success_url = reverse_lazy('tasks')

    #Trigger this method once form was submited
    def form_valid(self, form):
        user = form.save()      #Return User once submited
        if user is not None:
            login(self.request, user)   #Login User
        return super(RegisterPage, self).form_valid(form)

    #Trigger this, when User tried to access this form
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:  #Already logined
            return redirect('tasks')
        else:
            return super(RegisterPage, self).get(*args, **kwargs)


class TaskList(LoginRequiredMixin, ListView):   #Auto look for html (template) file with same class name (task_list.html)
    model = Task
    context_object_name = 'tasks'   #How class's obj is called in html

    #Overrider this method to only return [Task] which belongs to that User
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  #Call Super method
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()

        #IF User clicked in search bar, trigger SEARCH function, get data from GET, else '' (empty)
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)

        context['search_input_bar'] = search_input  #Refresh search bar with [search_input]
        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'    #Rewrite Auto template file seeking function


class TaskCreate(LoginRequiredMixin, CreateView):   #The CreateView auto create form field inside it
    model = Task
    # fields = '__all__'      #Use all fields in assigned [model]
    fields = ['title', 'description', 'complete']  #Since below method deal with [User] field, no need '__all__'
    success_url = reverse_lazy('tasks') #If all went successfully, go to 'tasks' in urlpatterns

    #Override to, Auto set a creating [Task]'s [User] field to current User
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):   #Auto fill form field, with given fields var
    model = Task 
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')


class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
