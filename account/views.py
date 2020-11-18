from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib import messages
from orders.models import Order, OrderItem

@login_required
def edit(request):

    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                             data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.email = user_form.cleaned_data['username']
            # Save the User object
            
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
        else:
            messages.error(request, 'Error creating a new account. Email may have been used.')

    return render(request,
                  'account/register.html',
                  )


def user_login(request):
    message = None
    next1 = None
    if request.method == 'GET':
        next1 = request.GET.get('next', False)
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    message = 'Authenticated successfully'
                    print(request.POST['next'])
                    if request.POST['next'] == 'False':
                        return redirect(reverse('shop:home'))

                    else:
                        return redirect(request.POST['next'])

                else:
                    message = 'Disabled account'
            else:
                message = 'Invalid login'

    return render(request, 'registration/login.html', {'message': message, 'next': next1})

def user_orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'account/user_orders.html', {'order': orders})

def user_orders_detail(request, id):
    order = get_object_or_404(Order, id=id, user=request.user)
    order_item = OrderItem.objects.filter(order = order)
    return render(request, 'account/user_orders_detail.html', {'order': order, 'order_item': order_item})