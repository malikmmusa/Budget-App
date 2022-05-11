class Category:
  def __init__(self, name):
    self.name = name
    self.balance = 0
    self.spent = 0
    self.ledger = []

  def __str__(self): 
    stars = '*' * round(((30-len(self.name)) / 2))
    newString = ''

    for item in self.ledger:
      desc = (item.get('description'))[:23]
      amount = str("{:.2f}".format(item.get('amount')))[:7]
      spaces = (' ' * (30 - len(desc) - len(amount)))
      newString += desc + spaces + amount + '\n'
    
    return stars + self.name + stars + '\n' + newString + 'Total: ' + str(self.balance)
  
  def deposit(self, amount, description=None):
    self.balance += amount
    if not description: self.ledger.append({"amount": amount, "description": ''})
    else: self.ledger.append({"amount": amount, "description": description})

  def withdraw(self, amount, description=None):
    if not self.check_funds(amount): return False
    self.balance -= amount
    if not description: self.ledger.append({"amount": -abs(amount), "description": ''})
    else: self.ledger.append({"amount": -abs(amount), "description": description})
    self.spent += amount
    return True

  def get_balance(self):
    return self.balance

  def transfer(self, amount, category):
    if not self.check_funds(amount): return False
    self.withdraw(amount, f'Transfer to {category.name}')
    category.deposit(amount, f'Transfer from {self.name}')
    return True

  def check_funds(self, amount):
    if self.balance < amount: return False
    return True

def create_spend_chart(categories):
  total = 0
  for category in categories:
    total += category.spent
  for category in categories:
    category.percent = round(category.spent / total * 100) // 10 * 10
    print(category.percent)
    
  newString = ''
  longestString = 0
  for num in range(100, -1, -10):
    circles = ' '
    for category in categories:
      if longestString == 0 or longestString < len(category.name): longestString = len(category.name)
      if num <= category.percent:
        circles += 'o  '
      else: circles += '   '
    newString += str(num).rjust(3, ' ') + '|' + circles + '\n'

  names = ''
  for i in range(0, longestString, 1):
    names += '     '
    for category in categories:
      try: names += category.name[i] + '  '
      except: names += '   '
    names += '\n'

  names = names[:len(names) - 1]
  return 'Percentage spent by category\n' + newString + '    ' + ('-' * (len(categories) * 3 + 1)) + '\n' + names