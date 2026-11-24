"""
testes_recomendacoes.py - rode com:  python testes_recomendacoes.py

Confere o banco de recomendações com perfis de exemplo. Não precisa
instalar nada. Se alguma verificação falhar, o programa diz qual.
"""

import itertools
import random
import re
import sys

import dados
import recomendacoes as rec

# Público de 15 e 16 anos: nenhum texto fala em emagrecer, peso a perder,
# calorias ou dieta.
PROIBIDAS = ("emagrec", "perder peso", " kg", "caloria", "dieta")

# Palavra que denuncia cada tipo de exercício num texto (código -> palavra).
PALAVRA = {2: "musculação", 3: "futebol", 5: "ciclismo", 6: "funcional",
           7: "natação", 9: "vôlei", 10: "dança"}


class DadosVazio:
    """Imita o módulo dados.py logo depois de aberto: tudo no valor inicial."""
    Idade = 0
    FaixaEtaria = 0
    Sexo = 0
    Altura = 0
    Peso = 0
    IMC = 0
    TempoParaComer = 0
    TempoDeSono = 0
    HoraQueDorme = -1
    HoraQueAcorda = -1
    TempoAtividadeFisica = -1
    TempoExercicioFisico = -1
    TipoExercicio1 = -1
    TipoExercicio2 = -1
    TipoExercicio3 = -1
    FrequenciaExercicio = -1
    IntensidadeExercicio = 0
    HorarioCafe = -1
    HorarioAlmoco = -1
    HorarioJantar = -1
    DoresArticulacoes = -1
    DoresMusculares = -1
    TempoDeTela = -1
    IpaqDias = -1
    IpaqMinutos = -1
    FrutasDias = -1
    VerdurasDias = -1
    SalgadinhosDias = -1
    DocesDias = -1
    RefrigeranteDias = -1
    PeviRespostas = []


def perfil(**respostas):
    """Perfil no valor inicial de dados.py, com as respostas indicadas."""
    p = rec.criar_perfil(DadosVazio)
    p.update(respostas)
    return p


def ativo():
    """Alguém que cumpre tudo."""
    return perfil(Idade=16, Sexo="F", TempoParaComer=60, TempoDeSono=8.5,
                  TempoAtividadeFisica=70, TempoExercicioFisico=60,
                  TipoExercicio1=3, TipoExercicio2=2, TipoExercicio3=0,
                  FrequenciaExercicio=5, IntensidadeExercicio=3,
                  DoresArticulacoes=0, DoresMusculares=0, TempoDeTela=2,
                  IpaqDias=5, IpaqMinutos=60, FrutasDias=7, VerdurasDias=6,
                  SalgadinhosDias=1, DocesDias=2, RefrigeranteDias=0,
                  PeviRespostas=[3] * 15)


def parado():
    """Alguém com tudo a melhorar."""
    return perfil(Idade=15, Sexo="M", TempoParaComer=20, TempoDeSono=6,
                  TempoAtividadeFisica=5, TempoExercicioFisico=0,
                  TipoExercicio1=0, FrequenciaExercicio=0,
                  IntensidadeExercicio=1, DoresArticulacoes=2,
                  DoresMusculares=2, TempoDeTela=7,
                  IpaqDias=0, IpaqMinutos=0, FrutasDias=0, VerdurasDias=0,
                  SalgadinhosDias=7, DocesDias=7, RefrigeranteDias=7,
                  PeviRespostas=[0] * 15)


