import reflex as rx
from app.state import State
import calendar
from datetime import datetime
from dateutil.relativedelta import relativedelta


def get_month_grid(
    year: int, month: int, current_date: datetime = None
) -> rx.Component:
    # Get number of days in the month
    num_days = calendar.monthrange(year, month)[1]

    # If this is the current month, only show up to current day
    if current_date and year == current_date.year and month == current_date.month:
        num_days = current_date.day

    return rx.vstack(
        rx.text(calendar.month_name[month], class_name="text-xl font-semibold mt-4"),
        rx.grid(
            *[
                rx.tooltip(
                    rx.button(
                        class_name="w-4 h-4 bg-gray-200 rounded-sm hover:bg-green-300"
                    ),
                    content=f"{calendar.month_name[month]} {day}, {year}",
                )
                for day in range(1, num_days + 1)
            ],
            columns="7",
            spacing="1",
            class_name="mt-2",
        ),
    )


def get_last_three_months() -> tuple[list[tuple[int, int]], datetime]:
    current_date = datetime.now()
    months = []

    for i in range(3, -1, -1):
        date = current_date - relativedelta(months=i)
        months.append((date.year, date.month))

    return months, current_date


def habit_calendar_view(habit: str) -> rx.Component:
    """Create a calendar view component for a specific habit."""
    months, current_date = get_last_three_months()
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.text(habit, class_name="text-3xl"),
                rx.box(
                    rx.hstack(
                        rx.icon("flame", size=20, color="#6366f1"),
                        rx.text(
                            "0 days", class_name="text-lg text-indigo-500 font-medium"
                        ),
                        class_name="flex items-center justify-center",
                    ),
                    class_name="bg-indigo-50 px-4 py-2 rounded-2xl shadow-sm ml-2",
                ),
                rx.spacer(),
                rx.button(
                    rx.icon("trash", color="gray"),
                    variant="ghost",
                ),
                class_name="mt-2 flex items-center",
                width="100%",
            ),
            rx.box(
                rx.hstack(
                    *[
                        get_month_grid(year, month, current_date)
                        for year, month in months
                    ],
                    class_name="min-w-max backdrop-blur-sm",
                ),
                class_name="w-full overflow-x-auto scrollbar-thin scrollbar-thumb-indigo-200 scrollbar-track-transparent",
            ),
            class_name="p-8 bg-white/50 border border-indigo-100 rounded-xl w-full shadow-2xl",
            align_items="start",
        ),
        class_name="w-full",
    )


def main_section() -> rx.Component:
    months, current_date = get_last_three_months()
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
        # calendar view
        rx.vstack(
            rx.foreach(State.habits, lambda habit: habit_calendar_view(habit)),
            class_name="w-full mt-6",
        ),
        class_name="flex justify-center items-center",
    )
