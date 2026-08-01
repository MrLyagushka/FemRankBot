from typing import List
from aiogram.filters.callback_data import CallbackData

from typing_extensions import Literal, TypedDict
from app.utils.utils_download_photos import DB_DownloadPhoto
from app.utils.utils_group import DB_Group
from app.utils.menu import Menu

from config import PATH_TO_DB_DATA, PATH_TO_DB_PHOTO


class MyCallbackData(CallbackData, prefix='my'):
    callback_data: str
    first_index: int
    row: int
    column: int
    is_always_bigger: Literal['yes', 'no']
    button_info: str
    len_button_list: int

class RatingKeyboard():

    def __init__(self, id):
        """
        Отправляей оценки от 1 до 5 с возможным расширением на избранное в будущем (подписку)
        Для отслеживания реакций добавляет к каждой фотографии уникальный id
        """
        self.id = id

    async def generate_keyboard(self):
        dinamic_keyboard = Menu('inline', 2)

        dinamic_keyboard.new_button('1', 1, callback_data=f'mark_1_{self.id}')
        dinamic_keyboard.new_button('2', 1, callback_data=f'mark_2_{self.id}')
        dinamic_keyboard.new_button('3', 1, callback_data=f'mark_3_{self.id}')
        dinamic_keyboard.new_button('4', 1, callback_data=f'mark_4_{self.id}')
        dinamic_keyboard.new_button('5', 1, callback_data=f'mark_5_{self.id}')
        dinamic_keyboard.new_button('⭐️', 2, callback_data=f'average_mark_{self.id}')

        return dinamic_keyboard.markup

class DinamicKeyboard():

    def __init__(self, row, column, is_always_bigger_column_multiply_row: Literal['yes', 'no'], first_index,
                 button_info: str):
        """
        Кароч, указываешь количество строк - row, столбцов - column. Также введи, будет ли твоя клавиатура
        всегда больше чем column*row или нет. И еще список кнопок.
        Формат button_info: st, tsa, tsd, tt. Список учеников, список заданий у ученика(активных и неактивных), список заданий у учителя.
        st_idteacher или ts_idstudent или tt_number
        """
        self.first_index = first_index
        self.row = row
        self.column = column
        self.is_always_bigger_column_multiply_row = is_always_bigger_column_multiply_row
        self.button_info = button_info

    async def generate_keyboard(self):
        """
        На будущее, тут можно вырать из трех режимов, так легче, чем указывать путь к файлу,
          или что-то подобноею После выбора режима и ввода через :  id , """
        dinamic_keyboard = Menu('inline', self.row+1)

        if self.button_info.split('_')[0] == 'groups':
            #Передать id учеников в массиве
            data = DB_Group(PATH_TO_DB_DATA)
            await data.get_groups()
            self.button_list = [x['full_name'] for x in data.groups]
            self.button_id = [x['id'] for x in data.groups]
            await data.close()
        elif self.button_info.split('_')[0] == 'archive':
            #Передать id учеников в массиве
            data = DB_DownloadPhoto(PATH_TO_DB_PHOTO)
            await data.get_download_photo_where_user_id(int(self.button_info.split('_')[1]))
            self.button_list = [x for x in range(len(data.groups_where_user_id))]
            self.button_id = [x['id'] for x in data.groups_where_user_id]
            await data.close()
        count = 0
        while count < self.row * self.column and self.first_index + count < len(self.button_list):
            row = count // self.column
            if self.button_info.split('_')[0] == 'groups':
                dinamic_keyboard.new_button(row_number=row+1, text=str(self.button_list[self.first_index+count]),# Т.к. в классе Menu, row_number идет от 0, для удобства пользования
                                        callback_data=f'callback_data_{self.button_info.split("_")[0]}_{self.button_list[self.first_index+count]}_{self.button_id[self.first_index+count]}')
            elif self.button_info.split('_')[0] == 'archive':
                dinamic_keyboard.new_button(row_number=row+1, text=str(self.button_list[self.first_index+count]),# Т.к. в классе Menu, row_number идет от 0, для удобства пользования
                                        callback_data=f'callback_data_{self.button_info.split("_")[0]}_{self.button_list[self.first_index+count]}_{self.button_id[self.first_index+count]}')
            count += 1
        if len(self.button_list) > self.row*self.column:
            dinamic_keyboard.new_button(row_number=self.row+1, text='<', # Т.к. в классе Menu, row_number идет от 0, для удобства пользования
                                    callback_data=MyCallbackData(callback_data='<', first_index=self.first_index, row=self.row, column=self.column, is_always_bigger=self.is_always_bigger_column_multiply_row, button_info=self.button_info, len_button_list=len(self.button_list)).pack())
            dinamic_keyboard.new_button(row_number=self.row+1, text='>', callback_data=MyCallbackData(callback_data='>', first_index=self.first_index, row=self.row, column=self.column, is_always_bigger= self.is_always_bigger_column_multiply_row, button_info=self.button_info, len_button_list=len(self.button_list)).pack())
        return dinamic_keyboard.markup