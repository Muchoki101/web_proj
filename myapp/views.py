from django.shortcuts import render, redirect
from myapp.models import Product, Users


# Create your views here.
def home(request):
    return render(request, 'home.html')

def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def signup_view(request):
    if request.method == "POST":
        user_name = request.POST.get('user_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')


        if password != confirm_password:
            return render(request, 'register.html', {'error': 'Passwords do not match!'})


        if Users.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': 'Email is already registered!'})
        if Users.objects.filter(user_name=user_name).exists():
            return render(request, 'register.html', {'error': 'Username is already taken!'})


        user = Users(user_name=user_name, email=email, password=password)
        user.save()

        return redirect('login')

    return render(request, 'register.html')

def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')


        try:
            user = Users.objects.get(email=email)
            if user.password == password:

                return redirect('home')
            else:
                return render(request, 'login.html', {'error': 'Incorrect password!'})
        except Users.DoesNotExist:
            return render(request, 'login.html', {'error': 'User does not exist!'})

    return render(request, 'login.html')
def sales(request):
    if request.method == "POST":
        prod_name = request.POST['prod_name']
        prod_price = request.POST['prod_price']
        prod_category = request.POST['prod_category']
        prod_desc = request.POST['prod_desc']
        prod_qty = request.POST['prod_qty']
        prod_img = request.FILES['prod_img']

        product = Product(
             prod_name=prod_name,
             prod_price=prod_price,
             prod_category=prod_category,
             prod_desc=prod_desc,
             prod_qty=prod_qty,
             prod_img=prod_img
        )

        product.save()
        return redirect('/')
    return render(request, 'sales_form.html')