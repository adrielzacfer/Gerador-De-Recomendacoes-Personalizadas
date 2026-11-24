"""
recomendacoes.py - banco de recomendações personalizadas.

Este arquivo cuida SÓ das recomendações. As perguntas ficam em dados.py
e não são alteradas aqui.

O banco usa as perguntas do perfil e as respostas de três questionários:
IPAQ (versão reduzida), Saúde na Boa e PEVI.

COMO SE LIGA AO RESTO DO PROGRAMA
---------------------------------
Depois que o usuário responder às perguntas de dados.py:

    import dados
    import recomendacoes

    perfil = recomendacoes.criar_perfil(dados)
    print(recomendacoes.formatar(perfil))

O "perfil" é um dicionário com os MESMOS nomes das variáveis de dados.py
(Idade, TempoDeSono, TempoDeTela, DoresArticulacoes...). Nenhum nome novo
foi inventado. Variável que ainda está com o valor inicial conta como
"não respondida", e as recomendações que dependem dela não aparecem.

COMO ACRESCENTAR UMA RECOMENDAÇÃO
---------------------------------
Copie um bloco de RECOMENDACOES e ajuste. `condicao` recebe o perfil e
devolve True quando a recomendação vale para a pessoa. `texto`, `motivo`
e `alternativas` podem ser texto fixo ou uma função do perfil, para o
texto mudar de pessoa para pessoa.

REGRAS DE SEGURANÇA (público de 15 e 16 anos)
---------------------------------------------
- Nenhuma meta de peso, contagem de calorias ou dieta.
- A dor só RETIRA exercícios das sugestões. Dor que persiste vira
  orientação para procurar um profissional.
- Nenhuma recomendação sugere um exercício que a dor relatada exclui.

AVISO: ferramenta educativa. Não faz diagnóstico.
"""

import textwrap


def criar_recomendacao(id, categoria, condicao, texto, motivo, fonte="",
                       alternativas=(), prioridade=5):
    """
    Cria uma regra de recomendação
    id: nome único da regra (ex.: "frutas_digestao")
    categoria: "atividade_fisica", "alimentacao", "sono", "sedentarismo"...
    condicao: função  perfil -> bool  (True = recomendação se aplica)
    texto: o que o usuário deve fazer
    motivo: por que isso ajuda (explicação para o usuário)
    fonte: referência do artigo que fundamenta a regra
    alternativas: o que fazer se o caminho principal não servir
    prioridade: 1 aparece primeiro; quanto maior, mais para o fim
    """
    return {
        "id": id,
        "categoria": categoria,
        "condicao": condicao,
        "texto": texto,
        "motivo": motivo,
        "fonte": fonte,
        "alternativas": alternativas,
        "prioridade": prioridade,
    }


# ---------------------------------------------------------------------------
# 1) O PERFIL: as variáveis de dados.py
# ---------------------------------------------------------------------------

# Em dados.py estas variáveis começam em 0, e 0 quer dizer "não respondida".
_VAZIO_E_ZERO = ("Idade", "FaixaEtaria", "Sexo", "Altura", "Peso", "IMC",
                 "TempoParaComer", "TempoDeSono", "IntensidadeExercicio")

# Estas começam em -1, porque nelas o 0 é uma resposta de verdade
# (nenhuma dor, nenhum exercício, zero minutos, meia-noite).
_VAZIO_E_MENOS_UM = ("HoraQueDorme", "HoraQueAcorda",
                     "TempoAtividadeFisica", "TempoExercicioFisico",
                     "TipoExercicio1", "TipoExercicio2", "TipoExercicio3",
                     "FrequenciaExercicio", "HorarioCafe", "HorarioAlmoco",
                     "HorarioJantar", "DoresArticulacoes", "DoresMusculares",
                     "TempoDeTela",
                     # respostas dos questionários IPAQ e Saúde na Boa
                     "IpaqDias", "IpaqMinutos", "FrutasDias", "VerdurasDias",
                     "SalgadinhosDias", "DocesDias", "RefrigeranteDias")

# O PEVI é uma lista com 15 respostas de 0 a 3. Lista vazia = não respondido.
_LISTAS = ("PeviRespostas",)

VARIAVEIS = _VAZIO_E_ZERO + _VAZIO_E_MENOS_UM + _LISTAS

# Os cinco componentes do PEVI, três afirmações cada, na ordem do instrumento.
PEVI_COMPONENTES = ("nutrição", "atividade física", "comportamento preventivo",
                    "relacionamentos", "controle do estresse")

# Os mesmos códigos que estão nos comentários de dados.py.
TIPOS_EXERCICIO = {
    1: "Corrida e caminhada", 2: "Musculação", 3: "Futebol/futsal",
    4: "Alongamento", 5: "Ciclismo", 6: "Treinamento funcional",
    7: "Natação", 8: "Pilates", 9: "Vôlei/futevôlei", 10: "Dança",
}
DORES_ARTICULACOES = {1: "coluna", 2: "joelho", 3: "artrite ou reumatismo",
                      4: "artrose", 5: "quadril"}
DORES_MUSCULARES = {1: "pescoço e ombros", 2: "lombar",
                    3: "dorsal e escápulas", 4: "braços, antebraços e mãos",
                    5: "quadril, glúteos e coxas"}


def criar_perfil(modulo_dados):
    """Monta o perfil a partir do módulo dados (ou de qualquer objeto que
    tenha as mesmas variáveis)."""
    perfil = {}
    for nome in VARIAVEIS:
        valor = getattr(modulo_dados, nome, None)
        # Copia a lista do PEVI: o perfil não deve mudar se dados.py mudar.
        perfil[nome] = list(valor) if isinstance(valor, list) else valor
    return perfil


def respondido(perfil, chave):
    """True se a variável tem uma resposta de verdade (não o valor inicial)."""
    valor = perfil.get(chave)
    if valor is None or isinstance(valor, bool):
        return False
    if chave in _LISTAS:
        return (isinstance(valor, (list, tuple)) and len(valor) == 15
                and all(isinstance(x, int) and not isinstance(x, bool)
                        and 0 <= x <= 3 for x in valor))
    if chave == "Sexo":
        return valor in ("M", "F")
    if not isinstance(valor, (int, float)):
        return False
    if chave in _VAZIO_E_ZERO:
        return valor > 0
    return valor >= 0


# ---------------------------------------------------------------------------
# 2) INDICADORES CALCULADOS A PARTIR DAS RESPOSTAS
# ---------------------------------------------------------------------------

def minutos_ativos_por_dia(perfil):
    """
    Minutos de atividade por dia, ou None se não der para saber.

    O questionário pergunta de três jeitos: os minutos de atividade por
    dia, os minutos de exercício com a frequência semanal e, no IPAQ, os
    dias e minutos de atividade na semana. Usamos o MAIOR dos três, para
    nunca dizer "comece do zero" a quem já se mexe bastante. Critério do
    projeto.
    """
    valores = []
    if respondido(perfil, "TempoAtividadeFisica"):
        valores.append(perfil["TempoAtividadeFisica"])
    if (respondido(perfil, "TempoExercicioFisico")
            and respondido(perfil, "FrequenciaExercicio")):
        valores.append(perfil["TempoExercicioFisico"]
                       * perfil["FrequenciaExercicio"] / 7.0)
    semana = ipaq_minutos_semana(perfil)
    if semana is not None:
        valores.append(semana / 7.0)
    return max(valores) if valores else None


