from aiogram.types import KeyboardButton,ReplyKeyboardMarkup


async def admin_button():
    button = ReplyKeyboardMarkup(resize_keyboard=True)
    button.add("Obunachilar sonini ko`rish") 
    button.add("Reklama berish")
    return button    


async def check_button():
    button = ReplyKeyboardMarkup(resize_keyboard=True)
    button.add("XA")
    button.add("YO`Q") 

    return button    

