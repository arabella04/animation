import flet as ft
import os

def main(page: ft.Page):
    page.title = "To Her"
    
    # Web App Window Settings
    page.window.width = 1050
    page.window.height = 600
    page.window.resizable = False  
    page.padding = 0

    # Force a direct backdrop color to bypass the gray screen completely
    page.bgcolor = "#FFF0F2"  

    # ROCK-SOLID PATH FIX: Get the absolute path of the directory running this file
    base_dir = os.path.dirname(os.path.abspath(__file__))
    page.assets_dir = os.path.join(base_dir, "assets")

    # --- NAVIGATION LOGIC ---
    def go_to_page2(e):
        page.clean()
        page.add(build_page_2())
        page.update()

    def go_to_page1(e):
        page.clean()
        page.add(main_layout)
        page.update()

    # --- PAGE 2 BUILDER ---
    def build_page_2():
        top_bar = ft.Container(
            padding=ft.Padding(20, 15, 20, 15),
            content=ft.Row(
                [
                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED,
                        icon_color="#6D4C41",
                        on_click=go_to_page1,
                        tooltip="Go Back"
                    ),
                    ft.Text(
                        value="Messages for My Favorite Nurse", 
                        size=20, 
                        weight=ft.FontWeight.W_600, 
                        color="#6D4C41",
                        font_family="Georgia"
                    ),
                    ft.Icon(ft.Icons.FAVORITE_ROUNDED, color="#EC407A", size=20)
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
        )

        def create_menu_card(title, subtitle, icon):
            return ft.Container(
                width=170,
                height=220,
                bgcolor="#FFFFFF",
                border_radius=20,
                padding=20,
                scale=1.0, 
                shadow=ft.BoxShadow(blur_radius=10, color="#1A000000", offset=ft.Offset(0, 4)),
                animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
                on_hover=lambda e: toggle_hover(e),
                content=ft.Column(
                    [
                        ft.Icon(icon, color="#EC407A", size=32),
                        ft.Container(height=10),
                        ft.Text(title, size=16, weight=ft.FontWeight.BOLD, color="#6D4C41"),
                        ft.Text(subtitle, size=12, color="#8D6E63"),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    horizontal_alignment="start" 
                )
            )

        def toggle_hover(e):
            # Evaluates the hover event safely
            e.control.scale = 1.05 if e.data == "true" or e.data is True else 1.0
            e.control.update()

        cards_row = ft.Row(
            [
                create_menu_card("Interactive cursor", "Things on my mind...", ft.Icons.AUTO_AWESOME_ROUNDED),
                create_menu_card("Things Unsaid", "What I've wanted to tell you", ft.Icons.FAVORITE_BORDER_ROUNDED),
                create_menu_card("Songs That u Like", "Little details I noticed", ft.Icons.AUTO_STORIES_ROUNDED),
                create_menu_card("Messages to Her", "Sincere notes just for you", ft.Icons.CHAT_BUBBLE_OUTLINE_ROUNDED),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=25
        )

        return ft.Stack(
            expand=True,
            controls=[
                # LAYER 1: Background Gradient
                ft.Container(
                    expand=True,
                    gradient=ft.LinearGradient(
                        begin="topCenter",
                        end="bottomCenter",
                        colors=["#FFF0F2", "#E8F7EE"]
                    ),
                ),
                
                # LAYER 2: Background Flower (No ignore pointer wrapper needed, it sits back natively!)
                ft.Container(
                    top=0,      
                    right=0,    
                    content=ft.Image(
                        src="flower2.png", 
                        width=1050,   
                        height=600,   
                        fit="cover"   
                    )
                ),
                
                # LAYER 3: Interactive UI Elements sitting comfortably on top
                ft.Column(
                    [
                        top_bar,
                        ft.Container(height=40),
                        ft.Text(
                            "Select a capsule to read:",
                            size=16,
                            italic=True,
                            color="#8D6E63",
                            text_align=ft.TextAlign.CENTER
                        ),
                        ft.Container(height=20),
                        cards_row
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            ]
        )

    # --- PAGE 1 LAYOUT ---
    main_layout = ft.Stack(
        expand=True,
        controls=[
            # LAYER 1 (BOTTOM): Background Pastel Linear Gradient
            ft.Container(
                expand=True,
                gradient=ft.LinearGradient(
                    begin="topCenter",
                    end="bottomCenter",
                    colors=["#FFF0F2", "#E8F7EE"] 
                ),
            ),
            
            # LAYER 2 (MIDDLE): Background Flower
            ft.Container(
                bottom=-20, 
                right=-20,
                content=ft.Image(
                    src="flower.png", 
                    width=750,  
                    height=450,
                    fit="contain" 
                )
            ),
            
            # LAYER 3 (TOP): Greetings Text and Clickable Button Layer
            ft.Container(
                alignment=ft.Alignment(0, -0.1),
                content=ft.Column(
                    [
                        ft.Text(
                            value='"Hi Nurse"',
                            size=56,  
                            weight=ft.FontWeight.W_500,
                            color="#6D4C41", 
                            italic=True,
                            font_family="Georgia"
                        ),
                        ft.Container(height=25),
                        ft.Button(
                            content=ft.Text(
                                value="click here", 
                                size=16, 
                                weight=ft.FontWeight.W_500,
                                color="#6D4C41"
                            ),
                            on_click=go_to_page2, 
                            style=ft.ButtonStyle(
                                bgcolor="#FFFFFF", 
                                padding=ft.Padding(40, 22, 40, 22), 
                                shape=ft.RoundedRectangleBorder(radius=30),
                                elevation=2,
                                overlay_color="#FFF5F5" 
                            )
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            )
        ]
    )

    page.add(main_layout)

ft.run(main)