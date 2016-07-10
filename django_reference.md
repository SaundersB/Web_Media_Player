# Django Reference Guide



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
####Template filters are simple ways of altering the value of variables before they’re displayed

    {{ my_list|first|upper }}




