from django.http import HttpResponse
import datetime

def hello(request):
	return HttpResponse("Hello World")



def homepage_view(request):
	return HttpResponse("This is the homepage")



def current_datetime(request):
	now = datetime.datetime.now()
	html = "<html><body>The time now is %s.</body></html>" % now
	return HttpResponse(html)