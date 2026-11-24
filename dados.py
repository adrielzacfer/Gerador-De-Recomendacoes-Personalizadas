# Todos os Dados e seus Formatos/Unidades de Medida (denada mano do artigo)
#
# Valor inicial = "ainda nao respondido":
#   0  nas variaveis em que zero nunca e uma resposta valida (idade, peso...);
#   -1 nas variaveis em que zero E uma resposta de verdade (nenhuma dor,
#      zero minutos, meia-noite).
Idade = 0 # idade em anos.
FaixaEtaria = 0 # 1 - Criança, 2 - Adolescente, 3 - Adulto, 4 - Idoso.
Sexo = 0 # Masculino ou Feminino.
Altura = 0 # Em metros.
Peso = 0 # Em Kilogramas.
IMC = 0 # Indice de Massa Corporal
TempoParaComer = 0 # Em minutos.
TempoDeSono = 0 # Em horas.
HoraQueDorme = -1 # Formato 24h.
HoraQueAcorda = -1 # Formato 24h
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

# Respostas dos tres questionarios (as perguntas estao nas funcoes ipaq, alimentacao e pevi, mais abaixo).
IpaqDias = -1 # IPAQ (versao reduzida): dias da semana com atividade fisica, de 0 a 7.
IpaqMinutos = -1 # IPAQ (versao reduzida): minutos de atividade em cada um desses dias.
FrutasDias = -1 # Saude na Boa: dias da semana em que come frutas, de 0 a 7.
VerdurasDias = -1 # Saude na Boa: dias da semana em que come verduras, de 0 a 7.
SalgadinhosDias = -1 # Saude na Boa: dias da semana em que come salgadinhos, de 0 a 7.
DocesDias = -1 # Saude na Boa: dias da semana em que come doces, de 0 a 7.
RefrigeranteDias = -1 # Saude na Boa: dias da semana em que toma refrigerante, de 0 a 7.
PeviRespostas = [] # PEVI: as 15 respostas, de 0 a 3. Lista vazia = ainda nao respondido.

# A mesma tabela do comentario acima, para mostrar ao usuario antes de perguntar o tipo de exercicio.
TABELA_EXERCICIOS = (
    "  0 - Nenhum                 1 - Corrida e Caminhada\n"
    "  2 - Musculacao             3 - Futebol/futsal\n"
    "  4 - Alongamento            5 - Ciclismo\n"
    "  6 - Treinamento Funcional  7 - Natacao\n"
    "  8 - Pilates                9 - Volei/futevolei\n"
    " 10 - Danca"
)

# Funcoes que leem um numero do teclado sem derrubar o programa.
# Se o usuario digitar algo que nao e numero (uma letra, por exemplo), devolvem None,
# e a funcao de pergunta trata como resposta invalida e pergunta de novo.
def ler_inteiro(pergunta):
    try:
        return int(input(pergunta).strip())
    except ValueError:
        return None

def ler_decimal(pergunta): # Aceita virgula ou ponto: 1,70 ou 1.70.
    try:
        return float(input(pergunta).strip().replace(",", "."))
    except ValueError:
        return None

# Definicao da idade do usuario.
def idade():
    global Idade
    while (Idade <= 0):
        definirIdade = ler_inteiro("Qual sua idade? ")
        if (definirIdade is not None) and (definirIdade > 0) and (definirIdade <= 120): # Se a idade informada pelo usuario for invalida (menor que 1 ou maior que 120), começa denovo.
            Idade = definirIdade
            break
        print("Idade Invalida. Tente novamente. \n")

# Definiçao da faixa etaria do usuario.
def faixaEtaria():
    global FaixaEtaria
    if (Idade < 12):
        FaixaEtaria = 1
    elif (Idade < 18): # De 12 a 17 anos.
        FaixaEtaria = 2
    elif (Idade < 60): # De 18 a 59 anos.
        FaixaEtaria = 3
    else:
        FaixaEtaria = 4

