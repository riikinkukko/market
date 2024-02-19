from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.db.models import Q
from django.views.generic import ListView, DetailView

from .models import *
from .forms import RegistrationForm, LoginForm

def index(request, *args, **kwargs):
    """
    Args:
        request:

    Returns:
        render index.html
    """
    Model = Good
    model_basket = Basket
    template_name = 'testmarket/index.html'
    user_id = request.user.id
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    goods = Model.objects.filter(name__iregex=q)

    if request.method == 'POST' and user_id is not None:
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
    return render(request, template_name, {
        'user_form': user_form
                   })

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
    return render(request, template_name, {
        'form': form, 'error_message': error_message
    })

def logout_view(request):
    """
    Args:
        request:

    Returns:
        logout to login.html
    """
    logout(request)
    return redirect('login')

@login_required #Можно поменять в шаблоне на высветку авторизации
def basket_view(request):
    """
    Args:
        request:

    Returns:
        basket.html
    Добавить удаление из корзины, количество штук
    """

    model_Basket = Basket
    model_Good = Good
    template_name = 'testmarket/basket.html'
    user_id = request.user.id
    all_cost = 0
    l = []
    counter = 1
    person_basket = model_Basket.objects.get_or_create(user_id=user_id)
    person_basket = model_Basket.objects.get(user_id=user_id)
    for i in list(person_basket.goods_id.split(","))[:-1]:
        l.append([
            model_Good.objects.get(id=int(i)).name,
            model_Good.objects.get(id=int(i)).price,
            model_Good.objects.get(id=int(i)).short_description,
            model_Good.objects.get(id=int(i)).image,
            model_Good.objects.get(id=int(i)).id,
        ])
        counter += 1
        all_cost += model_Good.objects.get(id=int(i)).price

        if request.method == 'POST':
            id = request.POST.get('button-delete')
            person_basket = model_Basket.objects.get(user_id=user_id)
            s = person_basket.goods_id
            lst = [i for i in s.split(",")]
            lst.remove(str(id))
            person_basket.goods_id = ','.join(lst)
            person_basket.save()
            return redirect('basket')

    return render(request, template_name, {
        'list': l,
        'all_cost': all_cost,
    })

def item_view(request, product_id):
    """
    Args:
        request:
        product_id: int из ссылки

    Returns:
        good card
        good.html
    """
    template_name = 'testmarket/good.html'
    model = Good
    model_Basket = Basket
    product = Good.objects.filter(id=product_id)
    user_id = request.user.id

    if request.method == 'POST' and user_id is not None:
        good_id = request.POST.get('btn-good')
        user_basket = model_Basket.objects.get_or_create(user_id=user_id)
        user_basket = model_Basket.objects.get(user_id=user_id)
        if str(good_id) not in user_basket.goods_id.split(","):
            user_basket.goods_id += str(good_id) + ','
            user_basket.save()
    return render(request, template_name, {
        'product': product,
    })
