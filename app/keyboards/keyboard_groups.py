from app.utils.menu import Menu

keyboard_groups_start = Menu('inline', 1)
keyboard_groups_start.new_button('В разработке', 1, callback_data="groups")

keyboard_groups_choice = Menu('inline', 1)
keyboard_groups_choice.new_button('✅Включено', 1, callback_data="groupsstatus_on")