from django.shortcuts import render, HttpResponse


def questions(request):
    return render(request, "quest.html")
