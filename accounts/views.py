from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm

def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user after signup
            return redirect('home')  # Redirect to homepage after signup
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})
