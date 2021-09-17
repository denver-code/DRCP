from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from PIL import ImageGrab
import os
from aiogram.types import InputFile
import requests
import platform
import webbrowser
import cv2
from subprocess import *
from win10toast import ToastNotifier
import api.config_api as cp

TOKEN = cp.get_value("TOKEN")
OWNER_ID = cp.get_value("OWNER_ID")

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

@dp.message_handler(commands=["start"], chat_id=OWNER_ID)
async def start_event(message: types.Message):
	await message.reply("DRPCS - Denver Remote PC System.\n/help - for view all commands.")

@dp.message_handler(commands=['openurl'], chat_id=OWNER_ID)
async def openurl_event(message: types.Message):
	try:
		user_msg = '{0}'.format(message.text)
		url = user_msg.split(' ')[1]
		webbrowser.open_new_tab(url)
	except:
		await bot.send_message(OWNER_ID, 'Error')

@dp.message_handler(commands=['tasklist'], chat_id=OWNER_ID)
async def tasklist_event(message: types.Message):
	try:
		await bot.send_chat_action(OWNER_ID, 'typing')

		prs = Popen('tasklist', shell=True, stdout=PIPE, stderr=STDOUT, stdin=PIPE).stdout.readlines()
		pr_list = [prs[i].decode('cp866', 'ignore').split()[0].split('.exe')[0] for i in range(3,len(prs))]

		pr_string = '\n'.join(pr_list)
		await bot.send_message(OWNER_ID, '`' + pr_string + '`', parse_mode="Markdown")

	except:
		await bot.send_message(OWNER_ID, '*Not Found*', parse_mode="Markdown")

@dp.message_handler(commands=['webcam'], chat_id=OWNER_ID)
async def webcam_event(message: types.Message):
	try:
		cap = cv2.VideoCapture(0)
		for i in range(30):
			cap.read()

		ret, frame = cap.read()
		cv2.imwrite(os.environ['ProgramData'] + '\\WebCam.jpg', frame)

		await bot.send_chat_action(OWNER_ID, 'upload_photo')
		cap.release()

		webcam = open(os.environ['ProgramData'] + '\\WebCam.jpg', 'rb')
		await bot.send_photo(OWNER_ID, webcam)
		webcam.close()

	except:
		await bot.send_chat_action(OWNER_ID, 'typing')
		await bot.send_message(OWNER_ID, '*Webcam not found*', parse_mode="Markdown")

@dp.message_handler(commands=['toast'], chat_id=OWNER_ID)
async def toast_send(message: types.Message):
	try:
		user_msg = '{0}'.format(message.text)
		text = user_msg.split(' ')[1:]
		toaster = ToastNotifier()
		toaster.show_toast(" ".join(text))
		await bot.send_message(OWNER_ID, 'Sended')
	except:
		await bot.send_message(OWNER_ID, 'Error')

@dp.message_handler(commands=['info', 'Info'], chat_id=OWNER_ID)
async def info_send(message: types.Message):
	username = os.getlogin()
	uname = platform.uname()
	r = requests.get('http://ip.42.pl/raw')
	ip = r.text
	windows = platform.platform()
	processor = platform.processor()

	await bot.send_message(OWNER_ID, f"""
*DENVER PC INFO:*

*Status:* _Online🟢_
*PC:* _{username}_
*IP:* _{ip}_
*OS:* _{windows}_
*Processor:* _{processor}_
*Machine:* _{uname.machine}_
*Version:* _{uname.version}_
*Release:* _{uname.release}_
*Node Name:* _{uname.node}_

""", parse_mode="Markdown")

@dp.message_handler(commands=["screen", "sc"], chat_id=OWNER_ID)
async def screenshot_event(message: types.Message):
	try:
		screen = ImageGrab.grab()
		screen.save(os.getenv("APPDATA") + '\\Sreenshot.jpg')
		screen = open(os.getenv("APPDATA") + '\\Sreenshot.jpg', 'rb')
		await bot.send_document(OWNER_ID, InputFile(screen))
	except:
		pass

@dp.message_handler(commands=["shutdown"], chat_id=OWNER_ID)
async def screenshot_event(message: types.Message):
	await bot.send_message(OWNER_ID, '*Computer shuts down*', parse_mode="Markdown")
	os.system("shutdown /s /t 1")

@dp.message_handler(commands=["ssh", "s"], chat_id=OWNER_ID)
async def screenshot_event(message: types.Message):
	await message.answer(f"""
{cp.get_value("ssh")}
""", parse_mode="Markdown")

@dp.message_handler(commands=["help"], chat_id=OWNER_ID)
async def help_event(message: types.Message, chat_id=OWNER_ID):
	await message.reply("""
*DRPCS COMMANDS:*
/screen /sc - get screenshot
/info - Information about computer
/tasklist - Get all process
/webcam - get snap from webcamera
/openurl <url> - open url in browser 
/toast <text> - send message with text
/ssh - list of saved ssh servers
/shutdown - power off pc
""", parse_mode="Markdown")

async def on_shutdown(_):
	await bot.send_message(OWNER_ID, '*Computer shuts down*', parse_mode="Markdown")

async def on_startup(_):
    await bot.send_message(OWNER_ID, '*DRPCS status* _- Online🟢_\n*Control started on your machine!*', parse_mode="Markdown")

if __name__ == "__main__":
	executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)