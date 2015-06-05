"""
    Copyright 2015 by Stefan Lehmann
    
"""


fst = lambda x: x[0]
strip = lambda x: x.strip()


def float_from_str(string):
    """
    Extract a float from a given String. Decimal is ',' and Thousand
    seperator is ".".

    :returns: float -- The extracted number

    >>> extract_float("The number is 12.567,57.")
    12567.57

    """
    import re
    pattern = re.compile(r"\b[0-9]{1,3}(\.[0-9]{3})*(,[0-9]+)?\b|,[0-9]+\b")
    res = pattern.search(string)

    if res is None:
        return 0.0

    res = res.group()
    res = res.replace(".", "")
    res = res.replace(",", ".")

    return float(res)