def ipaq_minutos_semana(perfil):
    """
    Total de minutos de atividade na semana pelo IPAQ reduzido (dias x
    minutos), ou None. O programa NÃO dá a classificação oficial do IPAQ
    (sedentário, ativo...): ela exige separar caminhada, atividade
    moderada e vigorosa, e aqui são só duas perguntas.
    """
    if respondido(perfil, "IpaqDias") and respondido(perfil, "IpaqMinutos"):
        return perfil["IpaqDias"] * perfil["IpaqMinutos"]
    return None


def pevi_medias(perfil):
    """
    Média (0 a 3) de cada componente do PEVI, na ordem de PEVI_COMPONENTES,
    ou None se o PEVI não foi respondido.
    """
    if not respondido(perfil, "PeviRespostas"):
        return None
    respostas = perfil["PeviRespostas"]
    return {nome: sum(respostas[n * 3:n * 3 + 3]) / 3.0
            for n, nome in enumerate(PEVI_COMPONENTES)}


def _pevi(perfil, componente):
    """Média do componente, ou 3 (o melhor valor) quando não há resposta,
    para as condições das regras não dispararem sem dado."""
    medias = pevi_medias(perfil)
    return 3.0 if medias is None else medias[componente]


def _dias(perfil, chave, sem_resposta):
    """Dias por semana do Saúde na Boa, ou `sem_resposta` se faltar."""
    return perfil[chave] if respondido(perfil, chave) else sem_resposta


def horas_de_sono(perfil):
    """
    Horas de sono por noite, ou None. Usa TempoDeSono; se faltar, calcula
    pela hora em que a pessoa dorme e acorda.
    """
    if respondido(perfil, "TempoDeSono"):
        horas = perfil["TempoDeSono"]
    elif (respondido(perfil, "HoraQueDorme")
          and respondido(perfil, "HoraQueAcorda")):
        horas = (perfil["HoraQueAcorda"] - perfil["HoraQueDorme"]) % 24
    else:
        return None
    # A pergunta de dados.py pede o sono em MINUTOS. Quem digita "8"
    # pensando em horas vira 0,13 hora. Fora de 2 a 16 horas, o valor é
    # tratado como engano e o sono não é avaliado (ver avisos()).
    return horas if SONO_PLAUSIVEL[0] <= horas <= SONO_PLAUSIVEL[1] else None


SONO_PLAUSIVEL = (2, 16)


def sono_implausivel(perfil):
    """True quando há resposta de sono, mas fora da faixa plausível."""
    tem_resposta = respondido(perfil, "TempoDeSono") or (
        respondido(perfil, "HoraQueDorme")
        and respondido(perfil, "HoraQueAcorda"))
    return tem_resposta and horas_de_sono(perfil) is None


def _dor(perfil, chave):
    """Código da dor (1 a 5), ou 0 se não há dor ou não foi respondido."""
    if respondido(perfil, chave) and perfil[chave] in (1, 2, 3, 4, 5):
        return int(perfil[chave])
    return 0


def tem_dor(perfil):
    return bool(_dor(perfil, "DoresArticulacoes")
                or _dor(perfil, "DoresMusculares"))


def sem_dor_confirmado(perfil):
    """True só se as duas perguntas de dor foram respondidas com 0."""
    return all(respondido(perfil, chave) and perfil[chave] == 0
               for chave in ("DoresArticulacoes", "DoresMusculares"))


# ---------------------------------------------------------------------------
# 3) FILTRO DE EXERCÍCIOS POR DOR
#
# REGRA DE PRECAUÇÃO DO PROJETO, não tratamento: para cada dor, quais dos
# dez tipos de exercício de dados.py deixam de ser SUGERIDOS. O alongamento
# e o pilates nunca saem, então sempre sobra opção.
# ---------------------------------------------------------------------------

# Qualquer dor em articulação tira os exercícios de impacto e de carga:
# musculação, futebol, funcional, vôlei e dança (e a corrida, mais abaixo).
_IMPACTO_E_CARGA = {2, 3, 6, 9, 10}
_EVITA_ARTICULACAO = {
    1: _IMPACTO_E_CARGA,      # coluna
    2: _IMPACTO_E_CARGA,      # joelho
    3: _IMPACTO_E_CARGA,      # artrite ou reumatismo
    4: _IMPACTO_E_CARGA,      # artrose
    5: _IMPACTO_E_CARGA,      # quadril
}
_EVITA_MUSCULAR = {
    1: {2, 7, 9},         # pescoço e ombros
    2: {2, 3, 6},         # lombar
    3: {2, 7, 9},         # dorsal e escápulas
    4: {2, 5, 9},         # braços, antebraços e mãos
    5: {3, 6, 10},        # quadril, glúteos e coxas
}
# Dores em que a corrida sai, mas a caminhada fica. (dados.py junta as duas
# no código 1, então não dá para tirar o código inteiro.)
_SEM_CORRIDA_ARTICULACAO = {1, 2, 3, 4, 5}
_SEM_CORRIDA_MUSCULAR = {2, 5}


def exercicios_excluidos(perfil):
    """Códigos de exercício que a dor relatada tira das sugestões."""
    return (_EVITA_ARTICULACAO.get(_dor(perfil, "DoresArticulacoes"), set())
            | _EVITA_MUSCULAR.get(_dor(perfil, "DoresMusculares"), set()))


def so_caminhada(perfil):
    """True quando a dor relatada tira a corrida e deixa só a caminhada."""
    return (_dor(perfil, "DoresArticulacoes") in _SEM_CORRIDA_ARTICULACAO
            or _dor(perfil, "DoresMusculares") in _SEM_CORRIDA_MUSCULAR)


def nome_exercicio(perfil, codigo):
    if codigo == 1 and so_caminhada(perfil):
        return "Caminhada"
    return TIPOS_EXERCICIO[codigo]


def exercicios_praticados(perfil):
    """Códigos (1 a 10) que a pessoa disse que pratica."""
    praticados = []
    for chave in ("TipoExercicio1", "TipoExercicio2", "TipoExercicio3"):
        if respondido(perfil, chave) and perfil[chave] in TIPOS_EXERCICIO:
            if perfil[chave] not in praticados:
                praticados.append(int(perfil[chave]))
    return praticados


def sugerir_exercicios(perfil, quantos=3, ordem=(1, 5, 7, 10, 3, 9, 6, 2, 8, 4),
                       fora=()):
    """
    Nomes de exercícios para sugerir: primeiro os que a pessoa já pratica,
    depois os da `ordem`, sempre sem os excluídos pela dor.
    """
    excluidos = exercicios_excluidos(perfil)
    candidatos = [c for c in exercicios_praticados(perfil) if c in ordem]
    candidatos += [c for c in ordem if c not in candidatos]
    nomes = [nome_exercicio(perfil, c) for c in candidatos
             if c not in excluidos and c not in fora]
    return nomes[:quantos]


def _lista(nomes):
    """['a', 'b', 'c'] -> 'a, b ou c' (em minúsculas)."""
    nomes = [n.lower() for n in nomes]
    if len(nomes) <= 1:
        return "".join(nomes)
    return ", ".join(nomes[:-1]) + " ou " + nomes[-1]