# Definicao do sexo do usuario.
def sexo() :
    global Sexo
    while (Sexo != "M") and (Sexo != "F"):
        definirSexo = input("Qual seu sexo (M ou F)? ").strip().upper()
        if (definirSexo == "M") or (definirSexo == "F"): # Se o sexo informado pelo usuario for diferente de "M" (Masculino) ou "F" (Feminino), começa denovo. Caso contrario, segue o baile.
            Sexo = definirSexo
            break
        print("Resposta Invalída. Tente novamente com M ou F. \n")

# Definiçao do IMC (Altura e Peso)
def altura(): # Funçao que define a altura do usuario
    global Altura
    while (Altura <= 0):
        definirAltura = ler_decimal("Qual sua altura em metros? ")
        if (definirAltura is not None) and (definirAltura >= 0.5) and (definirAltura <= 2.5): # Se a altura informada pelo usuario for invalida, começa denovo. Caso contrario, segue o baile.
            Altura = definirAltura
            break
        print("Altura Invalida. Informe em metros (exemplo: 1,70). Tente novamente. \n")

def peso(): # Funçao que define o peso do usuario
    global Peso
    while (Peso <= 0):
        definirPeso = ler_decimal("Qual seu peso em Kgs? ")
        if (definirPeso is not None) and (definirPeso >= 10) and (definirPeso <= 400): # Se o peso informado pelo usuario for invalido, começa denovo. Caso contrario, segue o baile.
            Peso = definirPeso
            break
        print("Peso Invalido. Tente novamente. \n")

def imc(): # So calcula depois que altura() e peso() ja foram respondidas.
    global IMC
    if (Altura > 0) and (Peso > 0):
        calculo = Peso / (Altura ** 2)
        IMC = calculo

# Funcao que define o tempo que o usuario tem para comer
def tempoparacomer():
    global TempoParaComer
    while (TempoParaComer <= 0):
        definirTempoParaComer = ler_inteiro("Quantos minutos voce tem por dia para comer (Somando todas as refeicoes)? ")
        if (definirTempoParaComer is not None) and (definirTempoParaComer > 0) and (definirTempoParaComer <= 600): # Se o tempo para comer informado pelo usuario for invalido, começa denovo. Caso contrario, segue o baile.
            TempoParaComer = definirTempoParaComer
            break
        print("Resposta invalida. Tente novamente. \n")

# Funcao que define o tempo que o usuario dorme.
def tempodesono():
    global TempoDeSono
    while (TempoDeSono <= 0):
        definirTempoDeSono = ler_inteiro("Quantos minutos voce tem por dia para dormir? ")
        if (definirTempoDeSono is not None) and (definirTempoDeSono >= 60) and (definirTempoDeSono <= 1200): # Se o tempo de sono informado pelo usuario for invalido (menos de 1 hora ou mais de 20), começa denovo. Caso contrario, segue o baile.
            definirTempoDeSonoFormatado = definirTempoDeSono / 60 # Guarda em horas.
            TempoDeSono = definirTempoDeSonoFormatado
            break
        print("Resposta invalida. Informe em minutos (exemplo: 480 para 8 horas). Tente novamente. \n")

# Funcao que define a hora que o usuario normalmente dorme
def horaquedorme():
    global HoraQueDorme
    while (HoraQueDorme < 0):
        definirHoraQueDorme = ler_inteiro("Qual o horario que voce normalmente dorme (Numero inteiro. Formato de 24h)? ")
        if (definirHoraQueDorme is not None) and (definirHoraQueDorme >= 0) and (definirHoraQueDorme <= 23): # Se a hora informada for invalida (fora de 0 a 23), começa denovo. Caso contrario, segue o baile.
            HoraQueDorme = definirHoraQueDorme
            break
        print("Resposta invalida. Tente novamente com um numero de 0 a 23. \n")

