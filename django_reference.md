# Django Reference Guide
Django is a high-level Python Web framework that encourages rapid development and clean, pragmatic design. Built by experienced developers, it takes care of much of the hassle of Web development, so you can focus on writing your app without needing to reinvent the wheel. It’s free and open source.

## Dot Operator and Access
* Dictionary lookup (e.g., foo["bar"])
* Attribute lookup (e.g., foo.bar)
* Method call (e.g., foo.bar())
* List-index lookup (e.g., foo[2])


## Template Rendering Example
    >>> from django.template import Template, Context
    >>> person = {'name': 'Sally', 'age': '43'}
    >>> t = Template('{{ person.name.upper }} is {{ person.age }} years old.')
    >>> c = Context({'person': person})
    >>> t.render(c)
    'SALLY is 43 years old.

## Basic Template Tags and Filters

### Evaluates a variable
    {% if today_is_weekend %}
    /<p>Welcome to the weekend!</p>
    {% endif %}

### Comments
    {# This is a comment #}

### Filter
Template filters are simple ways of altering the value of variables before they’re displayed

    {{ my_list|first|upper }}



### Templates
#### Rendering Templates
##### Template HTML 
    <html>
    	<body>
    		The time now is {{ current_date }}.
    	</body>
    </html>

##### Views.py
    from django.template.loader import get_template
    from django.template import Context
    from django.http import HttpResponse
    import datetime
    
    def current_datetime(request):
    	now = datetime.datetime.now()
    	#html = "<html><body>The time now is %s.</body></html>" % now
    	#return HttpResponse(html)
    	t = get_template('current_datetime.html')
    	html = t.render(Context({'current_date': now}))
    	return HttpResponse(html)

##### Settings.py
    ...
    TEMPLATES = [
    ...
            'OPTIONS': {
            'context_processors': [
                ...
                'django.template.backends.django.DjangoTemplates',
                'django.template.backends.jinja2.Jinja2',


#### Inluding Templates Into Other Templates
This tag allows you to include the contents of another template
    
    {% include "nav.html" %}


#### Delete Tables from Specified App
    In django 1.9.5:
    
    Delete your migrations folder
    In the database: DELETE FROM django_migrations WHERE app = 'app_name'.
    
    You could alternatively just truncate this table.
    python manage.py makemigrations app_name
    python manage.py migrate


