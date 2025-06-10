import tkinter as tk
from tkinter import ttk, messagebox
import db
import log_helper


def abrir_cadastro_categoria(usuario_logado):
    janela = tk.Toplevel()
    janela.state('zoomed')
    janela.title("Cadastro de Categorias")
    janela.geometry("600x600")
    janela.configure(bg="#f0f0f0")

    frame = tk.Frame(janela, bg="white", bd=2, relief="groove")
    frame.pack(padx=20, pady=20, fill="both", expand=True)

    tk.Label(frame, text="Cadastro de Categoria", font=("Arial", 14, "bold"), bg="white").pack(pady=(10, 5))

    input_frame = tk.Frame(frame, bg="white")
    input_frame.pack(pady=(10, 5))

    tk.Label(input_frame, text="Nome da Categoria:", bg="white").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    nome = tk.Entry(input_frame, width=30)
    nome.grid(row=0, column=1, padx=5, pady=5)

        # ---------- Tabela de categorias aprimorada ----------
    tabela_frame = tk.Frame(frame, bg="white")
    tabela_frame.pack(pady=10, fill="both", expand=True)

    style = ttk.Style()
    style.theme_use("clam")  # Visual mais agradável
    style.configure("Treeview",
                    background="white",
                    foreground="black",
                    rowheight=30,
                    fieldbackground="white",
                    font=("Arial", 10))
    style.configure("Treeview.Heading",
                    background="#4CAF50",
                    foreground="white",
                    font=("Arial", 11, "bold"))
    style.map('Treeview', background=[('selected', '#3399FF')])

    colunas = ("id", "nome")
    tabela = ttk.Treeview(tabela_frame, columns=colunas, show="headings")

    # Cabeçalhos
    tabela.heading("id", text="ID")
    tabela.heading("nome", text="Categoria")

    # Largura e alinhamento das colunas
    tabela.column("id", width=60, anchor="center")
    tabela.column("nome", width=400, anchor="center")

    tabela.pack(side="left", fill="both", expand=True)

    # Scrollbar
    scrollbar = ttk.Scrollbar(tabela_frame, orient="vertical", command=tabela.yview)
    tabela.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")


    def carregar_categorias():
        for row in tabela.get_children():
            tabela.delete(row)

        conn = db.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome FROM categorias ORDER BY nome")
        categorias = cursor.fetchall()
        conn.close()

        for c in categorias:
            tabela.insert("", "end", values=c)

    carregar_categorias()

    # ---------- Funções ----------
    def salvar():
        categoria_nome = nome.get().strip()
        if not categoria_nome:
            messagebox.showwarning("Atenção", "O nome da categoria não pode ser vazio.")
            return

        conn = db.conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO categorias (nome) VALUES (?)", (categoria_nome,))
            conn.commit()
            messagebox.showinfo("Sucesso", f"Categoria '{categoria_nome}' cadastrada com sucesso!")
            log_helper.registrar(usuario_logado, "Cadastro de Categoria", f"Categoria '{categoria_nome}' cadastrada.")
            nome.delete(0, tk.END)
            carregar_categorias()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar categoria: {e}")
        finally:
            conn.close()

    def excluir():
        item_selecionado = tabela.selection()
        if not item_selecionado:
            messagebox.showwarning("Atenção", "Selecione uma categoria para excluir.")
            return

        categoria = tabela.item(item_selecionado, "values")
        categoria_id, categoria_nome = categoria

        confirm = messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja excluir a categoria '{categoria_nome}'?")
        if not confirm:
            return

        conn = db.conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM categorias WHERE id = ?", (categoria_id,))
            conn.commit()
            messagebox.showinfo("Sucesso", f"Categoria '{categoria_nome}' excluída com sucesso!")
            log_helper.registrar(usuario_logado, "Exclusão de Categoria", f"Categoria ID {categoria_id} excluída.")
            carregar_categorias()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao excluir categoria: {e}")
        finally:
            conn.close()

    def editar():
        item_selecionado = tabela.selection()
        if not item_selecionado:
            messagebox.showwarning("Atenção", "Selecione uma categoria para editar.")
            return

        categoria = tabela.item(item_selecionado, "values")
        categoria_id, categoria_nome = categoria

        novo_nome = simple_input_dialog("Editar Categoria", f"Digite o novo nome para a categoria '{categoria_nome}':")
        if not novo_nome:
            return  # Cancelado ou vazio

        conn = db.conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE categorias SET nome = ? WHERE id = ?", (novo_nome.strip(), categoria_id))
            conn.commit()
            messagebox.showinfo("Sucesso", f"Categoria atualizada para '{novo_nome.strip()}'!")
            log_helper.registrar(usuario_logado, "Edição de Categoria", f"Categoria ID {categoria_id} atualizada para '{novo_nome.strip()}'.")
            carregar_categorias()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao editar categoria: {e}")
        finally:
            conn.close()

    def simple_input_dialog(titulo, mensagem):
        input_win = tk.Toplevel(janela)
        input_win.title(titulo)
        input_win.geometry("350x150")
        input_win.transient(janela)
        input_win.grab_set()

        tk.Label(input_win, text=mensagem).pack(pady=10)
        entry = tk.Entry(input_win, width=30)
        entry.pack(pady=5)
        entry.focus()

        resultado = {"valor": None}

        def confirmar():
            valor = entry.get().strip()
            if valor:
                resultado["valor"] = valor
                input_win.destroy()
            else:
                messagebox.showwarning("Atenção", "O nome não pode ser vazio.")

        def cancelar():
            input_win.destroy()

        btn_frame = tk.Frame(input_win)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Confirmar", command=confirmar, width=10, bg="#4CAF50", fg="white").grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Cancelar", command=cancelar, width=10, bg="#f44336", fg="white").grid(row=0, column=1, padx=5)

        input_win.wait_window()
        return resultado["valor"]

    # ---------- Botões ----------
    botoes_frame = tk.Frame(frame, bg="white")
    botoes_frame.pack(pady=10)

    tk.Button(botoes_frame, text="Salvar", width=15, bg="#4CAF50", fg="white", command=salvar).grid(row=0, column=0, padx=5)
    tk.Button(botoes_frame, text="Editar", width=15, bg="#2196F3", fg="white", command=editar).grid(row=0, column=1, padx=5)
    tk.Button(botoes_frame, text="Excluir", width=15, bg="#f44336", fg="white", command=excluir).grid(row=0, column=2, padx=5)
    tk.Button(botoes_frame, text="Fechar", width=15, command=janela.destroy).grid(row=0, column=3, padx=5)
