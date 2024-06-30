from django.shortcuts import render, redirect
from controls.models import *

# # Create your views here.
def homepage_view(request):
    return render(request, "index.html")
def shop_view(request):
    products = Product.objects.all()  # Retrieve all products
    return render(request, "shop.html", {'products': products})

def sproduct_view(request, product_id):
    sproducts = Product.objects.get(id=product_id)
    return render(request, "sproduct.html", {'product': sproducts})

def blog_view(request):
        # Fetch all registered admins
    blog_posts = BlogPost.objects.all()
    context = {
        'blog_posts': blog_posts
    }
    return render(request, "blog.html", context)

def contact_view(request):
    return render(request, "contact.html")

def cart_view(request):
    return render(request, "cart.html")

def checkout_view(request):
    user = request.user
    context = {
        'user': user,
    }
    return render(request, 'checkout.html', context)

def about_view(request):
    return render(request, "about.html")

def save_message(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message_body = request.POST.get('message')
        message = Message.objects.create(name=name, email=email, subject=subject, message=message_body)
        # Redirect to a success page or any other page
        return redirect('web:contact')
    return redirect('web:contact')  # Redirect back to contact page if not a POST request

from decimal import Decimal

def process_order(request):
    if request.method == 'POST':
        # Extract form data
        email = request.POST.get('email')
        item_name = request.POST.get('item_name')
        total = Decimal(request.POST.get('total', '0'))  # Convert to Decimal
        img = request.POST.get('img')
        size = request.POST.get('size')
        quantity = int(request.POST.get('quantity', '0'))  # Convert to int
        payment_method = request.POST.get('payment_method')

        # Ensure all required form fields are provided
        if not (email and item_name and total and quantity and payment_method):
            # Redirect back to checkout page with error message
            return redirect('web:checkout')  # You may include an error message in the redirect URL

        # Retrieve user by email
        user = CustomUser.objects.filter(email=email).first()
        if user:
            # Retrieve or create order for the user
            order = Order.objects.create(
                customer=user,
                total=total,
                payment_method=payment_method,
                payment_status="Pending"  # You may adjust this default value as needed
            )

            # Retrieve product by name
            product = Product.objects.filter(product_name=item_name).first()
            if product:
                # Add product to the order
                order.products.add(product)
                order.save()
                # Redirect to a success page (e.g., cart page)
                return redirect('web:cart')  # You may adjust the redirect URL as needed

            # Handle case where product is not found
            # Delete the order created for the user
            order.delete()
            # Redirect back to checkout page with error message
            return redirect('web:checkout')  # You may include an error message in the redirect URL

        # Handle case where user is not found
        return redirect('web:checkout')  # Redirect back to checkout page with error message if needed

    # Handle GET request or invalid submission
    return redirect('web:checkout')