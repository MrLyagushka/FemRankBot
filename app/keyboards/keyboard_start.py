from app.utils.menu import Menu

keyboard_start_user = Menu('reply', 1)
keyboard_start_user.new_button("Рейтинг", 1)
keyboard_start_user.new_button("Мои фоточки", 1)

keyboard_start_admin = Menu('reply', 2)
keyboard_start_admin.new_button("Рейтинг", 1)
keyboard_start_admin.new_button("Мои фоточки", 1)
keyboard_start_admin.new_button("Группы", 2)