# Funcao que define a hora que o usuario normalmente acorda
def horaqueacorda():
    global HoraQueAcorda
    while (HoraQueAcorda < 0):
        definirHoraQueAcorda = ler_inteiro("Qual o horario que voce normalmente acorda (Numero inteiro. Formato de 24h)? ")
        if (definirHoraQueAcorda is not None) and (definirHoraQueAcorda >= 0) and (definirHoraQueAcorda <= 23): # Se a hora informada for invalida (fora de 0 a 23), começa denovo. Caso contrario, segue o baile.
            HoraQueAcorda = definirHoraQueAcorda
            break
        print("Resposta invalida. Tente novamente com um numero de 0 a 23. \n")

# Funcao que define o tempo de atividade fisica diaria do usuario.
def tempoatividadefisica():
    global TempoAtividadeFisica
    while (TempoAtividadeFisica < 0):
        definirTempoAtividadeFisica = ler_inteiro("Quantos minutos por dia voce fica em atividade fisica? ")
        if (definirTempoAtividadeFisica is not None) and (definirTempoAtividadeFisica >= 0) and (definirTempoAtividadeFisica <= 1440): # Se o tempo informado pelo usuario for invalido (menor que 0 ou maior que as 24 horas do dia), começa denovo. Caso contrario, segue o baile.
            TempoAtividadeFisica = definirTempoAtividadeFisica
            break
        print("Resposta invalida. Tente novamente. \n")

# Funcao que define o tempo de exercicio fisico diario do usuario.
def tempoexerciciofisico():
    global TempoExercicioFisico
    while (TempoExercicioFisico < 0):
        definirTempoExercicioFisico = ler_inteiro("Quantos minutos por dia voce se exercita? ")
        if (definirTempoExercicioFisico is not None) and (definirTempoExercicioFisico >= 0) and (definirTempoExercicioFisico <= 1440): # Se o tempo informado pelo usuario for invalido (menor que 0 ou maior que as 24 horas do dia), começa denovo. Caso contrario, segue o baile.
            TempoExercicioFisico = definirTempoExercicioFisico
            break
        print("Resposta invalida. Tente novamente. \n")

# Funcoes que definem os tipos de exercicio fisico do usuario (maximo 3).
def tipoexercicio1():
    global TipoExercicio1
    if (TipoExercicio1 < 0):
        print(TABELA_EXERCICIOS) # Mostra os codigos antes de perguntar.
    while (TipoExercicio1 < 0):
        definirTipoExercicio1 = ler_inteiro("Qual o primeiro tipo de exercicio que voce pratica (0 a 10)? ")
        if (definirTipoExercicio1 is not None) and (definirTipoExercicio1 >= 0) and (definirTipoExercicio1 <= 10): # Se o tipo informado pelo usuario for invalido (fora de 0 a 10), começa denovo. Caso contrario, segue o baile.
            TipoExercicio1 = definirTipoExercicio1
            break
        print("Resposta invalida. Tente novamente com um numero de 0 a 10. \n")

def tipoexercicio2():
    global TipoExercicio2
    while (TipoExercicio2 < 0):
        definirTipoExercicio2 = ler_inteiro("Qual o segundo tipo de exercicio que voce pratica (0 a 10)? ")
        if (definirTipoExercicio2 is not None) and (definirTipoExercicio2 >= 0) and (definirTipoExercicio2 <= 10): # Se o tipo informado pelo usuario for invalido (fora de 0 a 10), começa denovo. Caso contrario, segue o baile.
            TipoExercicio2 = definirTipoExercicio2
            break
        print("Resposta invalida. Tente novamente com um numero de 0 a 10. \n")

def tipoexercicio3():
    global TipoExercicio3
    while (TipoExercicio3 < 0):
        definirTipoExercicio3 = ler_inteiro("Qual o terceiro tipo de exercicio que voce pratica (0 a 10)? ")
        if (definirTipoExercicio3 is not None) and (definirTipoExercicio3 >= 0) and (definirTipoExercicio3 <= 10): # Se o tipo informado pelo usuario for invalido (fora de 0 a 10), começa denovo. Caso contrario, segue o baile.
            TipoExercicio3 = definirTipoExercicio3
            break
        print("Resposta invalida. Tente novamente com um numero de 0 a 10. \n")

