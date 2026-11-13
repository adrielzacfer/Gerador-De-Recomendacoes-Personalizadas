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
TempoAtividadeFisica = -1 # Em minutos.
TempoExercicioFisico = -1 # Em minutos.
TipoExercicio1 = -1 # Primeiro tipo de exercicio (ver tabela abaixo).
TipoExercicio2 = -1 # Segundo tipo de exercicio.
TipoExercicio3 = -1 # Terceiro tipo de exercicio.
# 0 - Nenhum, 1 - Corrida e Caminhada, 2 - Musculacao, 3 - Futebol/futsal, 4 - Alongamento, 5 - Ciclismo,
# 6 - Treinamento Funcional, 7 - Natacao, 8 - Pilates, 9 - Volei/futevolei, 10 - Danca.
FrequenciaExercicio = -1 # De 0 a 7 vezes por semana.
IntensidadeExercicio = 0 # 1 - Leve, 2 - Moderado, 3 - Intenso.
HorarioCafe = -1 # Formato 24h (int).
HorarioAlmoco = -1 # Formato 24h (int).
HorarioJantar = -1 # Formato 24h (int).
DoresArticulacoes = -1 # 0 - Nenhuma, 1 - Coluna, 2 - Joelho, 3 - Artrite/reumatismo, 4 - Artrose em geral, 5 - Quadril.
DoresMusculares = -1 # 0 - Nenhuma, 1 - Pescoco e ombros, 2 - Lombar, 3 - Dorsal e escapulas, 4 - Bracos/antebracos/maos, 5 - Quadril/gluteos/coxas.
TempoDeTela = -1 # Em horas.

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

# Funcao que define o tempo de atividade fisica diaria do usuario.
def tempoatividadefisica():
    while (TempoAtividadeFisica < 0):
        definirTempoAtividadeFisica = int(input("Quantos minutos por dia voce fica em atividade fisica? "))
        if (definirTempoAtividadeFisica >= 0): # Se o tempo informado pelo usuario for menor do que 0 (invalido), começa denovo. Caso contrario, segue o baile.
            TempoAtividadeFisica = definirTempoAtividadeFisica
            break
        print("Resposta invalida. Tente novamente. \n")

# Funcao que define o tempo de exercicio fisico diario do usuario.
def tempoexerciciofisico():
    while (TempoExercicioFisico < 0):
        definirTempoExercicioFisico = int(input("Quantos minutos por dia voce se exercita? "))
        if (definirTempoExercicioFisico >= 0): # Se o tempo informado pelo usuario for menor do que 0 (invalido), começa denovo. Caso contrario, segue o baile.
            TempoExercicioFisico = definirTempoExercicioFisico
            break
        print("Resposta invalida. Tente novamente. \n")

# Funcoes que definem os tipos de exercicio fisico do usuario (maximo 3).
def tipoexercicio1():
    while (TipoExercicio1 < 0):
        definirTipoExercicio1 = int(input("Qual o primeiro tipo de exercicio que voce pratica (0 a 10)? "))
        if (definirTipoExercicio1 >= 0) and (definirTipoExercicio1 <= 10): # Se o tipo informado pelo usuario for invalido (fora de 0 a 10), começa denovo. Caso contrario, segue o baile.
            TipoExercicio1 = definirTipoExercicio1
            break
        print("Resposta invalida. Tente novamente com um numero de 0 a 10. \n")

def tipoexercicio2():
    while (TipoExercicio2 < 0):
        definirTipoExercicio2 = int(input("Qual o segundo tipo de exercicio que voce pratica (0 a 10)? "))
        if (definirTipoExercicio2 >= 0) and (definirTipoExercicio2 <= 10): # Se o tipo informado pelo usuario for invalido (fora de 0 a 10), começa denovo. Caso contrario, segue o baile.
            TipoExercicio2 = definirTipoExercicio2
            break
        print("Resposta invalida. Tente novamente com um numero de 0 a 10. \n")

def tipoexercicio3():
    while (TipoExercicio3 < 0):
        definirTipoExercicio3 = int(input("Qual o terceiro tipo de exercicio que voce pratica (0 a 10)? "))
        if (definirTipoExercicio3 >= 0) and (definirTipoExercicio3 <= 10): # Se o tipo informado pelo usuario for invalido (fora de 0 a 10), começa denovo. Caso contrario, segue o baile.
            TipoExercicio3 = definirTipoExercicio3
            break
        print("Resposta invalida. Tente novamente com um numero de 0 a 10. \n")

