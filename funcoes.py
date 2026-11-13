# IPAQ: calcula o tempo semanal de atividade física
def ipaq():
    dias = int(input("Dias de atividade física por semana: "))
    minutos = int(input("Minutos de atividade por dia: "))

    total = dias * minutos

    print("Atividade física semanal:", total, "minutos")

   # encontrar artigos relacionados a *minutos de atividade fisica por semana.* Relacionar conteudo dos artigos com as saidas e a importancia do IPAC.


# Saúde na Boa: calcula a frequência de consumo de alimentos
def alimentacao():
    dias = int(input("Dias de consumo de frutas por semana: "))

    percentual = (dias / 7) * 100

    print("Consumo de frutas:", percentual , "% da semana")
    # encontrar artigos relacionados a *consumo de frutas semanal* e seu impacto no desenvolvimento de obesidade. 


# PEVI: avalia o estilo de vida do usuário
def pevi():

    perguntas = [
        # Nutrição
        "Você consome frutas e verduras diariamente?",
        "Você evita alimentos gordurosos?",
        "Você costuma fazer de 4 a 5 refeições por dia?",

        # Atividade física
        "Você pratica atividades físicas regularmente?",
        "Você realiza exercícios de força ou alongamento?",
        "Você caminha ou pedala como forma de transporte?",

        # Comportamento preventivo
        "Você conhece e respeita as normas de trânsito?",
        "Você evita fumar e consumir álcool?",
        "Você costuma usar protetor solar?",

        # Relacionamentos sociais
        "Você procura manter amizades e relacionamentos positivos?",
        "Você participa de atividades em grupo?",
        "Você procura ajudar outras pessoas?",

        # Controle do estresse
        "Você reserva tempo para relaxar?",
        "Você consegue manter a calma diante de dificuldades?",
        "Você procura equilibrar trabalho, estudo e lazer?"
    ]

    total = 0

    for pergunta in perguntas:
        print("\n" + pergunta)
        resposta = int(input("Responda de 0 (nunca) a 3 (sempre): "))
        total += resposta

    print("\nPontuação total do PEVI:", total, "/ 45")
    # encontrar artigos relacionados ao PEVI e sua importancia para entender as causas do desenvolvimento de obesidade.

def introducao(): # Função que gera uma mensagem de boas vindas, explicando o codigo.
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
