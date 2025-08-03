from django.shortcuts import render, redirect

from .models import Room, Topic, PasswordReset

from .forms import RoomForm, MyUserCreationForm

from django.db.models import Q


# from django.contrib.auth.models import User  # No Longer needed this default User class provided by django
from django.contrib.auth import get_user_model
User = get_user_model()


from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required



from django.utils import timezone
from django.conf import settings
from django.core.mail import EmailMessage
from django.urls import reverse


from .models import Message, MessageFile

from django.http import HttpResponseForbidden
from django.shortcuts import redirect, get_object_or_404

from .forms import UserForm



def RegisterView(request):

    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.email = user.email.lower()
            user.save()

            messages.success(request, "Registered Successfully...! Now Login")
            return redirect('login')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'base/register.html', {'form': form})



def LoginView(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':

        # username = request.POST.get('username').lower()
    
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, "Wrong Username or Password..!")
            return render(request, 'base/login.html')
        
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Logged In..!")
            return redirect('home')
        else:
            messages.error(request, "Username or Password does not exist..!")


    return render(request, 'base/login.html')


def LogoutView(request):
    logout(request)
    return redirect('home')



def ForgotPassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email = email)

            # Send password reset email if email is valid
            new_password_reset = PasswordReset(user = user)
            new_password_reset.save()


            reset_path = reverse('reset-password', kwargs={'reset_id': new_password_reset.reset_id})
            password_reset_url = request.build_absolute_uri(reset_path)  # Email la https://127.0... 


            # email content
            email_body = f'Reset your password using the link below:\n\n\n{password_reset_url}'

            email_message = EmailMessage(
                'Reset your password',         # Subject of the email
                email_body,                    # Content / body of the email
                settings.EMAIL_HOST_USER,      # Sender email (from settings.py)
                [email]                        # List of recipients (receiver email)
            )


            email_message.fail_silently = True  # This prevents Django from crashing if the email fails.
            email_message.send()  # This line actually sends the email using SMTP settings defined in your settings.py.
            return redirect('password-reset-sent', reset_id=new_password_reset.reset_id)


        except User.DoesNotExist:
            messages.error(request, f"No user with email '{email}' found")
            return redirect('forgot-password')
    
    return render(request, 'base/forgot_password.html')


def PasswordResetSent(request, reset_id):
    if PasswordReset.objects.filter(reset_id=reset_id).exists():
        return render(request, 'base/password_reset_sent.html')  
    
    else:
        # redirect to forgot password page if code does not exist
        messages.error(request, 'Invalid reset id')
        return redirect('forgot-password')



def ResetPassword(request, reset_id):

    try:
        reset_entry = PasswordReset.objects.get(reset_id=reset_id)

        if request.method == 'POST':
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            passwords_have_error = False
            if password != confirm_password:
                passwords_have_error = True
                messages.error(request, 'Passwords do not match')

            if len(password) < 5:
                passwords_have_error = True
                messages.error(request, 'Password must be at least 5 characters long')


            # check to make sure link has not expired
            expiration_time = reset_entry.created_when + timezone.timedelta(minutes=10)

            if timezone.now() > expiration_time:
                # delete reset entry if expired
                reset_entry.delete()   
                passwords_have_error = True
                messages.error(request, 'Reset link has expired')

            # reset password
            if not passwords_have_error:
                user = reset_entry.user
                user.set_password(password)
                user.save()

                # delete reset id after use
                reset_entry.delete()

                # redirect to login
                messages.success(request, 'Password reset. Proceed to login')
                return redirect('login')
            
            else:
                
                return render(request, 'base/reset_password.html', {'reset_id': reset_entry.reset_id})
            

    except PasswordReset.DoesNotExist:
        # redirect to forgot password page if code does not exist
        messages.error(request, 'Invalid reset id')
        return redirect('forgot-password')
    

    return render(request, 'base/reset_password.html')






