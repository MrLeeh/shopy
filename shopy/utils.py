"""
    Copyright 2015 by Stefan Lehmann

"""
import os
import glob
import colorama


colorama.init()


def green(x):
    return colorama.Fore.GREEN + x + colorama.Fore.RESET


def red(x):
    return colorama.Fore.RED + x + colorama.Fore.RESET


def fst(x):
    return x[0]


def strip(x):
    return x.strip()


def shop_path():
    return os.path.join(os.path.dirname(__file__), 'shops')


def iter_shops():
    return (f for f in glob.glob(os.path.join(shop_path(), '*.json')))


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
