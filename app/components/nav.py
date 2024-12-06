import reflex as rx


def navbar() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.hstack(
                rx.icon("repeat-2", size=40),
                rx.text(
                    "habit",
                    class_name="text-2xl md:text-3xl font-bold text-indigo-600",
                ),
                class_name="flex justify-center items-center",
                spacing="2",
            ),
            rx.button(
                "sync",
                class_name="text-xl md:text-2xl rounded-2xl text-black",
                variant="ghost",
            ),
            class_name="flex justify-between items-center",
        ),
        class_name="mt-1 mx-auto w-full bg-gray-200 rounded-2xl p-4 md:p-8",
    )
