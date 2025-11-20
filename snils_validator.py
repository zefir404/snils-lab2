import re
import requests
from typing import List, Tuple

#регулярное выражение для ззахвата снилсов
SNILS_RE=re.compile(r'(?<!\d)(\d{3}[-\s]?\d{3}[-\s]?\d{3}[-\s]?\d{2}|\d{11})(?!\d)')

# Порог: '001-001-998' -> числово 001001998
SNILS_CHECK_THRESHOLD = 1001998  # числовое значение первых 9 цифр при котором начинается проверка


#функция которая все кроме цифр и возвращает 11-значную строку
def normalize(snils_raw: str) ->str:
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

# Проверяет синтаксис и контрольную сумму СНИЛС.
def is_valid_snils(snils_raw: str, strict_threshold_check: bool = True) ->bool:
    digits =normalize(snils_raw)
    if len(digits) !=11:
        return False
    first9 = digits[:9]
    check_digits = digits[9:]
    # проверка порога (если требуется)
    try:
        first9_value = int(first9)
    except ValueError:
        return False

    if strict_threshold_check and first9_value <= SNILS_CHECK_THRESHOLD:
        # для маленьких номеров не проверяем контрольную сумму — считаем синтаксически корректным
        return True

    computed = compute_snils_checksum(first9)
    # формат контрольного как две цифры (с лидирующим нулём)
    computed_str = f"{computed:02d}"
    return computed_str == check_digits