def home(request):

    q = request.GET.get('q') if request.GET.get('q') != None else ''

    topics = Topic.objects.all()[0:6]

    rooms = Room.objects.filter(
        Q (topic__name__icontains = q) |
        Q (name__icontains=q) |
        Q(description__icontains = q)
    )

    room_count = rooms.count()
    

    context = {
        'rooms':rooms,
        'topics':topics,
        'room_count':room_count
    }   
    return render(request, 'base/home.html', context)



def room(request, pk):
    room = Room.objects.get(id=pk)

    room_messages = room.message_set.all().order_by('created')

    participants = room.participants.all()


    if request.method == 'POST':
        body = request.POST.get('body').strip()  # Strip to remove only spaces
        uploaded_files = request.FILES.getlist('files')

        ALLOWED_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.pdf', '.mp4', '.mp3', '.wav']
        MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10 MB

        errors_found = False

        if not body and not uploaded_files:
            messages.error(request, "You can't send an empty message.")
            return redirect('room', pk=room.id)

        for file in uploaded_files:
            if not any(file.name.lower().endswith(ext) for ext in ALLOWED_EXTENSIONS):
                messages.error(request, f"{file.name} has an unsupported file type.")
                errors_found = True
            elif file.size > MAX_UPLOAD_SIZE:
                messages.error(request, f"{file.name} exceeds maximum size of 10MB.")
                errors_found = True

       
        if errors_found:
            return redirect('room', pk=room.id)


        message = Message.objects.create(
            user=request.user,
            room=room,
            body=body,
        )

        for file in uploaded_files:
            MessageFile.objects.create(file=file, message=message)

        room.participants.add(request.user)

        return redirect('room', pk=room.id)


    context = {'room':room, 'room_messages':room_messages, 'participants':participants}

    return render(request, 'base/room.html', context)


@login_required(login_url='login')
def delete_file(request, file_id):
    file = get_object_or_404(MessageFile, id=file_id)

    if file.message.user == request.user:
        file.delete()
    
    return redirect('room', pk=file.message.room.id)

@login_required(login_url='login')
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)

    if request.user == message.user:
        room_id = message.room.id

        message.delete()
        messages.success(request, "Message deleted.")

        return redirect('room', pk=room_id)
    else:
        return HttpResponseForbidden("You're not allowed to delete this message.")





def user_profile(request, pk):

    profile_user = User.objects.get(id=pk)

    rooms = profile_user.room_set.all()
    topics = Topic.objects.all()

    context = {
        'profile_user': profile_user,
        'rooms':rooms,
        'topics':topics
    }
    return render(request, 'base/profile.html', context)




@login_required(login_url='login')
def create_room(request):

    form = RoomForm()
    topics = Topic.objects.all()

    if request.method == 'POST':
        # print(request.POST)

        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description = request.POST.get('description'),
        )

        return redirect('home')

    context = {
        'form':form,
        'topics':topics,
    }
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def update_room(request, pk):

    room = Room.objects.get(id=pk)
    topics = Topic.objects.all()

    form = RoomForm(instance=room)  

    if request.user != room.host:
        messages.error(request, 'You are not allowed to edit this room.')
        return redirect('room', pk=room.id)

    if request.method == 'POST':

        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()

        return redirect('room', pk=room.id)

    context = {
        'form':form,
        'topics':topics,
        'room':room,
    }

    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def delete_room(request, pk):

    room = Room.objects.get(id=pk)

    if request.user != room.host:
        messages.error(request, 'You are not allowed to delete this room..')
        return redirect('room', pk=room.id)

    
    if request.method == 'POST':
        room.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj':room})



@login_required(login_url='login')
def update_user(request):

    user = request.user

    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            form.save()
            messages.success(request, "Profile Updated.")
            return redirect('user-profile', pk=user.id)
        
        messages.error(request, "Error occured while updating..!")

    return render(request, 'base/update_user.html', {'form':form})



def topics_page(request):

    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics':topics})