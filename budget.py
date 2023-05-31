class Category:
    def __init__(self, category):
        self.ledger = []
        self.category = category

    def __str__(self):
        category = ''
        length = 30 - len(self.category)
        i = 0
        while i < length:
            category = category + '*'
            if i == length // 2 - 1:
                category = category + self.category
            i += 1
        else:
            category = category + '\n'
        
        for transaction in self.ledger:
            if len(transaction["description"]) <= 23:
                category = category + transaction["description"]
                i = 0
                while i < 23 - len(transaction["description"]):
                    category = category + ' '
                    i += 1
            else:
                category = category + transaction["description"][:23]

            if len(str("{:.2f}".format(transaction["amount"]))) == 7:
                category = category + str("{:.2f}".format(transaction["amount"])) + '\n'
            elif len(str("{:.2f}".format(transaction["amount"]))) < 7:
                i = 0
                while i < 7 - len(str("{:.2f}".format(transaction["amount"]))):
                    category = category + ' '
                    i += 1
                category = category + str("{:.2f}".format(transaction["amount"])) + '\n'
            else:
                category = category + str("{:.2f}".format(transaction["amount"]))[:7] + '\n'

        category = category + "Total: " + str("{:.2f}".format(self.get_balance()))

        return category
    
    def deposit(self, amount, description = ''):
        self.ledger.append({"amount": amount, "description": description})
        return
    
    def withdraw(self, amount, description = ''):
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            return True
        else:
            return False
    
    def get_balance(self):
        balance = 0
        for transaction in self.ledger:
            balance = balance + transaction["amount"]
        return balance
    
    def transfer(self, amount, category):
        if self.check_funds(amount):
            self.withdraw(amount, "Transfer to "+ category.category)
            category.deposit(amount, "Transfer from "+ self.category)
            return True
        else:
            return False
    
    def check_funds(self, amount):
        if amount > self.get_balance():
            return False
        else:
            return True
    
    
def create_spend_chart(categories):
    chart = "Percentage spent by category\n"
    maxLenght = max([len(x.category) for x in categories])
    categorySpent = []
    categoryPercentage = []

    for category in categories:
        total = 0
        for transaction in category.ledger:
            if transaction["amount"] < 0:
                total = total + transaction["amount"] * -1
        categorySpent.append(total)
    
    for spent in categorySpent:
        percentage = round(spent * 10 // sum(categorySpent))
        categoryPercentage.append(percentage)

    i = 10
    while i > -1:
        if i >= -1:
            if i == 10:
                chart = chart + str(i) + "0| "
            elif i == 0:
                chart = chart + "  0| "
            else:
                chart = chart + " " + str(i) + "0| "

            for percentage in categoryPercentage:
                if percentage >= i:
                    chart = chart + "o  "
                else:
                    chart = chart + "   "
            else:
                chart = chart + "\n"
        i -= 1
    else:
        chart = chart + "    -" + "---" * len(categoryPercentage)

    i = 0
    while i < maxLenght:
        chart = chart + "\n     "
        for category in categories:
            if i < len(category.category):
                chart = chart + category.category[i] + "  "
            else:
                chart = chart + "   "
        i += 1

    return chart

# food = Category("Food")
# food.deposit(1000, "initial deposit")
# food.withdraw(10.15, "groceries")
# food.withdraw(15.89, "restaurant and more food for dessert")
# print(food.get_balance())
# clothing = Category("Clothing")
# food.transfer(50, clothing)
# clothing.withdraw(25.55)
# clothing.withdraw(100)
# auto = Category("Auto")
# auto.deposit(1000, "initial deposit")
# auto.withdraw(15)

# print(food)
# print(clothing)

# print(create_spend_chart([food, clothing, auto]))