import re
import requests
from typing import List, Tuple

#регулярное выражение для ззахвата снилсов
SNILS_RE=re.compile(r'(?<!\d)(\d{3}[-\s]?\d{3}[-\s]?\d{3}[-\s]?\d{2}|\d{11})(?!\d)')

#функция которая все кроме цифр и возвращает 11-значную строку
def normilize(snils_raw: str) ->str:
    digits=re.sub(r'\D','', snils_raw)
    return digits
