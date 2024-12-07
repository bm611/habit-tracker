import reflex as rx
from app.state import State


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
            rx.dialog.root(
                rx.dialog.trigger(
                    rx.button(
                        "sync",
                        class_name="text-xl md:text-2xl rounded-2xl text-black",
                        variant="ghost",
                    )
                ),
                rx.dialog.content(
                    rx.dialog.title(
                        "Sync ID", class_name="text-2xl font-bold mb-4 text-center"
                    ),
                    rx.vstack(
                        rx.text("Your Sync ID:", class_name="font-semibold"),
                        rx.hstack(
                            rx.text(
                                State.sync_id,
                                class_name="bg-gray-100 p-3 text-sm md:text-lg rounded-lg flex-grow",
                            ),
                            rx.button(
                                rx.cond(
                                    State.copied,
                                    rx.icon(
                                        "check",
                                        color="green",
                                    ),
                                    rx.icon("copy"),
                                ),
                                on_click=State.copy_sync_id,
                                variant="ghost",
                            ),
                            class_name="w-full gap-2 flex justify-center items-center",
                        ),
                        rx.divider(class_name="my-4"),
                        rx.text("Enter existing Sync ID:", class_name="font-semibold"),
                        rx.hstack(
                            rx.input(
                                value=State.input_sync_id,
                                on_change=State.set_input_sync_id,
                                placeholder="Enter sync ID...",
                                class_name="rounded-lg flex-grow text-sm md:h-12",
                            ),
                            rx.button(
                                "Sync",
                                on_click=State.connect_sync_id,
                                class_name="text-black bg-gray-200 rounded-lg hover:bg-gray-300 active:scale-95 transition-all md:h-12",
                            ),
                            class_name="w-full gap-2",
                        ),
                        rx.cond(
                            State.sync_error,
                            rx.text(
                                "Invalid sync ID",
                                color="red",
                                class_name="text-sm",
                            ),
                        ),
                        class_name="w-full",
                    ),
                    rx.dialog.close(
                        rx.button(
                            "Close",
                            class_name="text-black mt-4 bg-gray-200 px-4 py-2 rounded-lg hover:bg-gray-300",
                        ),
                    ),
                    class_name="bg-white p-6 rounded-2xl shadow-lg",
                ),
            ),
            class_name="flex justify-between items-center",
        ),
        class_name="mt-1 mx-auto w-full bg-gray-200 rounded-2xl p-4 md:p-8",
    )
