num1 = int(input("Dime un numero:    "))
num2 = int(input("dime otro numero:   "))
hac = int(input("pon 1 si quieres sumar, 2 para restar, 3 para multiplicar y 4 para dividir:   "))
if hac == 1:
    print(num1+num2)
elif hac == 2:
    print(num1-num2)
elif hac == 3:
    print(num1*num2)
elif hac == 4:
    print(num1//num2)   
else:
    print("Tienes que poner 1, 2, 3 o 4")