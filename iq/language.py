""" Filter for Jinja-Templates
"""

import arrow


def humanize(date):
    then = arrow.get(date)
    now = arrow.now()
    return then.humanize(then, locale='de')


def pluralize(count, singular, plural=None):
    if count == 1:
        return singular
    else:
        return plural if plural else singular + 's'


def decimal(value, precision=2):
    format_string = f'{{:.{precision}f}}'
    return format_string.format(value)