import reflex as rx

from app.state import State


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
    )
