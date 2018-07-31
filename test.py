import re
from decimal import Decimal

isMinus = True if re.search(r'Минус', 'USSD 8 Минус:18.70р') else False
balance = re.findall('\d+[,.]\d+', 'USSD 8 Минус:18.70р')[0]
print(isMinus)
print(str(-abs(Decimal(balance))))
