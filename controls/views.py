from django.shortcuts import render, redirect
from .models import *
from authentication.models import CustomUser
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Newsletter


# Create your views here.
def ahomepage(request):
    return render(request, "aindex.html")

def acontrol_view(request):
    # Fetch all registered admins
    admins = CustomUser.objects.filter(is_admin=True)

    # Pass the admins to the template context
    context = {
        'admins': admins
    }

    return render(request, 'admin-control.html', context)

def adproduct_view(request):
    return render(request, "add-product.html")

def aproducts_view(request):
        # Fetch all registered admins
    products = Product.objects.all()

    # Pass the admins to the template context
    context = {
        'products': products
    }
    return render(request, "products.html", context)

def customers_view(request):
    # Fetch all registered admins
    customers = CustomUser.objects.filter(is_admin=False)

    # Pass the admins to the template context
    context = {
        'customers': customers
    }

    return render(request, 'customers.html', context)


def aform_view(request):
    return render(request, "blog.html")

def analytics_view(request):
    return render(request, "analytics.html")

def cform_view(request):
    return render(request, "customer-form.html")

def messages_view(request):
        # Fetch all registered admins
    messages = Message.objects.all()

    # Pass the admins to the template context
    context = {
        'messages': messages
    }
    return render(request, "messages.html", context)

def news_view(request):
    # Fetch all registered admins
    blog_posts = BlogPost.objects.all()
    context = {
        'blog_posts': blog_posts
    }
    return render(request, 'newsletter.html', context)

def order_view(request):
    orders = Order.objects.all()
    context = {
        'orders': orders
    }
    return render(request, "orders.html", context)

def add_customer(request):
    if request.method == 'POST':
        # Handle form submission
        username = request.POST['username']
        first_name = request.POST['first_name']
        email = request.POST['email']
        password = request.POST['password']
        
        user = CustomUser.objects.create_user(username=username, first_name=first_name, email=email, password=password)
        return redirect('admins:customers')
    return render(request, 'customer-form.html')

def update_customer(request, user_id):
    if request.method == 'POST':
        users = CustomUser.objects.get(id=user_id)
        # Handle form submission
        users.username = request.POST['username']
        users.first_name = request.POST['first_name']
        users.email = request.POST['email']
        users.save()
        return redirect('admins:customers')
    else:
        # Retrieve the product object with given product_id
        users = CustomUser.objects.get(id=user_id)
        
        # Render the update product form with product data
        return render(request, 'customer-form.html', {'users': users})

def delete_customer(request, user_id):
    users = CustomUser.objects.get(id=user_id)
    users.delete()
    return redirect('admins:customers')

def add_admin(request):
    if request.method == 'POST':
        # Handle form submission
        username = request.POST['username']
        first_name = request.POST['first_name']
        email = request.POST['email']
        password = request.POST['password']
        
        admin = CustomUser.objects.create_user(username=username, first_name=first_name, email=email, password=password, is_admin=True)
        return redirect('admins:acontrol')
    return render(request, 'admin-form.html')

def update_admin(request, user_id):
    if request.method == 'POST':
        admin = CustomUser.objects.get(id=user_id)
        # Handle form submission
        admin.username = request.POST['username']
        admin.first_name = request.POST['first_name']
        admin.email = request.POST['email']
        admin.save()
        return redirect('admins:acontrol')
    else:
        # Retrieve the product object with given product_id
        admin = CustomUser.objects.get(id=user_id)
        
        # Render the update product form with product data
        return render(request, 'admin-form.html', {'admin': admin})

def delete_admin(request, user_id):
    admin = CustomUser.objects.get(id=user_id)
    admin.delete()
    return redirect('admins:acontrol')


