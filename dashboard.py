import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import db
import produtos
import usuarios
import backup
import restore
import categorias

def abrir_dashboard(usuario_logado):
    janela = tk.Tk()
    janela.title("Dashboard - Sistema de Gestão de Estoque - Senhor Açaí")
    janela.state('zoomed')
    janela.configure(bg="#eeeeee")

    # ---------- Funções de Consulta ----------
    def contar_produtos():
        try:
            conn = db.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM produtos")
            total = cursor.fetchone()[0]
            conn.close()
            return total
        except:
            return "Erro"

    def contar_usuarios():
        try:
            conn = db.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM usuarios")
            total = cursor.fetchone()[0]
            conn.close()
            return total
        except:
            return "Erro"

    def produtos_estoque_baixo():
        try:
            conn = db.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM produtos WHERE quantidade <= estoque_minimo")
            total = cursor.fetchone()[0]
            conn.close()
            return total
        except:
            return "Erro"

    def produtos_proximos_validade():
        try:
            conn = db.conectar()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) FROM produtos 
                WHERE validade IS NOT NULL AND date(validade) <= date('now', '+3 days')
            """)
            total = cursor.fetchone()[0]
            conn.close()
            return total
        except:
            return "Erro"

    # ---------- Cabeçalho ----------
    header = tk.Frame(janela, bg="#790071", pady=20)
    header.pack(fill="x")

    logo = tk.PhotoImage(file="media/logo.png")
    logo = logo.subsample(4, 4)
    logo_label = tk.Label(header, image=logo, bg="#790071")
    logo_label.image = logo
    logo_label.pack()

    tk.Label(header, text=f"Bem-vindo, {usuario_logado}", font=("Segoe UI", 12), bg="#790071", fg="white").pack()
    label_hora = tk.Label(header, font=("Segoe UI", 10), bg="#790071", fg="white")
    label_hora.pack()

    def atualizar_hora():
        agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        label_hora.config(text=agora)
        label_hora.after(1000, atualizar_hora)

    atualizar_hora()

    # ---------- Indicadores ----------
    frame_info = tk.Frame(janela, bg="#eeeeee", pady=20)
    frame_info.pack()

    def criar_card(titulo, obter_valor_func, emoji, cor):
        card = tk.Frame(frame_info, bg=cor, width=250, height=100, relief="raised", bd=2)
        card.pack_propagate(0)
        tk.Label(card, text=emoji, font=("Segoe UI Emoji", 24), bg=cor).pack(pady=(5, 0))
        tk.Label(card, text=titulo, font=("Segoe UI", 10, "bold"), bg=cor).pack()
        label_valor = tk.Label(card, text=obter_valor_func(), font=("Segoe UI", 14, "bold"), bg=cor)
        label_valor.pack()
        return card, label_valor, obter_valor_func

    cards_info = [
        ("Produtos", contar_produtos, "📦", "#ffffff"),
        ("Estoque Baixo", produtos_estoque_baixo, "⚠️", "#ffffff"),
        ("Próx. Validade", produtos_proximos_validade, "⏰", "#ffffff"),
        ("Usuários", contar_usuarios, "🧑‍💻", "#ffffff")
    ]

    cards_widgets = []
    for i, (titulo, func, emoji, cor) in enumerate(cards_info):
        card, label_valor, func_valor = criar_card(titulo, func, emoji, cor)
        card.grid(row=0, column=i, padx=15)
        cards_widgets.append((label_valor, func_valor))

    def atualizar_cards():
        for label, func in cards_widgets:
            try:
                novo_valor = func()
                label.config(text=novo_valor)
            except:
                label.config(text="Erro")
        janela.after(3000, atualizar_cards)  # Atualiza a cada 3 segundos

    atualizar_cards()

    # ---------- Botões ----------
    frame_botoes = tk.Frame(janela, bg="#eeeeee")
    frame_botoes.pack(pady=30)

    def abrir_sub_tela(func):
        func(usuario_logado)


    botoes = [
        ("📦 Gestão de Produtos", lambda: abrir_sub_tela(produtos.abrir_listagem_produtos)),
        ("🗂️ Cadastrar Categoria", lambda: categorias.abrir_cadastro_categoria(usuario_logado)),
        ("➕ Cadastrar Produto", lambda: produtos.abrir_cadastro_produto(usuario_logado)),
        ("👥 Gerenciar Usuários", lambda: abrir_sub_tela(usuarios.abrir_listagem_usuarios)),
        ("🪪 Cadastrar Novo Usuário", lambda: usuarios.abrir_cadastro_usuario(usuario_logado)),
        ("💾 Fazer Backup", lambda: backup.fazer_backup()),
        ("♻️ Restaurar Backup", lambda: restore.restaurar_backup()),
        ("🔄 Sair", lambda: janela.destroy()),
    ]

    for i, (texto, comando) in enumerate(botoes):
        btn = tk.Button(
            frame_botoes,
            text=texto,
            font=("Segoe UI", 11, "bold"),
            width=25,
            height=2,
            bg="#790071",
            fg="white",
            activebackground="#5d1e78",
            activeforeground="white",
            relief="raised",
            bd=3,
            command=comando
        )
        btn.grid(row=i//4, column=i%4, padx=15, pady=10)

    janela.mainloop()

# Teste isolado
if __name__ == "__main__":
    abrir_dashboard("Hian")
