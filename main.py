# Importações do Tkinter
from tkinter import *
from tkinter import Tk, ttk
from tkinter import messagebox, Label
from tkinter import filedialog as fd
from tkinter import END

# Importações de bibliotecas adicionais
from PIL import Image, ImageTk
from tkcalendar import DateEntry
from datetime import date

# Importações de módulos personalizados
from backend.crud import *
from frontend.color import *

# Criando janela ==============================
janela = Tk()
janela.title("Cadastro de Vendas")
janela.geometry("900x600")
janela.configure(background=indigo)
janela.resizable(width=FALSE, height=FALSE)
style = ttk.Style(janela)
style.theme_use("clam")

# Criando frames ==============================
frame_1 = Frame(janela, width=900, height=50, bg=royal_purple, relief=FLAT)
frame_1.grid(row=0, column=0)

frame_2 = Frame(janela, width=900, height=303, bg=medium_purple, pady=20, relief=FLAT)
frame_2.grid(row=1, column=0, pady=1, padx=0)

frame_3 = Frame(janela, width=900, height=300, bg=indigo, relief=FLAT)
frame_3.grid(row=2, column=0, pady=0, padx=1, sticky=NSEW)

# Criando funçoes e estabelecendo global ==============================
global tree

# Função para inserir dados ==============================
def inserir():
    global imagem, imagem_string, l_imagem

    nome = b_nome.get()
    tipo = b_tipo.get()
    marca = b_marca.get()
    data = b_data.get_date()
    valor = b_valor.get()
    numero = b_serie.get()
    imagem = imagem_string

    # Verifica se a imagem foi carregada
    if not imagem_string:  # Se imagem_string estiver vazia
        messagebox.showerror("Erro", "Por favor, carregue uma imagem.")
        return

    # Prepara os dados para inserção
    lista_inserir = [nome, tipo, marca, data, valor, numero, imagem]

    # Verifica se todos os campos foram preenchidos
    for i in lista_inserir:
        if i == '':
            messagebox.showerror('Erro', 'Preencha todos os campos')
            return

    # Tratamento para garantir que o valor seja numérico
    try:
        valor = float(b_valor.get())  # Tenta converter o valor para float
    except ValueError:
        messagebox.showerror('Erro', 'O campo "Valor" deve conter apenas números.')
        return

    # Agora que temos o valor validado, inserimos os dados
    lista_inserir[4] = valor  # Atualiza o valor convertido na lista de dados

    inserir_form(lista_inserir)
    messagebox.showinfo('Sucesso', 'Os dados foram inseridos com sucesso')

    # Limpa os campos após inserir
    b_nome.delete(0, END)
    b_tipo.delete(0, END)
    b_marca.delete(0, END)
    b_data.set_date(date.today())
    b_valor.delete(0, END)
    b_serie.delete(0, END)

    mostrar()

# Função atualizar ==============================
def atualizar():
    global imagem, imagem_string, l_imagem
    try:
        # Obtendo os dados do item selecionado na árvore
        treev_dados = tree.focus()
        treev_dicionario = tree.item(treev_dados)
        treev_lista = treev_dicionario['values']

        # Verificando se há um item selecionado
        if not treev_lista:
            messagebox.showerror("Erro", "Nenhum item selecionado")
            return

        # Limpa os campos antes de preencher
        b_nome.delete(0, END)
        b_tipo.delete(0, END)
        b_marca.delete(0, END)
        b_data.set_date(date.today())
        b_valor.delete(0, END)
        b_serie.delete(0, END)

        # Preenchendo os campos com os dados do item selecionado
        id = int(treev_lista[0])
        b_nome.insert(0, treev_lista[1])
        b_tipo.insert(0, treev_lista[2])
        b_marca.insert(0, treev_lista[3])
        b_data.set_date(date.today())
        b_valor.insert(0, treev_lista[5])
        b_serie.insert(0, treev_lista[6])
        imagem_string = treev_lista[7]

        # Função interna para atualizar os dados
        def update():
            global imagem, imagem_string, l_imagem

            nome = b_nome.get()
            tipo = b_tipo.get()
            marca = b_marca.get()
            data = b_data.get_date()
            valor = b_valor.get()
            numero = b_serie.get()
            imagem = imagem_string

            if imagem =='':
                imagem = b_serie(0, treev_lista[7])

            lista_atualizar = [nome, tipo, marca, data, valor, numero, imagem, id]

            for i in lista_atualizar:
                if i == '':
                    messagebox.showerror("Erro", "Preencha todos os campos")
                    return
            atualizar_(lista_atualizar)
            messagebox.showinfo("Sucesso", "Os dados foram atualizados com sucesso")

            b_nome.delete(0, END)
            b_tipo.delete(0, END)
            b_marca.delete(0, END)
            b_data.set_date(date.today())
            b_valor.delete(0, END)
            b_serie.delete(0, END)

            b_botao_confirmar.destroy()

            mostrar()

        img_confirmar = Image.open('frontend/Icones//icone_6.png')
        img_confirmar = img_confirmar.resize((20, 20))
        img_confirmar = ImageTk.PhotoImage(img_confirmar)
        b_botao_confirmar = Button(frame_2, command=update, image=img_confirmar, width=95, text="  CONFIRMAR".upper(), compound=LEFT, anchor=NW, overrelief=RIDGE, font=("Ivy 8"), bg=white, fg=black)
        b_botao_confirmar.place(x=330, y=115)

        b_botao_confirmar.image = img_confirmar

    except IndexError:
        messagebox.showerror("Erro", "Selecione um dos dados na tabela")

