from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)


conn = sqlite3.connect('loja_eletrodomesticos.db', check_same_thread=False)
cur = conn.cursor()


cur.execute('''
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL
    )
''')


cur.execute('''
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_produto TEXT NOT NULL,
        preco REAL NOT NULL
    )
''')

conn.commit()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro_cliente', methods=['GET', 'POST'])
def cadastro_cliente():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        cur.execute('INSERT INTO clientes (nome, email) VALUES (?, ?)', (nome, email))
        conn.commit()
        return redirect(url_for('index'))
    return render_template('cadastro_cliente.html')

@app.route('/cadastro_produto', methods=['GET', 'POST'])
def cadastro_produto():
    if request.method == 'POST':
        nome_produto = request.form['nome_produto']
        preco = request.form['preco']
        cur.execute('INSERT INTO produtos (nome_produto, preco) VALUES (?, ?)', (nome_produto, preco))
        conn.commit()
        return redirect(url_for('index'))
    return render_template('cadastro_produto.html')

@app.route('/clientes')
def ver_clientes():
    cur.execute('SELECT * FROM clientes')
    clientes = cur.fetchall()
    return render_template('clientes.html', clientes=clientes)

@app.route('/produtos')
def ver_produtos():
    cur.execute('SELECT * FROM produtos')
    produtos = cur.fetchall()
    return render_template('produtos.html', produtos=produtos)

if __name__ == '__main__':
    app.run(debug=True)
