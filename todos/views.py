from django.shortcuts import render, redirect, get_object_or_404
from .models import Todo
import requests
from decouple import config
TOKEN = config("TOKEN")
jin_id = config("jin_id")
jae_id = config("jae_id")


# Create your views here.
def index(request):
    todos = Todo.objects.all()
    context = {
        'todos': todos,
    }
    return render(request, 'todos/index.html', context)

def create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        due_date = request.POST.get('due-date')
        Todo.objects.create(title=title,due_date=due_date)
        chatbot()
        return redirect('todos:index')
    else:
        return render(request, 'todos/create.html')

def update(request, pk):
    todo = get_object_or_404(Todo, id=pk)

    if request.method == 'POST':
        title = request.POST.get('title')
        due_date = request.POST.get('due-date')
        todo.title = title
        todo.due_date = due_date
        todo.save()
        return redirect('todos:index')
    else:
        context = {
            'todo':todo,
        }   
        return render(request, 'todos/update.html', context)

def delete(request, pk):
    todo = get_object_or_404(Todo, id=pk)
    todo.delete()
    return redirect('todos:index')

def chatbot():
    base = "https://api.telegram.org/bot"
    method = "sendMessage"
    text = "새로운 일정이 생겼어요"
    url1 = base + TOKEN + "/" + method + "?" + "chat_id=" + jin_id + "&" + "text=" + text
    url2 = base + TOKEN + "/" + method + "?" + "chat_id=" + jae_id + "&" + "text=" + text
    response1 = requests.get(url1)
    response2 = requests.get(url2)