# Função Deletar ==============================
def Deletar():
    """Função principal para solicitar a confirmação antes de deletar o item."""
    global b_botao_confirmar

    # Função interna para confirmar a exclusão
    def confirmar_delecao():
        try:
            # Obtendo os dados do item selecionado na árvore
            treev_dados = tree.focus()
            treev_dicionario = tree.item(treev_dados)
            treev_lista = treev_dicionario.get('values', [])

            # Verificando se há um item selecionado
            if not treev_lista:
                messagebox.showerror("Erro", "Selecione um dos dados na tabela")
                return

            valor = treev_lista[0]  # Obtendo o ID do item selecionado

            # Deletando o item do banco de dados
            deletar_form(valor)
            messagebox.showinfo("Sucesso", "Os dados foram deletados com sucesso")

            # Atualizando a interface para refletir a exclusão
            mostrar()

            # Remover o botão de confirmação após a exclusão
            b_botao_confirmar.destroy()

        except IndexError:
            messagebox.showerror("Erro", "Selecione um dos dados na tabela")

    # Obtendo os dados do item selecionado na árvore
    treev_dados = tree.focus()
    treev_dicionario = tree.item(treev_dados)
    treev_lista = treev_dicionario.get('values', [])

    # Verificando se há um item selecionado
    if not treev_lista:
        messagebox.showerror("Erro", "Selecione um dos dados na tabela")
        return

    # Criando o botão de confirmação de exclusão
    img_deletar = Image.open('frontend/Icones//icone_6.png')
    img_deletar = img_deletar.resize((20, 20))
    img_deletar = ImageTk.PhotoImage(img_deletar)

    b_botao_confirmar = Button(
        frame_2, command=confirmar_delecao, image=img_deletar, width=95,
        text="  CONFIRMAR".upper(), compound=LEFT, anchor=NW,
        overrelief=RIDGE, font=("Ivy 8"), bg="white", fg="black"
    )
    b_botao_confirmar.place(x=330, y=115)

    # Prevenindo a imagem do botão de ser excluída pelo garbage collector
    b_botao_confirmar.image = img_deletar

# Função para escolher  ==============================
global imagem, imagem_string, l_imagem
def escolher_imagem():
    global imagem, imagem_string, l_imagem

    # Abrir diálogo para selecionar a imagem
    imagem_caminho = fd.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])

    # Verificar se uma imagem foi selecionada
    if not imagem_caminho:
        messagebox.showerror("Erro", "Nenhuma imagem selecionada")
        return

    imagem_string = imagem_caminho

    try:
        # Carregar e redimensionar a imagem
        imagem = Image.open(imagem_caminho)
        imagem = imagem.resize((170, 170))
        imagem = ImageTk.PhotoImage(imagem)
        # Exibir a nova imagem no frame
        l_imagem = Label(frame_2, image=imagem, bg=blue_violet, fg=white)
        l_imagem.place(x=700, y=10)
        print("Imagem carregada com sucesso")

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao carregar a imagem: {e}")

