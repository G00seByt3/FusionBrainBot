import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, FSInputFile

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from fb import get_image
import keyboards as keyboards


router = Router()

logging.basicConfig(level=logging.INFO, filename="logs.log",filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")

class GenerationParametrs(StatesGroup):
    negative_prompt = State()
    prompt = State()
    style = State()


def get_choosen_params(user_data: dict) -> str:
    """
    Функция для получения данных,
    заданных пользователем
    """
    message = '<b>Generation parametrs</b>\n\n'

    # Перебираем атрибуты класса состояний
    for param in GenerationParametrs.__all_states__:
        # Если какое-то из состояний было использовано, 
        # то добавляем его в сообщение
        if (param := param._state) in user_data:
            message += f'<b>{param.capitalize()}</b>: {user_data.get(param)}\n'
    
    return message


@router.message(Command("start"))
async def start_cmd(message: Message) -> None:
    await message.answer(text="Hello! I'm Fusion BrainBot!",
                         reply_markup=keyboards.main_keyboard)


@router.callback_query(F.data == 'prompt')
async def prompt_cmd(
    call: CallbackQuery,
    state: FSMContext) -> None:

    await call.message.edit_text(text="Enter the prompt",
                                 reply_markup=keyboards.exit_keyboard)

    await state.set_state(GenerationParametrs.prompt)
    

@router.message(GenerationParametrs.prompt)
async def entering_prompt(
    message: Message, 
    state: FSMContext) -> None:

    await state.update_data(prompt = message.text)
    await message.answer(text=get_choosen_params(await state.get_data()),
                         reply_markup=keyboards.main_keyboard)


@router.callback_query(F.data == 'negative_prompt')
async def negative_prompt_cmd(
    call: CallbackQuery, 
    state: FSMContext) -> None:

    await call.message.edit_text(text="Enter the negative prompt",
                                 reply_markup=keyboards.exit_keyboard)

    await state.set_state(GenerationParametrs.negative_prompt)


@router.message(GenerationParametrs.negative_prompt)
async def entering_negative_prompt(
    message: Message, 
    state: FSMContext) -> None:

    await state.update_data(negative_prompt = message.text)
    await message.answer(text=get_choosen_params(await state.get_data()),
                         reply_markup=keyboards.main_keyboard)


@router.callback_query(F.data == 'choose_style')
async def style_cmd(
    call: CallbackQuery, 
    state: FSMContext) -> None:

    await call.message.edit_text(text="Choose a style:",
                                 reply_markup=keyboards.styles_keyboard)

    await state.set_state(GenerationParametrs.style)


@router.callback_query(GenerationParametrs.style)
async def choosing_style(
    call: CallbackQuery, 
    state: FSMContext) -> None:

    await state.update_data(style = call.data)
    await call.message.edit_text(text=get_choosen_params(await state.get_data()),
                                 reply_markup=keyboards.main_keyboard)

    await state.set_state(state = None)


@router.callback_query(F.data == 'back')
async def back_cmd(
    call: CallbackQuery,
    state: FSMContext) -> None:
    await call.message.edit_reply_markup(text=get_choosen_params(await state.get_data()),
                                         reply_markup=keyboards.main_keyboard)


@router.callback_query(F.data == 'start_generation')
async def get_result(
    call: CallbackQuery,
    state: FSMContext) -> None:

    user_data = await state.get_data()

    if user_data.get('prompt') is None:
        await call.answer(text="You have not introduced prompt!")

    else:
        await call.message.delete_reply_markup()
        await call.answer(text="Your image is being prepared. Please wait")

        image_number = get_image(prompt=user_data.get('prompt'), 
                                 negative_prompt=user_data.get('negative_prompt'),
                                 style=user_data.get('style', 'DEFAULT'))
        
       
        img = FSInputFile(path=f'images/image_{image_number}.jpg')
    
        await call.message.answer_photo(photo=img)
        await call.message.answer_document(document=img)
        logging.info(f"Image {image_number} created")
        await state.clear()

