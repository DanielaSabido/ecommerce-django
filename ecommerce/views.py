#crear una funcion que haga asociacion al template a futuro
from django.shortcuts import render
from store.models import Product
def home(request):

    #hacer una consulta para la bd
    products=Product.objects.all().filter(is_available=True)
    context={
        'products':products,
    }


    return render(request,'home.html', context)
