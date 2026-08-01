from app.utils.menu import Menu

keyboard_rating_first_choice = Menu('inline', 2)
keyboard_rating_first_choice.new_button("Мили фембои", 1, callback_data="cute_femboys")
keyboard_rating_first_choice.new_button("Мили подкачанные фембои", 2, callback_data="cute_pumped_up_femboys")

keyboard_rating_cute_femboys = Menu('inline', 2)
keyboard_rating_cute_femboys.new_button('Ножки', 1, callback_data='cute_femboys_legs')
keyboard_rating_cute_femboys.new_button('Юбочки', 1, callback_data='cute_femboys_skirts')
keyboard_rating_cute_femboys.new_button('Прочая красота', 2, callback_data='cute_femboys_other_beauty')

keyboard_rating_cute_punped_up_femboys = Menu('inline', 1)
keyboard_rating_cute_punped_up_femboys.new_button('В разработке', 1, callback_data='in_development')

keyboard_rating_cute_femboys_legs = Menu('inline', 3)
keyboard_rating_cute_femboys_legs.new_button('Недельный рейтинг',1,callback_data="cute_femboys_legs_week")
keyboard_rating_cute_femboys_legs.new_button('Месячный рейтинг',2,callback_data="cute_femboys_legs_month")
keyboard_rating_cute_femboys_legs.new_button('Назад',3,callback_data="cute_femboys_legs_back")

keyboard_rating_cute_femboys_skirts = Menu('inline', 3)
keyboard_rating_cute_femboys_skirts.new_button('Недельный рейтинг',1,callback_data="cute_femboys_skirts_week")
keyboard_rating_cute_femboys_skirts.new_button('Месячный рейтинг',2,callback_data="cute_femboys_skirts_month")
keyboard_rating_cute_femboys_skirts.new_button('Назад',3,callback_data="cute_femboys_skirts_back")

keyboard_rating_cute_femboys_other_beauty = Menu('inline', 3)
keyboard_rating_cute_femboys_other_beauty.new_button('Недельный рейтинг',1,callback_data="cute_femboys_other_beauty_week")
keyboard_rating_cute_femboys_other_beauty.new_button('Месячный рейтинг',2,callback_data="cute_femboys_other_beauty_month")
keyboard_rating_cute_femboys_other_beauty.new_button('Назад',3,callback_data="cute_femboys_other_beauty_back")