def add_product(request):
    if request.method == 'POST':
        # Handle form submission to add a new product
        product_name = request.POST.get('product_name')
        category = request.POST.get('product_category')
        product_size = request.POST.get('product_size')
        product_price = request.POST.get('product_price')
        description = request.POST.get('description')
        main_img_url = request.POST.get('main_image_url')
        
        # Create the product instance
        new_product = Product.objects.create(
            product_name=product_name,
            category=category,
            product_size=product_size,
            product_price=product_price,
            description=description,
            main_image_url=main_img_url
        )
        
        # Handling multiple images
        images = request.FILES.getlist('image')  # Assuming 'image' is the name of the input field for images
        image_urls = request.POST.getlist('image_url')  # Assuming 'image_url' is the name of the input field for image URLs
        
        # Create product image instances for each image or URL
        for image in images:
            ProductImage.objects.create(
                product=new_product,
                image=image
            )
        
        for url in image_urls:
            ProductImage.objects.create(
                product=new_product,
                image_url=url
            )

        return redirect('admins:products')  # Redirect to the products page
    else:
        # Render the add product form
        return render(request, 'add-product.html', {'main_image_url':'','image_url': '', 'image': ''})

def update_product(request, product_id):
    if request.method == 'POST':
        # Retrieve the existing product object with the given product_id
        product = Product.objects.get(pk=product_id)
        
        # Update the attributes of the existing product
        product.product_name = request.POST.get('product_name')
        product.category = request.POST.get('product_category')
        product.product_size = request.POST.get('product_size')
        product.product_price = request.POST.get('product_price')
        product.description = request.POST.get('description')
        product.main_image_url = request.POST.get('main_image_url')
        
        # Save the updated product object
        product.save()

        # Update the associated product images if provided
        images = request.FILES.getlist('image')  # Assuming 'image' is the name of the input field for images
        image_urls = request.POST.getlist('image_url')  # Assuming 'image_url' is the name of the input field for image URLs
        
        # Create new product image instances for each image or URL
        for image in images:
            ProductImage.objects.create(
                product=product,
                image=image
            )
        
        for url in image_urls:
            ProductImage.objects.create(
                product=product,
                image_url=url
            )
        
        return redirect('admins:products')  # Redirect to the products page
    else:
        # Retrieve the product object with the given product_id
        product = Product.objects.get(pk=product_id)

        product_images = product.productimage_set.all()
        
        # Render the update product form with product data
        return render(request, 'add-product.html', {'product': product, 'product_images': product_images})

def delete_product(request, product_id):
    # Retrieve the product object with given product_id and delete it
    product = Product.objects.get(pk=product_id)
    product.delete()
    # Redirect to the products page
    return redirect('admins:products')

def delete_message(request, message_id):
    # Retrieve the product object with given product_id and delete it
    message = Message.objects.get(id=message_id)
    message.delete()
    # Redirect to the products page
    return redirect('admins:messages')


def create_blog(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        BlogPost.objects.create(title=title, description=description, image=image)
        return redirect('admins:news')

def update_blog(request, blog_id):
    if request.method == 'POST':
        blog_post = BlogPost.objects.get(id=blog_id)
        title = request.POST.get('title')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        blog_post.update_post(title, description, image)
        return redirect('admins:news')
    else:
        # Retrieve the product object with given product_id
        blog_post = BlogPost.objects.get(id=blog_id)
        
        # Render the update product form with product data
        return render(request, 'newsletter.html', {'blog_post': blog_post})

def delete_blog(request, blog_id):
        blog_post = BlogPost.objects.get(id=blog_id)
        blog_post.delete()
        return redirect('admins:news')

def newsletter(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        product_title = request.POST.get('product_title')
        description = request.POST.get('description')
        product_description = request.POST.get('product_description')
        image_url = request.FILES.get('image').url  # Assuming 'image' is the name of your file input
        
        # Update the newsletter template with the provided data
        rendered_template = render_to_string('tt-newsletter.html', {
            'title': title,
            'product_title': product_title,
            'description': description,
            'product_description': product_description,
            'image_url': image_url,
        })

        # Get email addresses of subscribed customers
        subscribed_customers = CustomUser.objects.filter(subscription='newsletter').values_list('email', flat=True)
        
        # Send the newsletter email to subscribed customers
        for email in subscribed_customers:
            send_mail(
                title,
                f"{product_title}\n\n{description}\n\n{product_description}",
                'your_email@example.com',
                [email],
                html_message=rendered_template,  # Use the rendered template as HTML content
                fail_silently=False,
            )
    
    return render(request, 'newsletter.html')


def delete_order(request, order_id):
    order = Order.objects.get(id=order_id)
    order.delete()
    return redirect('admins:order')
