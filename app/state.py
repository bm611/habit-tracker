import reflex as rx
import uuid
import asyncio
from app.db.database import (
    init_db,
    create_user,
    add_habit,
    toggle_habit_date,
    load_user_data,
    delete_habit,
)


class State(rx.State):
    habit: str = ""
    habits: list[str] = []
    habit_dates: dict[str, set[str]] = {}
    sync_id: str = str(uuid.uuid4())
    input_sync_id: str = ""
    copied: bool = False
    sync_error: bool = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        init_db()
        create_user(self.sync_id)
        # Load existing data for the user
        loaded_habits, loaded_dates = load_user_data(self.sync_id)
        self.habits = loaded_habits
        self.habit_dates = loaded_dates

    def set_habit(self, value: str):
        self.habit = value

    def handle_submit(self):
        self.habits.append(self.habit)
        # Initialize empty set for new habit
        if self.habit not in self.habit_dates:
            self.habit_dates[self.habit] = set()
        # Save to database
        add_habit(self.sync_id, self.habit)
        self.habit = ""
        yield rx.scroll_to("calendar-section", align_to_top=True)

    def set_input_sync_id(self, value: str):
        self.input_sync_id = value
        self.sync_error = False

    def toggle_date(self, habit: str, date_str: str):
        """Toggle a date for a specific habit"""
        if habit not in self.habit_dates:
            self.habit_dates[habit] = set()

        if date_str in self.habit_dates[habit]:
            self.habit_dates[habit].remove(date_str)
        else:
            self.habit_dates[habit].add(date_str)
        # Save to database
        toggle_habit_date(self.sync_id, habit, date_str)

    def delete_habit(self, habit: str):
        """Delete a habit and its dates."""
        if habit in self.habits:
            self.habits.remove(habit)
            if habit in self.habit_dates:
                del self.habit_dates[habit]
            delete_habit(self.sync_id, habit)

    def connect_sync_id(self):
        if len(self.input_sync_id) == 36:
            try:
                uuid.UUID(self.input_sync_id)
                self.sync_id = self.input_sync_id
                self.input_sync_id = ""
                self.sync_error = False
                # Load data for the new sync_id
                create_user(self.sync_id)
                self.habits, self.habit_dates = load_user_data(self.sync_id)
            except ValueError:
                self.sync_error = True
        else:
            self.sync_error = True

    async def copy_sync_id(self):
        self.copied = True
        yield rx.set_clipboard(self.sync_id)
        await asyncio.sleep(2)  # Show checkmark for 2 seconds
        self.copied = False