# Função para ver imagem ==============================
def ver_imagem():
    global imagem, l_imagem

    treev_dados = tree.focus()
    treev_dicionario = tree.item(treev_dados)
    treev_lista = treev_dicionario.get('values', [])

    if not treev_lista:
        messagebox.showerror("Erro", "Nenhum item selecionado")
        return

    valor = [int(treev_lista[0])]
    iten = ver_item(valor)

    # Verifica se iten possui elementos e o índice correto para a imagem
    if not iten or len(iten[0]) < 8:
        messagebox.showerror("Erro", "Detalhes insuficientes para exibir a imagem do item.")
        return

    try:
        caminho_imagem = iten[0][7]  # Ajustado para o índice correto
        imagem = Image.open(caminho_imagem)
        imagem = imagem.resize((170, 170))
        imagem = ImageTk.PhotoImage(imagem)
        l_imagem = Label(frame_2, image=imagem, bg="blue violet", fg="white")
        l_imagem.place(x=700, y=10)

    except FileNotFoundError:
        messagebox.showerror("Erro", f"A imagem '{caminho_imagem}' não foi encontrada.")

# Adicionando imagem e título ==============================
app = Image.open('frontend/Icones//icone_1.png')
app = app.resize((45, 45))
app = ImageTk.PhotoImage(app)
app_logo = Label(frame_1, image=app, text="Cadastramento de Vendas", width=900, compound=LEFT, relief=RAISED, anchor=NW,
                 font=("Verdana 20 bold"), bg=blue_violet, fg=white)
app_logo.place(x=0, y=0)

# Criando informações do frame_2 ==============================
# Nome
a_nome = Label(frame_2, text="Nome", height=1, anchor=NW, font=("Ivy 10 bold"), bg=medium_purple, fg=black)
a_nome.place(x=10, y=10)
b_nome = Entry(frame_2, width=30, justify='left', relief=SOLID)
b_nome.place(x=130, y=11)

# Tipo do Produto
a_tipo = Label(frame_2, text="Tipo de Produto", height=1, anchor=NW, font=("Ivy 10 bold"), bg=medium_purple, fg=black)
a_tipo.place(x=10, y=40)
b_tipo = Entry(frame_2, width=30, justify='left', relief=SOLID)
b_tipo.place(x=130, y=41)

# Marca/Modelo
a_marca = Label(frame_2, text="Marca/Modelo", height=1, anchor=NW, font=("Ivy 10 bold"), bg=medium_purple, fg=black)
a_marca.place(x=10, y=70)
b_marca = Entry(frame_2, width=30, justify='left', relief=SOLID)
b_marca.place(x=130, y=71)

# Data da Venda
a_data = Label(frame_2, text="Data da Venda", height=1, anchor=NW, font=("Ivy 10 bold"), bg=medium_purple, fg=black)
a_data.place(x=10, y=100)
b_data = DateEntry(frame_2, width=12, background='darkblue', borderwidth=2, year=2024)
b_data.place(x=130, y=101)

# Valor
a_valor = Label(frame_2, text="Valor", height=1, anchor=NW, font=("Ivy 10 bold"), bg=medium_purple, fg=black)
a_valor.place(x=10, y=130)
b_valor = Entry(frame_2, width=30, justify='left', relief=SOLID)
b_valor.place(x=130, y=131)

# Número de Série
a_serie = Label(frame_2, text="N /Série", height=1, anchor=NW, font=("Ivy 10 bold"), bg=medium_purple, fg=black)
a_serie.place(x=10, y=160)
b_serie = Entry(frame_2, width=30, justify='left', relief=SOLID)
b_serie.place(x=130, y=161)

# Botão carregar imagem
a_botao_imagem = Label(frame_2, text="Imagem do Item", height=1, anchor=NW, font=("Ivy 10 bold"), bg=medium_purple, fg=black)
a_botao_imagem.place(x=10, y=190)
b_botao_imagem = Button(frame_2,command=escolher_imagem, width=29, text="Carregar".upper(), compound=CENTER, anchor=CENTER, overrelief=RIDGE, font=("Ivy 8"), bg=white, fg=black)
b_botao_imagem.place(x=130, y=189)

# Botões de ação
img_adicionar = Image.open('frontend/Icones//icone_2.png')
img_adicionar = img_adicionar.resize((20, 20))
img_adicionar = ImageTk.PhotoImage(img_adicionar)
b_botao_adicionar = Button(frame_2, command=inserir, image=img_adicionar, width=95, text="  ADICIONAR".upper(), compound=LEFT, anchor=NW, overrelief=RIDGE, font=("Ivy 8"), bg=white, fg=black,)
b_botao_adicionar.place(x=330, y=10)

