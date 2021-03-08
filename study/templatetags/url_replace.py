from django import template
register = template.Library()

#https://stackoverflow.com/a/16609498
@register.simple_tag
def url_replace(request, field, value):
    dict_ = request.GET.copy()
    dict_[field] = value
    return f"?{dict_.urlencode()}"


