# Cria a classe Category e seis funções para ela,
# duas de uso interno _init_ e _repr_, e quatro
# de uso externo: deposit, withdraw, get_balance e transfer.
class Category:
    # Cria a função interna _init_ para estabelecer os valores
    # iniciais de Category. Usa um _ antes da função para
    # especificar ser um função interna. Aqui estabelecemos
    # os valores iniciais da class com self e description.
    # A descrição é atribuida ao self.description, usamos esse
    # recurso para facilitar o uso da variavél por outras funções.
    # Criamos também uma lista e atribuimos ela à self.ledger e
    # por fim criamos uma variavel interna _balance a self com valor 0.0.
    def __init__(self, description):
        self.description = description
        self.ledger = []
        self.__balance = 0.0

    # Cria a função _repr_. A função é padrão e serve para 
    # representar um objeto como string/texto. Ao chamar print(),
    # __repr__() devolve os atributos em memória do objeto.
    # A vantagem da função __repr__() é a possibilidade de
    # reescrevê-la para corresponder à demanda. O artificio \n
    # é para o python reconhecer uma quebra de linha.
    def __repr__(self):
        header = self.description.center(30, "*") + "\n"
        ledger = ""
        for item in self.ledger:
            # Formata description e amount conforme as orientações
            # do exercicio e cria variaveis para armazenar a formatação
            line_description = "{:<23}".format(item["description"])
            line_amount = "{:>7.2f}".format(item["amount"])
            # Cria uma nova variavel para receber as duas variaveis
            # anteriores e as formata dentro das especificações passadas.
            ledger += f"{(line_description[:23])}{(line_amount[:7])}\n"
            # O f antes de "" é outra forma de usar a função format()
            # para formatar o texto. outra forma de escrever a linha:
            # ledger += "{}{}\n".format(line_description[:23], line_amount[:7])
        total = "Total: {:.2f}".format(self.__balance)
        return header + ledger + total

    # Cria função deposit com variaveis self, amount (valor a
    # ser depositado) e description como uma linha aberta. A função
    # recebe as informações e soma a variavel amount ao _balance.
    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})
        self.__balance += amount

    # Cria função withdraw, com os mesmo principios da função
    # deposit, mas dessa vez subtraindo o valor da conta.
    # A condicional if checa se _balance da conta é maior que zero
    # caso sim subtrai da conta, caso seja menor que zero retornará falso.
    def withdraw(self, amount, description=""):
        if self.__balance - amount >= 0:
            self.ledger.append({"amount": -1 * amount, "description": description})
            self.__balance -= amount
            return True
        else:
            return False

    # Cria função get_balance para retornar o valor de _balance.
    def get_balance(self):
        return self.__balance

    # Cria a função transfer, com self, amount e category_instance.
    # A condicional if usa a função withdraw em self
    # e usa a função deposit com base nos parametros
    # de category_instance, caso de certo retorna True
    # e caso não funcione False.
    def transfer(self, amount, category_instance):
        if self.withdraw(amount, 
          f"Transfer to {(category_instance.description)}"
          ):
            category_instance.deposit(amount, 
            f"Transfer from {(self.description)}"
            )
            return True
        else:
            return False

    # Cria a função check_funds com atributos self e amount,
    # a função usa concidicional if para verificar se o _balance
    # da self é maior ou igual à amount, caso sim
    # retorna True e caso não False.
    def check_funds(self, amount):
        if self.__balance >= amount:
            return True
        else:
            return False

#--------------------------------------------------------

# Cria função create_spend_chart com atributo categories,
# dentro da função cria uma lista spent_amounts vazia.
# A função utiliza for para pegar o total gasto em cada categoria.
# Usamos a função abs() para transformar em um número absoluto,
# append() para apensar e round() para arredondar o valor usando
# o segundo paremetro como número de digitos .
def create_spend_chart(categories):
    spent_amounts = []
    for category in categories:
        spent = 0
        for item in category.ledger:
            if item["amount"] < 0:
                spent += abs(item["amount"])
        spent_amounts.append(round(spent, 2))

    # Cria uma função para calcular a porcentagem das
    # categorias e arredonda para 10. Usamos lambda para
    # executar a função com apenas uma linha de código.
    # Usando lambda não precisamos colocar def na frente
    # e também não precisa de return para devolver os valores.
    # Usamos map(), uma função de lambda, para iterar o código.
    total = round(sum(spent_amounts), 2)
    spent_percentage = list(map(lambda amount: int((((amount / total) * 10) // 1) * 10), spent_amounts))

    # Cabeçalho
    header = "Percentage spent by category\n"
    # Cria o grafico e formata para apresentação. A função reversed()
    # reverte a ordem de apresentação de um parametro. A função range()
    # usa um parametro obrigatório (ponto de parada) e dois opcionais
    # (onde começar e quais intervalos). No caso estamos pedindo para
    # começar no zero, terminar no 101 e pular de 10 em 10.
    # A função str() usa os valores criados no for e justifica à
    # direita com .rjust() acrescentando | ao final do número.
    chart = ""
    for value in reversed(range(0, 101, 10)):
        chart += str(value).rjust(3) + '|'
        # Usa a interação for para verificar se a variavel
        # spent_percentage corresponde à value, caso sim
        # marca um o e caso não deixa deixa vazio. 
        for percent in spent_percentage:
            if percent >= value:
                chart += " o "
            else:
                chart += "   "
        chart += " \n"
    # Cria uma variável para acrescentar - antes das categorias.
    # Usamos a função len() para usar como referencia quantas
    # categorias forem adicionadas e assim não fazer a mais ou menos.
    footer = "    " + "-" * ((3 * len(categories)) + 1) + "\n"

    descriptions = list(map(lambda category: category.description, categories))
    max_length = max(map(lambda description: len(description), descriptions))
    descriptions = list(map(lambda description: description.ljust(max_length), descriptions))
    
    # Usa a iteração for para percorrer a função zip() de todas
    # variaveis descriptions criando tuples com seus resultados.
    # Depois usamos a função join() para juntar esses resultados.
    for x in zip(*descriptions):
        footer += "    " + "".join(map(lambda s: s.center(3), x)) + " \n"

    return (header + chart + footer).rstrip("\n")
