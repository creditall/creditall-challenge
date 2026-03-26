# Desafio Creditall

API desenvolvida em FastAPI para gerenciamento de produtos, clientes e vendas, com persistência em banco de dados relacional.

## Tecnologias utilizadas

* FastAPI
* SQLAlchemy
* SQLite (dev)
* Pydantic
* Uvicorn
* Python 3

---

## Estrutura do projeto

```
app/
├── api/routes        # rotas da aplicação (products, clients, sales)
├── core              # configuração e banco de dados
├── models            # models do banco (SQLAlchemy)
├── schemas           # validação de dados (Pydantic)
├── static/uploads    # armazenamento de imagens
├── main.py           # inicialização da aplicação
```

---

## Funcionalidades

### Produtos

* Criar produto
* Listar produtos
* Atualizar produto
* Deletar produto
* Upload de imagem para produto

### Clientes

* Criar cliente
* Listar clientes
* Atualizar cliente
* Deletar cliente
* Validação de email
* Bloqueio de duplicidade (email e CPF)

### Vendas

* Criar venda
* Listar vendas
* Atualizar venda
* Deletar venda
* Validação de relacionamento (produto e cliente)

---

## Regras de negócio implementadas

* Produto deve existir para criar venda
* Cliente (se informado) deve existir
* Email validado com EmailStr
* CPF e Email únicos
* Upload de imagem apenas para arquivos válidos

---

## Como executar o projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/Matheus-sys/desafio-crud-fastapi.git
cd desafio-crud-fastapi
```

---

### 2. Criar ambiente virtual

```bash
python -m venv venv
```

Ativar:

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

---

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

---

### 4. Rodar a aplicação

```bash
python -m uvicorn app.main:app --reload
```

---

### 5. Acessar documentação

Swagger:

```
http://127.0.0.1:8000/docs
```

---

## Upload de imagem

Endpoint:

```
POST /products/{product_id}/upload-image
```

A imagem será salva em:

```
/static/uploads/
```

E poderá ser acessada via navegador:

```
http://127.0.0.1:8000/static/uploads/{nome_do_arquivo}
```

---

## Observações

* O banco utilizado é SQLite para ambiente de desenvolvimento
* As imagens enviadas não são versionadas no repositório (.gitignore)

---

## Autor

Matheus Pereira
>>>>>>> desafio-crud