def aleatorio(rnd):
    """Sorteia uma resposta dentro da faixa de cada pergunta de dados.py,
    deixando algumas sem responder."""
    p = perfil(
        Idade=rnd.randint(8, 70), Sexo=rnd.choice("MF"),
        TempoParaComer=rnd.randint(1, 180), TempoDeSono=rnd.uniform(3, 13),
        HoraQueDorme=rnd.randint(0, 23), HoraQueAcorda=rnd.randint(0, 23),
        TempoAtividadeFisica=rnd.randint(0, 180),
        TempoExercicioFisico=rnd.randint(0, 180),
        TipoExercicio1=rnd.randint(0, 10), TipoExercicio2=rnd.randint(0, 10),
        TipoExercicio3=rnd.randint(0, 10),
        FrequenciaExercicio=rnd.randint(0, 7),
        IntensidadeExercicio=rnd.randint(1, 3),
        HorarioCafe=rnd.randint(0, 23), HorarioAlmoco=rnd.randint(0, 23),
        HorarioJantar=rnd.randint(0, 23),
        DoresArticulacoes=rnd.randint(0, 5), DoresMusculares=rnd.randint(0, 5),
        TempoDeTela=rnd.uniform(0, 16),
        IpaqDias=rnd.randint(0, 7), IpaqMinutos=rnd.randint(0, 180),
        FrutasDias=rnd.randint(0, 7), VerdurasDias=rnd.randint(0, 7),
        SalgadinhosDias=rnd.randint(0, 7), DocesDias=rnd.randint(0, 7),
        RefrigeranteDias=rnd.randint(0, 7),
        PeviRespostas=[rnd.randint(0, 3) for _ in range(15)])
    vazio = rec.criar_perfil(DadosVazio)
    for chave in rnd.sample(sorted(p), rnd.randint(0, 8)):
        p[chave] = vazio[chave]
    return p


def ids(p):
    return [r["id"] for r in rec.gerar_recomendacoes(p)]


# ---------------------------------------------------------------------------

def teste_perfil_sem_respostas_nao_gera_nada_e_nao_quebra():
    for p in ({}, rec.criar_perfil(DadosVazio), {"Idade": "x", "Sexo": None}):
        assert rec.gerar_recomendacoes(p) == []
        assert rec.pontos_fortes(p) == []
        texto = rec.formatar(p)
        # Sem resposta nenhuma, o texto diz isso: não finge que está tudo bem.
        assert "Nenhuma resposta foi registrada" in texto
        assert "não deu para avaliar" in texto
        assert len(rec.nao_avaliado(p)) == 8


def teste_perfis_sorteados_nunca_quebram_e_cobrem_todas_as_regras():
    rnd = random.Random(2026)
    vistas = set()
    for _ in range(5000):
        p = aleatorio(rnd)
        for r in rec.gerar_recomendacoes(p):
            vistas.add(r["id"])
            assert r["texto"] and r["motivo"] and r["fonte"], r["id"]
            assert r["alternativas"], "sem alternativas: " + r["id"]
        texto = rec.formatar(p)
        for palavra in PROIBIDAS:
            assert palavra not in texto.lower(), palavra
    faltando = {r["id"] for r in rec.RECOMENDACOES} - vistas
    assert not faltando, "regras que nunca dispararam: %s" % faltando


def teste_quem_cumpre_tudo_nao_recebe_recomendacao():
    p = ativo()
    assert ids(p) == [], ids(p)
    assert len(rec.pontos_fortes(p)) == 9
    texto = rec.formatar(p)
    assert rec.nao_avaliado(p) == [] and "não deu para avaliar" not in texto
    assert "PELAS SUAS RESPOSTAS" in texto
    assert "futebol/futsal, musculação" in texto


def teste_sono_implausivel_nao_e_avaliado():
    # Quem digita 8 na pergunta em minutos fica com 0,13 hora em dados.py.
    p = perfil(TempoDeSono=8 / 60)
    assert rec.horas_de_sono(p) is None and ids(p) == []
    assert "minutos" in rec.avisos(p)[0] and "0,1 horas" not in rec.formatar(p)
    assert "sono" in rec.nao_avaliado(p)
    assert rec.avisos(perfil(TempoDeSono=7)) == []


def teste_sem_resposta_sobre_dor_ninguem_e_mandado_acelerar():
    base = dict(IntensidadeExercicio=1, FrequenciaExercicio=3,
                TempoAtividadeFisica=70)
    assert "atividade_intensidade" not in ids(perfil(**base))
    assert "atividade_intensidade" not in ids(
        perfil(DoresArticulacoes=0, **base))
    assert "atividade_intensidade" in ids(
        perfil(DoresArticulacoes=0, DoresMusculares=0, **base))


def teste_com_dor_a_alternativa_de_forca_passa_pelo_professor():
    base = dict(FrequenciaExercicio=1, TempoAtividadeFisica=40)
    for dor in (dict(DoresArticulacoes=2), dict(DoresMusculares=2)):
        r = [x for x in rec.gerar_recomendacoes(perfil(**base, **dor))
             if x["id"] == "atividade_frequencia"][0]
        junto = " ".join(r["alternativas"])
        assert "peso do próprio corpo" not in junto and "professor" in junto
    r = [x for x in rec.gerar_recomendacoes(perfil(**base))
         if x["id"] == "atividade_frequencia"][0]
    assert "peso do próprio corpo" in " ".join(r["alternativas"])


