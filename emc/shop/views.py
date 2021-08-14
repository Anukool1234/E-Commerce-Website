from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Orders, OrderUpdate, Contact
from math import ceil

def index(request):
    # products = Product.objects.all()
    # print(products)
    # n = len(products)
    # nslide = n//4 + ceil((n/4)-(n//4))
    allprods = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods }
    for cat in cats:
      prod = Product.objects.filter(category=cat)
      n = len(prod)
      nslide = n // 4 + ceil((n / 4) - (n // 4))
      allprods.append([prod, range(nslide),nslide])
    # param = {'no_of_slide': nslide,'range':range(nslide) ,'product': products}
    # allprods = [[products, range(nslide),nslide],[products, range(nslide),nslide]]
    param = {'allprods':allprods}
    return render(request,'shop/index.html',param)

def about(request):
    # return HttpResponse("hi am about")
    return render(request,'shop/about.html')

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
    return render(request, 'shop/contact.html')

def tracker(request):
    return render(request,'shop/tracker.html')

def search(request):
    return HttpResponse("hi am search")

def productview(request,myid):
    product = Product.objects.filter(id=myid)
    return render(request,'shop/prodview.html',{'product':product[0]})

def checkout(request):
    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')

        order = Orders(items_json=items_json, name=name, email=email, address=address, city=city, state=state,
                       zip_code=zip_code, phone=phone)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        return render(request, 'shop/checkout.html', {'thank': thank, 'id': id})
    return render(request, 'shop/checkout.html')