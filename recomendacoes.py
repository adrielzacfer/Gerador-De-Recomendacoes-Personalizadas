def criar_recomendacao(id, categoria, condicao, texto, motivo, fonte=""):
    return {
        "id": id,
        "categoria": categoria,
        "condicao": condicao,
        "texto": texto,
        "motivo": motivo,
        "fonte": fonte,
    }
"""
    Cria uma regra de recomendação
    id: nome único da regra (ex.: "frutas_digestao")
    categoria: "atividade_fisica", "alimentacao", "sono", "sedentarismo"...
    condicao: função  perfil -> bool  (True = recomendação se aplica)
    texto: o que o usuário deve fazer
    motivo: por que isso ajuda (explicação para o usuário)
    fonte: referência do artigo que fundamenta a regra
"""
