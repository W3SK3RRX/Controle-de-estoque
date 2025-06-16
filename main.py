import tkinter as tk
from tkinter import messagebox
import os
import sys

from db import criar_tabelas, criar_usuario_padrao
from auth import autenticar
from logs import registrar_log
from dashboard import abrir_dashboard

# Função para localizar arquivos ao rodar com PyInstaller
def resource_path(relative_path):
    """Retorna o caminho absoluto, lidando com o _MEIPASS do PyInstaller."""
    try:
        base_path = sys._MEIPASS  # PyInstaller cria essa pasta temporária
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def realizar_login():
    usuario = entrada_usuario.get()
    senha = entrada_senha.get()

    if autenticar(usuario, senha):
        registrar_log("Login bem-sucedido", usuario)
        janela_login.destroy()  # Fecha a tela de login
        abrir_dashboard(usuario)
    else:
        registrar_log("Tentativa de login falhou", usuario)
        messagebox.showerror("Erro", "Usuário ou senha incorretos.")


# Inicializar banco
criar_tabelas()
criar_usuario_padrao()

# Tela de Login
janela_login = tk.Tk()
janela_login.title("Login - Sistema de Controle de Estoque - Senhor Açaí")

# Definir janela em tela cheia
try:
    janela_login.state('zoomed')  # Windows e Linux
except:
    janela_login.attributes('-fullscreen', True)  # Mac

# Carregar e configurar a imagem de fundo
background_image_path = resource_path("media/bg.png")
background_image = tk.PhotoImage(file=background_image_path)
background_label = tk.Label(janela_login, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Frame centralizado
frame = tk.Frame(janela_login, bg="#790071", padx=40, pady=30, relief="raised", bd=3)
frame.place(relx=0.5, rely=0.5, anchor="center")

# Título
tk.Label(
    frame,
    text="Controle de Estoque - Senhor Açaí",
    font=("Helvetica", 24, "bold"),
    bg="#790071",
    fg="white"
).grid(row=0, column=0, columnspan=2, pady=(0, 30))

# Labels e Entradas
tk.Label(frame, text="Usuário:", font=("Arial", 14, "bold"), bg="#790071", fg="white").grid(row=1, column=0, padx=(10, 2), pady=10, sticky="e")
entrada_usuario = tk.Entry(frame, font=("Arial", 14), width=25)
entrada_usuario.grid(row=1, column=1, padx=(2, 10), pady=10)

tk.Label(frame, text="Senha:", font=("Arial", 14, "bold"), bg="#790071", fg="white").grid(row=2, column=0, padx=(10, 2), pady=10, sticky="e")
entrada_senha = tk.Entry(frame, font=("Arial", 14), show="*", width=25)
entrada_senha.grid(row=2, column=1, padx=(2, 10), pady=10)

# Botões
botao_entrar = tk.Button(
    frame,
    text="ENTRAR",
    font=("Helvetica", 12, "bold"),
    bg="#8DB038",
    fg="white",
    padx=20,
    pady=10,
    bd=0,
    cursor="hand2",
    activebackground="#7B1FA2",
    activeforeground="white",
    command=realizar_login
)
botao_entrar.grid(row=3, column=0, columnspan=2, pady=30)

botao_sair = tk.Button(
    frame,
    text="SAIR",
    font=("Helvetica", 10, "bold"),
    bg="#B51E00",
    fg="#E1BEE7",
    padx=15,
    pady=8,
    bd=0,
    cursor="hand2",
    activebackground="#4A148C",
    activeforeground="white",
    command=janela_login.quit
)
botao_sair.grid(row=4, column=0, columnspan=2, pady=(0, 10))

entrada_usuario.focus_set()
janela_login.bind('<Return>', lambda event: realizar_login())

janela_login.mainloop()
