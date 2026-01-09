import sqlite3 as lite
import sqlite3

# Conectar ao banco de dados =================================
con = lite.connect("database/date.db")

# Inserir dados =================================
def inserir_form(i):
    with con:
        cur = con.cursor()
        query = "INSERT INTO cadastramento (nome, tipo_produto, marca_modelo, data_venda, valor, numero_serie, imagem)VALUES (?, ?, ?, ?, ?, ?, ?)"
        cur.execute(query, i)

# Atualizar cadastramento pelo id =================================
def atualizar_(i):
    with con:
        cur = con.cursor()
        query = """UPDATE cadastramento 
        SET nome=?, tipo_produto=?, marca_modelo=?, data_venda=?, valor=?, numero_serie=?, imagem=? 
        WHERE id=?"""
        cur.execute(query, i)

# Deletar um registro específico e reorganizar os IDs =================================
def deletar_form(i):
    # Conectando ao banco de dados
    with sqlite3.connect("database/date.db") as con:
        cur = con.cursor()

        # Passo 1: Excluir o item com o ID especificado
        query = "DELETE FROM cadastramento WHERE id=?"
        cur.execute(query, (i,))  # Passando 'i' como uma tupla

        # Passo 2: Criar uma tabela temporária para armazenar os dados restantes
        cur.execute("""
            CREATE TABLE IF NOT EXISTS temp_cadastramento(
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

        # Passo 3: Copiar os dados da tabela original (sem o ID excluído) para a tabela temporária
        cur.execute("""
            INSERT INTO temp_cadastramento (nome, tipo_produto, marca_modelo, data_venda, valor, numero_serie, imagem)
            SELECT nome, tipo_produto, marca_modelo, data_venda, valor, numero_serie, imagem
            FROM cadastramento
            ORDER BY id
        """)

        # Passo 4: Substituir a tabela original pela nova tabela temporária
        cur.execute("DROP TABLE cadastramento")
        cur.execute("ALTER TABLE temp_cadastramento RENAME TO cadastramento")

        # Salvando as alterações
        con.commit()

# Exemplo de chamada da função
deletar_form(6)

# Ver todos os dados =================================
def ver_form():
    ver_dados = []
    with con:
        cur = con.cursor()
        query = "SELECT * FROM cadastramento"
        cur.execute(query)

        rows = cur.fetchall()
        for row in rows:
            ver_dados.append(row)
    return ver_dados

# Ver dados individual pelo id =================================
def ver_item(id):
    ver_dados_individual = []
    with con:
        cur = con.cursor()
        query = "SELECT * FROM cadastramento WHERE id=?"
        cur.execute(query, id)

        rows = cur.fetchall()
        for row in rows:
            ver_dados_individual.append(row)

    return ver_dados_individual