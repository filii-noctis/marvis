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
        )
    ]
