import re
str = "USSD 1 Na Vashem schete 0.19 grn. Tarif 'Vodafone Light+'. Nomer deystvitelen do 26.06.2019. Deshovyi rouming v Evrope za 60 grn na 3 dnya: *600*9#"
print(re.findall('\d+\.\d+', str)[0])