def teste_ligacao_com_o_dados_py_de_verdade():
    # Os nomes do perfil são exatamente as variáveis do dados.py real.
    # (TABELA_EXERCICIOS é só o texto da tabela, não uma resposta.)
    reais = {n for n, v in vars(dados).items()
             if n[0].isupper() and not callable(v)
             and n not in ("TABELA_EXERCICIOS", "PEVI_AFIRMACOES",
                           "PEVI_ESCALA")}
    assert reais == set(rec.VARIAVEIS), reais ^ set(rec.VARIAVEIS)
    # Contrato entre os dois arquivos: com o dados.py recém-aberto, nenhuma
    # das 23 variáveis conta como respondida (0 em umas, -1 em outras).
    novo = rec.criar_perfil(dados)
    assert [n for n in rec.VARIAVEIS if rec.respondido(novo, n)] == []
    # As duas linhas do README, com respostas colocadas no módulo.
    antes = {n: getattr(dados, n) for n in rec.VARIAVEIS}
    try:
        dados.Idade, dados.TempoDeTela, dados.TempoDeSono = 16, 6, 6.5
        dados.DoresArticulacoes, dados.DoresMusculares = 2, 0
        p = rec.criar_perfil(dados)
        texto = rec.formatar(p)
        assert ids(p) == ["dor_adaptar", "tela_reduzir", "sono_aumentar",
                          "sono_telas"], ids(p)
        assert "Idade: 16 anos" in texto and "Dor: joelho" in texto
    finally:
        for nome, valor in antes.items():
            setattr(dados, nome, valor)
    assert rec.gerar_recomendacoes(rec.criar_perfil(dados)) == []


def teste_quem_tem_tudo_a_melhorar():
    p = parado()
    assert ids(p) == [
        "dor_adaptar", "atividade_comecar", "tela_reduzir", "sono_aumentar",
        "sono_telas", "refrigerante", "comer_com_calma", "frutas_verduras",
        "salgadinhos", "doces", "pevi_estresse", "pevi_relacionamentos",
    ], ids(p)


def teste_ninguem_ativo_ouve_comece_do_zero():
    # Pouca atividade "por dia", mas treina 5 vezes por semana por 90 min:
    # vale o maior dos dois, então não é caso de "começar".
    p = perfil(TempoAtividadeFisica=5, TempoExercicioFisico=90,
               FrequenciaExercicio=5)
    assert round(rec.minutos_ativos_por_dia(p)) == 64
    assert "atividade_comecar" not in ids(p)
    # O mesmo vale para o IPAQ: 5 dias de 60 minutos dão 43 minutos por dia.
    p = perfil(TempoAtividadeFisica=5, IpaqDias=5, IpaqMinutos=60)
    assert round(rec.minutos_ativos_por_dia(p)) == 43
    assert ids(p) == ["atividade_aumentar"], ids(p)
    rnd = random.Random(3)
    for _ in range(3000):
        p = aleatorio(rnd)
        minutos = rec.minutos_ativos_por_dia(p)
        if minutos is not None and minutos >= 30:
            assert "atividade_comecar" not in ids(p)
        if minutos is not None and minutos >= 60:
            assert "atividade_aumentar" not in ids(p)


def teste_todas_as_36_combinacoes_de_dor():
    for articulacao, muscular in itertools.product(range(6), range(6)):
        p = parado()
        p.update(DoresArticulacoes=articulacao, DoresMusculares=muscular,
                 TipoExercicio1=3, TipoExercicio2=9, TipoExercicio3=2,
                 FrequenciaExercicio=1, TempoAtividadeFisica=40)
        excluidos = rec.exercicios_excluidos(p)
        sobra = [c for c in rec.TIPOS_EXERCICIO if c not in excluidos]
        assert len(sobra) >= 2 and 4 in sobra, (articulacao, muscular)
        recomendacoes = rec.gerar_recomendacoes(p)
        assert ("dor_adaptar" in [r["id"] for r in recomendacoes]) == bool(
            articulacao or muscular)
        for r in recomendacoes:
            if r["id"] == "dor_adaptar":
                continue     # é a única que nomeia o que ficou de fora
            junto = (r["texto"] + " " + " ".join(r["alternativas"])).lower()
            for codigo in excluidos:
                assert PALAVRA[codigo] not in junto, (r["id"], codigo)
            if rec.so_caminhada(p):
                assert "corrida" not in junto, r["id"]


