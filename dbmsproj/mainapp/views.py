from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import OrderForm, CreateUserForm, CustomerForm
from django.contrib import messages
from django.forms import inlineformset_factory
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user, allowed_users, admin_only

# Create your views here.


@unauthenticated_user
def registerPage(request):
    # if request.user.is_authenticated:
    #     return redirect('home')
    # else:
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            # form.save()
            user = form.save()
            print('User:', user)
            # user = form.cleaned_data.get('username')
            username = form.cleaned_data.get('username')

            # group = Group.objects.get(name='customer')
            # user.groups.add(group)
            # Customer.objects.create(
            #     user=user,
            # )

            # messages.success(request, 'Account was created for ' + user)
            messages.success(request, 'Account was created for ' + username)
            return redirect('login')
    context = {'form': form}
    return render(request, 'mainapp/register.html', context)


@unauthenticated_user
def loginPage(request):
    # if request.user.is_authenticated:
    #     return redirect('home')
    # else:
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')
    context = {}
    return render(request, 'mainapp/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'customer'])
def userPage(request):
    images = request.user.customer.images_set.all()
    # 'images': images
    context = {'images': images}
    print("IMAGES:", images)
    return render(request, 'mainapp/user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'mainapp/account_settings.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'customer'])
# @admin_only
def home(request):
    images = Images.objects.all()
    customers = Customer.objects.all()
    total_images = images.count()
    return render(request, 'mainapp/dashboard.html', {'images': images, 'total_images': total_images, 'customers': customers})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'customer'])
def images(request):
    images = Images.objects.all()

    return render(request, 'mainapp/products.html', {'images': images})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'customer'])
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    images = customer.images_set.all()
    myFilter = OrderFilter(request.GET, queryset=images)
    images = myFilter.qs
    # ids = 2
    context = {'customer': customer, 'images': images, 'myFilter': myFilter}
    return render(request, 'mainapp/customer.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'customer'])
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(
        Customer, Images, fields=('name', 'description', 'image'), extra=5)
    customer = Customer.objects.get(id=pk)
    formSet = OrderFormSet(queryset=Images.objects.none(), instance=customer)
    # form = OrderForm(initial={'customer': customer})
    if request.method == 'POST':
        # print('printing POST:', request.POST)
        # form = OrderForm(request.POST, request.FILES)
        formSet = OrderFormSet(request.POST, request.FILES, instance=customer)
        # if form.is_valid():
        #     form.save()
        #     img_obj = form.instance
        #     return redirect('/')
        if formSet.is_valid():
            formSet.save()
            img_obj = formSet.instance
            return redirect('/')
    # context = {'form': form}
    context = {'formSet': formSet}
    return render(request, 'mainapp/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'customer'])
def deleteOrder(request, pk):
    order = Images.objects.filter(id=pk)
    order.delete()
    messages.success(request, "Product Deleted Successfully")
    return redirect('/')
    # context = {'item': order}
    # return render(request, 'mainapp/delete.html', context)
