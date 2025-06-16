import tkinter as tk
from tkinter import ttk, messagebox
import db
import log_helper
from datetime import datetime, timedelta



def abrir_cadastro_produto(usuario_logado):
    janela = tk.Toplevel()
    janela.state('zoomed')
    janela.title("Cadastrar Produto")
    janela.geometry("600x600")
    janela.configure(bg="#e9ecef")

    frame = tk.Frame(janela, bg="white", bd=3, relief="ridge")
    frame.pack(padx=20, pady=20, fill="both", expand=True)

    # Título
    tk.Label(
        frame, text="Cadastro de Produto",
        font=("Arial", 18, "bold"),
        bg="white", fg="#333"
    ).pack(pady=(15, 10))

    form_frame = tk.Frame(frame, bg="white")
    form_frame.pack(pady=10)

    # Labels e Inputs
    campos = [
        ("Nome:", "nome"),
        ("Categoria:", "categoria"),
        ("Quantidade:", "quantidade"),
        ("Unidade (ex.: kg, un):", "unidade"),
        ("Validade (AAAA-MM-DD):", "validade"),
        ("Estoque Mínimo:", "estoque_minimo")
    ]

    entries = {}

    for i, (label_text, key) in enumerate(campos):
        tk.Label(
            form_frame, text=label_text,
            bg="white", fg="#555",
            font=("Arial", 10, "bold")
        ).grid(row=i, column=0, sticky="e", padx=10, pady=8)

        if key == "categoria":
            entry = ttk.Combobox(form_frame, width=30, state="readonly")
            entry['values'] = obter_categorias()
        else:
            entry = tk.Entry(form_frame, width=32)

        entry.grid(row=i, column=1, pady=5, padx=10)
        entries[key] = entry

    # Função de salvar
    def salvar():
        try:
            conn = db.conectar()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO produtos (nome, categoria, quantidade, unidade, validade, estoque_minimo)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                entries['nome'].get(),
                entries['categoria'].get(),
                int(entries['quantidade'].get()),
                entries['unidade'].get(),
                entries['validade'].get(),
                int(entries['estoque_minimo'].get())
            ))
            conn.commit()
            conn.close()

            log_helper.registrar(
                usuario_logado, "Cadastro de Produto",
                f"Produto '{entries['nome'].get()}' cadastrado."
            )
            messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
            janela.destroy()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {e}")

    # Botões
    botoes_frame = tk.Frame(frame, bg="white")
    botoes_frame.pack(pady=20)

    tk.Button(
        botoes_frame, text="Salvar", width=15,
        bg="#4CAF50", fg="white",
        font=("Arial", 10, "bold"),
        command=salvar
    ).grid(row=0, column=0, padx=10)

    tk.Button(
        botoes_frame, text="Cancelar", width=15,
        bg="#f44336", fg="white",
        font=("Arial", 10, "bold"),
        command=janela.destroy
    ).grid(row=0, column=1, padx=10)



def obter_categorias():
    try:
        conn = db.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT nome FROM categorias")
        categorias = [linha[0] for linha in cursor.fetchall()]
        conn.close()
        return categorias
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao carregar categorias: {e}")
        return []

# ==========================
# 📄 Frame de Listagem de Produtos




