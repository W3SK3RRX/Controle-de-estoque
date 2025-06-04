import tkinter as tk
from tkinter import ttk, messagebox
import db
import log_helper


def abrir_cadastro_usuario(usuario_logado):
    janela = tk.Toplevel()
    janela.title("Cadastro de Usuário")
    janela.geometry("400x300")
    janela.configure(bg="#f0f0f0")

    frame = tk.Frame(janela, bg="white", bd=2, relief="groove")
    frame.pack(padx=20, pady=20, fill="both", expand=True)

    tk.Label(frame, text="Cadastro de Usuário", font=("Arial", 14, "bold"), bg="white").pack(pady=(10, 5))

    input_frame = tk.Frame(frame, bg="white")
    input_frame.pack(pady=10)

    tk.Label(input_frame, text="Nome:", bg="white").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    nome = tk.Entry(input_frame, width=30)
    nome.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(input_frame, text="Senha:", bg="white").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    senha = tk.Entry(input_frame, show="*", width=30)
    senha.grid(row=1, column=1, padx=5, pady=5)

    def salvar():
        nome_usuario = nome.get().strip()
        senha_usuario = senha.get().strip()

        if not nome_usuario or not senha_usuario:
            messagebox.showwarning("Atenção", "Preencha todos os campos.")
            return

        conn = db.conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO usuarios (nome, senha) VALUES (?, ?)", (nome_usuario, senha_usuario))
            conn.commit()
            messagebox.showinfo("Sucesso", f"Usuário '{nome_usuario}' cadastrado com sucesso!")
            log_helper.registrar(usuario_logado, "Cadastro de Usuário", f"Usuário '{nome_usuario}' cadastrado.")
            janela.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar usuário: {e}")
        finally:
            conn.close()

    botoes_frame = tk.Frame(frame, bg="white")
    botoes_frame.pack(pady=10)

    tk.Button(botoes_frame, text="Salvar", width=15, bg="#4CAF50", fg="white", command=salvar).grid(row=0, column=0, padx=5)
    tk.Button(botoes_frame, text="Cancelar", width=15, command=janela.destroy).grid(row=0, column=1, padx=5)


def abrir_listagem_usuarios(usuario_logado):
    janela = tk.Toplevel()
    janela.title("Gerenciar Usuários")
    janela.geometry("500x400")
    janela.configure(bg="#f0f0f0")

    frame = tk.Frame(janela, bg="white", bd=2, relief="groove")
    frame.pack(padx=20, pady=20, fill="both", expand=True)

    tk.Label(frame, text="Gerenciar Usuários", font=("Arial", 14, "bold"), bg="white").pack(pady=(10, 5))

    tabela_frame = tk.Frame(frame, bg="white")
    tabela_frame.pack(pady=10, fill="both", expand=True)

    colunas = ("id", "nome")
    tabela = ttk.Treeview(tabela_frame, columns=colunas, show="headings")
    tabela.heading("id", text="ID")
    tabela.heading("nome", text="Nome")

    tabela.column("id", width=50, anchor="center")
    tabela.column("nome", width=300, anchor="center")  # <-- Centralizado

    tabela.pack(fill="both", expand=True)

    # Carregar usuários
    def carregar_usuarios():
        for row in tabela.get_children():
            tabela.delete(row)

        conn = db.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome FROM usuarios ORDER BY nome")
        usuarios = cursor.fetchall()
        conn.close()

        for u in usuarios:
            tabela.insert("", "end", values=u)

    carregar_usuarios()

    def excluir():
        item_selecionado = tabela.selection()
        if not item_selecionado:
            messagebox.showwarning("Atenção", "Selecione um usuário para excluir.")
            return

        usuario = tabela.item(item_selecionado, "values")
        usuario_id, usuario_nome = usuario

        confirm = messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja excluir o usuário '{usuario_nome}'?")
        if not confirm:
            return

        conn = db.conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM usuarios WHERE id = ?", (usuario_id,))
            conn.commit()
            messagebox.showinfo("Sucesso", f"Usuário '{usuario_nome}' excluído com sucesso!")
            log_helper.registrar(usuario_logado, "Exclusão de Usuário", f"Usuário ID {usuario_id} excluído.")
            carregar_usuarios()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao excluir usuário: {e}")
        finally:
            conn.close()

    botoes_frame = tk.Frame(frame, bg="white")
    botoes_frame.pack(pady=10)

    tk.Button(botoes_frame, text="Excluir", width=15, bg="#f44336", fg="white", command=excluir).grid(row=0, column=0, padx=5)
    tk.Button(botoes_frame, text="Fechar", width=15, command=janela.destroy).grid(row=0, column=1, padx=5)
