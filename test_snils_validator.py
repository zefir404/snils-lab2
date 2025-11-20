# test_snils_validator.py
import unittest
from snils_validator import extract_and_validate_from_file

from snils_validator import compute_snils_checksum, is_valid_snils, normalize

class TestSnils(unittest.TestCase):

    def test_compute_checksum_examples(self):
        # пример: первые 9 цифр '112233445'
        first9 = '112233445'
        checksum = compute_snils_checksum(first9)
        # убедимся что функция возвращает целое 0..99
        self.assertIsInstance(checksum, int)
        self.assertGreaterEqual(checksum, 0)
        self.assertLessEqual(checksum, 99)

    def test_valid_snils_formatted_and_unformatted(self):
        # возьмём 9 цифр и вычислим корректную контрольную сумму
        first9 = '123456789'
        cs = compute_snils_checksum(first9)
        snils = f"{first9}{cs:02d}"
        # без форматирования
        self.assertTrue(is_valid_snils(snils))
        # с дефисами и пробелом
        formatted = f"{snils[0:3]}-{snils[3:6]}-{snils[6:9]} {snils[9:11]}"
        self.assertTrue(is_valid_snils(formatted))

    def test_invalid_length_and_chars(self):
        self.assertFalse(is_valid_snils("123"))  # короткое
        self.assertFalse(is_valid_snils("abcdefghijk"))  # буквы

    def test_wrong_checksum(self):
        # тот же first9, но поменяем контрольные
        first9 = '987654321'
        cs = compute_snils_checksum(first9)
        wrong = f"{first9}{(cs+1)%100:02d}"
        self.assertFalse(is_valid_snils(wrong))
    def test_reading_from_file(self):
        file_path = "without_snils.txt"

        results = extract_and_validate_from_file(file_path)
        # Проверяем, что что-то найдено
        self.assertGreater(len(results), 0)

        # Можно проверить конкретный известный СНИЛС в твоём файле
        normalized_snils = results[0][0]  # первая найденная запись
        is_valid = results[0][1]

        # просто проверим типы данных
        self.assertIsInstance(normalized_snils, str)
        self.assertIsInstance(is_valid, bool)

    def test_threshold_behavior(self):
        # номер <= 001001998 -> проверка контрольной не выполняется в нашей реализации
        small_first9 = '001001998'  # равен порогу
        # добавим какие-то два контрольных
        candidate = small_first9 + "12"
        # по умолчанию strict_threshold_check=True -> для этого номера is_valid_snils вернёт True
        self.assertTrue(is_valid_snils(candidate))
        # но если требовать всегда проверять контрольную -> False (скорее всего)
        self.assertFalse(is_valid_snils(candidate, strict_threshold_check=False))

if __name__ == "__main__":
    unittest.main()