def _n(x):
    """7.0 -> '7'; 6.5 -> '6,5'."""
    return ("%.1f" % x).replace(".", ",").replace(",0", "")


# ---------------------------------------------------------------------------
# 4) REFERÊNCIAS (padrão ABNT)
#
# Dados bibliográficos dos artigos conferidos no PubMed, com os números
# lidos nos resumos. O manual da SBP, o Guia Alimentar e a diretriz de
# açúcares da OMS foram conferidos por busca na web.
# ---------------------------------------------------------------------------

REFERENCIAS = {
    "BULL et al., 2020":
        "BULL, F. C. et al. World Health Organization 2020 guidelines on "
        "physical activity and sedentary behaviour. British Journal of "
        "Sports Medicine, v. 54, n. 24, p. 1451-1462, 2020. "
        "DOI: 10.1136/bjsports-2020-102955.",
    "CHAPUT et al., 2020":
        "CHAPUT, J.-P. et al. 2020 WHO guidelines on physical activity and "
        "sedentary behaviour for children and adolescents aged 5-17 years: "
        "summary of the evidence. International Journal of Behavioral "
        "Nutrition and Physical Activity, v. 17, n. 1, p. 141, 2020. "
        "DOI: 10.1186/s12966-020-01037-z.",
    "JANSSEN; LEBLANC, 2010":
        "JANSSEN, I.; LEBLANC, A. G. Systematic review of the health "
        "benefits of physical activity and fitness in school-aged children "
        "and youth. International Journal of Behavioral Nutrition and "
        "Physical Activity, v. 7, p. 40, 2010. DOI: 10.1186/1479-5868-7-40.",
    "GUTHOLD et al., 2020":
        "GUTHOLD, R. et al. Global trends in insufficient physical activity "
        "among adolescents: a pooled analysis of 298 population-based "
        "surveys with 1.6 million participants. The Lancet Child & "
        "Adolescent Health, v. 4, n. 1, p. 23-35, 2020. "
        "DOI: 10.1016/S2352-4642(19)30323-2.",
    "TREMBLAY et al., 2011":
        "TREMBLAY, M. S. et al. Systematic review of sedentary behaviour "
        "and health indicators in school-aged children and youth. "
        "International Journal of Behavioral Nutrition and Physical "
        "Activity, v. 8, p. 98, 2011. DOI: 10.1186/1479-5868-8-98.",
    "SBP, 2024":
        "SOCIEDADE BRASILEIRA DE PEDIATRIA. #MenosTelas #MaisSaúde: manual "
        "de orientação. Atualização 2024. Rio de Janeiro: SBP, 2024.",
    "PARUTHI et al., 2016":
        "PARUTHI, S. et al. Recommended amount of sleep for pediatric "
        "populations: a consensus statement of the American Academy of "
        "Sleep Medicine. Journal of Clinical Sleep Medicine, v. 12, n. 6, "
        "p. 785-786, 2016. DOI: 10.5664/jcsm.5866.",
    "CARTER et al., 2016":
        "CARTER, B. et al. Association between portable screen-based media "
        "device access or use and sleep outcomes: a systematic review and "
        "meta-analysis. JAMA Pediatrics, v. 170, n. 12, p. 1202-1208, 2016. "
        "DOI: 10.1001/jamapediatrics.2016.2341.",
    "FATIMA; DOI; MAMUN, 2015":
        "FATIMA, Y.; DOI, S. A. R.; MAMUN, A. A. Longitudinal impact of "
        "sleep on overweight and obesity in children and adolescents: a "
        "systematic review and bias-adjusted meta-analysis. Obesity "
        "Reviews, v. 16, n. 2, p. 137-149, 2015. DOI: 10.1111/obr.12245.",
    "BRASIL, 2014":
        "BRASIL. Ministério da Saúde. Guia alimentar para a população "
        "brasileira. 2. ed. Brasília: Ministério da Saúde, 2014.",
    "WHO, 2015":
        "WORLD HEALTH ORGANIZATION. Guideline: sugars intake for adults and "
        "children. Geneva: WHO, 2015.",
}

REFERENCIAS.update({
    "AUNE et al., 2017":
        "AUNE, D. et al. Fruit and vegetable intake and the risk of "
        "cardiovascular disease, total cancer and all-cause mortality: a "
        "systematic review and dose-response meta-analysis of prospective "
        "studies. International Journal of Epidemiology, v. 46, n. 3, "
        "p. 1029-1056, 2017. DOI: 10.1093/ije/dyw319.",
    "MALIK et al., 2010":
        "MALIK, V. S. et al. Sugar-sweetened beverages and risk of metabolic "
        "syndrome and type 2 diabetes: a meta-analysis. Diabetes Care, v. 33, "
        "n. 11, p. 2477-2483, 2010. DOI: 10.2337/dc10-1079.",
    "DE RUYTER et al., 2012":
        "DE RUYTER, J. C. et al. A trial of sugar-free or sugar-sweetened "
        "beverages and body weight in children. The New England Journal of "
        "Medicine, v. 367, n. 15, p. 1397-1406, 2012. "
        "DOI: 10.1056/NEJMoa1203034.",
    "CRAIG et al., 2003":
        "CRAIG, C. L. et al. International physical activity questionnaire: "
        "12-country reliability and validity. Medicine & Science in Sports & "
        "Exercise, v. 35, n. 8, p. 1381-1395, 2003. "
        "DOI: 10.1249/01.MSS.0000078924.61453.FB.",
    "NAHAS et al., 2007":
        "NAHAS, M. V. et al. Reprodutibilidade e validade do questionário "
        "Saúde na Boa para avaliar atividade física e hábitos alimentares em "
        "escolares do ensino médio. Revista Brasileira de Atividade Física & "
        "Saúde, v. 12, n. 3, p. 12-20, 2007. "
        "DOI: 10.12820/rbafs.v.12n3p12-20.",
    "NAHAS; BARROS; FRANCALACCI, 2000":
        "NAHAS, M. V.; BARROS, M. V. G.; FRANCALACCI, V. L. O pentáculo do "
        "bem-estar: base conceitual para avaliação do estilo de vida de "
        "indivíduos ou grupos. Revista Brasileira de Atividade Física & "
        "Saúde, v. 5, n. 2, p. 48-59, 2000.",
    "BOTH et al., 2008":
        "BOTH, J. et al. Validação da escala \"Perfil do Estilo de Vida "
        "Individual\". Revista Brasileira de Atividade Física & Saúde, "
        "v. 13, n. 1, p. 5-14, 2008. DOI: 10.12820/rbafs.v.13n1p5-14.",
})

CRITERIO = "Critério do projeto"     # usado em `fonte` quando não há artigo


# ---------------------------------------------------------------------------
# 5) TEXTOS QUE DEPENDEM DA PESSOA
# ---------------------------------------------------------------------------

def _motivo_atividade(perfil):
    return (
        "Pelas suas respostas, você soma cerca de %s minutos de atividade "
        "física por dia. A OMS recomenda para a sua idade uma média de 60 "
        "minutos por dia de atividade moderada a vigorosa. Não precisa "
        "chegar lá de uma vez: em jovens de 5 a 17 anos, parte dos "
        "benefícios já aparece com uma média de 30 minutos por dia, e "
        "quanto mais atividade, maior o benefício. E você não está "
        "sozinho(a): no mundo, 81%% dos estudantes de 11 a 17 anos não "
        "atingem a recomendação." % _n(minutos_ativos_por_dia(perfil)))


