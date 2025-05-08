from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.kbd import Button

from dialogs.start.getters import get_hello
from dialogs.start.handlers import button_click
from states.start import StartSG

start_dialog = Dialog(
    Window(
        Format('{hello_user}'),
        Button(Format('{button_button}'),
               id='button_pressed',
               on_click=button_click),
        getter=get_hello,
        state=StartSG.start,
    ),
)