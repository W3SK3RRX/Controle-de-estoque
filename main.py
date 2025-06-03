import tkinter as tk
from tkinter import messagebox
from db import criar_tabelas, criar_usuario_padrao
from auth import autenticar
from logs import registrar_log
from dashboard import abrir_dashboard

def realizar_login():
    usuario = entrada_usuario.get()
    senha = entrada_senha.get()

    if autenticar(usuario, senha):
        registrar_log("Login bem-sucedido", usuario)
        janela_login.destroy()  # Fecha a tela de login
        abrir_dashboard(usuario)  # <- Aqui você abre a tela principal

    else:
        registrar_log("Tentativa de login falhou", usuario)
        messagebox.showerror("Erro", "Usuário ou senha incorretos.")


# Inicializar banco
criar_tabelas()
criar_usuario_padrao()


# Tela de Login
janela_login = tk.Tk()
janela_login.title("Login - Sistema de Controle de Estoque")

# Definir janela em tela cheia
try:
    janela_login.state('zoomed')  # Windows e Linux
except:
    janela_login.attributes('-fullscreen', True)  # Mac

# Frame centralizado
frame = tk.Frame(janela_login, bg="#441858", padx=40, pady=30, relief="raised", bd=3)
frame.place(relx=0.5, rely=0.5, anchor="center")

# Título
tk.Label(
    frame,
    text="Controle de Estoque",
    font=("Arial", 22, "bold"),
    bg="#441858",
    fg="white"
).grid(row=0, column=0, columnspan=2, pady=(0, 20))

# Labels e Entradas
tk.Label(frame, text="Usuário:", font=("Arial", 14), bg="#441858", fg="white").grid(row=1, column=0, padx=10, pady=10, sticky="e")
entrada_usuario = tk.Entry(frame, font=("Arial", 14), width=25)
entrada_usuario.grid(row=1, column=1, padx=10, pady=10)

tk.Label(frame, text="Senha:", font=("Arial", 14), bg="#441858", fg="white").grid(row=2, column=0, padx=10, pady=10, sticky="e")
entrada_senha = tk.Entry(frame, font=("Arial", 14), show="*", width=25)
entrada_senha.grid(row=2, column=1, padx=10, pady=10)

# Botão Entrar
tk.Button(
    frame,
    text="Entrar",
    font=("Arial", 14, "bold"),
    bg="#2E7D32",
    fg="white",
    padx=10,
    pady=5,
    command=realizar_login
).grid(row=3, column=0, columnspan=2, pady=20)

# Botão Sair
tk.Button(
    frame,
    text="Sair",
    font=("Arial", 12, "bold"),
    bg="#f44336",
    fg="white",
    padx=10,
    pady=5,
    command=janela_login.quit
).grid(row=4, column=0, columnspan=2, pady=(0, 10))

# Focar no campo de usuário
entrada_usuario.focus_set()

# Atalho para tecla Enter
janela_login.bind('<Return>', lambda event: realizar_login())

janela_login.mainloop()
