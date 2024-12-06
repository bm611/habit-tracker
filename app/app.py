import reflex as rx
from .components.nav import navbar
from .components.body import main_section


@rx.page(route="/", title="habit tracker")
def index() -> rx.Component:
    return rx.container(
        navbar(),
        main_section(),
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
