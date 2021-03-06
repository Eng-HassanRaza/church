from django import template

register = template.Library()

#https://stackoverflow.com/a/50992575
@register.filter
def make_ordinal(n):
    '''
    Convert an integer into its ordinal representation::

        make_ordinal(0)   => '0th'
        make_ordinal(3)   => '3rd'
        make_ordinal(122) => '122nd'
        make_ordinal(213) => '213th'
    '''
    n = int(n)
    suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    return str(n) + suffix

@register.filter
def minutes_to_hours(n):
    n = int(n)
    hours = n // 60
    mins = n % 60
    return "%d hours, %d minutes" % (hours,mins)

