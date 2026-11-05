# Todos os Dados e seus Formatos/Unidades de Medida (denada mano do artigo)
Idade = 0 # idade em anos.
FaixaEtaria = 0 # 1 - Criança, 2 - Adolescente, 3 - Adulto, 4 - Idoso.
Sexo = 0 # Masculino ou Feminino.
Altura = 0 # Em metros.
Peso = 0 # Em Kilogramas.
IMC = 0 # Indice de Massa Corporal
TempoParaComer = 0 # Em minutos.
TempoDeSono = 0 # Em horas.
HoraQueDorme = 0 # Formato 24h.
HoraQueAcorda = 0 # Formato 24h

# Definicao da idade do usuario.
def idade():
    while (Idade < 0):
        definirIdade = int(input("Qual sua idade?" ))
        if (Idade > 0): # Se a idade informada pelo usuario for menor do que 0 (invalida), começa denovo.
            Idade = definirIdade
            break
        print("Idade Invalida. Tente novamente. \n")

# Definiçao da faixa etaria do usuario.
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
def sexo() :
    while (Sexo != "M" or "F"):
        definirSexo = input("Qual seu sexo (M ou F)? ")
        if (Sexo == "M" or "F"): # Se o sexo informado pelo usuario for diferente de "M" (Masculino) ou "F" (Feminino), começa denovo. Caso contrario, segue o baile.
            Sexo = definirSexo 
        print("Resposta Invalída. Tente novamente com M ou F. \n")

# Definiçao do IMC (Altura e Peso)
def altura(): # Funçao que define a altura do usuario
    while (Altura < 0):
        definirAltura = int(input("Qual sua altura em metros?" ))
        if (Idade > 0): # Se a altura informada pelo usuario for menor do que 0 (invalida), começa denovo. Caso contrario, segue o baile.
            Altura = definirAltura
            break
        print("Altura Invalida. Tente novamente. \n")    

def peso(): # Funçao que define o peso do usuario
    while (Peso < 0):
        definirPeso = int(input("Qual seu peso em Kgs?" ))
        if (Peso > 0): # Se o peso informado pelo usuario for menor do que 0 (invalido), começa denovo. Caso contrario, segue o baile.
            Peso = definirPeso
            break
        print("Peso Invalido. Tente novamente. \n") 

def imc():
    calculo = Peso / (Altura ** 2) 
    IMC = calculo

# Funcao que define o tempo que o usuario tem para comer
def tempoparacomer():
    while (TempoParaComer < 0): 
        definirTempoParaComer = int(input("Quantos minutos voce tem por dia para comer (Somando todas as refeicoes)? "))
        if (definirTempoParaComer > 0): # Se o tempo para comer informado pelo usuario for menor do que 0 (invalido), começa denovo. Caso contrario, segue o baile.
            TempoParaComer = definirTempoParaComer
            break
        print("Resposta invalida. Tente novamente. \n")

# Funcao que define o tempo que o usuario dorme.
def tempodesono():
    while (TempoDeSono < 0):
        definirTempoDeSono = int(input("Quantos minutos voce tem por dia para dormir? "))
        definirTempoDeSonoFormatado = definirTempoDeSono / 60
        if (definirTempoDeSono > 0): # Se o tempo de sono informado pelo usuario for menor do que 0 (invalido), começa denovo. Caso contrario, segue o baile.
            TempoDeSono = definirTempoDeSonoFormatado
            break
        print("Resposta invalida. Tente novamente. \n")

# Funcao que define a hora que o usuario normalmente dorme 
def horaquedorme():
    while (HoraQueDorme < 0):
        definirHoraQueDorme = int(input("Qual o horario que voce normalmente dorme (Numero inteiro. Formato de 24h)? "))
        if (definirHoraQueDorme > 0): # Se a hora que o usuario normalmente dorme informada for menor do que 0 (invalido), começa denovo. Caso contrario, segue o baile.
            HoraQueDorme = definirHoraQueDorme
            break
         print("Resposta invalida. Tente novamente. \n")

# Funcao que define a hora que o usuario normalmente acorda
def horaqueacorda():
    while (HoraQueAcorda < 0):
        definirHoraQueAcorda = int(input("Qual o horario que voce normalmente acorda (Numero inteiro. Formato de 24h)? "))
        if (definirHoraQueAcorda > 0): # Se a hora que o usuario normalmente acorda informada for menor do que 0 (invalido), começa denovo. Caso contrario, segue o baile.
            HoraQueAcorda = definirHoraQueAcorda
            break
        print("Resposta invalida. Tente novamente. \n")

