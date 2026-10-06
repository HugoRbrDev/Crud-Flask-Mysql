# CRUD Flask + MySQL

Este projeto é uma aplicação web simples em Python usando Flask para realizar operações de CRUD (Create, Read, Update e Delete) em uma tabela de pessoas no MySQL.

A ideia central é permitir cadastrar registros com nome e idade, listar todos os cadastros, editar um item existente e excluir registros do banco de dados.

## Visão geral

O projeto usa:

- Flask para criar a aplicação web
- Jinja2 para renderizar os templates HTML
- MySQL Connector para comunicação com o banco de dados MySQL
- Bootstrap-like CSS simples em arquivos locais

A aplicação funciona como um pequeno sistema de gestão de pessoas, com interface web para interagir com o banco.

## Estrutura do projeto

```text
crud-flask-mysql/
├── app.py                  # Aplicação Flask e rotas do CRUD
├── requirements.txt        # Dependências do projeto
├── static/
│   └── estilo.css         # Estilos da interface
├── templates/
│   ├── base.html          # Layout base com mensagens flash
│   ├── index.html         # Página de listagem
│   └── form.html          # Formulário de cadastro/edição
└── README.md              # Documentação do projeto
```

## Como o projeto funciona

### 1. Inicialização da aplicação

No arquivo `app.py`, a aplicação Flask é criada com:

```python
app = Flask(__name__)
app.secret_key = "troque-por-uma-chave-qualquer"
```

A `secret_key` é usada para armazenar mensagens de sucesso e erro com `flash()`, que aparecem na interface.

### 2. Configuração do banco de dados

A conexão com o MySQL é configurada em um dicionário chamado `DB`:

```python
DB = dict(
    host="127.0.0.1",
    user="root",
    password="",
    database="crud_flask",
)
```

Esse bloco define:

- host local do MySQL
- usuário do banco
- senha do usuário
- nome do banco a ser usado

> Em ambientes locais do macOS, o MySQL costuma ser usado com usuário `root` e senha vazia, mas isso pode variar conforme a instalação.

### 3. Função de acesso ao banco

A função `query()` centraliza toda a interação com o banco:

```python
def query(sql, params=None, fetch=False):
    conn = mysql.connector.connect(**DB)
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql, params or ())
    if fetch:
        resultado = cursor.fetchall()
    else:
        conn.commit()
        resultado = None
    cursor.close()
    conn.close()
    return resultado
```

Essa função:

- abre a conexão
- executa o SQL
- retorna linhas quando `fetch=True`
- faz `commit()` quando for operação de escrita
- fecha conexão para evitar vazamento de recursos

### 4. Rotas da aplicação

O projeto tem 4 operações principais:

#### Listar registros

```python
@app.get("/")
def listar():
    pessoas = query("SELECT id, nome, idade FROM pessoas ORDER BY id", fetch=True)
    return render_template("index.html", pessoas=pessoas)
```

- acessa a URL `/`
- busca todos os registros da tabela `pessoas`
- envia os dados para `index.html`

#### Criar registro

```python
@app.route("/novo", methods=["GET", "POST"])
def novo():
    if request.method == "POST":
        nome = request.form["nome"].strip()
        idade = request.form["idade"].strip()

        if not nome or not idade:
            flash("Preencha nome e idade.", "erro")
            return render_template("form.html", pessoa=None, action=url_for("novo"))

        query("INSERT INTO pessoas (nome, idade) VALUES (%s, %s)", (nome, idade))
        flash("Pessoa cadastrada com sucesso!", "ok")
        return redirect(url_for("listar"))
```

- ao abrir `/novo`, exibe o formulário
- ao enviar o formulário, valida nome e idade
- insere os dados no banco
- redireciona para a página inicial

#### Editar registro

```python
@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    if request.method == "POST":
        nome = request.form["nome"].strip()
        idade = request.form["idade"].strip()
        query("UPDATE pessoas SET nome=%s, idade=%s WHERE id=%s", (nome, idade, id))
        flash("Cadastro atualizado!", "ok")
        return redirect(url_for("listar"))
```

- busca o registro pelo `id`
- preenche o formulário com os dados atuais
- salva as alterações no banco

#### Excluir registro

```python
@app.post("/excluir/<int:id>")
def excluir(id):
    query("DELETE FROM pessoas WHERE id=%s", (id,))
    flash("Registro excluído.", "ok")
    return redirect(url_for("listar"))
```

- remove o registro do banco
- retorna para a listagem

## Templates e renderização

Os arquivos em `templates/` controlam a interface:

### `base.html`

- define o layout principal
- carrega o CSS em `static/estilo.css`
- exibe mensagens de `flash()`

### `index.html`

- mostra a tabela com todos os cadastros
- inclui botões para editar e excluir cada pessoa
- possui link para criar um novo cadastro

### `form.html`

- formulário único para criar ou editar registros
- recebe `nome` e `idade`
- usa `action` para indicar a rota correta

## Banco de dados necessário

Antes de rodar a aplicação, o MySQL precisa existir e o banco `crud_flask` precisa ser criado.

Exemplo de criação da tabela:

```sql
CREATE DATABASE crud_flask;
USE crud_flask;

CREATE TABLE pessoas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    idade INT NOT NULL
);
```

Se a tabela ainda não existir, a aplicação não conseguirá consultar nem salvar registros.

## Como rodar o projeto

### 1. Criar ambiente virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Instalar dependências

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Iniciar o MySQL

No macOS com Homebrew:

```bash
brew install mysql
brew services start mysql
```

Verificar se o serviço subiu:

```bash
brew services list
mysql -u root -e "SELECT VERSION();"
```

### 4. Executar a aplicação

```bash
python -m flask --app app run --debug --port 5001
```

A aplicação estará disponível em:

```text
http://127.0.0.1:5001
```

## Observações importantes

- O projeto usa conexão direta com MySQL sem ORM.
- A chave `app.secret_key` deve ser trocada em produção por uma sequência segura.
- O banco está configurado para `root` sem senha em ambiente local, mas em um projeto real é recomendável criar um usuário específico e senha forte.
- A pasta `static` contém o CSS usado para deixar a aplicação visualmente simples e funcional.

## Fluxo completo de uso

1. Usuário acessa a página inicial
2. A aplicação consulta todos os registros em `pessoas`
3. O usuário clica em "Novo cadastro"
4. O formulário envia dados para a rota `/novo`
5. O banco insere os dados
6. A aplicação redireciona para a listagem
7. O usuário pode editar ou excluir qualquer registro a qualquer momento

## Resumo

## Passo a passo:

## Mac:

instalar o mysql:
brew install mysql
brew services start mysql

conferir:
brew services list # mysql deve aparecer como "started"
mysql -u root -e "SELECT VERSION();"

Rodar o Mysql para rodar shell:
mysql -u root

Criar ambiente virtual:
python3 -m venv .venv
source .venv/bin/activate

Instalar requirements e atualizar o pip:
python -m pip install --upgrade pip
pip install -r requirements.txt # vai criar o arquivo a seguir primeiro

rodando:
python -m flask --app app run --debug --port 5001

Dica para um projeto SQLite + Mysql
Usar uuid para que os aparelhos offline não gerem o mesmo id em novas colunas.
import uuid
novo_id = str(uuid.uuid4()) # Ex: 'c9bf9e57-1685-4c89-bafb-ff5af830be8a'
