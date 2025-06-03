
# 📦 Sistema de Gerenciamento de Estoque

Este é um sistema simples de gerenciamento de estoque desenvolvido em Python, utilizando SQLite como banco de dados. O sistema permite o gerenciamento de usuários, produtos, categorias e oferece um painel de dashboard com estatísticas e controle de acesso por autenticação.

## 🚀 Funcionalidades

- 🔐 **Autenticação de Usuários**
  - Login e logout.
  - Controle de permissões.

- 👥 **Gerenciamento de Usuários**
  - Cadastro, listagem, atualização e remoção de usuários.

- 🗂️ **Gerenciamento de Categorias**
  - Cadastro, edição, listagem e exclusão de categorias de produtos.

- 📦 **Gerenciamento de Produtos**
  - Cadastro de produtos.
  - Atualização e exclusão de produtos.
  - Listagem por categoria.

- 📊 **Dashboard**
  - Estatísticas de produtos e usuários.
  - Relatórios resumidos do estoque.

- 🪵 **Logs do Sistema**
  - Armazena logs de ações dos usuários e do sistema na pasta `logs/`.

- 🧪 **Seed de Dados**
  - Script para popular o banco de dados com dados de teste (`seed_test_data.py`).

## 🗂️ Estrutura de Arquivos

```
.
├── auth.py               # Lógica de autenticação
├── categorias.py         # CRUD de categorias
├── dashboard.py          # Geração de relatórios e estatísticas
├── db.py                 # Conexão e gestão do banco de dados SQLite
├── estoque.db            # Banco de dados SQLite
├── log_helper.py         # Funções auxiliares para logs
├── logs/                 # Pasta com arquivos de logs
├── logs.py               # Gerenciamento de logs
├── main.py               # Arquivo principal para executar o sistema
├── produtos.py           # CRUD de produtos
├── usuarios.py           # CRUD de usuários
├── seed_test_data.py     # Popula o banco com dados de teste
└── README.md             # Documentação do projeto
```

## 🏗️ Tecnologias Utilizadas

- 🐍 Python 3.x
- 🗃️ SQLite3
- 📄 Log com arquivos locais (`logs/`)

## ⚙️ Como Executar o Projeto

1. Clone este repositório:

```bash
git clone https://github.com/seu-usuario/seu-repo.git
cd seu-repo
```

2. Instale as dependências necessárias (se houver).

> 🔸 Este projeto não possui bibliotecas externas além da biblioteca padrão do Python.

3. Execute o arquivo principal:

```bash
python main.py
```

4. (Opcional) Para gerar dados de teste:

```bash
python seed_test_data.py
```

## 📝 Observações

- O banco de dados é armazenado localmente no arquivo `estoque.db`.
- Todos os logs ficam salvos na pasta `logs/`.
- É um sistema de linha de comando simples, sem interface gráfica.

## 💡 Melhorias Futuras

- Interface Web ou Desktop.
- Sistema de backup do banco de dados.
- Relatórios mais detalhados em PDF ou CSV.
- Autenticação com hash de senha.

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se livre para abrir issues ou enviar pull requests.

## 📜 Licença

Este projeto está sob a licença [MIT](LICENSE).
