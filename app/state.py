import reflex as rx
import uuid
import asyncio


class State(rx.State):
    habit: str = ""
    habits: list[str] = []
    sync_id: str = str(uuid.uuid4())
    input_sync_id: str = ""
    copied: bool = False
    sync_error: bool = False

    def set_habit(self, value: str):
        self.habit = value

    def handle_submit(self):
        self.habits.append(self.habit)
        self.habit = ""

    def set_input_sync_id(self, value: str):
        self.input_sync_id = value
        self.sync_error = False

    def connect_sync_id(self):
        if len(self.input_sync_id) == 36:
            try:
                uuid.UUID(self.input_sync_id)
                self.sync_id = self.input_sync_id
                self.input_sync_id = ""
                self.sync_error = False
            except ValueError:
                self.sync_error = True
        else:
            self.sync_error = True

    async def copy_sync_id(self):
        self.copied = True
        yield rx.set_clipboard(self.sync_id)
        await asyncio.sleep(2)  # Show checkmark for 2 seconds
        self.copied = False
