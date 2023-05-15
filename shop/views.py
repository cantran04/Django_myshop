from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from . models import Cart, Customer, Product
from . forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from .forms import LoginForm

# Create your views here.
def index(request): 
    return render(request, 'pages/home.html')

def about(request): 
    return render(request, 'pages/about.html')

def contact(request): 
    return render(request, 'pages/contact.html')

class CategoryView(View):
    def get(sefl,request,val): 
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request, 'pages/category.html',locals())
    

class CategoryTitle(View):
    def get(sefl,request,val): 
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        return render(request, 'pages/category.html',locals())
 

class ProductDetail(View):
    def get(sefl,request,pk): 
        product = Product.objects.get(pk=pk)
        return render(request, 'pages/productdetail.html',locals())
    

class CustomerRegistetrationView(View):
    def get(sefl, request):
        form = CustomerRegistrationForm()
        return render(request, 'pages/customerregistration.html',locals())
    
    def post(sefl, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulation! User Register Successfully")
        else:
            messages.warning(request, "Invalid Input Data")
        return render(request, 'pages/customerregistration.html', locals())


class ProfileView(View):
    def get(self, request):
        form= CustomerProfileForm()
        return render(request, 'pages/profile.html', locals())
    def post(self, request):
        form= CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            
            reg = Customer(user=user, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, "Congratulation! Profile Save Successfully")
        else:
            messages.warning(request, "Invalid Input Data")
        return render(request, 'pages/profile.html', locals())
    

def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'pages/address.html',locals())

class updateAddress(View):
    def get(self, request, pk):
        form= CustomerProfileForm()
        return render(request, 'pages/updateAddress.html', locals())
    def post(self, request, pk):
        form= CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            
            add.save()
            messages.success(request, "Congratulation! Profile Save Successfully")
        else:
            messages.warning(request, "Invalid Input Data")
        return redirect("address")
    

def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'pages/address.html',locals())


def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')

def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount = amount + 40
    return render(request, 'pages/addtocart.html',locals())

class checkout(View):
    def get(self, request):
        user = request.user
        add=Customer.objects.filter(user=user)
        cart_item = Cart.objects.filter(user=user)
        famount = 0
        for p in cart_item:
            value = p.quantity * p.product.discounted_price
            famount = famount + value
        totalamount = famount + 40
        return render(request, 'pages/checkout.html', locals())



def plus_cart(request):
    if request.method == "GET":
        prod_id = request.GET.get('prod_id')
        user = request.user
        carts = Cart.objects.filter(product=prod_id, user=user)
        if carts.exists():
            c = carts.first()
            c.quantity += 1
            c.save()
            cart = Cart.objects.filter(user=user)
            amount = 0
            for p in cart:
                value = p.quantity * p.product.discounted_price
                amount = amount + value
            totalamount = amount + 40
            data = {
                'quantity': c.quantity,
                'amount': amount,
                'totalamount': totalamount
            }
            return JsonResponse(data)
        else:
            return HttpResponse("Error: Cart does not exist.")


# def plus_cart(request):
#     if request.method == "GET":
#         prod_id = request.GET['prod_id']
#         user = request.user
#         c = Cart.objects.get(product=prod_id, user=user)
#         c.quantity += 1
#         c.save()
#         cart = Cart.objects.filter(user=user)
#         amount = 0
#         for p in cart:
#             value = p.quantity * p.product.discounted_price
#             amount = amount + value
#         totalamount = amount + 40
#         data = {
#             'quantity': c.quantity,
#             'amount': amount,
#             'totalamount': totalamount
#         }
#         return JsonResponse(data)
    

def minus_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        user = request.user
        c = Cart.objects.get(product=prod_id, user=user)
        c.quantity -= 1
        c.save()
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)


def remove_cart(request):
    if request.method == "GET":
        prod_id = request.GET.get('prod_id')
        user = request.user
        try:
            cart_item  = Cart.objects.filter(product=prod_id, user=user).first()
            cart_item.delete()
            cart_items = Cart.objects.filter(user=user)
            amount = sum(item.quantity * item.product.discounted_price for item in cart_items)
            total_amount = amount + 40
            data = {
                'amount': amount,
                'totalamount': total_amount
            }
            return JsonResponse(data)
        except Cart.DoesNotExist:
            return HttpResponse("Error: Cart does not exist.")

# def remove_cart(request):
#     if request.method == "GET":
#         prod_id = request.GET['prod_id']
#         user = request.user
#         try:
#             c = Cart.objects.get(product=prod_id, user=user)
#             c.delete()
#         except Cart.DoesNotExist:
#             pass
#         cart = Cart.objects.filter(user=user)
#         amount = 0
#         for p in cart:
#             value = p.quantity * p.product.discounted_price
#             amount = amount + value
#         totalamount = amount + 40
#         data = {
#             'amount': amount,
#             'totalamount': totalamount
#         }
#         return JsonResponse(data)

