from django.shortcuts import render
from django.http import HttpResponse

posts = [
	{
		'author':'CoreyMS',
		'title':'Paper Title 1',
		'content':'First paper abstract. First paper abstract. First paper abstract. First paper abstract. First paper abstract. First paper abstract. First paper abstract. First paper abstract. First paper abstract. First paper abstract. First paper abstract. First paper abstract. First paper abstract. First paper abstract. First paper abstract. First paper abstract. First paper abstract. First paper abstract. ',
		'date_posted':'2020-03-27'
	},
	{
		'author':'Jane Doe',
		'title':'Paper Title 2',
		'content':'Second paper abstract. Second paper abstract. Second paper abstract. Second paper abstract. Second paper abstract. Second paper abstract. Second paper abstract. Second paper abstract. Second paper abstract. Second paper abstract. Second paper abstract. Second paper abstract. Second paper abstract. Second paper abstract. Second paper abstract. Second paper abstract. Second paper abstract. Second paper abstract. Second paper abstract. ',
		'date_posted':'2020-03-26'
	}
]

def home(request):
	context = {
		'posts':posts
	}
	return render(request, 'bioi_modeling/home.html', context)

def about(request):
	return render(request, 'bioi_modeling/about.html', {'title':'About'})

def topmodeling(request):
	return render(request, 'bioi_modeling/topmodeling.html', {'title':'Topic Modeling'})