def teste_dor_no_joelho_tira_impacto_e_nao_manda_largar_o_esporte():
    p = perfil(DoresArticulacoes=2, DoresMusculares=0, TipoExercicio1=3,
               TempoAtividadeFisica=20)
    assert rec.exercicios_excluidos(p) == {2, 3, 6, 9, 10}
    # Toda dor em articulação tira os mesmos exercícios de impacto e carga.
    for codigo in rec.DORES_ARTICULACOES:
        assert rec.exercicios_excluidos(
            perfil(DoresArticulacoes=codigo)) == {2, 3, 6, 9, 10}
    assert rec.nome_exercicio(p, 1) == "Caminhada"
    sugeridos = rec.sugerir_exercicios(p, 10)
    assert "Futebol/futsal" not in sugeridos and "Natação" in sugeridos
    dor = [r for r in rec.gerar_recomendacoes(p) if r["id"] == "dor_adaptar"][0]
    assert "não precisa abandonar" in dor["texto"]
    assert "futebol/futsal" in dor["motivo"]
    # Com dor relatada, ninguém é mandado aumentar a intensidade.
    p.update(IntensidadeExercicio=1, FrequenciaExercicio=3)
    assert "atividade_intensidade" not in ids(p)


def teste_valor_inicial_de_dados_py_nao_vira_resposta():
    # Em dados.py, 0 é "não respondido" para sono e -1 para tela.
    p = perfil(TempoDeSono=0, TempoDeTela=-1, TempoParaComer=0)
    assert ids(p) == []
    # Zero minutos de atividade é resposta de verdade.
    assert ids(perfil(TempoAtividadeFisica=0)) == ["atividade_comecar"]
    # Sem TempoDeSono, o sono sai da hora de dormir e de acordar.
    p = perfil(HoraQueDorme=23, HoraQueAcorda=6)
    assert rec.horas_de_sono(p) == 7 and ids(p) == ["sono_aumentar"]
    # Meia-noite (0) é resposta de verdade para a hora de dormir.
    assert rec.horas_de_sono(perfil(HoraQueDorme=0, HoraQueAcorda=7)) == 7
    assert rec.horas_de_sono(perfil(HoraQueDorme=0)) is None


def teste_idade_fora_da_adolescencia_vira_aviso():
    assert rec.avisos(perfil(Idade=16)) == []
    assert rec.avisos(perfil()) == []
    for idade in (8, 25, 70):
        assert "adolescentes" in rec.avisos(perfil(Idade=idade))[0]
        assert "ATENÇÃO:" in rec.formatar(perfil(Idade=idade))


def teste_toda_fonte_citada_tem_referencia_completa():
    for regra in rec.RECOMENDACOES:
        fonte = regra["fonte"]
        resto = re.sub(re.escape(rec.CRITERIO) + r" \([^)]*\)", "", fonte)
        for citacao in rec.REFERENCIAS:
            resto = resto.replace(citacao, "")
        assert not resto.strip("; "), (regra["id"], resto)
    texto = rec.formatar(parado())
    for citacao, completa in rec.REFERENCIAS.items():
        citada = any(citacao in r["fonte"] for r in rec.gerar_recomendacoes(parado()))
        if citada:
            assert completa.split(".")[0] in texto.replace("\n    ", " "), citacao


def teste_o_contrato_de_criar_recomendacao_continua_valendo():
    # Os seis campos originais, na mesma ordem, e os dois novos opcionais.
    r = rec.criar_recomendacao("x", "sono", lambda p: True, "t", "m")
    assert [r[k] for k in ("id", "categoria", "texto", "motivo", "fonte")] == [
        "x", "sono", "t", "m", ""]
    assert r["condicao"]({}) is True
    assert r["alternativas"] == () and r["prioridade"] == 5
    assert set(rec.VARIAVEIS) == {n for n in vars(DadosVazio)
                                  if not n.startswith("_")}


# ---------------------------------------------------------------------------
# Os três questionários: IPAQ, Saúde na Boa e PEVI
# ---------------------------------------------------------------------------

