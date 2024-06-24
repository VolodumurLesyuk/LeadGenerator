from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache

from customer.forms import EmailCheckForm
from customer.models import Customer

from faker import Faker

fake = Faker()


def switch_language(request, language):
    request.session['django_language'] = language
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@never_cache
def check_credentials(request):
    if request.method == 'POST':
        form = EmailCheckForm(request.POST)  # Передайте request.POST в конструктор форми
        if form.is_valid():
            email = form.cleaned_data['email']
            # Логіка після успішної валідації
            if Customer.objects.filter(email=email).exists():
                customer = Customer.objects.get(email=email)
                user = authenticate(request, username=customer.login, password=customer.password)
                if user is not None:
                    login(request, user)
                    return redirect('home')
                else:
                    print("Cannot login")
            else:
                if True: # тут буде функція перевірти чи є в СРМ
                    # Логіка для створення нового користувача
                    username = fake.user_name()
                    password = fake.password()
                    try:
                        user = User.objects.create_user(username=username, email=email, password=password)
                        customer = Customer.objects.create(email=email, login=username, password=password, user=user)
                        customer.save()
                        login(request, user)
                        print("User created and logged in successfully")
                        return redirect('home')
                    except Exception as e:
                        print("Error creating user", e)
                else:
                    print("Редірект на сайт реєстрації СРМ")
                    return redirect('new_user')
        else:
            print("Form is not valid", form.errors)
    else:
        form = EmailCheckForm()

    return render(request, 'auth/login.html', {'form': form})


@login_required
def home(request):
    return render(request, 'base.html')


def new_user(request):
    return render(request, 'notify/new_user.html')
