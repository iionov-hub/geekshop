import os
import json

#главная директория (mainapp)
dir = os.path.dirname(__file__)

from django.shortcuts import render
from django.core.paginator import Paginator
import datetime
from mainapp.models import Product, ProductCategory
# Create your views here.
# функции = вьюхи = контроллеры
def index(request):
    context = {'title': 'GeekShop'}
    return render(request, 'mainapp/index.html',context)


def products(request, category_id=None, page=1):

    context = {'date_time': datetime.datetime.now(),
                'title': 'GeekShop - Каталог',
                'categories': ProductCategory.objects.all(),
    }

    if category_id:
        products = Product.objects.filter(category_id=category_id).order_by('-price')
        #context.update({'products': Product.objects.filter(category_id=category_id)})
    else:
        products = Product.objects.all().order_by('-price')
        #context.update({'products': Product.objects.all()})
    paginator = Paginator(products, 3)#Постраничный вывод объектов 3 объекта на странице
    products_paginator = paginator.page(page)#Выбираем страницу со списком продуктов
    context.update({'products': products_paginator})#в контексте указываем список продуктов
    #путь к файлу products.json
    #file_path = os.path.join(dir, 'fixtures/products.json')
    #меняем контекст на данные с джейсона
    # context.update(json.load(open(file_path, encoding='utf-8')))
    return render(request, 'mainapp/products.html', context)