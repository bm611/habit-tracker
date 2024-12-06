import reflex as rx


class State(rx.State):
    habit: str = ""
    habits: list[str] = []

    def set_habit(self, value: str):
        self.habit = value

    def handle_submit(self):
        self.habits.append(self.habit)
        self.habit = ""
