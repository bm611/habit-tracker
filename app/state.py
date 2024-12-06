import reflex as rx
import uuid


class State(rx.State):
    habit: str = ""
    habits: list[str] = []
    sync_id: str = str(uuid.uuid4())

    def set_habit(self, value: str):
        self.habit = value

    def handle_submit(self):
        self.habits.append(self.habit)
        self.habit = ""

    def copy_sync_id(self):
        return rx.set_clipboard(self.sync_id)
