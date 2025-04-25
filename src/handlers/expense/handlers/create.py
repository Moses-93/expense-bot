import logging
from typing import Dict
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.states.expenses import AddExpenseStates
from src.services.expense.expense_service import ExpenseMutationService
from src.utils.message_provider import MessageProvider
from src.core.messages.enums import AddExpenseMessage
from src.models.expense_dto import ExpenseDTO


logger = logging.getLogger(__name__)


class ExpenseCreateHandler:
    def __init__(
        self,
        message_provider: MessageProvider[AddExpenseMessage],
        mutation_service: ExpenseMutationService,
    ):
        self.message_provider = message_provider
        self.mutation_service = mutation_service

    async def handle_start(self, message: Message, state: FSMContext):
        await state.clear()
        await state.set_state(AddExpenseStates.TITLE)
        await message.answer(
            self.message_provider.get(AddExpenseMessage.START), parse_mode="Markdown"
        )

    async def handle_set_expense_name(
        self, message: Message, state: FSMContext, title: str
    ):
        await state.update_data(title=title)
        await state.set_state(AddExpenseStates.DATE)
        await message.answer(
            self.message_provider.get(AddExpenseMessage.SET_DATE), parse_mode="Markdown"
        )

    async def handle_set_expense_date(
        self, message: Message, state: FSMContext, date: str
    ):
        await state.update_data(date=date)

        await state.set_state(AddExpenseStates.AMOUNT)
        await message.answer(
            self.message_provider.get(AddExpenseMessage.SET_AMOUNT),
            parse_mode="Markdown",
        )

    async def handle_set_expense_amount(
        self, message: Message, state: FSMContext, amount: float
    ):
        state_data = await state.update_data(amount=amount)
        await state.clear()

        await self._finalize_creation(message, state_data)

    async def _finalize_creation(self, message: Message, state_data: Dict):
        expense_data = ExpenseDTO(**state_data)
        await self.mutation_service.create(message.from_user.id, expense_data)
        await message.answer(
            self.message_provider.get(AddExpenseMessage.SUCCESS).format(
                name=expense_data.title,
                date=expense_data.date.isoformat(),
                amount=expense_data.amount,
            ),
            parse_mode="Markdown",
        )