def _texto_comecar(perfil):
    return (
        "Nas próximas duas semanas, some 10 a 15 minutos de movimento por "
        "dia ao que você já faz. Depois aumente aos poucos, a caminho dos "
        "60 minutos por dia. Boas opções para você: %s. Escolha um horário "
        "fixo, como logo depois da aula."
        % _lista(sugerir_exercicios(perfil, 3)))


def _texto_aumentar(perfil):
    return (
        "Você já se mexe, e isso conta. Acrescente 10 minutos aos dias em "
        "que já faz atividade, ou um dia ativo a mais na semana, até chegar "
        "aos 60 minutos por dia. Boas opções para você: %s."
        % _lista(sugerir_exercicios(perfil, 3)))


def _alternativas_atividade(perfil):
    ja = sugerir_exercicios(perfil, 3)
    outras = [n for n in sugerir_exercicios(perfil, 10) if n not in ja][:2]
    alternativas = [
        "Sem tempo seguido? Três blocos de 10 minutos ao longo do dia "
        "somam do mesmo jeito.",
        "Com companhia fica mais fácil manter: chame alguém para ir junto.",
    ]
    if outras:
        alternativas.insert(1, "Enjoou ou não gostou? Troque por %s."
                            % _lista(outras))
    return alternativas


def _texto_frequencia(perfil):
    forca = sugerir_exercicios(perfil, 2, ordem=(6, 2, 8))
    return (
        "Distribua o exercício em pelo menos 3 dias da semana, e inclua "
        "nesses dias algo que fortaleça os músculos. Opções para você: %s. "
        "Comece com um dia a mais do que faz hoje." % _lista(forca))


def _alternativas_frequencia(perfil):
    alternativas = ["Semana cheia? Sessões de 15 minutos em casa já contam "
                    "como um dia."]
    if tem_dor(perfil):
        # Com dor, o programa não sugere exercício de força por conta
        # própria além do que passou pelo filtro.
        alternativas.insert(0, "Como você relatou dor, peça ao professor "
                            "de Educação Física exercícios de força "
                            "adaptados para você.")
    else:
        alternativas.insert(0, "Sem academia e sem equipamento? O peso do "
                            "próprio corpo e duas garrafas de água cheias "
                            "são suficientes para começar.")
    return alternativas


def _dores_relatadas(perfil):
    partes = []
    if _dor(perfil, "DoresArticulacoes"):
        partes.append(DORES_ARTICULACOES[_dor(perfil, "DoresArticulacoes")])
    if _dor(perfil, "DoresMusculares"):
        partes.append(DORES_MUSCULARES[_dor(perfil, "DoresMusculares")])
    return " e ".join(partes)


def _motivo_dor(perfil):
    excluidos = sorted(exercicios_excluidos(perfil))
    fora = [TIPOS_EXERCICIO[c].lower() for c in excluidos]
    if so_caminhada(perfil):
        fora.append("corrida (a caminhada continua)")
    return (
        "Você relatou dor em: %s. Por precaução, o programa deixou de "
        "sugerir para você: %s. Isso é uma regra de segurança do projeto, "
        "não um tratamento. Parar de se mexer por causa da dor costuma não "
        "ser a saída: o caminho é adaptar a atividade enquanto a dor é "
        "avaliada." % (_dores_relatadas(perfil), ", ".join(fora)))


def _texto_dor(perfil):
    texto = ("Continue ativo(a) com o que não provoca a dor: %s. Avise o "
             "professor de Educação Física para ele adaptar a aula."
             % _lista(sugerir_exercicios(perfil, 4)))
    excluidos = exercicios_excluidos(perfil)
    pratica = [TIPOS_EXERCICIO[c].lower() for c in exercicios_praticados(perfil)
               if c in excluidos]
    if pratica:
        texto += (" Você pratica %s: não precisa abandonar. Converse com o "
                  "professor ou treinador para adaptar o treino e reduzir a "
                  "carga até a dor ser avaliada." % _lista(pratica))
    if _dor(perfil, "DoresArticulacoes") in (3, 4):
        texto += (" Artrite, reumatismo e artrose na adolescência pedem "
                  "acompanhamento médico: se você ainda não tem, procure.")
    return texto


def _motivo_tela(perfil):
    return (
        "Você informou %s horas por dia em telas. A pergunta soma todas as "
        "telas, inclusive as de estudo. Para o uso por lazer, a Sociedade "
        "Brasileira de Pediatria orienta, de 11 a 18 anos, limitar telas e "
        "videogames a 2 a 3 horas por dia e nunca virar a noite. Em uma "
        "revisão com 232 estudos de jovens de 5 a 17 anos, mais de 2 horas "
        "de TV por dia se associaram a pior composição corporal, menor "
        "aptidão física, pior autoestima e pior desempenho escolar."
        % _n(perfil["TempoDeTela"]))


def _motivo_sono_curto(perfil):
    return (
        "Pelas suas respostas, você dorme cerca de %s horas por noite. O "
        "consenso da Academia Americana de Medicina do Sono é de 8 a 10 "
        "horas por dia para quem tem de 13 a 18 anos. Em estudos que "
        "acompanharam crianças e adolescentes ao longo do tempo, quem "
        "dormia pouco teve cerca de duas vezes mais chance de desenvolver "
        "excesso de peso." % _n(horas_de_sono(perfil)))


def _motivo_sono_longo(perfil):
    return (
        "Pelas suas respostas, você dorme cerca de %s horas por noite, "
        "acima da faixa de 8 a 10 horas indicada para 13 a 18 anos. Dormir "
        "bastante não é um problema por si só; o que importa é como você "
        "se sente durante o dia." % _n(horas_de_sono(perfil)))


def _motivo_comer(perfil):
    return (
        "Você informou %s minutos por dia para todas as refeições. O "
        "programa considera pouco quando o total do dia fica abaixo de 45 "
        "minutos, o que dá menos de 15 minutos por refeição principal. A "
        "Sociedade Brasileira de Pediatria orienta não usar telas durante "
        "as refeições." % _n(perfil["TempoParaComer"]))


# ---------------------------------------------------------------------------
# 6) O BANCO DE RECOMENDAÇÕES
# ---------------------------------------------------------------------------

def _ativos(perfil):
    """Minutos ativos por dia, ou -1 quando não dá para saber."""
    minutos = minutos_ativos_por_dia(perfil)
    return -1 if minutos is None else minutos


def _sono(perfil):
    """Horas de sono, ou -1 quando não dá para saber."""
    horas = horas_de_sono(perfil)
    return -1 if horas is None else horas


