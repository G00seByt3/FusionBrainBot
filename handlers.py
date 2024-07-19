import os
from typing import Any

from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery, FSInputFile

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

import keyboards
import parametrs
from fb_app import get_image


router = Router()


class GenerationParametrs(StatesGroup):
    negative_prompt = State()
    prompt = State()
    style = State()
    ratio = State()


def get_params(user_data: dict) -> str:
    msg = '<b>Generation parameters:</b>\n\n'

    params = ['prompt', 'negative_prompt', 'style', 'ratio']

    for param in params:
        if param in user_data:
            msg += f'<b>{param.capitalize().replace("_", " ")}</b>: {user_data.get(param)}\n'
            
    return msg


@router.message(Command("start"))
async def start_cmd(message: Message) -> None:
    await message.answer(text="Hello! I'm Fusion BrainBot - your guide to the world of neural network art!",
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

    await message.answer(text=get_params(await state.get_data()),
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

    await message.answer(text=get_params(await state.get_data()),
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

    await state.update_data(style = parametrs.styles[int(call.data[-1])])

    await call.message.edit_text(text=get_params(await state.get_data()),
                                 reply_markup=keyboards.main_keyboard)

    await state.set_state(state = None)


@router.callback_query(F.data == 'choose_ratio')
async def ratio_cmd(
    call: CallbackQuery, 
    state: FSMContext) -> None:

    await call.message.edit_text(text="Select the ratio:",
                                 reply_markup=keyboards.ratio_keyboard)

    await state.set_state(GenerationParametrs.ratio)


@router.callback_query(GenerationParametrs.ratio)
async def choosing_ratio(
    call: CallbackQuery, 
    state: FSMContext) -> None:

    await state.update_data(ratio = parametrs.ratio[int(call.data[-1])])

    await call.message.edit_text(text=get_params(await state.get_data()),
                                 reply_markup=keyboards.main_keyboard)

    await state.set_state(state = None)


@router.callback_query(F.data == 'back')
async def back_cmd(
    call: CallbackQuery,
    state: FSMContext) -> None:
    await call.message.answer(text=get_params(await state.get_data()),
                              reply_markup=keyboards.main_keyboard)


@router.callback_query(F.data == 'start_generation')
async def get_result(
    call: CallbackQuery,
    state: FSMContext) -> None:

    user_data = await state.get_data()

    if user_data.get('prompt') is None:
        await call.answer(text="You have not introduced prompt!")

    else:
        await call.answer(text="Your image is being prepared. Please wait")

        image_number = get_image(prompt=user_data.get('prompt'), 
                                 negative_prompt=user_data.get('negative_prompt'),
                                 style=user_data.get('style', 'DEFAULT'),
                                 ratio=user_data.get('ratio', (1024, 1024)))
        if image_number == -1:
            await call.message.answer(text="An error occurred while generating")
            
        else:
            img = FSInputFile(path=f'images/image{image_number}.jpg')
    
            await call.message.answer_photo(photo=img)
    
            os.remove(f'images/image{image_number}.jpg')
    
            await state.clear()