# Funcao que define a frequencia semanal de exercicio fisico do usuario.
def frequenciaexercicio():
    while (FrequenciaExercicio < 0):
        definirFrequenciaExercicio = int(input("Quantas vezes por semana voce se exercita (0 a 7)? "))
        if (definirFrequenciaExercicio >= 0) and (definirFrequenciaExercicio <= 7): # Se a frequencia informada pelo usuario for invalida (fora de 0 a 7), começa denovo. Caso contrario, segue o baile.
            FrequenciaExercicio = definirFrequenciaExercicio
            break
        print("Resposta invalida. Tente novamente com um numero de 0 a 7. \n")

# Funcao que define a intensidade do exercicio fisico do usuario.
def intensidadeexercicio():
    while (IntensidadeExercicio < 1):
        definirIntensidadeExercicio = int(input("Qual a intensidade do seu exercicio (1 - Leve, 2 - Moderado, 3 - Intenso)? "))
        if (definirIntensidadeExercicio >= 1) and (definirIntensidadeExercicio <= 3): # Se a intensidade informada pelo usuario for diferente de 1, 2 ou 3 (invalida), começa denovo. Caso contrario, segue o baile.
            IntensidadeExercicio = definirIntensidadeExercicio
            break
        print("Resposta invalida. Tente novamente com 1, 2 ou 3. \n")

# Funcoes que definem o horario das refeicoes do usuario.
def horariocafe():
    while (HorarioCafe < 0):
        definirHorarioCafe = int(input("Qual o horario do seu cafe da manha (Numero inteiro. Formato de 24h)? "))
        if (definirHorarioCafe >= 0) and (definirHorarioCafe <= 23): # Se o horario informado pelo usuario for invalido (fora de 0 a 23), começa denovo. Caso contrario, segue o baile.
            HorarioCafe = definirHorarioCafe
            break
        print("Resposta invalida. Tente novamente. \n")

def horarioalmoco():
    while (HorarioAlmoco < 0):
        definirHorarioAlmoco = int(input("Qual o horario do seu almoco (Numero inteiro. Formato de 24h)? "))
        if (definirHorarioAlmoco >= 0) and (definirHorarioAlmoco <= 23): # Se o horario informado pelo usuario for invalido (fora de 0 a 23), começa denovo. Caso contrario, segue o baile.
            HorarioAlmoco = definirHorarioAlmoco
            break
        print("Resposta invalida. Tente novamente. \n")

def horariojantar():
    while (HorarioJantar < 0):
        definirHorarioJantar = int(input("Qual o horario da sua janta (Numero inteiro. Formato de 24h)? "))
        if (definirHorarioJantar >= 0) and (definirHorarioJantar <= 23): # Se o horario informado pelo usuario for invalido (fora de 0 a 23), começa denovo. Caso contrario, segue o baile.
            HorarioJantar = definirHorarioJantar
            break
        print("Resposta invalida. Tente novamente. \n")

# Funcao que define as dores especificas em articulacoes do usuario.
def doresarticulacoes():
    while (DoresArticulacoes < 0):
        definirDoresArticulacoes = int(input("Sente dor em alguma articulacao (0 - Nenhuma, 1 - Coluna, 2 - Joelho, 3 - Artrite/reumatismo, 4 - Artrose em geral, 5 - Quadril)? "))
        if (definirDoresArticulacoes >= 0) and (definirDoresArticulacoes <= 5): # Se a resposta do usuario for invalida (fora de 0 a 5), começa denovo. Caso contrario, segue o baile.
            DoresArticulacoes = definirDoresArticulacoes
            break
        print("Resposta invalida. Tente novamente com um numero de 0 a 5. \n")

# Funcao que define as dores musculares especificas do usuario.
def doresmusculares():
    while (DoresMusculares < 0):
        definirDoresMusculares = int(input("Sente dor muscular em alguma regiao (0 - Nenhuma, 1 - Pescoco e ombros, 2 - Lombar, 3 - Dorsal e escapulas, 4 - Bracos/antebracos/maos, 5 - Quadril/gluteos/coxas)? "))
        if (definirDoresMusculares >= 0) and (definirDoresMusculares <= 5): # Se a resposta do usuario for invalida (fora de 0 a 5), começa denovo. Caso contrario, segue o baile.
            DoresMusculares = definirDoresMusculares
            break
        print("Resposta invalida. Tente novamente com um numero de 0 a 5. \n")

# Funcao que define o tempo de tela do usuario.
def tempodetela():
    while (TempoDeTela < 0):
        definirTempoDeTela = float(input("Quantas horas por dia voce passa em telas? "))
        if (definirTempoDeTela >= 0) and (definirTempoDeTela <= 24): # Se o tempo de tela informado pelo usuario for invalido (menor que 0 ou maior que 24), começa denovo. Caso contrario, segue o baile.
            TempoDeTela = definirTempoDeTela
            break
        print("Resposta invalida. Tente novamente. \n")
