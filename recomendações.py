#RECOMENDAÇÔES
def gerar_recomendacoes(ipaq, alimentacao, pevi):
    recomendacoes = []

#atividade física
if ipaq["minutos_semana"] < 150:
    recomendacoes.append(
        " É recomendado aumentar a prática de atividade física para pelo menos 150 minutos por semana," \
        "conforme as diretrizes da Organização Mundial da Saúde (OMS)." \
        "Como podemos ver é na semana, então voce pode praticar AF por curtos periodos de tempo," \
        "nos dias em que voce não tem tanto tempo assim deixando acumular para os dias que voce tem mais tempo livre, " \
        "mas é importante que voce pratique, no minímo, 3 dias semanais." \
        )
else:
    recomendacoes.append(
        "Parabéns! Você está atingindo a recomendação mínima de atividade física semanal."
    )

if ipaq["dias_semana"] < 3:
    recomendacoes.append(
        " É recomendado praticar atividade física por pelo menos 3 dias por semana," \
        "conforme as diretrizes da Organização Mundial da Saúde (OMS)."
    )
else:
    recomendacoes.append(
        "Parabéns! Você está atingindo a recomendação mínima de dias de atividade física semanal."
    )

if alimentação["frutas_verduras"] :
    recomendacoes.append(
        " É recomendado consumir pelo menos 5 porções de frutas e verduras por dia,"
    )
else:
    recomendacoes.append(
        "Parabéns! Você está atingindo a recomendação mínima de frutas e verduras por dia."
    )

if pevi["Frutas_Verduras_diariamente"] < 7:
    recomendacoes.append(
        " É recomendado consumir frutas e verduras diariamente, conforme as diretrizes da Organização Mundial da Saúde (OMS)."
    )
else:
    recomendacoes.append(
        "Parabéns! Você está atingindo a recomendação mínima de frutas e verduras diariamente."
    )

if