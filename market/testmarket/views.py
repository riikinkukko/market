from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate

from .models import *
from .forms import RegistrationForm, LoginForm

def index(request):
    """
    Args:
        request:

    Returns:
        render index.html
    """
    Model = Good
    model_basket = Basket
    template_name = 'testmarket/index.html'
    goods = Model.objects.all()
    user_id = request.user.id

    if request.method == 'POST':
        good_id = request.POST.get('button')
        user_basket = model_basket.objects.get_or_create(user_id=user_id)
        user_basket = model_basket.objects.get(user_id=user_id)
        if str(good_id) not in user_basket.goods_id.split(","):
            user_basket.goods_id += str(good_id)+','
            user_basket.save()
    return render(request, template_name, {
        'goods': goods,
    })

def register(request):
    """
    Args:
        request:

    Returns:
        register.html
    """
    template_name = 'testmarket/registration.html'
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.save()
            return redirect('login')
    else:
        user_form = RegistrationForm()
    return render(request, template_name, {'user_form': user_form})

def login_view(request):
    """
    Args:
        request:

    Returns:
        login.html
    """
    template_name = 'testmarket/login.html'
    form = LoginForm
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Неверные учетные данные. Попробуйте еще раз.'
    else:
        error_message = ''
    return render(request, template_name, {'form': form, 'error_message': error_message})

def logout_view(request):
    """
    Args:
        request:

    Returns:
        logout to login.html
    """
    logout(request)
    return redirect('login')

@login_required
def basket_view(request):
    """
    Args:
        request:

    Returns:
        basket.html
    """

    model_Basket = Basket
    model_Good = Good
    user_id = request.user.id

    l = []

    person_basket = model_Basket.objects.get_or_create(user_id=user_id)
    person_basket = model_Basket.objects.get(user_id=user_id)
    for i in list(person_basket.goods_id.split(","))[:-1]:
        l.append([
            model_Good.objects.get(id=int(i)).name,
            model_Good.objects.get(id=int(i)).price,
            model_Good.objects.get(id=int(i)).short_description,
            model_Good.objects.get(id=int(i)).image,
        ])

    return render(request, 'testmarket/basket.html', {
        'list': l,
    })