import logging
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.fsm.expense import (
    add_expense_fsm,
    update_expense_fsm,
    delete_expense_fsm,
    get_expense_report_fsm,
)

logger = logging.getLogger(__name__)


class ExpenseCreateHandler:

    def __init__(self, fsm_service: add_expense_fsm.AddExpenseFSMService):
        self.fsm_service = fsm_service

    async def handle_add_expense(self, message: Message, state: FSMContext):
        msg = await self.fsm_service.start(state)
        await message.answer(msg, parse_mode="Markdown")

    async def handle_set_expense_name(self, message: Message, state: FSMContext):
        msg = await self.fsm_service.set_name(state, message.text)
        await message.answer(msg, parse_mode="Markdown")

    async def handle_set_expense_date(self, message: Message, state: FSMContext):
        """Handle the 'Додати витрату' button."""
        msg = await self.fsm_service.set_date(state, message.text)
        await message.answer(msg, parse_mode="Markdown")

    async def handle_set_expense_amount(self, message: Message, state: FSMContext):
        """Handle the 'Додати витрату' button."""
        msg = await self.fsm_service.set_amount(
            state, message.from_user.id, message.text
        )
        await message.answer(msg, parse_mode="Markdown")


class ExpenseGetReportHandler:

    def __init__(self, fsm_service: get_expense_report_fsm.GetReportFSMService):
        self.fsm_service = fsm_service

    async def handle_start_expense_report(self, message: Message, state: FSMContext):
        msg = await self.fsm_service.start(state)
        await message.answer(msg, parse_mode="Markdown")

    async def handle_set_report_start_date(self, message: Message, state: FSMContext):
        msg = await self.fsm_service.set_start_date(message.text, state)
        await message.answer(msg, parse_mode="Markdown")

    async def handle_generate_expense_report(self, message: Message, state: FSMContext):
        await state.update_data(end_date=message.text)
        msg, report = await self.fsm_service.set_end_date(
            message.from_user.id, message.text, state
        )

        await message.answer_document(report, caption=msg)


class ExpenseUpdateHandler:

    def __init__(self, fsm_service: update_expense_fsm.UpdateFSMService):
        self.fsm_service = fsm_service

    async def handle_start_update_expense(self, message: Message, state: FSMContext):
        msg, keyboard = await self.fsm_service.start_update_expenses(
            message.from_user.id, state
        )
        await message.answer(text=msg, reply_markup=keyboard)

    async def set_expense_id(self, callback: CallbackQuery, state: FSMContext):
        msg = await self.fsm_service.set_expense_id(callback.data, state)
        await callback.message.answer(msg, parse_mode="Markdown")

    async def set_new_expense_name(self, message: Message, state: FSMContext):
        msg = await self.fsm_service.set_new_name(message.text, state)
        await message.answer(text=msg, parse_mode="Markdown")

    async def set_new_expense_date(self, message: Message, state: FSMContext):
        msg = await self.fsm_service.set_new_date(
            message.from_user.id, message.text, state
        )
        await message.answer(text=msg, parse_mode="Markdown")

    async def handle_update_expense(self, callback: CallbackQuery, state: FSMContext):
        msg = await self.fsm_service.set_expense_id(
            callback.from_user.id, callback.data, state
        )
        await callback.message.answer(text=msg, parse_mode="Markdown")


class ExpenseDeleteHandler:

    def __init__(self, fsm_service: delete_expense_fsm.DeleteFSMService):
        self.fsm_service = fsm_service

    async def start(self, message: Message, state: FSMContext):
        msg, keyboard = await self.fsm_service.start_delete_expense(
            message.from_user.id, state
        )
        await message.answer(text=msg, reply_markup=keyboard)

    async def handle_delete_expense(self, callback: CallbackQuery, state: FSMContext):
        msg = await self.fsm_service.delete_expense(
            callback.from_user.id, callback.data, state
        )
        await callback.message.answer(msg, parse_mode="Markdown")