# Funcao que define a frequencia semanal de exercicio fisico do usuario.
def frequenciaexercicio():
    global FrequenciaExercicio
    while (FrequenciaExercicio < 0):
        definirFrequenciaExercicio = ler_inteiro("Quantas vezes por semana voce se exercita (0 a 7)? ")
        if (definirFrequenciaExercicio is not None) and (definirFrequenciaExercicio >= 0) and (definirFrequenciaExercicio <= 7): # Se a frequencia informada pelo usuario for invalida (fora de 0 a 7), começa denovo. Caso contrario, segue o baile.
            FrequenciaExercicio = definirFrequenciaExercicio
            break
        print("Resposta invalida. Tente novamente com um numero de 0 a 7. \n")

# Funcao que define a intensidade do exercicio fisico do usuario.
def intensidadeexercicio():
    global IntensidadeExercicio
    while (IntensidadeExercicio < 1):
        definirIntensidadeExercicio = ler_inteiro("Qual a intensidade do seu exercicio (1 - Leve, 2 - Moderado, 3 - Intenso)? ")
        if (definirIntensidadeExercicio is not None) and (definirIntensidadeExercicio >= 1) and (definirIntensidadeExercicio <= 3): # Se a intensidade informada pelo usuario for diferente de 1, 2 ou 3 (invalida), começa denovo. Caso contrario, segue o baile.
            IntensidadeExercicio = definirIntensidadeExercicio
            break
        print("Resposta invalida. Tente novamente com 1, 2 ou 3. \n")

# Funcoes que definem o horario das refeicoes do usuario.
def horariocafe():
    global HorarioCafe
    while (HorarioCafe < 0):
        definirHorarioCafe = ler_inteiro("Qual o horario do seu cafe da manha (Numero inteiro. Formato de 24h)? ")
        if (definirHorarioCafe is not None) and (definirHorarioCafe >= 0) and (definirHorarioCafe <= 23): # Se o horario informado pelo usuario for invalido (fora de 0 a 23), começa denovo. Caso contrario, segue o baile.
            HorarioCafe = definirHorarioCafe
            break
        print("Resposta invalida. Tente novamente. \n")

def horarioalmoco():
    global HorarioAlmoco
    while (HorarioAlmoco < 0):
        definirHorarioAlmoco = ler_inteiro("Qual o horario do seu almoco (Numero inteiro. Formato de 24h)? ")
        if (definirHorarioAlmoco is not None) and (definirHorarioAlmoco >= 0) and (definirHorarioAlmoco <= 23): # Se o horario informado pelo usuario for invalido (fora de 0 a 23), começa denovo. Caso contrario, segue o baile.
            HorarioAlmoco = definirHorarioAlmoco
            break
        print("Resposta invalida. Tente novamente. \n")

def horariojantar():
    global HorarioJantar
    while (HorarioJantar < 0):
        definirHorarioJantar = ler_inteiro("Qual o horario da sua janta (Numero inteiro. Formato de 24h)? ")
        if (definirHorarioJantar is not None) and (definirHorarioJantar >= 0) and (definirHorarioJantar <= 23): # Se o horario informado pelo usuario for invalido (fora de 0 a 23), começa denovo. Caso contrario, segue o baile.
            HorarioJantar = definirHorarioJantar
            break
        print("Resposta invalida. Tente novamente. \n")

# Funcao que define as dores especificas em articulacoes do usuario.
def doresarticulacoes():
    global DoresArticulacoes
    while (DoresArticulacoes < 0):
        definirDoresArticulacoes = ler_inteiro("Sente dor em alguma articulacao (0 - Nenhuma, 1 - Coluna, 2 - Joelho, 3 - Artrite/reumatismo, 4 - Artrose em geral, 5 - Quadril)? ")
        if (definirDoresArticulacoes is not None) and (definirDoresArticulacoes >= 0) and (definirDoresArticulacoes <= 5): # Se a resposta do usuario for invalida (fora de 0 a 5), começa denovo. Caso contrario, segue o baile.
            DoresArticulacoes = definirDoresArticulacoes
            break
        print("Resposta invalida. Tente novamente com um numero de 0 a 5. \n")

