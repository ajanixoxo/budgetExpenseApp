from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Budget



def budgets(request):
    budgets = Budget.objects.all().values()
    context = {
        'budgets': budgets
    }
    # The render() shortcut automatically loads the template, fills the context, and returns an HttpResponse.
    # We pass the request so that context processors (like user authentication, messages, etc.) can add extra context variables.
    return render(request, 'budgets.html', context)