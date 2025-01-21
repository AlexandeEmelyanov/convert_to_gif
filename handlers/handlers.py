import os
from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config_data.config import Config, load_config
from aiogram.types.input_file import FSInputFile
from database.database import insert_database
from keyboards.keyboard import html_keyboard
from lexicon.lexicon import LEXICON_RU
from utils.utils import convert_video_to_gif_moviepy


config: Config = load_config()
bot = Bot(token=config.tg_bot.token)

class TargetFormat(object):
    GIF = ".gif"
    MP4 = ".mp4"
    AVI = ".avi"

class FPS(StatesGroup):
    fps = State()
router = Router()
class File(StatesGroup):
    file = State()
router = Router()

@router.message(Command(commands=['start']))
async def process_start_command(message: Message):
    await message.answer(f"<b>Привет, {message.from_user.full_name}!👀</b>", parse_mode="HTML")
    await message.answer(LEXICON_RU['/start'],
    reply_markup = html_keyboard)

@router.message(F.text == 'Начать конвертацию')
async def get_video(message: Message, state: FSMContext):
    await state.set_state(File.file)
    await message.answer('Выгрузите Ваш файл.')
@router.message(File.file)
async def handle_video(message: Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.username
    insert_database(user_id, username)
    if not message.video:
        await message.reply("Ошибка: Пожалуйста, отправьте видеофайл.")
        return
    video = message.video
    file_id = video.file_id
    await state.update_data(file=file_id)
    await message.reply("Обрабатываю запрос...")
    data = await state.get_data()
    file = data.get("file")
    file = await bot.get_file(file_id)


    # Скачиваем видеофайл
    video_file_path = f"./temps/{username}+{video.file_id}.mp4"
    await bot.download_file(file.file_path, video_file_path)
    convert_video_to_gif_moviepy(video_file_path, f"./temps/{username}+{video.file_id}.gif", max_fps=10,min_fps=1)
    document = FSInputFile(f'./temps/{username}+{video.file_id}.gif')
    await bot.send_document(user_id, document, caption=f'Ваш GIF-файл!')
    os.remove(f'./temps/{username}+{video.file_id}.mp4')

# Обработчик команды /help
@router.message(Command(commands=["help"]))
async def start_command(message:Message):
    await message.answer(text=LEXICON_RU['/help'], reply_markup=html_keyboard, parse_mode="HTML")