import flet as ft

# Three screens for the navigation
def home_screen(page):
    return [
        ft.Text("Your List", size=30, weight=ft.FontWeight.BOLD),
        ft.ListView(
            [
                grocery_item(
                    "Fresh Bagged Carrots",
                    "Walmart Canada",
                    27.49,
                    1.02,
                    True
                ),
                grocery_item(
                    "3kg Yellow Potatoes",
                    "Walmart Canada",
                    14.99,
                    0.60,
                    False
                ),
                grocery_item(
                    "Fresh Bagged Carrots",
                    "Walmart Canada",
                    27.49,
                    1.02,
                    True
                ),
                grocery_item(
                    "Fresh Bagged Carrots",
                    "Walmart Canada",
                    27.49,
                    1.02,
                    True
                ),
            ],
            spacing=10,
            padding=20,


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
    ]

def explore_screen(page):
    return [
        ft.Text("Explore", size=30, weight=ft.FontWeight.BOLD),
        ft.Container(
            ft.Column([
                ft.TextField(
                    hint_text="Search for Items",
                    prefix_icon=ft.icons.SEARCH,
                    border_radius=20,
                    filled=True,
                    expand=True
                ),
                ft.Divider(height=20, color=ft.colors.TRANSPARENT),
                ft.Text("Featured Items", size=20, weight=ft.FontWeight.BOLD),
                ft.ListView(
                    [
                        grocery_item(
                            "Organic Bananas",
                            "Walmart Canada",
                            4.99,
                            0.75,
                            True
                        ),
                        grocery_item(
                            "Lean Ground Beef",
                            "Walmart Canada",
                            12.99,
                            0.30,
                            False
                        ),
                    ],
                    spacing=10,
                    height=300,
                )
            ]),
            padding=20
        )
    ]

    return [

# Component for grocery item
def grocery_item(name, store, price, price_change, price_increased):
    return ft.Container(
        ft.Column([
            ft.Row([
                ft.Container(
                    content=ft.Icon(ft.icons.IMAGE, size=40),
                    width=60,
                    height=60,
                    bgcolor=ft.colors.GREY_300,
                    border_radius=8,
                ),
                ft.Column([
                    ft.Text(name, weight=ft.FontWeight.BOLD),
                    ft.Text(store, size=12),
                    ft.Row([
                        ft.Container(width=10, height=10, bgcolor="#FFD700", border_radius=10),
                        ft.Container(width=10, height=10, bgcolor="#008000", border_radius=10),
                        ft.Container(width=10, height=10, bgcolor="#0000FF", border_radius=10),
                    ], spacing=5)
                ], spacing=5, expand=True)
            ]),
            ft.Row([
                ft.Text(f"${price:.2f}", size=24, weight=ft.FontWeight.BOLD),
                ft.Text(
                    f"${price_change:.2f} {'Increase' if price_increased else 'Decrease'} Over Last Year",
                    size=12,
                    color=ft.colors.RED if price_increased else ft.colors.GREEN,
                ),
                ft.Icon(
                    ft.icons.ARROW_UPWARD if price_increased else ft.icons.ARROW_DOWNWARD,
                    color=ft.colors.RED if price_increased else ft.colors.GREEN,
                    size=14
                )
            ])
        ]),
        padding=10,
        bgcolor="#FFE4E1",  # Light pink background
        border_radius=8,
        width=400
    )

# Component for news item
def news_item(title, description, date):
    return ft.Container(
        ft.Column([
            ft.Text(title, weight=ft.FontWeight.BOLD, size=16),
            ft.Text(description, size=14),
            ft.Row([
                ft.Text(date, size=12, color=ft.colors.GREY_600),
                ft.TextButton("Read more", icon=ft.icons.ARROW_FORWARD)
            ])
        ]),
        padding=10,
        bgcolor=ft.colors.WHITE,
        border_radius=8,
        border=ft.border.all(1, ft.colors.GREY_300),
        width=400
    )

def main(page: ft.Page):
    page.fonts = {
        "Jacques Francois": "/assets/JacquesFrancois-Regular.ttf"
    }
    page.theme = ft.Theme(font_family="Jacques Francois")
    page.title = "Marvis"

    page.adaptive = True
    page.bgcolor = "#96979A"

    page.appbar = ft.AppBar(
        title=ft.Text("MARVIS", weight=ft.FontWeight.BOLD, color="#F8C3C3", size=50),
        center_title=True,
        bgcolor=ft.colors.with_opacity(0, "#96979A"),
    )

    content_pagelet = ft.Container(
        content=ft.Column(),
        visible=True
    )

    # Function to change screen content
    def change_screen(index):
        if index == 0:
            content_pagelet.content = ft.Column(home_screen(page))
        elif index == 1:
            content_pagelet.content = ft.Column(explore_screen(page))
        elif index == 2:
            content_pagelet.content = ft.Column(news_screen(page))

        page.update()

    # Create navigation bar
    navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(
                icon=ft.icons.BOOKMARK_BORDER,
                selected_icon=ft.icons.BOOKMARK,
                label="Your List",
            ),
            ft.NavigationBarDestination(icon=ft.icons.EXPLORE, label="Explore"),
            ft.NavigationBarDestination(icon=ft.icons.FEED_ROUNDED, label="Recent News"),
        ],
        selected_index=1,
        on_change=lambda e: change_screen(e.control.selected_index)
    )

    # Main page layout with content and navigation bar
    page.add(
        content_pagelet,
    )
    # page.go("/home")



if __name__ == "__main__":
    ft.app(main)
