from django.shortcuts import redirect, render

# Create your views here.
def index(request):
    return render(request,'index.html')
def home(request):
    return render(request,'home.html')



from .models import UserRegister

def register(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        profile_pic = request.FILES.get('profile_pic')
        age = request.POST.get('age')
        phone = request.POST.get('phone')
        if UserRegister.objects.filter(email=email).exists():
            return render(request, 'register.html', {
                'error': 'Account already exists with this email.'
            })
        UserRegister.objects.create(
            name=name,
            email=email,
            password=password,
            profile_pic=profile_pic,
            age=age,
            phone=phone
           
        )

        return redirect('login')  # Redirect to the login page after successful registration

    return render(request, 'register.html')

def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = UserRegister.objects.get(email=email)
            if user.password == password:
                request.session['email'] = user.email

                return redirect('home')  # Redirect to the home page after successful login
            else:
                return render(request, 'login.html', {
                    'error': 'Invalid email or password.'
                })
        except UserRegister.DoesNotExist:
            return render(request, 'login.html', {
                'error': 'Invalid email or password.'
            })

    return render(request, 'login.html')

from django.shortcuts import render, redirect
from .models import UserRegister

def profile(request):
    if 'email' not in request.session:
        return redirect('login')

    user = UserRegister.objects.get(email=request.session['email'])

    return render(request, 'profile.html', {'user': user})
from django.shortcuts import render, redirect
from .models import UserRegister

def edit_profile(request):
    if 'email' not in request.session:
        return redirect('login')

    user = UserRegister.objects.get(email=request.session['email'])

    if request.method == 'POST':
        user.name = request.POST.get('name')
        user.age = request.POST.get('age')
        user.phone = request.POST.get('phone')

        if request.FILES.get('profile_pic'):
            user.profile_pic = request.FILES['profile_pic']

        user.save()

        return redirect('profile')

    return render(request, 'edit_profile.html', {'user': user})
from django.shortcuts import render, redirect
from .models import UserRegister, Product

def add_product(request):
    if request.method == "POST":
        email = request.session.get('email')

        user = UserRegister.objects.get(email=email)

        Product.objects.create(
            user=user,
            product_name=request.POST.get('product_name'),
            description=request.POST.get('description'),
            price=request.POST.get('price'),
            product_image=request.FILES.get('product_image'),
            stock=request.POST.get('stock')  # Add stock field
        )

        return redirect('product_list')   # change if needed

    return render(request, 'add_product.html')
from django.shortcuts import render
from .models import Product

def product_list(request):
    products = Product.objects.all()

    return render(request, 'product_list.html', {
        'products': products
    })
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, UserRegister

def my_products(request):
    email = request.session.get('email')

    user = UserRegister.objects.get(email=email)
    print(user.email)
    print(user.name)

    products = Product.objects.filter(user=user)

    return render(request, 'my_products.html', {
        'products': products
    })
def edit_product(request, id):
    email = request.session.get('email')

    user = UserRegister.objects.get(email=email)

    product = get_object_or_404(Product, id=id, user=user)
    
    if request.method == "POST":
        helo=request.POST.get('stock')
        print(helo)
        product.product_name = request.POST.get('product_name')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        product.stock = request.POST.get('stock')  # Update stock field

        if request.FILES.get('product_image'):
            product.product_image = request.FILES.get('product_image')

        product.save()

        return redirect('my_products')

    return render(request, 'edit-product.html', {
        'product': product
    })
def delete_product(request, id):
    email = request.session.get('email')

    user = UserRegister.objects.get(email=email)

    product = get_object_or_404(Product, id=id, user=user)

    product.delete()

    return redirect('my_products')
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Cart, UserRegister

def add_to_cart(request, id):
    email = request.session.get('email')

    if not email:
        return redirect('login')

    user = UserRegister.objects.get(email=email)
    product = get_object_or_404(Product, id=id)

    if request.method == "POST":
        quantity = int(request.POST.get('quantity'))

        if quantity > product.stock:
            quantity = product.stock

        cart_item = Cart.objects.filter(
            user=user,
            product=product
        ).first()

        if cart_item:
            new_quantity = cart_item.quantity + quantity

            if new_quantity > product.stock:
                new_quantity = product.stock

            cart_item.quantity = new_quantity
            cart_item.save()
        else:
            Cart.objects.create(
                user=user,
                product=product,
                quantity=quantity
            )

        return redirect('cart')

    return render(request, 'add_to_cart.html', {
        'product': product
    })

def cart(request):
    email = request.session.get('email')

    user = UserRegister.objects.get(email=email)

    cart_items = Cart.objects.filter(user=user)

    total = 0

    for item in cart_items:
        total += item.product.price * item.quantity

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })
def remove_cart(request, id):
    email = request.session.get('email')

    user = UserRegister.objects.get(email=email)

    item = get_object_or_404(
        Cart,
        id=id,
        user=user
    )

    item.delete()

    return redirect('cart')
from django.shortcuts import render, redirect, get_object_or_404
from .models import *

def update_cart(request, id):
    email = request.session.get('email')

    user = UserRegister.objects.get(email=email)

    cart_item = get_object_or_404(
        Cart,
        id=id,
        user=user
    )

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))

        # Check stock availability
        if quantity <= cart_item.product.stock and quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()

    return redirect('cart')