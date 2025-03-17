import flet as ft

def home_screen(page: ft.Page):
    return [
        ft.Container(
            content=ft.Stack([ # rendering text outlines involves stacking
                ft.Text(
                    spans=[
                        ft.TextSpan(
                            "MARVIS",
                            ft.TextStyle(
                                size=40,
                                weight=ft.FontWeight.BOLD,
                                foreground=ft.Paint(
                                    color='#f8c3c3',
                                    stroke_width=2,
                                    stroke_join=ft.StrokeJoin.ROUND,
                                    style=ft.PaintingStyle.STROKE,
                                ),
                            ),
                        ),
                    ],
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Text(
                    spans=[
                        ft.TextSpan(
                            "MARVIS",
                            ft.TextStyle(
                                size=40,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.with_opacity(0.41, '#f8c3c3'),
                            ),
                        ),
                    ],
                    text_align=ft.TextAlign.CENTER
                ),
            ]),
            alignment=ft.alignment.top_center,
            expand=True,
        ),
        # ft.Text("test page")
        ft.NavigationBar(
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
    ]
