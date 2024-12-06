import reflex as rx
import uuid
import asyncio


class State(rx.State):
    habit: str = ""
    habits: list[str] = []
    sync_id: str = str(uuid.uuid4())
    copied: bool = False

    def set_habit(self, value: str):
        self.habit = value

    def handle_submit(self):
        self.habits.append(self.habit)
        self.habit = ""

    async def copy_sync_id(self):
        self.copied = True
        yield rx.set_clipboard(self.sync_id)
        await asyncio.sleep(2)  # Show checkmark for 2 seconds
        self.copied = False
