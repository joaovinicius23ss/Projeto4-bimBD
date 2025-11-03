import tkinter as tk
from tkinter import messagebox
from cryptography.fernet import Fernet
from pymongo import MongoClient
from PIL import Image, ImageTk


def adicionar():
    nome = criancausu.get().strip()
    doce = doceusu.get().strip()
    qtd = qtdusu.get().strip()

    if not nome or not doce or not qtd:
        status.config(text='Todos os campos devem ser preenchidos!', fg='#ff0606')
        return
    if not qtd.isdigit():
        status.config(text='A quantidade deve ser um número!', fg='#ff0606')
        return
    docefernet = fernet.encrypt(doce.encode())
    colecao.insert_one({
        'crianca': nome,
        'nome_doce': docefernet,
        'quantidade': qtd
    })

    status.config(text=f'Doce do(a) {nome} foi salvo.', fg='#47ff06')

    criancausu.delete(0, 'end')
    doceusu.delete(0, 'end')
    qtdusu.delete(0, 'end')


def listar():
    texto.delete('1.0', 'end')
    memoria.clear()
    for item in colecao.find():
        nome = item['crianca']
        docefernet = item['nome_doce']
        qtd = item['quantidade']
        memoria.append({
            'crianca': nome,
            'nome_doce': docefernet,
            'quantidade': qtd
        })
    if not memoria:
        texto.insert('end', 'Nenhum doce cadastrado...')
        status.config(text='A lista está vazia!', fg='red')
        return

    for d in memoria:
        nome_crianca = d['crianca']
        qtd = d['quantidade']
        doce = fernet.decrypt(d['nome_doce']).decode()

        linha = f"Criança: {nome_crianca} / Doce: {doce} / Qtd: {qtd}\n"
        texto.insert('end', linha)

    status.config(text='Lista de doces carregada.', fg='#47ff06')


cliente = MongoClient(
    "mongodb+srv://root:123@cluster0.8avsoth.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
banco = cliente["projeto"]
colecao = banco["projeto"]
memoria = []

try:
    with open('key.txt', 'r') as arquivo:
        chave = arquivo.read()
        fernet = Fernet(chave)
except Exception as erro:
    messagebox.showwarning("Erro", f"Não foi possível acessar a chave Fernet.\n ->{erro}")

    colecao.drop()
    banco = cliente["halloween"]
    colecao = banco["cofre"]

    chave = Fernet.generate_key()
    fernet = Fernet(chave)
    with open('key.txt', 'wb') as arquivo:
        arquivo.write(chave)


janela = tk.Tk()
janela.title('Cofre de Doces Criptografado')
janela.geometry('700x500')

img = Image.open("fundo.jpg")
img = ImageTk.PhotoImage(img)
bg = tk.Label(janela, image=img)
bg.place(x=0, y=0, relwidth=1, relheight=1)

tk.Label(janela, text='Nome da Criança:', bg='#58023f', fg='#f33cbd', font=('Arial', 10, 'bold')).pack(anchor='w', padx=10)
criancausu = tk.Entry(janela, width=50, bg='#58023f', fg='#f33cbd')
criancausu.pack(anchor='w', padx=10)

tk.Label(janela, text='Nome do Doce:', bg='#58023f', fg='#f33cbd', font=('Arial', 10, 'bold')).pack(anchor='w', padx=10)
doceusu = tk.Entry(janela, width=40, bg='#58023f', fg='#f33cbd')
doceusu.pack(anchor='w', padx=10)

tk.Label(janela, text='Quantidade:', bg='#58023f', fg='#f33cbd', font=('Arial', 10, 'bold')).pack(anchor='w', padx=10)
qtdusu = tk.Entry(janela, width=40, bg='#58023f', fg='#f33cbd')
qtdusu.pack(anchor='w', padx=10)

texto = tk.Text(janela, height=12, width=65, bg='#58023f', fg='#f33cbd')
texto.pack(pady=30)

status = tk.Label(janela, text='', fg='green', bg='#58023f', font=('Arial', 10, 'bold'))
status.pack()

tk.Button(janela, text='Adicionar Doce', bg='white', fg='grey', width=25, command=adicionar).pack(pady=4)
tk.Button(janela, text='Listar Doces', bg='white', fg='grey', width=25, command=listar).pack(pady=4)

janela.mainloop()