RECOMENDACOES = [
    # ---------------- saúde: a dor vem antes de tudo ---------------------
    criar_recomendacao(
        id="dor_adaptar",
        categoria="saude",
        prioridade=1,
        condicao=tem_dor,
        texto=_texto_dor,
        motivo=_motivo_dor,
        fonte=CRITERIO + " (precaução)",
        alternativas=[
            "Se uma atividade da lista também doer, pare e escolha outra.",
            "Dor que dura mais de duas semanas, que piora com o movimento, "
            "que vem com inchaço ou que acorda você à noite precisa ser "
            "avaliada por médico ou fisioterapeuta.",
        ],
    ),
    # ---------------- atividade física -----------------------------------
    criar_recomendacao(
        id="atividade_comecar",
        categoria="atividade_fisica",
        prioridade=2,
        condicao=lambda p: 0 <= _ativos(p) < 30,
        texto=_texto_comecar,
        motivo=_motivo_atividade,
        fonte="BULL et al., 2020; CHAPUT et al., 2020; JANSSEN; LEBLANC, "
              "2010; GUTHOLD et al., 2020",
        alternativas=_alternativas_atividade,
    ),
    criar_recomendacao(
        id="atividade_aumentar",
        categoria="atividade_fisica",
        prioridade=2,
        condicao=lambda p: 30 <= _ativos(p) < 60,
        texto=_texto_aumentar,
        motivo=_motivo_atividade,
        fonte="BULL et al., 2020; CHAPUT et al., 2020; JANSSEN; LEBLANC, "
              "2010; GUTHOLD et al., 2020",
        alternativas=_alternativas_atividade,
    ),
    criar_recomendacao(
        id="atividade_frequencia",
        categoria="atividade_fisica",
        prioridade=4,
        # Só para quem já saiu do zero: abaixo de 30 minutos por dia a
        # recomendação "começar" já cobre o assunto.
        condicao=lambda p: (respondido(p, "FrequenciaExercicio")
                            and p["FrequenciaExercicio"] < 3
                            and _ativos(p) >= 30),
        texto=_texto_frequencia,
        motivo=lambda p: (
            "Pelas suas respostas, você se exercita em %d dia(s) da semana. "
            "Em uma revisão "
            "com jovens de 5 a 17 anos, a recomendação foi incluir "
            "atividades que fortalecem músculos e ossos em pelo menos 3 "
            "dias da semana." % p["FrequenciaExercicio"]),
        fonte="JANSSEN; LEBLANC, 2010",
        alternativas=_alternativas_frequencia,
    ),
    criar_recomendacao(
        id="atividade_intensidade",
        categoria="atividade_fisica",
        prioridade=5,
        # Só quando a pessoa RESPONDEU que não tem dor nas duas perguntas.
        # Com dor, ou sem resposta, não se pede para aumentar a intensidade.
        condicao=lambda p: (respondido(p, "IntensidadeExercicio")
                            and p["IntensidadeExercicio"] == 1
                            and respondido(p, "FrequenciaExercicio")
                            and p["FrequenciaExercicio"] >= 1
                            and sem_dor_confirmado(p)),
        texto="Em dois dos seus dias de exercício, suba o ritmo por alguns "
              "minutos, até ficar difícil conversar sem pausar. Aumente "
              "esse tempo aos poucos, semana a semana.",
        motivo="Você informou que seu exercício é leve. Em uma revisão com "
               "jovens de 5 a 17 anos, a atividade precisou ser pelo menos "
               "moderada para trazer benefício substancial à saúde, e a "
               "vigorosa pode trazer benefício ainda maior.",
        fonte="JANSSEN; LEBLANC, 2010",
        alternativas=[
            "Não quer acelerar o tempo todo? Alterne um minuto forte com "
            "dois minutos leves.",
            "Se sentir dor (não confundir com cansaço), volte ao ritmo "
            "leve.",
        ],
    ),
    # ---------------- sedentarismo: telas --------------------------------
    criar_recomendacao(
        id="tela_reduzir",
        categoria="sedentarismo",
        prioridade=3,
        condicao=lambda p: respondido(p, "TempoDeTela") and p["TempoDeTela"] > 3,
        texto="Veja no relatório de tempo de uso do próprio celular quanto "
              "do seu tempo de tela é lazer. Se o lazer passar de 3 horas, "
              "corte 30 minutos por dia nesta semana e repita o corte até "
              "ficar em no máximo 3 horas. Coloque um limite diário nos "
              "dois aplicativos que mais tomam tempo.",
        motivo=_motivo_tela,
        fonte="SBP, 2024; TREMBLAY et al., 2011",
        alternativas=[
            "Se a tela é como você fala com os amigos: combine algo "
            "presencial uma vez na semana.",
            "Se você joga online: defina antes quantas partidas vai jogar "
            "e fique em pé entre uma e outra.",
            "Se a tela é o seu descanso: mantenha, mas depois de se mexer, "
            "não no lugar.",
        ],
    ),
    # ---------------- sono -----------------------------------------------
    criar_recomendacao(
        id="sono_aumentar",
        categoria="sono",
        prioridade=3,
        condicao=lambda p: 0 < _sono(p) < 8,
        texto="Ganhe 30 minutos de sono por noite nesta semana, adiantando "
              "a hora de deitar. Conte 8 a 9 horas para trás a partir da "
              "hora em que precisa acordar: essa é a sua hora de deitar. "
              "Mantenha horários parecidos também no fim de semana.",
        motivo=_motivo_sono_curto,
        fonte="PARUTHI et al., 2016; FATIMA; DOI; MAMUN, 2015",
        alternativas=[
            "Não consegue dormir mais cedo de uma vez? Adiante 15 minutos "
            "a cada três ou quatro dias.",
            "Se cochila à tarde: no máximo 30 minutos e antes das 16h.",
            "Se você dorme 8 horas e mesmo assim acorda cansado(a), ou "
            "leva mais de 30 minutos para pegar no sono quase toda noite, "
            "converse com um médico.",
        ],
    ),
    criar_recomendacao(
        id="sono_telas",
        categoria="sono",
        prioridade=4,
        # Combina duas respostas: muita tela E pouco sono.
        condicao=lambda p: (respondido(p, "TempoDeTela")
                            and p["TempoDeTela"] > 3 and 0 < _sono(p) < 8),
        texto="Largue as telas 30 minutos antes de deitar nesta semana e "
              "vá aumentando até 1 hora. Carregue o celular longe da cama, "
              "de preferência fora do quarto.",
        motivo="Suas respostas juntam muito tempo de tela e pouco sono. Em "
               "uma meta-análise com mais de 125 mil crianças e "
               "adolescentes, usar celular ou tablet na hora de dormir se "
               "associou a 2,2 vezes mais chance de dormir menos que o "
               "necessário. A Sociedade Brasileira de Pediatria orienta "
               "desconectar de 1 a 2 horas antes de dormir.",
        fonte="CARTER et al., 2016; SBP, 2024",
        alternativas=[
            "Usa o celular como despertador? Deixe do outro lado do "
            "quarto: você ainda precisa levantar para desligar.",
            "Precisa de algo para pegar no sono? Música ou podcast com "
            "temporizador e a tela virada para baixo.",
        ],
    ),
    criar_recomendacao(
        id="sono_observar",
        categoria="sono",
        prioridade=6,
        condicao=lambda p: _sono(p) > 10,
        texto="Observe por duas semanas se você acorda descansado(a): "
              "anote a hora de dormir, a de acordar e como se sentiu.",
        motivo=_motivo_sono_longo,
        fonte="PARUTHI et al., 2016",
        alternativas=[
            "Se mesmo dormindo muito você vive cansado(a) ou sem ânimo, "
            "converse com um médico.",
        ],
    ),
    # ---------------- alimentação ----------------------------------------
    criar_recomendacao(
        id="comer_com_calma",
        categoria="alimentacao",
        prioridade=5,
        condicao=lambda p: (respondido(p, "TempoParaComer")
                            and p["TempoParaComer"] < 45),
        texto="Proteja pelo menos uma refeição do dia: sentado(a), sem "
              "tela e sem pressa. Comece pela mais fácil, que costuma ser "
              "o jantar, e deixe o celular fora da mesa.",
        motivo=_motivo_comer,
        fonte=CRITERIO + " (corte de 45 minutos); SBP, 2024",
        alternativas=[
            "Manhã apertada? Deixe o café da manhã separado na véspera.",
            "Intervalo curto na escola? Leve algo que dê para comer com "
            "calma em 10 minutos.",
        ],
    ),
    # ---------------- alimentação: questionário Saúde na Boa -------------
    # As perguntas são do Saúde na Boa (NAHAS et al., 2007). Os cortes em
    # dias por semana são critérios do projeto: o instrumento não traz.
    criar_recomendacao(
        id="refrigerante",
        categoria="alimentacao",
        prioridade=4,
        condicao=lambda p: _dias(p, "RefrigeranteDias", 0) >= 3,
        texto="Troque o refrigerante por água em um dia a mais por semana, "
              "até ele ficar para no máximo dois dias. Ande com uma garrafa "
              "de água e deixe água gelada na geladeira.",
        motivo=lambda p: (
            "Você informou refrigerante em %d dia(s) da semana. Em um "
            "ensaio clínico com CRIANÇAS, trocar a bebida açucarada por uma "
            "versão sem açúcar reduziu o acúmulo de gordura corporal ao "
            "longo de 18 meses. Em estudos com ADULTOS, quem mais tomava "
            "bebidas açucaradas teve risco 26%% maior de diabetes tipo 2. A "
            "OMS recomenda que os açúcares livres fiquem abaixo de 10%% da "
            "energia do dia." % p["RefrigeranteDias"]),
        fonte="DE RUYTER et al., 2012; MALIK et al., 2010; WHO, 2015; "
              + CRITERIO + " (corte de 3 dias)",
        alternativas=[
            "Sente falta do gás? Água com gás e limão.",
            "Não quer cortar de uma vez? Diminua o tamanho: copo pequeno "
            "em vez de garrafa.",
        ],
    ),
    criar_recomendacao(
        id="frutas_verduras",
        categoria="alimentacao",
        prioridade=5,
        condicao=lambda p: (_dias(p, "FrutasDias", 7) < 5
                            or _dias(p, "VerdurasDias", 7) < 5),
        texto="Some um dia por semana com fruta e um com verdura, até "
              "chegar a pelo menos 5 dias de cada. Deixe a fruta à vista e "
              "leve uma na mochila; no almoço, comece pela verdura de que "
              "você mais gosta.",
        motivo=lambda p: (
            "Você informou frutas em %s e verduras em %s dia(s) da semana. "
            "A regra de ouro do Guia Alimentar brasileiro é preferir "
            "alimentos in natura ou minimamente processados. Em estudos com "
            "ADULTOS, comer mais frutas e verduras se associou a menor "
            "risco de doença cardiovascular e de morte por qualquer causa."
            % (_dias(p, "FrutasDias", "?"), _dias(p, "VerdurasDias", "?"))),
        fonte="BRASIL, 2014; AUNE et al., 2017; " + CRITERIO
              + " (corte de 5 dias)",
        alternativas=[
            "Não gosta de salada crua? Legume refogado, assado ou dentro "
            "da comida vale do mesmo jeito.",
            "Fruta e verdura da estação costumam ser mais baratas; as "
            "congeladas duram mais.",
        ],
    ),
    criar_recomendacao(
        id="salgadinhos",
        categoria="alimentacao",
        prioridade=5,
        condicao=lambda p: _dias(p, "SalgadinhosDias", 0) >= 3,
        texto="Troque o salgadinho por outro lanche em dois dias desta "
              "semana. Leve o lanche de casa quando der; na cantina, "
              "escolha o que parece comida feita na hora.",
        motivo=lambda p: (
            "Você informou salgadinhos, como coxinhas e pastéis, em %d "
            "dia(s) da semana. Evitar frituras e alimentos gordurosos é um "
            "dos comportamentos de nutrição avaliados no PEVI."
            % p["SalgadinhosDias"]),
        fonte="BOTH et al., 2008; " + CRITERIO + " (corte de 3 dias)",
        alternativas=[
            "Pipoca de panela, fruta com amendoim ou um sanduíche caseiro "
            "seguram a fome até a próxima refeição.",
            "Se o salgado é o programa com os amigos: mantenha um dia e "
            "troque os outros.",
        ],
    ),
    criar_recomendacao(
        id="doces",
        categoria="alimentacao",
        prioridade=5,
        condicao=lambda p: _dias(p, "DocesDias", 0) >= 4,
        texto="Escolha dois ou três dias da semana para o doce de que você "
              "mais gosta. Nos outros, tenha uma fruta à mão para a "
              "vontade de doce depois do almoço.",
        motivo=lambda p: (
            "Você informou doces em %d dia(s) da semana. A OMS recomenda "
            "que os açúcares livres fiquem abaixo de 10%% da energia do "
            "dia." % p["DocesDias"]),
        fonte="WHO, 2015; " + CRITERIO + " (corte de 4 dias)",
        alternativas=[
            "Não precisa proibir: combinar os dias funciona melhor do que "
            "cortar tudo.",
            "Banana aquecida com canela ou salada de frutas resolvem a "
            "vontade de sobremesa.",
        ],
    ),
    # ---------------- bem-estar: questionário PEVI -----------------------
    # O corte de 1,5 na média do componente é critério do projeto. Não há
    # regra para a afirmação sobre cigarro e álcool: uma resposta baixa
    # nela pode ter mais de uma leitura.
    criar_recomendacao(
        id="pevi_estresse",
        categoria="bem_estar",
        prioridade=6,
        condicao=lambda p: _pevi(p, "controle do estresse") < 1.5,
        texto="Reserve cinco minutos por dia só para relaxar, sem tela, "
              "durante duas semanas. Respire devagar: puxe o ar em 4 "
              "tempos e solte em 6.",
        motivo=lambda p: (
            "No componente \"controle do estresse\" do PEVI, sua média "
            "foi %s em uma escala de 0 a 3. Esse é um dos cinco "
            "componentes do estilo de vida avaliados pelo instrumento."
            % _n(_pevi(p, "controle do estresse"))),
        fonte="NAHAS; BARROS; FRANCALACCI, 2000; BOTH et al., 2008; "
              + CRITERIO + " (corte de 1,5)",
        alternativas=[
            "Ficar parado(a) não funciona para você? Caminhar ouvindo "
            "música também desacelera.",
            "Se tristeza, ansiedade ou irritação atrapalham seu sono ou "
            "seus estudos por mais de duas semanas, fale com um adulto de "
            "confiança, com a equipe da escola ou com a unidade de saúde.",
        ],
    ),
    criar_recomendacao(
        id="pevi_relacionamentos",
        categoria="bem_estar",
        prioridade=6,
        condicao=lambda p: _pevi(p, "relacionamentos") < 1.5,
        texto="Faça uma atividade em grupo por semana, de qualquer tipo. "
              "Veja o que a escola oferece ou chame alguém para caminhar "
              "ou estudar junto.",
        motivo=lambda p: (
            "No componente \"relacionamentos\" do PEVI, sua média foi %s "
            "em uma escala de 0 a 3. Esse é um dos cinco componentes do "
            "estilo de vida avaliados pelo instrumento."
            % _n(_pevi(p, "relacionamentos"))),
        fonte="NAHAS; BARROS; FRANCALACCI, 2000; BOTH et al., 2008; "
              + CRITERIO + " (corte de 1,5)",
        alternativas=[
            "Grupo grande cansa? Uma pessoa só já conta.",
            "Começar pela internet vale, desde que leve a um encontro de "
            "verdade de vez em quando.",
        ],
    ),
]


