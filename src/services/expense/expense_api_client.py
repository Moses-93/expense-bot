import logging
from typing import Dict, List
from aiohttp import ClientResponseError
from src.services.api_client import APIClient


logger = logging.getLogger(__name__)


class ExpenseAPIClient:
    def __init__(self, api_client: APIClient):
        self.api_client = api_client

    async def get_expenses(self, user_id: int) -> List[Dict]:
        try:
            return await self.api_client.get("/expenses", user_id)

        except ClientResponseError as e:
            logger.error(f"Error getting expenses: {e}")
            return None

    async def get_expenses_report(
        self, user_id: int, start_date: str, end_date: str, report_type: str = "excel"
    ) -> bytes:
        """Get the expenses report for the user."""
        try:
            return await self.api_client.get(
                f"/expenses/report/{report_type}?start_date={start_date}&end_date={end_date}",  # TODO: Add prefix "excel"
                user_id,
                response_type="bytes",
            )
        except ClientResponseError as e:
            logger.error(f"Error getting expenses report: {e}")
            return None

    async def create_expense(self, user_id: int, expense_data: dict):
        """Add a new expense for the user."""
        logger.debug(f"Adding expense for user {user_id}: {expense_data}")
        try:
            response = await self.api_client.post(
                f"/expenses", user_id, json=expense_data
            )
            return response
        except ClientResponseError as e:
            print(f"Error adding expense: {e}")
            return None

    async def update_expense(self, user_id: int, expense_id: int, update_data: dict):
        """Update an existing expense for the user."""
        try:
            response = await self.api_client.patch(
                f"/expenses/{expense_id}", user_id, json=update_data
            )
            return response
        except ClientResponseError as e:
            print(f"Error updating expense: {e}")
            return None

    async def delete_expense(self, user_id: int, expense_id: int):
        """Delete an existing expense for the user."""
        try:
            response = await self.api_client.delete(f"/expenses/{expense_id}", user_id)
            return response
        except ClientResponseError as e:
            print(f"Error deleting expense: {e}")
            return None
