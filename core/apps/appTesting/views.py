from django.shortcuts import render, redirect, get_list_or_404


def dashboard(request):
    return render(request, 'dashboard.html')