# O que a pessoa já faz bem: (condição, texto).
PONTOS_FORTES = [
    (lambda p: _ativos(p) >= 60,
     "Você soma 60 minutos ou mais de atividade física por dia, que é a "
     "média recomendada para a sua idade."),
    (lambda p: (respondido(p, "FrequenciaExercicio")
                and p["FrequenciaExercicio"] >= 3),
     "Você se exercita em 3 ou mais dias da semana."),
    (lambda p: 8 <= _sono(p) <= 10,
     "Você dorme dentro da faixa de 8 a 10 horas."),
    (lambda p: respondido(p, "TempoDeTela") and p["TempoDeTela"] <= 3,
     "Seu tempo de tela está em 3 horas ou menos por dia."),
    (lambda p: respondido(p, "TempoParaComer") and p["TempoParaComer"] >= 45,
     "Você tem tempo para fazer as refeições com calma."),
    (lambda p: (_dias(p, "FrutasDias", 0) >= 5
                and _dias(p, "VerdurasDias", 0) >= 5),
     "Você come frutas e verduras em 5 ou mais dias da semana."),
    (lambda p: _dias(p, "RefrigeranteDias", 7) <= 1,
     "Você quase não toma refrigerante."),
    (lambda p: (respondido(p, "PeviRespostas")
                and _pevi(p, "relacionamentos") >= 2),
     "Pelo PEVI, você cuida bem dos seus relacionamentos."),
    (lambda p: (respondido(p, "PeviRespostas")
                and _pevi(p, "controle do estresse") >= 2),
     "Pelo PEVI, você lida bem com o estresse do dia a dia."),
]

