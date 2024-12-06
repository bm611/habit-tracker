import reflex as rx
from app.state import State
import calendar


def get_month_grid(year: int, month: int) -> rx.Component:
    # Get number of days in the month
    num_days = calendar.monthrange(year, month)[1]

    return rx.vstack(
        rx.text(calendar.month_name[month], class_name="text-xl font-semibold mt-4"),
        rx.grid(
            *[
                rx.button(
                    class_name="w-4 h-4 bg-gray-200 rounded-sm hover:bg-green-300"
                )
                for day in range(1, num_days + 1)
            ],
            columns="7",
            spacing="1",
            class_name="mt-2",
        ),
    )


def main_section() -> rx.Component:
    return rx.vstack(
        # hero section
        rx.vstack(
            rx.heading("habit tracker", class_name="text-5xl md:text-6xl"),
            rx.text(
                "Create and maintain your habits to build healthy life patterns",
                class_name="text-lg md:text-xl font-normal mt-2 text-center mx-4 text-gray-400",
            ),
            spacing="0",
            class_name="w-full flex items-center justify-center mt-10",
        ),
        # input section
        rx.hstack(
            rx.input(
                value=State.habit,
                class_name="w-full mt-4 mx-auto text-black text-2xl bg-transparent rounded-lg h-16",
                on_change=State.set_habit,
            ),
            rx.button(
                rx.hstack(
                    rx.icon("plus", size=28),
                    rx.text("create", class_name="text-2xl font-semibold"),
                    class_name="flex items-center justify-center",
                ),
                class_name="mt-4 mx-auto text-black bg-gray-200 rounded-lg p-8",
                on_click=State.handle_submit,
            ),
            class_name="w-full flex items-center justify-center",
        ),
        # habit section
        rx.foreach(
            State.habits,
            lambda habit: rx.text(habit, class_name="text-2xl font-semibold"),
        ),
        # calendar view
        rx.hstack(
            get_month_grid(2024, 10),
            get_month_grid(2024, 11),
            get_month_grid(2024, 12),
            class_name="mt-8",
        ),
        class_name="flex justify-center items-center",
    )
