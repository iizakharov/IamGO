from django.shortcuts import render


def main(request):
    title = 'Главная'
    context = {
        'title': title
    }
    return render(request, 'mainapp/index.html', context)


def product(request):
    content = {
        'title': 'Мероприятие',
    }

    return render(request, 'mainapp/product.html', content)
