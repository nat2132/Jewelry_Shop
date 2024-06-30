from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .forms import PasswordResetForm
from .tokens import generate_token
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import  login, logout, authenticate
from Jewelry__Shop import settings
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse
from .models import *


def user_home(request):
    user = request.user
    return render(request, "user.html", {'user': user})

def user_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('user_signup')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email is already in use.")
            return redirect('user_signup')

        if len(username) > 10:
            messages.error(request, "Username is too long!")
            return redirect('user_signup')

        if len(username) < 5:
            messages.error(request, "Username is too short!")
            return redirect('user_signup')

        if password != confirm_password:
            messages.error(request, "Passwords didn't match!")
            return redirect('user_signup')

        if len(password) < 6:
            messages.error(request, "Passwords length must be greater than 6!")
            return redirect('user_signup')

        # Validate username format
        if not username.isalnum():
            messages.error(request, "Username can only contain letters and numbers.")
            return redirect('user_signup')

        # Create regular user
        myuser = CustomUser.objects.create_user(username, email, password)
        myuser.first_name = fname
        myuser.is_active = False
        myuser.save()
        messages.success(request, "Your Account has been created successfully!! Please check your email to activate your account.")

        # Welcome Email
        subject = "Welcome to Tezeta Tearsures - Login!!"
        message = "Hello " + myuser.first_name + "!! \n" + "Welcome to Tezeta Tearsures!! \nThank you for visiting our website\n. We have also sent you a confirmation email, please confirm your email address. \n\nThanking You!!\nTezeta Tearsures"        
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        # Email Address Confirmation Email
        current_site = get_current_site(request)
        email_subject = "Confirm your Email @ Tezeta Tearsures - Login!!"
        message2 = render_to_string('email_confirmation.html',{
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.fail_silently = True
        email.send()

    return render(request, "user_register.html")

def user_signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        regular_user = authenticate(username=username, password=password)
        print("Authenticated user:", regular_user)

        if regular_user is not None and regular_user.is_active and not regular_user.is_admin:
            if regular_user.is_active and not regular_user.is_admin:
                login(request, regular_user)
                fname = regular_user.full_name
                return render(request, "user.html", {'fname': fname})
            else:
                messages.error(request, "Invalid user account or account is not activated yet.")
                return HttpResponseRedirect('/')
        else:
            messages.error(request, "Invalid username or password!")
            return HttpResponseRedirect('/')
    else:
        return render(request, 'user_register.html')

def user_signout(request):
    logout(request)
    messages.success(request, "You have been signed out")
    return redirect('user_signup')

def user_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
       myuser.is_active = True
       myuser.save()
       login(request, myuser)
       messages.success(request, "Your account has been activated successfully!")
       return redirect('user_signup')
    else:
        return render(request, 'activation_failed.html')

def user_password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            # Retrieve user by email
            user = CustomUser.objects.get(email=email)
            # Send password reset email
            subject = "Password Reset Request"
            message = "Please click the link below to reset your password:\n"
            message += f"{request.build_absolute_uri('/')[:-1]}{reverse('password_recovery', kwargs={'uidb64': urlsafe_base64_encode(force_bytes(user.pk)), 'token': generate_token.make_token(user)})}"
            send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=True)
            messages.success(request, "Password reset email sent successfully. Please check your email.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'user_register'))
        else:
            messages.error(request, form.errors['email'][0])
    else:
        form = PasswordResetForm(request.POST or None)
    return render(request, 'password_reset.html', {'form': form})

def user_password_recovery(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and generate_token.check_token(user, token):
        if request.method == 'POST':
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            if password and confirm_password and password != confirm_password:
                messages.error(request, "The new password and confirmed password do not match.")
            elif password and len(password) < 6:
                messages.error(request, "The new password must be at least 6 in length.")
            else:
                user.set_password(password)
                user.save()
                messages.success(request, "Your password has been reset successfully.")
                return HttpResponseRedirect(reverse('user_signin'))
        return render(request, 'password_recovery.html', {'uidb64': uidb64, 'token': token})
    else:
        messages.error(request, "Invalid password reset link.")
        return HttpResponseRedirect(reverse('user_signin'))

def user_save_profile(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name', '')
        email = request.POST.get('email')
        password = request.POST.get('password')

        errors = []

        if len(username) > 10:
            errors.append("Username is too long!")
        elif len(username) < 5:
            errors.append("Username is too short!")

        if len(password) < 6:
            errors.append("Password length must be greater than 6!")

        if errors:
            for error in errors:
                messages.error(request, error)
            return HttpResponseRedirect(reverse('user_home'))

        user = request.user
        user.username = username
        user.first_name = first_name
        user.email = email

        if password:
            user.set_password(password)

        user.save()

        messages.success(request, "Profile updated successfully!")
        return HttpResponseRedirect(reverse('user_home'))

def admin_home(request):
    user = request.user
    return render(request, "admin.html", {'user': user})

def admin_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('admin_signup')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email is already in use.")
            return redirect('admin_signup')

        if len(username) > 10:
            messages.error(request, "Username is too long!")
            return redirect('admin_signup')

        if len(username) < 5:
            messages.error(request, "Username is too short!")
            return redirect('admin_signup')

        if password != confirm_password:
            messages.error(request, "Passwords didn't match!")
            return redirect('admin_signup')
        
        if len(password) < 6 :
            messages.error(request, "Passwords length must be greater than 6!")
            return redirect('admin_signup')

        # Validate username format
        if not username.isalnum():
            messages.error(request, "Username can only contain letters and numbers.")
            return redirect('admin_signup')

        # Create admin user
        myuser = CustomUser.objects.create_user(username, fname, email, password)
        myuser.first_name = fname
        myuser.is_active = False
        myuser.is_admin = True
        myuser.save()
        messages.success(request, "Your Admin Account has been created successfully!! Please check your email to activate your account.")

        # Welcome Email
        subject = "Welcome to Tezeta Tearsures - Admin Login!!"
        message = "Hello " + myuser.first_name + "!! \n" + "Welcome to Tezeta Tearsures Admin Panel!! \nThank you for registering as an admin on our website. \n\nThanking You!!\nTezeta Tearsures Admin"        
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        
        # Email Address Confirmation Email
        current_site = get_current_site(request)
        email_subject = "Confirm your Email @ Tezeta Tearsures - Admin Login!!"
        message2 = render_to_string('aemail_confirmation.html',{
            
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = EmailMessage(
        email_subject,
        message2,
        settings.EMAIL_HOST_USER,
        [myuser.email],
        )
        email.fail_silently = True
        email.send()

    return render(request, "admin_register.html")

def admin_signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
    
        admin_user = authenticate(username=username, password=password)

        if admin_user is not None and admin_user.is_active and admin_user.is_admin:
            # Check if the user is active
            if admin_user.is_active and admin_user.is_admin:
                login(request, admin_user)
                fname = admin_user.full_name
                return render(request, "admin.html", {'fname': fname})
            
            else:
                # User is not active or not an admin, display appropriate message
                messages.error(request, "Invalid admin user account or account is not activated yet.")
                return HttpResponseRedirect('admin_register')
        else:
            # Authentication failed, handle invalid credentials
            messages.error(request, "Invalid username or password.!")
            return HttpResponseRedirect('admin_register')
    else:
        # Handle GET request for rendering the sign-in form
        return render(request, 'admin_register.html') 

def admin_signout(request):
    logout(request)
    messages.success(request, "You have been signed out")
    return redirect('admin_signup')

def admin_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
       myuser.is_active = True
       myuser.save()
       login(request, myuser)
       messages.success(request, "Your admin account has been activated successfully!")
       return redirect('admin_signup')
    else:
        return render(request, 'activation_failed.html')

def admin_password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            # Retrieve user by email
            user = CustomUser.objects.get(email=email)
            # Send password reset email
            subject = "Admin Password Reset Request"
            message = "Please click the link below to reset your password:\n"
            message += f"{request.build_absolute_uri('/')[:-1]}{reverse('password_recovery', kwargs={'uidb64': urlsafe_base64_encode(force_bytes(user.pk)), 'token': generate_token.make_token(user)})}"
            send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=True)
            messages.success(request, "Admin password reset email sent successfully. Please check your email.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            messages.error(request, form.errors['email'][0])
    else:
        form = PasswordResetForm(request.POST or None)
    return render(request, 'password_reset.html', {'form': form})

def admin_password_recovery(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and generate_token.check_token(user, token):
        if request.method == 'POST':
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            if password and confirm_password and password != confirm_password:
                messages.error(request, "The new password and confirmed password do not match.")
            elif password and len(password) < 6:
                messages.error(request, "The new password must be at least 6 characters long.")
            else:
                user.set_password(password)
                user.save()
                messages.success(request, "Admin password has been reset successfully.")
                return HttpResponseRedirect(reverse('admin_signin'))
        return render(request, 'password_recovery.html', {'uidb64': uidb64, 'token': token})
    else:
        messages.error(request, "Invalid password reset link.")
        return HttpResponseRedirect(reverse('admin_signin'))    

def admin_save_profile(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name', '')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Perform validation
        errors = []

        if len(username) > 10:
            errors.append("Username is too long!")
        elif len(username) < 5:
            errors.append("Username is too short!")

        if len(password) < 6:
            errors.append("Password length must be greater than 6!")

        if errors:
            for error in errors:
                messages.error(request, error)
            return HttpResponseRedirect(reverse('admin_home'))

        # Update the user's profile
        user = request.user
        user.username = username
        user.first_name = first_name
        user.email = email

        if password:
            user.set_password(password)

        user.save()

        messages.success(request, "Admin profile updated successfully!")
        return HttpResponseRedirect(reverse('admin_home'))


