import logging
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from src.keyboards.display_data_keyboard import DisplayData
from src.states.expenses import DeleteExpenseStates
from src.utils.message_provider import MessageProvider
from src.services.expense import (
    expense_service as exp_service,
)
from src.core.messages.enums import DeleteExpenseMessage


logger = logging.getLogger(__name__)


class ExpenseDeleteHandler:
    def __init__(
        self,
        mutation_service: exp_service.ExpenseMutationService,
        message_provider: MessageProvider[DeleteExpenseMessage],
    ):
        self.mutation_service = mutation_service
        self.message_provider = message_provider

    async def start(self, message: Message, state: FSMContext):
        await state.clear()

        expense_keyboard = await self.get_expense(message.from_user.id)
        await state.set_state(DeleteExpenseStates.EXPENSE_ID)
        await message.answer(
            self.message_provider.get(DeleteExpenseMessage.START),
            reply_markup=expense_keyboard,
        )

    async def handle_delete_expense(self, callback: CallbackQuery, state: FSMContext):

        await self.mutation_service.delete(callback.data, callback.from_user.id)

        await callback.message.answer(
            self.message_provider.get(DeleteExpenseMessage.SUCCESS),
            parse_mode="Markdown",
        )
        await state.clear()

    async def get_expense(self, user_id: int):
        url = exp_service.ExpenseReportURLBuilder("json").build_url()
        row_expense_data = await self.mutation_service.get(user_id, "json", url)
        expense_keyboard = DisplayData.generate_keyboard(
            row_expense_data, ("title", "date", "uah_amount"), ("id",)
        )
        return expense_keyboard