# Funcao que define as dores musculares especificas do usuario.
def doresmusculares():
    global DoresMusculares
    while (DoresMusculares < 0):
        definirDoresMusculares = ler_inteiro("Sente dor muscular em alguma regiao (0 - Nenhuma, 1 - Pescoco e ombros, 2 - Lombar, 3 - Dorsal e escapulas, 4 - Bracos/antebracos/maos, 5 - Quadril/gluteos/coxas)? ")
        if (definirDoresMusculares is not None) and (definirDoresMusculares >= 0) and (definirDoresMusculares <= 5): # Se a resposta do usuario for invalida (fora de 0 a 5), começa denovo. Caso contrario, segue o baile.
            DoresMusculares = definirDoresMusculares
            break
        print("Resposta invalida. Tente novamente com um numero de 0 a 5. \n")

# Funcao que define o tempo de tela do usuario.
def tempodetela():
    global TempoDeTela
    while (TempoDeTela < 0):
        definirTempoDeTela = ler_decimal("Quantas horas por dia voce passa em telas? ")
        if (definirTempoDeTela is not None) and (definirTempoDeTela >= 0) and (definirTempoDeTela <= 24): # Se o tempo de tela informado pelo usuario for invalido (menor que 0 ou maior que 24), começa denovo. Caso contrario, segue o baile.
            TempoDeTela = definirTempoDeTela
            break
        print("Resposta invalida. Tente novamente. \n")

# CACHE! nao apagar. ---------------------------------------------------------------------------

# Funcao auxiliar dos questionarios: repete a pergunta ate vir um numero inteiro entre minimo e maximo.
def perguntar_numero(pergunta, minimo, maximo):
    while True:
        resposta = ler_inteiro(pergunta)
        if (resposta is not None) and (resposta >= minimo) and (resposta <= maximo):
            return resposta
        print("Resposta invalida. Tente novamente com um numero de", minimo, "a", maximo, "\n")

# IPAQ (versao reduzida): calcula o tempo semanal de atividade física
# O IPAQ completo separa caminhada, atividade moderada e atividade vigorosa. Aqui sao so duas perguntas,
# entao o resultado e o total de minutos na semana, sem a classificacao oficial do instrumento.
def ipaq():
    global IpaqDias, IpaqMinutos
    if (IpaqDias < 0):
        IpaqDias = perguntar_numero("Dias de atividade física por semana: ", 0, 7)
    if (IpaqDias == 0): # Sem nenhum dia de atividade, nao faz sentido perguntar os minutos.
        IpaqMinutos = 0
    elif (IpaqMinutos < 0):
        IpaqMinutos = perguntar_numero("Minutos de atividade por dia: ", 0, 1440)

    total = IpaqDias * IpaqMinutos

    print("Atividade física semanal:", total, "minutos")


# Saúde na Boa: frequência de consumo de alimentos, em dias por semana
# As cinco perguntas usam a redacao do questionario Saude na Boa (NAHAS et al., 2007).
def alimentacao():
    global FrutasDias, VerdurasDias, SalgadinhosDias, DocesDias, RefrigeranteDias
    if (FrutasDias < 0):
        FrutasDias = perguntar_numero("Em quantos dias de uma semana normal você come frutas ou toma sucos naturais de frutas? ", 0, 7)
    if (VerdurasDias < 0):
        VerdurasDias = perguntar_numero("Em quantos dias de uma semana normal você come verduras (saladas verdes, tomate, cenoura, chuchu, abóbora, couve-flor, etc)? ", 0, 7)
    if (SalgadinhosDias < 0):
        SalgadinhosDias = perguntar_numero("Em quantos dias de uma semana normal você come salgadinhos (coxinhas, pastéis, empanados)? ", 0, 7)
    if (DocesDias < 0):
        DocesDias = perguntar_numero("Em quantos dias de uma semana normal você come doces (bolos, tortas, sonhos, sorvetes)? ", 0, 7)
    if (RefrigeranteDias < 0):
        RefrigeranteDias = perguntar_numero("Em quantos dias de uma semana normal você toma refrigerantes? ", 0, 7)

    percentual = (FrutasDias / 7) * 100

    print("Consumo de frutas:", round(percentual), "% da semana")


