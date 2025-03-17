import flet as ft

from home_screen import home_screen


# ================================ #
# USER EDITABLE ROUTES
# place routes here for the router to read.
# each entry here will be automatically routed to when the route changes to it's key.
# routes can be either an array of components, or a function that returns one.
# -------------------------------- #
route_builder: dict[str, list[any]] = {
    "/home": home_screen,
}
# ================================ #



def main(page: ft.Page):
    routes: dict[str, list[any]] = {name: input(page) if callable(input) else input for name, input in route_builder.items()}

    page.fonts = {
        "Jacques Francois": "/assets/JacquesFrancois-Regular.ttf"
    }
    page.theme = ft.Theme(font_family="Jacques Francois")

    page.title = "marvis"
    page.adaptive = True

    """
    Route change handler fires every time the route changes. Note that
    this can only happen through page.go() calls since this isn't a web app.
    """
    def route_change(route):
        page.views.clear()
        # append static (always on-screen) components here
        page.views.append(
            ft.View(
                page.route,
                routes[str(page.route)]
            )
        )
        page.update()

    # def view_pop(view):
    #     page.views.pop()
    #     top_view = page.views[-1]
    #     page.go(top_view.root)

    # page.on_view_pop = view_pop
    page.on_route_change = route_change

    # load topbar
    page.appbar = ft.AppBar(
        title=ft.Text("Adaptive AppBar"),
        center_title=True,
        bgcolor=ft.Colors.with_opacity(0.04, ft.CupertinoColors.SYSTEM_BACKGROUND),
    )

    # load navbar at bottom
    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(
                icon=ft.Icons.BOOKMARK_BORDER,
                selected_icon=ft.Icons.BOOKMARK,
                label="Your List",
            ),
            ft.NavigationBarDestination(icon=ft.Icons.EXPLORE, label="Explore"),
            ft.NavigationBarDestination(icon=ft.Icons.FEED_ROUNDED, label="Recent News"),
        ],
        selected_index=1,
        border=ft.Border(
            top=ft.BorderSide(color=ft.CupertinoColors.SYSTEM_GREY2, width=0)
        ),
        on_change=lambda e: page.go(["/list", "/explore", "/news"][e.index])
    )

    page.add(
        ft.SafeArea(
            ft.Column(
                [
                    ft.Checkbox(value=False, label="Dark Mode"),
                    ft.Text("First field:"),
                    ft.TextField(keyboard_type=ft.KeyboardType.TEXT),
                    ft.Text("Second field:"),
                    ft.TextField(keyboard_type=ft.KeyboardType.TEXT),
                    ft.Switch(label="A switch"),
                    ft.FilledButton(content=ft.Text("Adaptive button")),
                    ft.Text("Text line 1"),
                    ft.Text("Text line 2"),
                    ft.Text("Text line 3"),
                ]
            )
        )
    )
    # page.go("/home")


if __name__ == "__main__":
    ft.app(main)
    