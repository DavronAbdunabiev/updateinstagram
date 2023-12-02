from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp
from keyboards.default.adminmenu import admin_button,check_button
from loader import dp,db,bot
from states.mystate import ReklamaState
from aiogram.dispatcher import FSMContext
from data.config import ADMINS

@dp.message_handler(commands='admin',user_id=ADMINS)
async def bot_help(message: types.Message):
    text = 'Welcome'
    
    await message.answer((text),reply_markup=await admin_button())

@dp.message_handler(text='Obunachilar sonini ko`rish',user_id =ADMINS)
async def bot_help(message: types.Message):
        users_count =db.alluser_count() 
        await message.answer(f"Botdagi foydalanuvchilar soni: {users_count[0]} ta")

@dp.message_handler(text='Reklama berish',state="*",user_id =ADMINS)
async def bot_help(message: types.Message,state:FSMContext):
    await message.answer('Rasmni yuboring: ')
    await ReklamaState.add_image.set()

@dp.message_handler(content_types='photo',state=ReklamaState.add_image)
async def bot_helo(message:types.Message,state:FSMContext):
    image_user = message.photo[-1].file_id
    await state.update_data(add_image = image_user)
    await message.answer('Matini yuboring: ')
    await ReklamaState.add_text.set()

@dp.message_handler(state=ReklamaState.add_text)
async def bot_help(messsage:types.Message,state:FSMContext):
    text_user = messsage.text
    await state.update_data(add_text = text_user)
    await messsage.answer("Malumotlaringiz to`g`rimi")
  
    
    
    data = await state.get_data()
    add_image_ = data.get('add_image')
    add_text_ = data.get('add_text') 
    await messsage.answer_photo(photo=add_image_,caption=add_text_,reply_markup= await check_button())
    await ReklamaState.add_check.set()




@dp.message_handler(state=ReklamaState.add_check)
async def bot_help(messsage:types.Message,state:FSMContext):
    if messsage.text == 'XA':
        await messsage.answer("Yuborilmoqda",reply_markup= types.ReplyKeyboardRemove())
        data = await state.get_data()
        add_image_ = data.get('add_image')
        add_text_ = data.get('add_text') 
        await messsage.answer_photo(photo=add_image_,caption=add_text_)

        users = db.all_users()
        spam = 0
        nospam = 0
        for user in users:
            try:
                await bot.send_photo(chat_id=user[0],photo=add_image_,caption=add_text_)
                nospam +=1
            except:
                spam +=1
        info = f"Habar yetib borganlari {nospam}:\nHabar yetib bormaganlari{spam}"        
        await admin_send(info)
       
    
    else:
        await messsage.answer("Malumotlar o`chirildi: ",reply_markup=types.ReplyKeyboardRemove())
       
    await state.finish()
    await state.reset_data()
    
    
    
async def admin_send(text):
    for i in ADMINS:
        await bot.send_message(i,text)