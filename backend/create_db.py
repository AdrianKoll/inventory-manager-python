import sqlite3 as lite

# Criando conexao
con = lite.connect('database/date.db')

# Excluindo e criando tabela
with con:
    cur = con.cursor()

    # Excluindo a tabela se existir
    '''cur.execute("DROP TABLE IF EXISTS cadastramento;")'''

    # Criando a tabela novamente
    cur.execute("""
        CREATE TABLE cadastramento(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome VARCHAR(25) NOT NULL, 
            tipo_produto VARCHAR(25) NOT NULL,
            marca_modelo VARCHAR(25) NOT NULL,
            data_venda DATE NOT NULL,
            valor REAL NOT NULL,
            numero_serie VARCHAR(50) NOT NULL,
            imagem VARCHAR(100)
        )
    """)
    print("Tabela criada com sucesso!")