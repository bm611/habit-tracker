import reflex as rx
from app.state import State
import calendar
from datetime import datetime
from dateutil.relativedelta import relativedelta


def get_button_class(habit: str, year: int, month: int, day: int):
    """Helper function to determine button class based on completion status."""
    date_str = f"{year}-{month:02d}-{day:02d}"
    current_date = datetime.now()
    button_date = datetime(year, month, day)

    is_current_day = (
        year == current_date.year
        and month == current_date.month
        and day == current_date.day
    )

    is_future = button_date.date() > current_date.date()

    base_classes = "w-4 h-4 rounded-sm transition-all duration-200"

    # Add current day indicator classes
    if is_current_day:
        current_day_classes = "ring-2 ring-indigo-500 ring-offset-2"
        base_classes = f"{base_classes} {current_day_classes}"

    # Future dates should be grayed out and not interactive
    if is_future:
        return f"{base_classes} bg-gray-100 opacity-50 cursor-not-allowed"

    return rx.cond(
        State.habit_dates[habit].contains(date_str),
        f"{base_classes} completed bg-green-400 hover:bg-green-500 shadow-lg shadow-green-400/50",
        f"{base_classes} bg-gray-200 hover:bg-green-300",
    )


def get_month_grid(
    habit: str, year: int, month: int, current_date: datetime = None
) -> rx.Component:
    num_days = calendar.monthrange(year, month)[1]
    current = datetime.now()

    return rx.vstack(
        rx.text(calendar.month_name[month], class_name="text-xl font-semibold mt-4"),
        rx.grid(
            *[
                rx.tooltip(
                    rx.button(
                        class_name=get_button_class(habit, year, month, day),
                        on_click=lambda d=day: State.toggle_date(
                            habit, f"{year}-{month:02d}-{d:02d}"
                        ),
                        # Disable button for future dates
                        disabled=datetime(year, month, day).date() > current.date(),
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

    for i in range(0, 4):
        date = current_date - relativedelta(months=i)
        months.append((date.year, date.month))

    return months, current_date


def habit_calendar_view(habit: str) -> rx.Component:
    """Create a calendar view component for a specific habit."""
    months, current_date = get_last_three_months()

    # Using rx.cond for the streak count
    streak_count = rx.cond(
        State.habit_dates.contains(habit), State.habit_dates[habit].length(), 0
    )

    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.text(
                    habit,
                    class_name="text-2xl md:text-4xl font-bold bg-gradient-to-r from-indigo-600 to-indigo-400 bg-clip-text text-transparent",
                ),
                rx.spacer(),
                rx.box(
                    rx.hstack(
                        rx.icon("flame", size=20, color="#6366f1"),
                        rx.text(
                            f"{streak_count} days",
                            class_name="text-lg text-indigo-500 font-medium",
                        ),
                        class_name="bg-indigo-50/80 backdrop-blur-sm px-4 py-2 rounded-2xl shadow-sm hover:shadow-md transition-all duration-200 mx-auto flex justify-center items-center",
                    ),
                    class_name="w-full flex justify-center items-center",
                ),
                rx.box(
                    rx.hstack(
                        rx.button(
                            rx.image(
                                "/2.svg",
                                class_name="w-7 h-7 hover:opacity-75 hover:[filter:invert(93%)_sepia(7%)_saturate(1202%)_hue-rotate(95deg)_brightness(99%)_contrast(87%)]",
                            ),
                            variant="ghost",
                            on_click=lambda h=habit: State.mark_today(h),
                            class_name="hover:bg-indigo-50/50 rounded-xl transition-all duration-200",
                        ),
                        rx.dialog.root(
                            rx.dialog.trigger(
                                rx.button(
                                    rx.icon(
                                        "trash",
                                        color="gray",
                                        class_name="hover:text-red-500 transition-colors",
                                    ),
                                    variant="ghost",
                                    class_name="hover:bg-red-50/50 rounded-xl transition-all duration-200",
                                ),
                            ),
                            rx.dialog.content(
                                rx.dialog.title(
                                    "Delete Habit",
                                    class_name="text-3xl font-bold mb-2 text-center bg-gradient-to-r from-red-500 to-red-600 bg-clip-text text-transparent",
                                ),
                                rx.vstack(
                                    rx.box(
                                        rx.icon(
                                            "octagon-alert", size=24, color="#ef4444"
                                        ),
                                        rx.text(
                                            "Are you sure you want to delete this habit?",
                                            class_name="text-gray-700 font-medium ml-2",
                                        ),
                                        class_name="flex items-center justify-center mt-4",
                                    ),
                                    rx.text(
                                        "This action cannot be undone.",
                                        class_name="text-gray-500 text-sm mt-2",
                                    ),
                                    rx.box(
                                        rx.text(
                                            habit,
                                            class_name="font-bold text-xl",
                                        ),
                                        class_name="mt-4 p-4 bg-red-50/50 backdrop-blur-sm rounded-xl border border-red-100 text-center",
                                    ),
                                    rx.hstack(
                                        rx.dialog.close(
                                            rx.button(
                                                "Cancel",
                                                class_name="bg-white/80 backdrop-blur-sm border-2 border-gray-200 hover:bg-gray-50 text-gray-800 px-6 py-2.5 rounded-xl font-medium transition-all duration-200",
                                            ),
                                        ),
                                        rx.button(
                                            "Delete",
                                            on_click=lambda h=habit: State.delete_habit(
                                                h
                                            ),
                                            class_name="bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700 text-white px-6 py-2.5 rounded-xl font-medium shadow-lg shadow-red-500/30 transition-all duration-200",
                                        ),
                                        class_name="mt-4 space-x-4 w-full justify-end",
                                    ),
                                    class_name="w-full",
                                ),
                                class_name="bg-white/95 backdrop-blur-sm p-6 rounded-3xl shadow-2xl border border-gray-100 max-w-md mx-auto",
                            ),
                        ),
                        class_name="flex items-center justify-center",
                    ),
                    class_name="bg-indigo-50/80 backdrop-blur-sm px-6 py-2 rounded-2xl shadow-sm hover:shadow-md transition-all duration-200",
                ),
                class_name="w-full items-center justify-center",
            ),
            rx.box(
                rx.hstack(
                    *[
                        get_month_grid(habit, year, month, current_date)
                        for year, month in months
                    ],
                    class_name="min-w-max backdrop-blur-sm",
                ),
                class_name="w-full overflow-x-auto scrollbar-thin scrollbar-thumb-indigo-200 scrollbar-track-transparent mt-2",
            ),
            class_name="p-8 bg-white/50 backdrop-blur-sm border border-indigo-100 rounded-2xl w-full shadow-2xl",
            align_items="start",
        ),
        class_name="w-full",
    )


def main_section() -> rx.Component:
    months, current_date = get_last_three_months()
    return rx.vstack(
        # hero section
        rx.box(
            rx.vstack(
                rx.text(
                    "habit tracker", class_name="text-5xl md:text-6xl font-extrabold"
                ),
                rx.text(
                    "Create and maintain your habits to build healthy life patterns",
                    class_name="text-lg md:text-xl font-normal mt-2 text-center mx-4",
                ),
                rx.image("/Chill-Time.svg", class_name="w-60 h-60 md:w-80 md:h-80"),
                spacing="0",
                class_name="w-full flex items-center justify-center mt-10",
            ),
            class_name="w-full mt-4 bg-yellow-200 rounded-3xl p-4",
        ),
        # input section
        rx.hstack(
            rx.input(
                value=State.habit,
                class_name="w-full mt-4 mx-auto text-black text-2xl bg-transparent rounded-2xl h-16",
                on_change=State.set_habit,
            ),
            rx.button(
                rx.hstack(
                    rx.icon("plus", size=28),
                    rx.text("create", class_name="text-2xl font-semibold"),
                    class_name="flex items-center justify-center",
                ),
                class_name="mt-4 mx-auto text-black bg-gray-200 rounded-2xl p-8",
                on_click=State.handle_submit,
            ),
            class_name="w-full flex items-center justify-center",
        ),
        # calendar view
        rx.vstack(
            rx.foreach(State.habits, lambda habit: habit_calendar_view(habit)),
            class_name="w-full mt-6",
            id="calendar-section",
        ),
        class_name="flex justify-center items-center mb-10",
    )
