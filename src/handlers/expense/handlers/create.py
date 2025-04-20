import logging
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.services.api_client import APIClient
from src.states.expenses import AddExpenseStates
from src.services.expense import expense_service as exp_service
from src.handlers.expense.base_handler import BaseExpenseHandler
from src.handlers.expense.messages import ADD_EXPENSE_MESSAGES
from src.utils.expense_validators import (
    amount_validator,
    date_validator,
    name_validator,
)

logger = logging.getLogger(__name__)


class ExpenseCreateHandler(BaseExpenseHandler):
    def __init__(self, api_client: APIClient):
        super().__init__(
            ADD_EXPENSE_MESSAGES,
            {
                "title": name_validator,
                "date": date_validator,
                "amount": amount_validator,
            },
            {
                "title": "invalid_title",
                "date": "invalid_date",
                "amount": "invalid_uah_amount",
            },
        )
        self.api_client = api_client

    async def handle_add_expense(self, message: Message, state: FSMContext):
        await state.clear()
        await state.set_state(AddExpenseStates.ADD_EXPENSE_NAME)
        await message.answer(self.messages.get("start"), parse_mode="Markdown")

    async def handle_set_expense_name(self, message: Message, state: FSMContext):
        success = await self._handle(
            message, state, "title", AddExpenseStates.ADD_EXPENSE_DATE
        )
        if success:
            await message.answer(self.messages.get("set_date"), parse_mode="Markdown")

    async def handle_set_expense_date(self, message: Message, state: FSMContext):
        success = await self._handle(
            message, state, "date", AddExpenseStates.ADD_EXPENSE_AMOUNT
        )
        if success:
            await message.answer(self.messages.get("set_amount"), parse_mode="Markdown")

    async def handle_set_expense_amount(self, message: Message, state: FSMContext):
        await self._handle(message, state, field="amount", next_state=None)

        await self._finalize_creation(message, state)

    async def _finalize_creation(self, message: Message, state: FSMContext):
        data = await state.get_data()
        logger.debug(f"{data=}")
        service = exp_service.ExpenseMutationService(
            self.api_client, message.from_user.id
        )
        created_expense = await service.create(data)
        await message.answer(
            self.messages.get("success_create").format(
                name=created_expense.get("title", "-"),
                date=created_expense.get("date", "-"),
                amount=created_expense.get("uah_amount", "-"),
            )
        )
        await state.clear()