# Orientação de alimentação IGUAL PARA TODOS, além das recomendações que
# saem das respostas do Saúde na Boa: (texto, fonte).
ALIMENTACAO_GERAL = [
    ("Prefira alimentos in natura ou minimamente processados (arroz, "
     "feijão, frutas, verduras, legumes, ovos, leite, carnes) e as "
     "preparações feitas com eles aos ultraprocessados.", "BRASIL, 2014"),
]


# ---------------------------------------------------------------------------
# 7) GERAR E FORMATAR
# ---------------------------------------------------------------------------

def _resolver(valor, perfil):
    return valor(perfil) if callable(valor) else valor


def gerar_recomendacoes(perfil):
    """
    Devolve as recomendações que valem para o perfil, em ordem de
    prioridade. Cada item é um dicionário com id, categoria, texto, motivo,
    fonte e alternativas, já com os textos prontos para mostrar.
    """
    escolhidas = []
    for posicao, regra in enumerate(RECOMENDACOES):
        try:
            vale = regra["condicao"](perfil)
        except (KeyError, TypeError):
            vale = False          # faltou dado: a regra não se aplica
        if not vale:
            continue
        escolhidas.append((regra["prioridade"], posicao, {
            "id": regra["id"],
            "categoria": regra["categoria"],
            "texto": _resolver(regra["texto"], perfil),
            "motivo": _resolver(regra["motivo"], perfil),
            "fonte": regra["fonte"],
            "alternativas": list(_resolver(regra["alternativas"], perfil)),
        }))
    escolhidas.sort(key=lambda item: item[:2])
    return [item[2] for item in escolhidas]


def pontos_fortes(perfil):
    fortes = []
    for condicao, texto in PONTOS_FORTES:
        try:
            if condicao(perfil):
                fortes.append(texto)
        except (KeyError, TypeError):
            pass
    return fortes


def avisos(perfil):
    """Avisos sobre o perfil que o usuário precisa ler antes do resto."""
    lista = []
    if respondido(perfil, "Idade") and not 10 <= perfil["Idade"] <= 19:
        lista.append(
            "As recomendações usam valores para adolescentes (10 a 19 "
            "anos). Com %d anos, leia com cautela: os números podem não "
            "valer para você." % perfil["Idade"])
    if sono_implausivel(perfil):
        lista.append(
            "O tempo de sono informado ficou fora do esperado (menos de %d "
            "ou mais de %d horas). A pergunta pede o sono em minutos. O "
            "sono não foi avaliado." % SONO_PLAUSIVEL)
    return lista


def resumo_respostas(perfil):
    """As respostas da pessoa, por extenso: [(rótulo, valor)]. Só entra o
    que foi respondido."""
    p, linhas = perfil, []
    if respondido(p, "Idade"):
        linhas.append(("Idade", "%d anos" % p["Idade"]))
    if respondido(p, "Sexo"):
        linhas.append(("Sexo", "Masculino" if p["Sexo"] == "M" else "Feminino"))
    minutos = minutos_ativos_por_dia(p)
    if minutos is not None:
        linhas.append(("Atividade física", "%s minutos por dia" % _n(minutos)))
    if respondido(p, "FrequenciaExercicio"):
        linhas.append(("Exercício", "%d dia(s) por semana"
                       % p["FrequenciaExercicio"]))
    if respondido(p, "IntensidadeExercicio") and p["IntensidadeExercicio"] in (1, 2, 3):
        linhas.append(("Intensidade", ("leve", "moderada", "intensa")[
            int(p["IntensidadeExercicio"]) - 1]))
    praticados = [TIPOS_EXERCICIO[c].lower() for c in exercicios_praticados(p)]
    if praticados:
        linhas.append(("Pratica", ", ".join(praticados)))
    if all(respondido(p, c) for c in ("DoresArticulacoes", "DoresMusculares")):
        linhas.append(("Dor", _dores_relatadas(p) or "nenhuma"))
    elif tem_dor(p):
        linhas.append(("Dor", _dores_relatadas(p)))
    if respondido(p, "TempoDeTela"):
        linhas.append(("Telas", "%s horas por dia" % _n(p["TempoDeTela"])))
    if horas_de_sono(p) is not None:
        linhas.append(("Sono", "%s horas por noite" % _n(horas_de_sono(p))))
    if respondido(p, "TempoParaComer"):
        linhas.append(("Tempo para comer", "%s minutos por dia"
                       % _n(p["TempoParaComer"])))
    semana = ipaq_minutos_semana(p)
    if semana is not None:
        linhas.append(("IPAQ (versão reduzida)",
                       "%d minutos de atividade na semana" % semana))
    alimentos = [(rotulo, p[chave]) for chave, rotulo in (
        ("FrutasDias", "frutas"), ("VerdurasDias", "verduras"),
        ("SalgadinhosDias", "salgadinhos"), ("DocesDias", "doces"),
        ("RefrigeranteDias", "refrigerante")) if respondido(p, chave)]
    if alimentos:
        linhas.append(("Saúde na Boa (dias por semana)", ", ".join(
            "%s %d" % par for par in alimentos)))
    medias = pevi_medias(p)
    if medias:
        linhas.append(("PEVI (média de 0 a 3)", ", ".join(
            "%s %s" % (nome, _n(medias[nome])) for nome in PEVI_COMPONENTES)))
    return linhas


