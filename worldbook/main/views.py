from django.shortcuts import render

# Create your views here.


def home(request):
    context = {
        'title': 'Главная страница',
        'content': 'Контент на главной странице',
    }

    return render(request, template_name='main/base.html', context=context)


def about(request):
    context = {
        'title': 'О нас',
        'content': 'Контент на странице о Нас!',
    }

    return render(request, template_name='main/about.html', context=context)
