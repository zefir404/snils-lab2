import re
import requests
from typing import List, Tuple

#регулярное выражение для ззахвата снилсов
SNILS_RE=re.compile(r'(?<!\d)(\d{3}[-\s]?\d{3}[-\s]?\d{3}[-\s]?\d{2}|\d{11})(?!\d)')



#функция которая все кроме цифр и возвращает 11-значную строку
def normilize(snils_raw: str) ->str:
    digits=re.sub(r'\D','', snils_raw)
    return digits


#Вычисляет контрольное число по первым 9 цифрам. Возвращает целое от 0 до 99.
def compute_snils_checksum(first_nine: str) -> int:
    if len(first_nine) != 9 or not first_nine.isdigit():
        raise ValueError("Первый аргумент должен быть строкой из 9 цифр")
    weights = list(range(9,0,-1))
    s= sum(int(d)* w for d, w in zip(first_nine,weights))
    if s<100:
        checksum=s
    elif s in(100,101):
        checksum=0
    else:
        checksum=  s% 101
        if checksum in (100,101):
            checksum=0
    return checksum