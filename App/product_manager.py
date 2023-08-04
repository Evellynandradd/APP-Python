import sqlite3
from product import Product


class ProductManager:
    def __init__(self, database):
        self.database = database
        self.create_database()

    def create_database(self):
        with sqlite3.connect(self.database) as conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS products
                             (id INTEGER PRIMARY KEY AUTOINCREMENT,
                             name TEXT NOT NULL,
                             description TEXT,
                             price REAL,
                             quantity INTEGER);''')

    def add_product(self, product):
        with sqlite3.connect(self.database) as conn:
            conn.execute("INSERT INTO products (name, description, price, quantity) VALUES (?, ?, ?, ?)",
                         (product.name, product.description, product.price, product.quantity))

    def get_product(self, product_id):
        with sqlite3.connect(self.database) as conn:
            cursor = conn.execute(
                "SELECT * FROM products WHERE id = ?", (product_id,))
            return cursor.fetchone()

    def list_products(self):
        with sqlite3.connect(self.database) as conn:
            cursor = conn.execute("SELECT * FROM products")
            return cursor.fetchall()

    def update_product(self, product_id, name, description, price, quantity):
        with sqlite3.connect(self.database) as conn:
            conn.execute("UPDATE products SET name = ?, description = ?, price = ?, quantity = ? WHERE id = ?",
                         (name, description, price, quantity, product_id))

    def remove_product(self, product_id):
        with sqlite3.connect(self.database) as conn:
            conn.execute("DELETE FROM products WHERE id = ?", (product_id,))


def menu(product_manager):
    while True:
        print("=== Gerenciamento de Produtos ===")
        print("1. Cadastrar novo produto")
        print("2. Listar produtos")
        print("3. Atualizar produto")
        print("4. Remover produto")
        print("5. Sair")

        choice = input("Escolha uma opção: ")

        if choice == "1":
            name = input("Nome do produto: ")
            description = input("Descrição do produto: ")
            price = float(input("Preço do produto: "))
            quantity = int(input("Quantidade em estoque: "))
            product = Product(name, description, price, quantity)
            product_manager.add_product(product)
            print("Produto cadastrado com sucesso!")
        elif choice == "2":
            products = product_manager.list_products()
            for product in products:
                print(f"ID: {product[0]}")
                print(f"Nome: {product[1]}")
                print(f"Descrição: {product[2]}")
                print(f"Preço: R${product[3]}")
                print(f"Quantidade: {product[4]}")
                print("-" * 20)
        elif choice == "3":
            product_id = int(input("ID do produto a ser atualizado: "))
            product = product_manager.get_product(product_id)
            if product:
                name = input("Novo nome do produto: ")
                description = input("Nova descrição do produto: ")
                price = float(input("Novo preço do produto: "))
                quantity = int(input("Nova quantidade em estoque: "))
                product_manager.update_product(
                    product_id, name, description, price, quantity)
                print("Produto atualizado com sucesso!")
            else:
                print("Produto não encontrado.")
        elif choice == "4":
            product_id = int(input("ID do produto a ser removido: "))
            product = product_manager.get_product(product_id)
            if product:
                product_manager.remove_product(product_id)
                print("Produto removido com sucesso!")
            else:
                print("Produto não encontrado.")
        elif choice == "5":
            print("Encerrando o programa...")
            break
        else:
            print("Opção inválida. Tente novamente.")
        print()


# Execução do aplicativo
if __name__ == '__main__':
    product_manager = ProductManager('database.db')
    menu(product_manager)