# PEVI: avalia o estilo de vida do usuário
# As 15 afirmacoes seguem a redacao do instrumento (BOTH et al., 2008), tres por componente.
# Tres foram ADAPTADAS para adolescentes, porque o PEVI foi escrito para adultos. Redacao original:
#   8a - "Você não fuma e não ingere álcool (ou ingere com moderação)"
#   9a - "Você respeita as normas de trânsito (como pedestre, ciclista ou motorista); se dirige, usa sempre
#         o cinto de segurança e nunca ingere álcool"
#  15a - "Você equilibra o tempo dedicado ao trabalho com o tempo dedicado ao lazer"
PEVI_AFIRMACOES = [
    # Nutrição
    "Sua alimentação diária inclui pelo menos 5 porções de frutas e hortaliças.",
    "Você evita ingerir alimentos gordurosos (carnes gordas, frituras) e doces.",
    "Você faz 4 a 5 refeições variadas ao dia, incluindo café da manhã completo.",

    # Atividade física
    "Você realiza ao menos 30 minutos de atividades físicas moderadas/intensas, de forma contínua ou acumulada, 5 ou mais dias na semana.",
    "Ao menos duas vezes por semana você realiza exercícios que envolvam força e alongamento muscular.",
    "No seu dia a dia, você caminha ou pedala como meio de transporte e, preferencialmente, usa as escadas ao invés do elevador.",

    # Comportamento preventivo
    "Você conhece sua pressão arterial, seus níveis de colesterol e procura controlá-los.",
    "Você não fuma e não ingere álcool.",
    "Você respeita as normas de trânsito (como pedestre, ciclista ou passageiro) e usa sempre o cinto de segurança.",

    # Relacionamentos sociais
    "Você procura cultivar amigos e está satisfeito com seus relacionamentos.",
    "Seu lazer inclui encontros com amigos, atividades esportivas em grupo, participação em associações ou entidades sociais.",
    "Você procura ser ativo em sua comunidade, sentindo-se útil no seu ambiente social.",

    # Controle do estresse
    "Você reserva tempo (ao menos 5 minutos) todos os dias para relaxar.",
    "Você mantém uma discussão sem alterar-se, mesmo quando contrariado.",
    "Você equilibra o tempo dedicado aos estudos (ou ao trabalho) com o tempo dedicado ao lazer."
]

PEVI_ESCALA = (
    "  0 - absolutamente não faz parte do seu estilo de vida\n"
    "  1 - às vezes corresponde ao seu comportamento\n"
    "  2 - quase sempre verdadeiro no seu comportamento\n"
    "  3 - sempre verdadeiro no seu dia a dia"
)

def pevi():
    global PeviRespostas
    if (len(PeviRespostas) == len(PEVI_AFIRMACOES)): # Ja foi respondido.
        return

    print("Para cada afirmação, responda com um número de 0 a 3:")
    print(PEVI_ESCALA)

    respostas = []

    for afirmacao in PEVI_AFIRMACOES:
        print("\n" + afirmacao)
        resposta = perguntar_numero("Responda de 0 a 3: ", 0, 3)
        respostas.append(resposta)

    PeviRespostas = respostas
    total = sum(PeviRespostas)

    print("\nPontuação total do PEVI:", total, "/ 45")

