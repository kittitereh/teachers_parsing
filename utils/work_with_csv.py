import itertools
import os
import pandas as pd

from typing import Sequence


class CsvWriter:
    def __init__(self, csv_file_name: str, headers: list | tuple = None):
        self._file = open(csv_file_name, "w+")
        self._first_recording = True

        if headers:
            self._append_iterable_to_csv(headers)
    # функция записывает в csv значения из словаря с разделителем ;
    def _append_iterable_to_csv(self, sequence: Sequence):
        joined = ";".join(str(el) for el in sequence)
        self._file.write(f"{joined}\n")
    # у ключа может быть несколько значений  (например, предметы), поэтому мы создаем список ключей, у которых тэг содержит несколько значений (сиблингов одного уровня)
    def _append_complex_dict_to_csv(self, target_dict: dict):
        complex_fields_keys = []
        for key, value in target_dict.items():
            if isinstance(value, list):
                complex_fields_keys.append(key)

        # имеется ли на данной странице поля, где присутсвует несколько значений
        if complex_fields_keys:
            # получаем списки значений для них и создаем список этих списков
            itertools_args = [target_dict[key] for key in complex_fields_keys]

            # составляем все возможные комбинации значений из полей с несколькими значениями для составления нескольких строчек
            for fields in itertools.product(*itertools_args):
                field_dict = dict(zip(complex_fields_keys, fields))

                # создаем новый словарь для таких ключей и значений на основе созданного словаря с ключами и пустыми значениями
                dict_for_record = target_dict.copy()

                dict_for_record.update(field_dict)

                # записываем значения в csv
                self._append_iterable_to_csv(dict_for_record.values())
        # если ключи содержат только одно значение, записываем значения сразу в csv
        else:
            self._append_iterable_to_csv(target_dict.values())

    # флаг является ли записываемая строка в csv первой
    @property
    def first_recording(self) -> bool:
        if self._first_recording:
            self._first_recording = False
            return True
        else:
            return False

    # функция записи словаря в csv
    def append_to_csv(self, smth_to_write: dict):
        match smth_to_write:
            # если на запись пришел словарь:
            case dict(some_dict):
                # если это первый словарь на запись, то дополнительно записываются в csv ключи словаря, чтобы назвать столбцы
                if self.first_recording:
                    self._append_iterable_to_csv(some_dict.keys())
                self._append_complex_dict_to_csv(some_dict)
            #если на запись пришел лист или кортеж (на всякий случай):
            case list(some_iterable) | tuple(some_iterable):
                self._append_iterable_to_csv(some_iterable)
            # если пришло что-то другое, то выводим ошибку
            case _:
                raise RuntimeError(f"unknown type of smth_to_write: {smth_to_write}, type: {type(smth_to_write)}")

    def flush(self):
        self._file.flush()

    def __del__(self):
        self._file.close()


# позволяет создавать датафрейм из csv файла
def get_dataframe_from_csv(filename: str) -> pd.DataFrame:
    if not os.path.isfile(filename):
        raise RuntimeError(f"csv file with dataframe {filename} not found")
    return pd.read_csv(filename)
