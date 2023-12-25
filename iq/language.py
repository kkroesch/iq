


def pluralize(count, singular, plural=None):
    if count == 1:
        return singular
    else:
        return plural if plural else singular + 's'