img_atualizar = Image.open('frontend/Icones//icone_3.png')
img_atualizar = img_atualizar.resize((20, 20))
img_atualizar = ImageTk.PhotoImage(img_atualizar)
b_botao_atualizar = Button(frame_2, command=atualizar, image=img_atualizar, width=95, text="  ATUALIZAR".upper(), compound=LEFT, anchor=NW, overrelief=RIDGE, font=("Ivy 8"), bg=white, fg=black)
b_botao_atualizar.place(x=330, y=45)

img_deletar = Image.open('frontend/Icones//icone_4.png')
img_deletar = img_deletar.resize((20, 20))
img_deletar = ImageTk.PhotoImage(img_deletar)
b_botao_deletar = Button(frame_2,command=Deletar, image=img_deletar, width=95, text="  DELETAR".upper(), compound=LEFT, anchor=NW, overrelief=RIDGE, font=("Ivy 8"), bg=white, fg=black)
b_botao_deletar.place(x=330, y=80)

img_ver = Image.open('frontend/Icones//icone_5.png')
img_ver = img_ver.resize((20, 20))
img_ver = ImageTk.PhotoImage(img_ver)
b_botao_ver = Button(frame_2, command=ver_imagem, image=img_ver, width=95, text="  VER ITEM".upper(), compound=LEFT, anchor=NW, overrelief=RIDGE, font=("Ivy 8"), bg=white, fg=black)
b_botao_ver.place(x=330, y=188)

# Variáveis de total e quantidade
l_total = Label(frame_2, text="", width=14, height=2, anchor=CENTER, font=("Ivy 17 bold"), bg=royal_purple, fg=white,relief="groove", bd=1)
l_total.place(x=450, y=17)
l_total_ = Label(frame_2, text="  Valor Total das Vendas /Mês  ", height=1, anchor=NW, font=("Ivy 10 bold"), bg=royal_purple, fg=white, relief="groove", bd=1)
l_total_.place(x=450, y=12)

l_quantidade = Label(frame_2, text="", width=14, height=3, anchor=CENTER, font=("Ivy 17 bold"), bg=royal_purple, fg=white, relief="groove", bd=1)
l_quantidade.place(x=450, y=90)
l_quantidade_ = Label(frame_2, text="   Total de Itens Vendido /Mês  ", height=1, anchor=NW, font=("Ivy 10 bold"), bg=royal_purple, fg=white, relief="groove", bd=1)
l_quantidade_.place(x=450, y=90)

#tabela ==============================
def mostrar():
    global tree
    tabela_head = ['#iD', 'Nome', 'Tipo de Produto', 'Marca/Modelo', 'Data da Venda', 'Valor', 'N /Série']

    lista_itens = ver_form()

    global tree

    # Criação do Treeview para exibir a tabela
    tree = ttk.Treeview(frame_3, selectmode="extended", columns=tabela_head, show="headings")

    # Scrollbars vertical e horizontal
    vsb = ttk.Scrollbar(frame_3, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(frame_3, orient="horizontal", command=tree.xview)

    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    tree.grid(row=0, column=0, sticky='nsew')
    vsb.grid(row=0, column=1, sticky='ns')
    hsb.grid(row=1, column=0, sticky='ew')
    frame_3.grid_rowconfigure(0, weight=1)
    frame_3.grid_columnconfigure(0, weight=1)


    # Configuração das colunas e cabeçalhos
    hd = ["center","center","center","center","center","center","center"]
    h = [40, 150, 100, 100, 130, 100, 100, 100]
    n=0

    for col in tabela_head:
        tree.heading(col, text=col.title(), anchor=CENTER)
        tree.column(col, width=h[n], anchor=hd[n])
        n+=1

    # inserir os itens dentro da tabela
    for item in lista_itens:
        tree.insert('', 'end', values=item)

    quantidade = []
    for item in lista_itens:
        try:
            quantidade.append(float(item[5]))
        except ValueError:
            print(f"Erro ao converter o valor '{item[5]}' para float. Verifique os dados.")

    total_valor = sum(quantidade)
    total_itens = len(lista_itens)

    l_total['text'] = 'R$ {:,.2f}'.format(total_valor)
    l_quantidade['text'] = total_itens

mostrar()
janela.mainloop()