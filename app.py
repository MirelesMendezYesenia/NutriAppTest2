import flet as ft

def LoginView(page, auth_controller): email_input = ft.TextField(label="Ingresar el correo del usuario", hint_text="correo",width=350,border=ft.InputBorder.NONE,icon=ft.Icons.EMAIL, border_radius=1)

pass_input = ft.TextField( label="Ingresa la contraseña", hint_text="Contraseña", width=350,border=ft.InputBorder.NONE,password=True,can_reveal_password=True, icon=ft.Icons.LOCK,border_radius=10)

mensaje_recuperacion = ft.Text( "Correo para recuperar enviado", color=ft.Colors.WHITE,bgcolor=ft.Colors.BLACK, visible=False )

def mostrar_mensaje(e):
    mensaje_recuperacion.visible = True
    page.update()

def cerrar_alerta(e):
    alerta.open = False
    page.update()

alerta = ft.AlertDialog( title=ft.Text("Error"),
    content=ft.Text("Tus datos son incorrectos"),
    actions=[
        ft.TextButton("Cerrar", on_click=cerrar_alerta)
    ]
)

def login_click(e):
    if not email_input.value or not pass_input.value:
        page.snack_bar = ft.SnackBar(
            ft.Text("Por favor llene todos los campos")
        )
        page.snack_bar.open = True
        page.update()
        return

    user, msg = auth_controller.login(
        email_input.value,
        pass_input.value
    )
    if user:
        page.user_data = user
        page.go("/dashboard")
    else:
        page.dialog = alerta
        alerta.content = ft.Text(msg)
        alerta.open = True
        page.update()

login_button = ft.ElevatedButton("Iniciar", on_click=login_click, width=350,bgcolor=ft.Colors.BLACK,color=ft.Colors.WHITE )

return ft.View(
    route="/",
    vertical_alignment=ft.MainAxisAlignment.CENTER,
    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    controls=[
        ft.Column(
            [
                ft.Text("Iniciar Sesión",size=30,weight=ft.FontWeight.BOLD),
                email_input,
                pass_input,
                ft.TextButton("Olvidaste la contraseña?", on_click=mostrar_mensaje),
                login_button,
                mensaje_recuperacion,
                ft.TextButton("Crear una cuenta nueva",on_click=lambda _: page.go("/registro")
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )
    ]
)
