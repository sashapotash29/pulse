from django.shortcuts import render

# Create your views here.

def graphs(request):
	return render(request, 'pulse/main.html',{})
