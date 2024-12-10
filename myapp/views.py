from datetime import date
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from .models import Product
from django.db.models import Avg
from django.db.models import Sum, F, Max
from django.utils import timezone
from datetime import datetime
from .forms import ExpenseForm
from .models import Product, Expense
from calendar import monthrange



# Create your views here.
def home(request):
    return render(request, 'home.html')
def sales_form(request):
    return render(request, 'sales_form.html')

def register(request):
    if request.method == "POST":
        user_name = request.POST.get('user_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(request, 'register.html', {'error': 'Passwords do not match!'})

        if User.objects.filter(username=user_name).exists():
            return render(request, 'register.html', {'error': 'Username is already taken!'})
        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': 'Email is already registered!'})

        # Create User
        user = User.objects.create_user(username=user_name, email=email, password=password)
        user.save()
        return redirect('login')

    return render(request, 'register.html')

def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            auth_user = authenticate(username=user.username, password=password)
            if auth_user:
                auth_login(request, auth_user)  # Login user
                return redirect('home')
            else:
                return render(request, 'login.html', {'error': 'Incorrect password!'})
        except User.DoesNotExist:
            return render(request, 'login.html', {'error': 'User does not exist!'})

    return render(request, 'login.html')

@login_required
def sales(request):
    if request.method == "POST":
        prod_name = request.POST['prod_name']
        prod_price = request.POST['prod_price']
        prod_category = request.POST['prod_category']
        prod_desc = request.POST['prod_desc']
        prod_qty = request.POST['prod_qty']
        prod_img = request.FILES['prod_img']

        product = Product(
            user=request.user,  # Associate product with logged-in user
            prod_name=prod_name,
            prod_price=prod_price,
            prod_category=prod_category,
            prod_desc=prod_desc,
            prod_qty=prod_qty,
            prod_img=prod_img
        )
        product.save()
        return redirect('sales_view')
    products = Product.objects.filter(user=request.user)
    return render(request, 'sales_view.html', {'products': products})

@login_required
def update_product(request, id):
    product = Product.objects.get(id=id)
    if request.method == "POST":
        prod_name = request.POST['prod_name']
        prod_price = request.POST['prod_price']
        prod_category = request.POST['prod_category']
        prod_desc = request.POST['prod_desc']
        prod_qty = request.POST['prod_qty']
        prod_img = request.FILES['prod_img']

        product.prod_name = prod_name
        product.prod_price = prod_price
        product.prod_category = prod_category
        product.prod_desc = prod_desc
        product.prod_qty = prod_qty
        product.prod_img = prod_img


        product.save()
        return redirect('sales_view')

    return render(request, 'update_product.html', {'product': product})

def delete_product(request, id):
    product = Product.objects.get(pk=id)
    product.delete()
    return redirect('sales_view')


def visual_report(request):
    # Restrict to logged-in user's products
    products = Product.objects.filter(user=request.user).values('prod_name').annotate(
        total_sales=Sum('prod_qty'),
        total_sales_value=Sum(F('prod_price') * F('prod_qty'))
    )

    # Prepare data for the chart
    product_names = [product['prod_name'] for product in products]
    product_sales = [product['total_sales'] for product in products]
    product_sales_value = [product['total_sales_value'] for product in products]

    # Calculate overall metrics
    total_sales = sum(product_sales_value)
    total_products = len(products)
    avg_price = Product.objects.filter(user=request.user).aggregate(Avg('prod_price'))['prod_price__avg']
    best_selling_product = Product.objects.filter(user=request.user).order_by('-prod_qty').first()

    context = {
        'total_sales': total_sales,
        'total_products': total_products,
        'avg_price': avg_price,
        'best_selling_product': best_selling_product.prod_name if best_selling_product else 'None',
        'product_names': product_names,
        'product_sales': product_sales,
        'product_sales_value': product_sales_value,
    }

    return render(request, 'visual_report.html', context)



def single_day_report(request):
    date_str = request.GET.get('date', str(timezone.now().date()))
    date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()

    # Restrict to the logged-in user's products
    products = Product.objects.filter(user=request.user, created_at__date=date_obj)

    # Aggregate sales data by normalized product name
    product_sales = products.values('prod_name', 'prod_category', 'prod_price').annotate(total_qty=Sum('prod_qty'))

    # Category-wise sales for the pie chart
    categories_sales = products.values('prod_category').annotate(total_qty=Sum('prod_qty'))

    context = {
        'date': date_str,
        'product_sales': product_sales,
        'categories_sales': categories_sales,
    }
    return render(request, 'single_day_report.html', context)



@login_required
def month_report(request):
    # Get the month and year from the query parameter (if available)
    month_str = request.GET.get('month', str(timezone.now().month))  # Default to current month if no month is provided
    year_str = request.GET.get('year', str(timezone.now().year))  # Default to current year if no year is provided

    # Convert to integers
    month = int(month_str)
    year = int(year_str)

    # Get the start and end dates for the given month and year
    start_date = datetime(year, month, 1)
    end_date = datetime(year, month + 1, 1) if month != 12 else datetime(year + 1, 1, 1)

    # Filter products by the specific month for the logged-in user
    products = Product.objects.filter(user=request.user, created_at__range=[start_date, end_date])

    # Prepare data for the pie chart (product categories and their sales quantity)
    categories_sales = products.values('prod_category').annotate(total_qty=Sum('prod_qty'))

    # Prepare data for the table (products and their sales quantity)
    product_sales = products.values('prod_name', 'prod_category', 'prod_price').annotate(total_qty=Sum('prod_qty'))

    # Prepare context data
    context = {
        'month': f'{month}/{year}',
        'categories_sales': categories_sales,
        'product_sales': product_sales,
    }

    return render(request, 'month_report.html', context)




@login_required
def sales_view(request):
    # Fetch products only for the logged-in user
    products = Product.objects.filter(user=request.user)
    return render(request, 'sales_view.html', {'products': products})



@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user  # Associate with logged-in user
            expense.save()
            return redirect('view_expenses')
    else:
        form = ExpenseForm()
    return render(request, 'add_expense.html', {'form': form})

@login_required
def view_expenses(request):
    # Fetch expenses only for the logged-in user
    expenses = Expense.objects.filter(user=request.user)
    return render(request, 'view_expenses.html', {'expenses': expenses})



@login_required
def business_performance(request):
    # Get the current month and year
    current_month = timezone.now().month
    current_year = timezone.now().year
    days_in_month = monthrange(current_year, current_month)[1]  # Total days in the current month

    # Get sales data grouped by day for the logged-in user
    sales = (
        Product.objects.filter(user=request.user, created_at__month=current_month, created_at__year=current_year)
        .annotate(day=F('created_at__day'))
        .values('day')
        .annotate(daily_sales=Sum(F('prod_price') * F('prod_qty')))
    )

    # Get expenses data grouped by day for the logged-in user
    expenses = (
        Expense.objects.filter(user=request.user, date__month=current_month, date__year=current_year)
        .annotate(day=F('date__day'))
        .values('day')
        .annotate(daily_expenses=Sum('amount'))
    )

    # Prepare data for the graph
    dates = list(range(1, days_in_month + 1))  # All days in the current month
    sales_data = {entry['day']: entry['daily_sales'] for entry in sales}
    expenses_data = {entry['day']: entry['daily_expenses'] for entry in expenses}

    # Match sales and expenses to each day, defaulting to 0 if no data
    sales_trend = [sales_data.get(day, 0) for day in dates]
    expenses_trend = [expenses_data.get(day, 0) for day in dates]

    # Calculate total sales and expenses
    total_sales = sum(sales_trend)
    total_expenses = sum(expenses_trend)

    # Calculate profit
    profit = total_sales - total_expenses

    # Prepare context data
    context = {
        'dates': dates,  # X-axis labels
        'sales_trend': sales_trend,  # Sales data for the graph
        'expenses_trend': expenses_trend,  # Expenses data for the graph
        'total_sales': total_sales,
        'total_expenses': total_expenses,
        'profit': profit,
        'current_month': timezone.now().strftime('%B'),  # Month name
        'current_year': current_year,
    }

    return render(request, 'business_performance.html', context)

def custom_logout(request):
    logout(request)
    return redirect('login')