# Função que gera uma mensagem de boas vindas, explicando a função do codigo.
def introducao():
    print("=" * 55)
    print()
    print("  ███   ███  █   █      █   █  ███  █   █  ██     ██   █")
    print("  █  █  █    ██ ██      █   █   █   ██  █  █ █   █  █  █")
    print("  █ █   ██   █ █ █  ██  █   █   █   █ █ █  █  █  █  █  █")
    print("  █  █  █    █   █       █ █    █   █  ██  █ █   █  █   ")
    print("  ███   ███  █   █        █    ███  █   █  ██     ██   █")
    print()
    print("=" * 55)
    print()
    print("Olá! Este programa foi desenvolvido por estudantes do")
    print("IFRS Câmpus Rolante para ajudar você a conhecer melhor")
    print("a sua rotina e a reduzir o sedentarismo.")
    print()
    print("Você vai responder algumas perguntas sobre atividade")
    print("física, alimentação, sono e hábitos do dia a dia.")
    print("Com base nas respostas, vamos sugerir mudanças simples")
    print("e adequadas à sua realidade e às suas limitações.")
    print()
    print("ATENÇÃO: este programa é educativo e NÃO faz diagnóstico.")
    print("Ele não substitui a avaliação de médicos, nutricionistas")
    print("ou profissionais de educação física.")
    print()
    print("Responda com sinceridade: não há respostas certas ou erradas.")
    print("=" * 55)
    input("\nPressione ENTER para começar...")

# Funcao que faz todas as perguntas, na ordem. Cada pergunta so e feita se ainda nao foi respondida.
def responder_tudo():
    global TipoExercicio1, TipoExercicio2, TipoExercicio3, FrequenciaExercicio

    idade()
    faixaEtaria() # Depende da idade.
    sexo()
    altura()
    peso()
    imc() # Depende da altura e do peso.
    tempoparacomer()
    horariocafe()
    horarioalmoco()
    horariojantar()
    tempodesono()
    horaquedorme()
    horaqueacorda()
    tempoatividadefisica()
    tempoexerciciofisico()

    if (TempoExercicioFisico == 0): # Quem nao se exercita nao precisa responder tipo, frequencia nem intensidade.
        TipoExercicio1 = 0
        TipoExercicio2 = 0
        TipoExercicio3 = 0
        FrequenciaExercicio = 0
    else:
        tipoexercicio1()
        if (TipoExercicio1 == 0): # Se nao tem um primeiro tipo, nao tem segundo nem terceiro.
            TipoExercicio2 = 0
            TipoExercicio3 = 0
        else:
            tipoexercicio2()
            if (TipoExercicio2 == 0):
                TipoExercicio3 = 0
            else:
                tipoexercicio3()
        frequenciaexercicio()
        if (FrequenciaExercicio > 0):
            intensidadeexercicio()

    doresarticulacoes()
    doresmusculares()
    tempodetela()

    # Depois das perguntas do perfil, os tres questionarios.
    print("\nAgora, tres questionarios curtos sobre a sua semana e o seu estilo de vida.\n")
    ipaq()
    print()
    alimentacao()
    print()
    pevi()

# Para rodar o programa inteiro:  python dados.py
# Mostra a introducao, faz as perguntas e mostra as recomendacoes (que ficam em recomendacoes.py).
if __name__ == "__main__":
    import sys
    import recomendacoes

    # Se o terminal nao souber mostrar algum caractere (os blocos do titulo, por exemplo),
    # troca por "?" em vez de derrubar o programa.
    try:
        sys.stdout.reconfigure(errors="replace")
    except (AttributeError, ValueError):
        pass

    try:
        introducao()
        print()
        responder_tudo()
        print()
        perfil = recomendacoes.criar_perfil(sys.modules[__name__])
        print(recomendacoes.formatar(perfil))
    except (EOFError, KeyboardInterrupt): # Ctrl+C ou fim da entrada: sai sem mensagem de erro.
        print("\n\nPrograma encerrado.")
