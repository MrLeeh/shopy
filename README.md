# shopy

Python package for comfortable concurrent article research on multiple shopping platforms. The parsing rules for each shop are defined as *xpath* expressions in a *json* file. This makes it easy to add new websites to the shoplist. Search results are presented as a list objects allowing further processing like ordering and filtering.

### Code Sample

```python
>>> from shopy import Shoplist, Shop
>>> from itertools import islice

>>> shoplist = Shoplist()
>>> shoplist.shops = [Shop.from_file('amazon')]

>>> iterator = islice(sorted(shoplist.find('Batterie AAA 1.5V'),
                             key=lambda x: x.price), 5)
>>> for item in iterator: 
        print(item.name[:30], "%0.2f" % item.price)

Panasonic LR 03 PAP Alkali Mic 3.15
Varta® Batterie (4103) Longlif 3.29
Micro-Batterie VARTA LONGLIFE  4.79
Panasonic LR 03 PSP Alkali Mic 5.75
Batterien Sparpack - 10 Stück  5.90

```

The parsing of a shops website is done via xpath syntax and is defined in a *json* file.

`amazon.json`:
```json
{
  "__type__": "Shop",
  "name": "Amazon",
  "url": "http://www.amazon.de",
  "search_url": "http://www.amazon.de/s/ref=nb_sb_noss_2?",
  "params": {
    "__mk_de_DE": "ÅMÅŽÕÑ",
    "url": "search-alias%3Daps"
  },
  "search_param": "field-keywords",
  "items": {
    "container": {"xpath": ".//li[@class=\"s-result-item\"]"},
    "name": {"xpath": ".//h2[contains(@class,\"s-access-title\")]/text()"},
    "price": {"xpath": ".//span[contains(@class, \"s-price\")]/text()"},
    "url": {"xpath": ".//a[contains(@class,\"a-link-norma\")]/@href"},
    "images": {"xpath": ".//img[contains(@class,\"s-access-image\")]/@src"}
  }
}

```