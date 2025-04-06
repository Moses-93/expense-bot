import logging
from typing import Optional
from aiohttp import ClientResponseError
from yarl import URL
from src.services.api_client import APIClient


logger = logging.getLogger(__name__)


class ExpenseAPIClient:
    def __init__(self, api_client: APIClient):
        self.api_client = api_client

    async def get_expense(self, user_id: int, expense_id: int):
        try:
            return await self.api_client.get(f"/expenses/{expense_id}", user_id)
        except ClientResponseError as e:
            logger.error(f"Error getting expenses report: {e}")
            return None

    async def get_expenses_report(
        self,
        user_id: int,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        all_expenses: Optional[bool] = None,
        report_type: str = "excel",
    ) -> Optional[bytes]:
        """Get the expenses report for the user."""
        try:
            base_url = f"/expenses/report/{report_type}"
            query_params = {}

            if all_expenses:
                query_params["all_expenses"] = "true"
            else:
                if start_date:
                    query_params["start_date"] = start_date
                if end_date:
                    query_params["end_date"] = end_date

            full_url = str(URL(base_url).with_query(query_params))

            return await self.api_client.get(
                full_url,
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
            return await self.api_client.post(f"/expenses", user_id, json=expense_data)
        except ClientResponseError as e:
            print(f"Error adding expense: {e}")
            return None

    async def update_expense(self, user_id: int, expense_id: int, update_data: dict):
        """Update an existing expense for the user."""
        try:
            return await self.api_client.patch(
                f"/expenses/{expense_id}", user_id, json=update_data
            )
        except ClientResponseError as e:
            print(f"Error updating expense: {e}")
            return None

    async def delete_expense(self, user_id: int, expense_id: int):
        """Delete an existing expense for the user."""
        try:
            return await self.api_client.delete(f"/expenses/{expense_id}", user_id)
        except ClientResponseError as e:
            print(f"Error deleting expense: {e}")
            return None
