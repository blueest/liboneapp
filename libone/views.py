from django.shortcuts import render

def kebijakan(request):
    return render(request, 'kebijakan.html')

def syarat_dan_ketentuan(request):
    return render(request, 'syarat_dan_ketentuan.html')