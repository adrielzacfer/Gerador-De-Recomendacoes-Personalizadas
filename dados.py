# Definicao da idade do usuario.
Idade = 0
def idade():
    while (Idade < 0):
        definirIdade = int(input("Qual sua idade?" ))
        if (Idade > 0): # Se a idade informada pelo usuario for menor do que 0 (invalida), começa denovo.
            Idade = definirIdade
            break
        print("Idade Invalida. Tente novamente \n")

# Definiçao da faixa etaria do usuario.
# 1 - Criança, 2 - Adolescente, 3 - Adulto, 4 - Idoso
FaixaEtaria = 0   
def faixaEtaria():
    if (Idade < 12):
        FaixaEtaria = 1
    elif (Idade > 12) and (Idade < 18):
        FaixaEtaria = 2
    elif (Idade > 18) and (Idade < 60):
        FaixaEtaria = 3
    else:
        FaixaEtaria = 4


# Definicao do sexo do usuario.
Sexo = 0
def sexo() :
    while (Sexo != "M" or "F"):
        definirSexo = input("Qual seu sexo (M ou F)? ")
        if (Sexo == "M" or "F"): # Se o sexo informado pelo usuario for diferente de "M" (Masculino) ou "F" (Feminino), começa denovo. Caso contrario, segue o baile.
            Sexo = definirSexo
        print("Resposta Invalída. Tente novamente com M ou F. \n")

# Definiçao do IMC (Altura e Peso)
Altura = 0
Peso = 0
IMC = 0
def altura(): # Funçao que define a altura do usuario
    while (Altura < 0):
        definirAltura = int(input("Qual sua altura em metros?" ))
        if (Idade > 0): # Se a altura informada pelo usuario for menor do que 0 (invalida), começa denovo. Caso contrario, segue o baile.
            Altura = definirAltura
            break
        print("Altura Invalida. Tente novamente \n")    

def peso(): # Funçao que define o peso do usuario
    while (Peso < 0):
        definirPeso = int(input("Qual seu peso em Kgs?" ))
        if (Peso > 0): # Se o peso informado pelo usuario for menor do que 0 (invalida), começa denovo. Caso contrario, segue o baile.
            Peso = definirPeso
            break
        print("Altura Invalida. Tente novamente \n") 

def imc():
    calculo = Peso / (Altura ** 2) 
    IMC = calculo