def nao_avaliado(perfil):
    """Temas que ficaram sem avaliação porque a resposta não existe."""
    p, faltou = perfil, []
    if minutos_ativos_por_dia(p) is None:
        faltou.append("atividade física")
    if not respondido(p, "FrequenciaExercicio"):
        faltou.append("frequência de exercício")
    if not all(respondido(p, c) for c in ("DoresArticulacoes", "DoresMusculares")):
        faltou.append("dores")
    if not respondido(p, "TempoDeTela"):
        faltou.append("tempo de tela")
    if horas_de_sono(p) is None:
        faltou.append("sono")
    if not respondido(p, "TempoParaComer"):
        faltou.append("tempo para comer")
    if not any(respondido(p, c) for c in (
            "FrutasDias", "VerdurasDias", "SalgadinhosDias", "DocesDias",
            "RefrigeranteDias")):
        faltou.append("alimentação (Saúde na Boa)")
    if not respondido(p, "PeviRespostas"):
        faltou.append("estilo de vida (PEVI)")
    return faltou


def sobre_os_questionarios(perfil):
    """
    Uma linha honesta sobre cada questionário que a pessoa respondeu:
    [(texto, [citações])]. Diz o que foi reduzido ou adaptado.
    """
    p, linhas = perfil, []
    if ipaq_minutos_semana(p) is not None:
        linhas.append((
            "IPAQ: usamos uma versão reduzida, com duas perguntas, que dá o "
            "total de minutos na semana e não a classificação oficial. O "
            "IPAQ foi validado em adultos de 18 a 65 anos (CRAIG et al., "
            "2003).", ["CRAIG et al., 2003"]))
    if any(respondido(p, c) for c in ("FrutasDias", "VerdurasDias",
                                      "SalgadinhosDias", "DocesDias",
                                      "RefrigeranteDias")):
        linhas.append((
            "Saúde na Boa: usamos cinco perguntas de alimentação do "
            "questionário, feito para estudantes do ensino médio (NAHAS et "
            "al., 2007). Os cortes em dias por semana são critérios do "
            "projeto.", ["NAHAS et al., 2007"]))
    if respondido(p, "PeviRespostas"):
        linhas.append((
            "PEVI: usamos as 15 afirmações do instrumento (NAHAS; BARROS; "
            "FRANCALACCI, 2000; BOTH et al., 2008), que foi feito para "
            "adultos. Três foram adaptadas para adolescentes.",
            ["NAHAS; BARROS; FRANCALACCI, 2000", "BOTH et al., 2008"]))
    return linhas


_TITULOS = {
    "saude": "SAÚDE",
    "atividade_fisica": "ATIVIDADE FÍSICA",
    "sedentarismo": "SEDENTARISMO E TELAS",
    "sono": "SONO",
    "alimentacao": "ALIMENTAÇÃO",
    "bem_estar": "BEM-ESTAR",
}


def _paragrafo(rotulo, texto, largura):
    return textwrap.wrap("%s %s" % (rotulo, texto), largura,
                         initial_indent="  ", subsequent_indent="    ")


def formatar(perfil, largura=72):
    """
    Devolve o texto completo das recomendações, pronto para um print().
    Quem escreve o programa principal decide quando mostrar ou salvar.
    """
    linhas = ["=" * largura, "RECOMENDAÇÕES PERSONALIZADAS".center(largura),
              "=" * largura]
    for aviso in avisos(perfil):
        linhas += [""] + _paragrafo("ATENÇÃO:", aviso, largura)

    respostas = resumo_respostas(perfil)
    if respostas:
        linhas += ["", "SEU PERFIL, PELAS SUAS RESPOSTAS", "-" * largura]
        for rotulo, valor in respostas:
            linhas += _paragrafo(rotulo + ":", valor, largura)
    faltou = nao_avaliado(perfil)
    if faltou:
        linhas += [""] + _paragrafo(
            "Sem resposta, não deu para avaliar:", ", ".join(faltou) + ".",
            largura)

    fortes = pontos_fortes(perfil)
    if fortes:
        linhas += ["", "O QUE VOCÊ JÁ FAZ BEM", "-" * largura]
        for forte in fortes:
            linhas += _paragrafo("-", forte, largura)

    recomendacoes = gerar_recomendacoes(perfil)
    citadas = []
    if not recomendacoes and not respostas:
        linhas += ["", "Nenhuma resposta foi registrada ainda, então não "
                   "há recomendação a mostrar."]
    elif not recomendacoes:
        linhas += ["", "Nos temas que deu para avaliar, não há "
                   "recomendação a fazer agora."]
    for numero, rec in enumerate(recomendacoes, start=1):
        titulo = _TITULOS.get(rec["categoria"], rec["categoria"].upper())
        linhas += ["", "%d. %s" % (numero, titulo), "-" * largura]
        linhas += _paragrafo("O que fazer:", rec["texto"], largura)
        linhas += _paragrafo("Por quê:", rec["motivo"], largura)
        if rec["alternativas"]:
            linhas.append("  Se isso não servir para você:")
            for alternativa in rec["alternativas"]:
                linhas += textwrap.wrap(alternativa, largura,
                                        initial_indent="    - ",
                                        subsequent_indent="      ")
        linhas += _paragrafo("Fonte:", rec["fonte"], largura)
        # Não dá para separar por "; ": alguns autores já vêm com ponto e
        # vírgula ("JANSSEN; LEBLANC, 2010"). Procuramos cada citação.
        citadas += [c for c in REFERENCIAS if c in rec["fonte"]]

    linhas += ["", "ALIMENTAÇÃO: ORIENTAÇÃO GERAL", "-" * largura]
    for texto, fonte in ALIMENTACAO_GERAL:
        linhas += _paragrafo("-", "%s (%s)" % (texto, fonte), largura)
        citadas.append(fonte)

    sobre = sobre_os_questionarios(perfil)
    if sobre:
        linhas += ["", "SOBRE OS QUESTIONÁRIOS", "-" * largura]
        for texto, fontes in sobre:
            linhas += _paragrafo("-", texto, largura)
            citadas += fontes

    referencias = sorted({REFERENCIAS[c] for c in citadas if c in REFERENCIAS})
    if referencias:
        linhas += ["", "REFERÊNCIAS", "-" * largura]
        for referencia in referencias:
            linhas += textwrap.wrap(referencia, largura, initial_indent="  ",
                                    subsequent_indent="    ") + [""]

    linhas += textwrap.wrap(
        "Este programa é educativo e não faz diagnóstico. Ele não "
        "substitui a avaliação de médicos, nutricionistas ou profissionais "
        "de educação física.", largura)
    return "\n".join(linhas)