def abrir_listagem_produtos(usuario_logado):
    janela = tk.Toplevel()
    janela.state('zoomed')
    janela.title("Gestão de Produtos")
    janela.configure(bg="#f0f0f0")

    frame = tk.Frame(janela, bg="white", bd=2, relief="groove")
    frame.pack(padx=20, pady=20, fill="both", expand=True)

    tk.Label(frame, text="Produtos Cadastrados", font=("Arial", 16, "bold"), bg="white").pack(pady=10)

    # Filtros
    filtro_frame = tk.Frame(frame, bg="white")
    filtro_frame.pack(pady=5)

    tk.Label(filtro_frame, text="Nome:", bg="white").grid(row=0, column=0, padx=5, pady=5)
    filtro_nome = tk.Entry(filtro_frame, width=20)
    filtro_nome.grid(row=0, column=1, padx=5)

    tk.Label(filtro_frame, text="Categoria:", bg="white").grid(row=0, column=2, padx=5)
    filtro_categoria = ttk.Combobox(filtro_frame, width=18, state="readonly")
    filtro_categoria.grid(row=0, column=3, padx=5)

    tk.Label(filtro_frame, text="Qtd ≥", bg="white").grid(row=0, column=4, padx=5)
    filtro_quantidade = tk.Entry(filtro_frame, width=10)
    filtro_quantidade.grid(row=0, column=5, padx=5)

    # Tabela
    colunas = ("ID", "Nome", "Categoria", "Quantidade", "Unidade", "Validade", "Estoque Mínimo")

    tree = ttk.Treeview(frame, columns=colunas, show="headings", height=15)
    tree.pack(padx=10, pady=10, fill="both", expand=True)

    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, anchor=tk.CENTER, width=100)

    tree.column("Nome", width=180)
    tree.column("Categoria", width=120)

    scrollbar = ttk.Scrollbar(tree, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

        # ===============================
    # 🔵 Legenda das Cores
    legenda_frame = tk.Frame(frame, bg="white")
    legenda_frame.pack(pady=(0, 10))

    tk.Label(legenda_frame, text="Legenda:", bg="white", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5)

    tk.Label(legenda_frame, bg="#d4edda", width=2, height=1, bd=1, relief="solid").grid(row=0, column=1)
    tk.Label(legenda_frame, text="Validade OK", bg="white").grid(row=0, column=2, padx=5)

    tk.Label(legenda_frame, bg="#fff3cd", width=2, height=1, bd=1, relief="solid").grid(row=0, column=3)
    tk.Label(legenda_frame, text="Vence em até 7 dias", bg="white").grid(row=0, column=4, padx=5)

    tk.Label(legenda_frame, bg="#f8d7da", width=2, height=1, bd=1, relief="solid").grid(row=0, column=5)
    tk.Label(legenda_frame, text="Vencido", bg="white").grid(row=0, column=6, padx=5)

    tk.Label(legenda_frame, bg="white", width=2, height=1, bd=1, relief="solid").grid(row=0, column=7)
    tk.Label(legenda_frame, text="Sem validade", bg="white").grid(row=0, column=8, padx=5)


    # Função para carregar categorias no Combobox
    def carregar_categorias():
        try:
            conn = db.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT categoria FROM produtos WHERE categoria IS NOT NULL AND categoria <> ''")
            categorias = [row[0] for row in cursor.fetchall()]
            conn.close()
            filtro_categoria['values'] = [""] + categorias  # O primeiro item vazio para permitir "todos"
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar categorias: {e}")


    def carregar_dados():
        tree.tag_configure("estoque_baixo", background="#ffcccc", foreground="red")

        for item in tree.get_children():
            tree.delete(item)

        conn = db.conectar()
        cursor = conn.cursor()

        consulta = "SELECT id, nome, categoria, quantidade, unidade, validade, estoque_minimo FROM produtos WHERE 1=1"
        params = []

        if filtro_nome.get():
            consulta += " AND nome LIKE ?"
            params.append(f"%{filtro_nome.get()}%")
        if filtro_categoria.get():
            consulta += " AND categoria = ?"
            params.append(filtro_categoria.get())
        if filtro_quantidade.get():
            try:
                qtd = int(filtro_quantidade.get())
                consulta += " AND quantidade >= ?"
                params.append(qtd)
            except ValueError:
                messagebox.showerror("Erro", "Quantidade mínima deve ser um número inteiro.")
                return

        cursor.execute(consulta, params)
        produtos = cursor.fetchall()
        conn.close()

        hoje = datetime.now().date()

        for p in produtos:
            estoque_atual = p[3]
            estoque_minimo = p[6]

            validade_str = p[5]
            try:
                validade = datetime.strptime(validade_str, "%Y-%m-%d").date()
            except:
                validade = None

            if validade:
                if validade < hoje:
                    cor = "#f8d7da"  # vencido
                elif validade <= hoje + timedelta(days=7):
                    cor = "#fff3cd"  # vence em breve
                else:
                    cor = "#d4edda"  # validade ok
            else:
                cor = "white"  # sem validade

            # Cor de estoque baixo tem prioridade
            if estoque_atual < estoque_minimo:
                tree.insert("", tk.END, values=p, tags=("estoque_baixo",))
            else:
                tree.insert("", tk.END, values=p, tags=(str(p[0]),))

            tree.tag_configure(str(p[0]), background=cor)


    carregar_categorias()
    carregar_dados()

    # Função para excluir
    def excluir():
        selecionado = tree.selection()
        if selecionado:
            item = tree.item(selecionado)
            produto_id = item["values"][0]

            confirmar = messagebox.askyesno("Confirmar", "Deseja realmente excluir este produto?")
            if confirmar:
                try:
                    conn = db.conectar()
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))
                    conn.commit()
                    conn.close()

                    log_helper.registrar(usuario_logado, "Exclusão de Produto", f"Produto ID {produto_id} excluído.")
                    messagebox.showinfo("Sucesso", "Produto excluído!")
                    carregar_dados()
                    carregar_categorias()
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao excluir: {e}")

    # Função para editar
    def editar():
        selecionado = tree.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um produto para editar.")
            return

        item = tree.item(selecionado)
        valores = item["values"]

        janela_editar = tk.Toplevel()
        janela_editar.title("Editar Produto")
        janela_editar.geometry("600x600")
        janela_editar.configure(bg="#f0f0f0")

        frame_editar = tk.Frame(janela_editar, bg="white", bd=2, relief="groove")
        frame_editar.pack(padx=20, pady=20, fill="both", expand=True)

        tk.Label(frame_editar, text="Editar Produto", font=("Arial", 14, "bold"), bg="white").grid(row=0, column=0, columnspan=2, pady=10)

        labels = ["Nome:", "Categoria:", "Quantidade:", "Unidade:", "Validade (AAAA-MM-DD):", "Estoque Mínimo:"]
        entries = []

        for i, texto in enumerate(labels):
            tk.Label(frame_editar, text=texto, bg="white").grid(row=i + 1, column=0, sticky="e", padx=10, pady=5)
            entrada = tk.Entry(frame_editar, width=30)
            entrada.grid(row=i + 1, column=1, pady=5, padx=10)
            entries.append(entrada)

        nome, categoria, quantidade, unidade, validade, estoque_minimo = entries

        # Preencher os dados atuais
        nome.insert(0, valores[1])
        categoria.insert(0, valores[2])
        quantidade.insert(0, valores[3])
        unidade.insert(0, valores[4])
        validade.insert(0, valores[5])
        estoque_minimo.insert(0, valores[6])

        def salvar_edicao():
            try:
                conn = db.conectar()
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE produtos 
                    SET nome = ?, categoria = ?, quantidade = ?, unidade = ?, validade = ?, estoque_minimo = ?
                    WHERE id = ?
                """, (
                    nome.get(),
                    categoria.get(),
                    int(quantidade.get()),
                    unidade.get(),
                    validade.get(),
                    int(estoque_minimo.get()),
                    valores[0]
                ))
                conn.commit()
                conn.close()

                log_helper.registrar(usuario_logado, "Edição de Produto", f"Produto ID {valores[0]} editado.")
                messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")
                janela_editar.destroy()
                carregar_dados()
                carregar_categorias()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar: {e}")

        # Botões
        tk.Button(frame_editar, text="Salvar", width=15, bg="#4CAF50", fg="white", command=salvar_edicao).grid(row=8, column=0, pady=15)
        tk.Button(frame_editar, text="Cancelar", width=15, bg="#f44336", fg="white", command=janela_editar.destroy).grid(row=8, column=1, pady=15)

    # Botões principais
    btn_frame = tk.Frame(frame, bg="white")
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="🔄 Atualizar", width=15, bg="#2196F3", fg="white", command=carregar_dados).grid(row=0, column=0, padx=10)
    tk.Button(btn_frame, text="✏️ Editar Produto", width=15, bg="#FF9800", fg="white", command=editar).grid(row=0, column=1, padx=10)
    tk.Button(btn_frame, text="🗑️ Excluir Produto", width=15, bg="#f44336", fg="white", command=excluir).grid(row=0, column=2, padx=10)
    tk.Button(btn_frame, text="❌ Fechar", width=15, bg="#607D8B", fg="white", command=janela.destroy).grid(row=0, column=3, padx=10)
