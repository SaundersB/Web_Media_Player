from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
import datetime

def hello(request):
	return HttpResponse("Hello World")

def homepage_view(request):
	return HttpResponse("This is the homepage")

def current_datetime(request):
	now = datetime.datetime.now()
	#html = "<html><body>The time now is %s.</body></html>" % now
	#return HttpResponse(html)
	t = get_template('current_datetime.html')
	html = t.render(Context({'current_date': now}))
	return HttpResponse(html)