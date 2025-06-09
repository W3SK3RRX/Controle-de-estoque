import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import db
import produtos
import usuarios
import restore
import categorias  # Importe seu módulo de categorias aqui (onde está o abrir_cadastro_categoria)

def abrir_dashboard(usuario_logado):
    janela = tk.Tk()
    janela.title("Dashboard - Sistema de Gestão de Estoque - Senhor Açaí")
    janela.state('zoomed')
    janela.configure(bg="#eeeeee")

    # ---------- Indicadores ----------
    def contar_produtos():
        conn = db.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM produtos")
        total = cursor.fetchone()[0]
        conn.close()
        return total

    def contar_usuarios():
        conn = db.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        total = cursor.fetchone()[0]
        conn.close()
        return total

    def produtos_estoque_baixo():
        conn = db.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM produtos WHERE quantidade <= estoque_minimo")
        total = cursor.fetchone()[0]
        conn.close()
        return total

    def produtos_proximos_validade():
        conn = db.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM produtos 
            WHERE validade IS NOT NULL AND date(validade) <= date('now', '+3 days')
        """)
        total = cursor.fetchone()[0]
        conn.close()
        return total

    # ---------- Cabeçalho ----------
    header = tk.Frame(janela, bg="#790071", pady=20)
    header.pack(fill="x")

    # Carregar e redimensionar a logo
    logo = tk.PhotoImage(file="media/logo.png")
    logo = logo.subsample(4, 4)  # Reduz a imagem para 1/4 do tamanho original
    logo_label = tk.Label(header, image=logo, bg="#790071")
    logo_label.image = logo  # Manter referência para evitar garbage collection
    logo_label.pack()
    
    tk.Label(header, text=f"Bem-vindo, {usuario_logado}", font=("Segoe UI", 12), bg="#790071", fg="white").pack()
    # Label para data e hora
    label_hora = tk.Label(header, font=("Segoe UI", 10), bg="#790071", fg="white")
    label_hora.pack()

    # Função para atualizar data e hora em tempo real
    def atualizar_hora():
        agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        label_hora.config(text=agora)
        label_hora.after(1000, atualizar_hora)  # atualiza a cada 1000 ms (1 segundo)

    atualizar_hora()

    # ---------- Indicadores ----------
    frame_info = tk.Frame(janela, bg="#eeeeee", pady=20)
    frame_info.pack()

    def criar_card(titulo, valor, emoji, cor):
        card = tk.Frame(frame_info, bg=cor, width=250, height=100, relief="raised", bd=2)
        card.pack_propagate(0)
        tk.Label(card, text=emoji, font=("Segoe UI Emoji", 24), bg=cor).pack(pady=(5, 0))
        tk.Label(card, text=titulo, font=("Segoe UI", 10, "bold"), bg=cor).pack()
        tk.Label(card, text=valor, font=("Segoe UI", 14, "bold"), bg=cor).pack()
        return card

    cards = [
        criar_card("Produtos", contar_produtos(), "📦", "#ffffff"),
        criar_card("Estoque Baixo", produtos_estoque_baixo(), "⚠️", "#ffffff"),
        criar_card("Próx. Validade", produtos_proximos_validade(), "⏰", "#ffffff"),
        criar_card("Usuários", contar_usuarios(), "🧑‍💻", "#ffffff")
    ]

    for i, card in enumerate(cards):
        card.grid(row=0, column=i, padx=15)

    # ---------- Botões ----------
    frame_botoes = tk.Frame(janela, bg="#eeeeee")
    frame_botoes.pack(pady=30)

    def abrir_sub_tela(func):
        janela.withdraw()
        func(usuario_logado)
        janela.deiconify()

    botoes = [
        ("📦 Gestão de Produtos", lambda: abrir_sub_tela(produtos.abrir_listagem_produtos)),
        ("🗂️ Cadastrar Categoria", lambda: categorias.abrir_cadastro_categoria(usuario_logado)),
        ("➕ Cadastrar Produto", lambda: produtos.abrir_cadastro_produto(usuario_logado)),
        ("👥 Gerenciar Usuários", lambda: abrir_sub_tela(usuarios.abrir_listagem_usuarios)),
        ("🪪 Cadastrar Novo Usuário", lambda: usuarios.abrir_cadastro_usuario(usuario_logado)),
        ("♻️ Restaurar Backup", restore.restaurar_backup_mais_recente),
        ("🔄 Sair", lambda: janela.destroy())
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