def teste_saude_na_boa_dispara_pelos_dias_da_semana():
    assert ids(perfil(RefrigeranteDias=3)) == ["refrigerante"]
    assert ids(perfil(RefrigeranteDias=2)) == []
    assert ids(perfil(FrutasDias=4, VerdurasDias=7)) == ["frutas_verduras"]
    assert ids(perfil(FrutasDias=5, VerdurasDias=5)) == []
    assert ids(perfil(SalgadinhosDias=3)) == ["salgadinhos"]
    assert ids(perfil(DocesDias=4)) == ["doces"]
    assert ids(perfil(DocesDias=3)) == []
    # Só uma das duas respondida: a recomendação mostra "?" na que falta.
    r = rec.gerar_recomendacoes(perfil(FrutasDias=1))[0]
    assert "frutas em 1 e verduras em ?" in r["motivo"]


def teste_pevi_usa_a_media_de_cada_componente():
    bom = [3] * 15
    assert ids(perfil(PeviRespostas=bom)) == []
    # Estresse = as três últimas afirmações; relacionamentos = 10 a 12.
    estresse = bom[:12] + [1, 1, 2]                    # média 1,33
    assert ids(perfil(PeviRespostas=estresse)) == ["pevi_estresse"]
    relacoes = bom[:9] + [0, 2, 2] + bom[12:]          # média 1,33
    assert ids(perfil(PeviRespostas=relacoes)) == ["pevi_relacionamentos"]
    no_corte = bom[:12] + [1, 2, 2]                    # média 1,67
    assert ids(perfil(PeviRespostas=no_corte)) == []
    medias = rec.pevi_medias(perfil(PeviRespostas=estresse))
    assert list(medias) == list(rec.PEVI_COMPONENTES)
    assert abs(medias["controle do estresse"] - 4 / 3) < 0.001
    # A afirmação sobre cigarro e álcool (a 8a) não gera recomendação.
    so_a_oitava = bom[:7] + [0] + bom[8:]
    assert ids(perfil(PeviRespostas=so_a_oitava)) == []


def teste_pevi_incompleto_ou_invalido_nao_conta_como_respondido():
    for invalido in ([], [1, 2, 3], [4] * 15, ["2"] * 15, [True] * 15, None):
        p = perfil(PeviRespostas=invalido)
        assert not rec.respondido(p, "PeviRespostas"), invalido
        assert rec.pevi_medias(p) is None and ids(p) == []
    # O perfil guarda uma cópia: mexer no original não muda o perfil.
    class Copia(DadosVazio):
        PeviRespostas = [2] * 15
    p = rec.criar_perfil(Copia)
    Copia.PeviRespostas.append(9)
    assert len(p["PeviRespostas"]) == 15


def teste_ipaq_reduzido_da_minutos_e_nunca_classificacao():
    p = perfil(IpaqDias=3, IpaqMinutos=40)
    assert rec.ipaq_minutos_semana(p) == 120
    assert rec.ipaq_minutos_semana(perfil(IpaqDias=3)) is None
    texto = rec.formatar(p)
    assert "120 minutos de atividade na semana" in texto
    assert "versão reduzida" in texto and "CRAIG, C. L." in texto
    for categoria in ("Sedentário", "Irregularmente ativo", "Muito ativo"):
        assert categoria not in texto, categoria


def teste_texto_diz_o_que_foi_reduzido_ou_adaptado():
    texto = rec.formatar(parado())
    assert "SOBRE OS QUESTIONÁRIOS" in texto
    assert "Três foram adaptadas" in texto and "critérios do projeto" in texto
    assert "SOBRE OS QUESTIONÁRIOS" not in rec.formatar(perfil(TempoDeTela=5))
    # As novas categorias aparecem depois de telas e sono.
    posicoes = [texto.index(t) for t in ("SEDENTARISMO E TELAS", ". SONO",
                                         ". ALIMENTAÇÃO", ". BEM-ESTAR")]
    assert posicoes == sorted(posicoes), posicoes


if __name__ == "__main__":
    testes = [(n, f) for n, f in sorted(globals().items())
              if n.startswith("teste_") and callable(f)]
    falhas = 0
    for nome, funcao in testes:
        try:
            funcao()
            print("ok    ", nome)
        except Exception as erro:            # mostra e segue para o próximo
            falhas += 1
            print("FALHOU", nome, "->", type(erro).__name__, erro)
    print("\n%d teste(s), %d falha(s)" % (len(testes), falhas))
    sys.exit(1 if falhas else 0)
