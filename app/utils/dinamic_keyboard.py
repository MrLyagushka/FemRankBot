from typing import List
from aiogram.filters.callback_data import CallbackData

from typing_extensions import Literal, TypedDict
from app.utils.utils_group import DB_Group
from app.utils.menu import Menu

from config import PATH_TO_DB_DATA


class MyCallbackData(CallbackData, prefix='my'):
    callback_data: str
    first_index: int
    row: int
    column: int
    is_always_bigger: Literal['yes', 'no']
    button_info: str
    len_button_list: int


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
            print('Тут жопа')
            self.button_list = [x['full_name'] for x in data.groups]
            self.button_id = [x['id'] for x in data.groups]
            data.close()

        count = 0
        while count < self.row * self.column and self.first_index + count < len(self.button_list):
            row = count // self.column
            if self.button_info.split('_')[0] == 'groups':
                dinamic_keyboard.new_button(row_number=row+1, text=str(self.button_list[self.first_index+count]),# Т.к. в классе Menu, row_number идет от 0, для удобства пользования
                                        callback_data=f'callback_data_{self.button_info.split("_")[0]}_{self.button_list[self.first_index+count]}_{self.button_id[self.first_index+count]}')
            count += 1
        if len(self.button_list) > self.row*self.column:
            dinamic_keyboard.new_button(row_number=self.row+1, text='<', # Т.к. в классе Menu, row_number идет от 0, для удобства пользования
                                    callback_data=MyCallbackData(callback_data='<', first_index=self.first_index, row=self.row, column=self.column, is_always_bigger=self.is_always_bigger_column_multiply_row, button_info=self.button_info, len_button_list=len(self.button_list)).pack())
            dinamic_keyboard.new_button(row_number=self.row+1, text='>', callback_data=MyCallbackData(callback_data='>', first_index=self.first_index, row=self.row, column=self.column, is_always_bigger= self.is_always_bigger_column_multiply_row, button_info=self.button_info, len_button_list=len(self.button_list)).pack())
        return dinamic_keyboard.markup