from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import *

def index(request):
    Model = Good
    template_name = 'testmarket/index.html'
    goods = Model.objects.all()
    return render(request, template_name, {
        'goods': goods,
    })
