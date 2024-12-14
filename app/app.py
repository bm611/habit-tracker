import reflex as rx
from .components.nav import navbar
from .components.body import main_section
from app.state import State


@rx.page(route="/", title="habit tracker")
def index() -> rx.Component:
    return rx.container(
        navbar(),
        main_section(),
        on_mount=State.load_initial_data,
    )


style = {
    "font_family": "Figtree",
}


app = rx.App(
    style=rx.Style(style),
    stylesheets=["/fonts/font.css"],
    theme=rx.theme(
        appearance="light",
    ),
)
