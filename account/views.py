from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from account.forms import RegistrationForm, AccountAuthenticationForm
from django.contrib import messages
# Create your views here.

def index(request):

    return render(request, 'index.html')


def register(request):
	context = {}
	if request.POST:
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			email = form.cleaned_data.get('email')
			raw_password = form.cleaned_data.get('password1')
			account = authenticate(email=email, password=raw_password)
			messages.success(request, 'Вы успешно зарегистрировались')
			login(request, account)
			return redirect('index')
		else:
			context['registration_form'] = form

	else:
		form = RegistrationForm()
		context['registration_form'] = form
	return render(request, 'register.html', context)


def logoutUser(request):
	messages.success(request,'Вы успешно вышли из системы')
	logout(request)
	return redirect('index')


def loginUser(request):

	context = {}

	user = request.user
	if user.is_authenticated: 
		return redirect("index")

	if request.POST:
		form = AccountAuthenticationForm(request.POST)
		if form.is_valid():
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(email=email, password=password)

			if user:
				login(request, user)
				messages.success(request, 'Вы успешно вошли')
				return redirect("index")

	else:
		form = AccountAuthenticationForm()

	context['login_form'] = form

	# print(form)
	return render(request, "login.html", context)