from app.utils.menu import Menu

keyboard_my_photos_first_choice = Menu('inline', 1)
keyboard_my_photos_first_choice.new_button('Архив', 1, callback_data="arcive")
keyboard_my_photos_first_choice.new_button('Добавить', 1, callback_data="new_photos")

keyboard_my_photos_new_photos = Menu('inline', 2)
keyboard_my_photos_new_photos.new_button('Закончить отправку✅', 1, callback_data="finish_sending")
keyboard_my_photos_new_photos.new_button('Назад', 2, callback_data="back_my_photos_first_choice")

keyboard_my_photos_is_sending = Menu('inline', 1)
keyboard_my_photos_is_sending.new_button('Отправить', 1, callback_data='send')
keyboard_my_photos_is_sending.new_button('Сохранить', 1, callback_data='saving_in_archive')
