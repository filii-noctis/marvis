import flet as ft


# ================================ #
# USER EDITABLE ROUTES
# place routes here for the router to read.
# each entry here will be automatically routed to when the route changes to it's key.
# routes can be either an array of components, or a function that returns one.
# -------------------------------- #
route_builder: dict[str, list[any]] = {
    "/test": [
        ft.Text("test page")],
}
# ================================ #

routes: dict[str, list[any]] = {name: input() if callable(input) else input for name, input in route_builder.items()}


def main(page):
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

    page.on_route_change = route_change

    # load topbar
    page.appbar = ft.AppBar(
        leading=ft.TextButton("New", style=ft.ButtonStyle(padding=0)),
        title=ft.Text("Adaptive AppBar"),
        actions=[
            ft.IconButton(ft.cupertino_icons.ADD, style=ft.ButtonStyle(padding=0))
        ],
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
        border=ft.Border(
            top=ft.BorderSide(color=ft.CupertinoColors.SYSTEM_GREY2, width=0)
        ),
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


if __name__ == "__main__":
    ft.app(main)
    