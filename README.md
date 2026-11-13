# Gerador de Recomendações Personalizadas

Programa em Python, executado no terminal, que coleta informações sobre a rotina de adolescentes e gera **recomendações personalizadas** para reduzir o sedentarismo e promover hábitos de vida mais saudáveis, ajudando na prevenção de fatores associados à obesidade.

Projeto de pesquisa desenvolvido no **IFRS – Câmpus Rolante** (Curso Técnico em Informática), vinculado ao artigo *"A influência do sedentarismo na obesidade dos alunos do IFRS Campus Rolante"*.

> ⚠️ **Aviso:** este é um projeto educativo. A ferramenta **não tem finalidade diagnóstica**, não é clinicamente validada e não substitui a avaliação de médico, nutricionista ou profissional de educação física.

---

## Sobre o projeto

A obesidade é reconhecida pela OMS como uma epidemia global de Doença Crônica Não Transmissível (DCNT), e o sedentarismo é um de seus principais fatores modificáveis. Este projeto parte da seguinte pergunta de pesquisa:

> *Como um programa pode contribuir para a orientação de jovens de 15 e 16 anos no que diz respeito à obtenção de um estilo de vida saudável?*

**Hipótese:** um programa capaz de analisar a rotina de adolescentes de 15 a 16 anos, identificando práticas que precisam ser melhoradas e oferecendo recomendações adequadas a cada usuário, pode contribuir para uma rotina menos sedentária e para a prevenção de fatores ligados à obesidade.

**Público-alvo:** estudantes do 2º ano de Informática (turno matutino) do IFRS Câmpus Rolante.

---

## Como funciona

```
USUÁRIO
   ↓
QUESTIONÁRIO
   ↓
┌────────────┼────────────┐
↓            ↓            ↓
IPAQ     Saúde na Boa    PEVI
↓            ↓            ↓
atividade    alimentação  estilo de
física e     e hábitos    vida geral
sedentarismo
└────────────┼────────────┘
             ↓
     CLASSIFICAÇÕES
             ↓
  RECOMENDAÇÕES PERSONALIZADAS
```

1. **Coleta:** o usuário responde a um questionário no terminal.
2. **Classificação:** as respostas são analisadas segundo os critérios de três instrumentos científicos.
3. **Identificação:** o programa aponta os pontos da rotina que podem melhorar, com atenção especial à atividade física e ao comportamento sedentário.
4. **Recomendação:** um banco de recomendações é associado ao perfil, evitando sugestões genéricas.

### Adaptação às limitações do usuário

As recomendações levam em conta as condições informadas. Por exemplo, se o usuário relata dor no joelho, o programa **não recomenda exercícios de alto impacto**.

### Instrumentos utilizados

| Instrumento | Foco | O que avalia |
|---|---|---|
| **IPAQ** (Questionário Internacional de Atividade Física) | Atividade física e sedentarismo | Volume de atividade física diária/semanal e tempo sedentário |
| **Saúde na Boa** | Alimentação e hábitos | Hábitos alimentares e comportamentos saudáveis |
| **PEVI** (Perfil do Estilo de Vida Individual) | Estilo de vida geral | Nutrição, atividade física, comportamento preventivo, relacionamentos sociais e controle do estresse |

A alimentação foi mantida como aspecto secundário, devido à complexidade da realidade de cada usuário. O foco principal é o **sedentarismo**.

---

## Dados coletados

| Categoria | Variáveis |
|---|---|
| Perfil | idade, faixa etária, sexo, altura, peso, IMC |
| Sono | tempo de sono, horário em que dorme e acorda |
| Alimentação | tempo disponível para comer, horários de café, almoço e jantar |
| Atividade física | tempo de atividade física, tempo de exercício, até 3 tipos de exercício, frequência semanal (0 a 7) e intensidade (leve, moderada, intensa) |
| Saúde musculoesquelética | dores em articulações e dores musculares |
| Comportamento sedentário | tempo de tela (horas) |

Tipos de exercício reconhecidos: corrida e caminhada, musculação, futebol/futsal, alongamento, ciclismo, treinamento funcional, natação, pilates, vôlei/futevôlei e dança.

---

## Estrutura do repositório

```
Gerador-De-Recomendacoes-Personalizadas/
├── dados.py      # variáveis do perfil do usuário e funções de coleta/validação
├── funcoes.py    # protótipos dos módulos IPAQ, Saúde na Boa e PEVI
└── README.md
```

- **`dados.py`**: define todas as variáveis do perfil (com unidades e códigos de cada categoria) e as funções que coletam e validam cada resposta.
- **`funcoes.py`**: contém os protótipos dos três módulos de avaliação:
  - `ipaq()`: calcula os minutos semanais de atividade física (dias × minutos por dia);
  - `alimentacao()`: calcula o percentual da semana com consumo de frutas;
  - `pevi()`: aplica 15 perguntas em 5 dimensões, com respostas de 0 (nunca) a 3 (sempre), totalizando até 45 pontos.

---

## Como executar

**Requisitos:** Python 3.10 ou superior (sem dependências externas).

```bash
git clone https://github.com/<seu-usuario>/Gerador-De-Recomendacoes-Personalizadas.git
cd Gerador-De-Recomendacoes-Personalizadas
python funcoes.py
```

---

## Status do desenvolvimento

🚧 **Em desenvolvimento.**

- [x] Definição das variáveis e unidades de medida
- [x] Protótipos dos módulos IPAQ, Saúde na Boa e PEVI
- [ ] Finalizar a coleta e a validação das respostas
- [ ] Implementar a classificação conforme os critérios de cada instrumento
- [ ] Montar o banco de recomendações com base em artigos científicos
- [ ] Implementar as regras de personalização (limitações físicas, rotina, nível de atividade)
- [ ] Interface final de terminal com o fluxo completo
- [ ] Testes com perfis de exemplo

---

## Fundamentação científica

As perguntas e os critérios de classificação são adaptados de instrumentos estudados e validados para a população brasileira:

- **IPAQ (versão brasileira):** [estudo de validação](https://rbafs.org.br/RBAFS/article/view/931)
- **Saúde na Boa:** [estudo de reprodutibilidade e validade](https://rbafs.org.br/RBAFS/article/view/817)
- **PEVI:** [estudo de validação](https://rbafs.org.br/RBAFS/article/view/778)

Outras referências:

- Organização Mundial da Saúde (OMS). [*Obesity and overweight*](https://www.who.int/news-room/fact-sheets/detail/obesity-and-overweight).
- Organização Mundial da Saúde (OMS). [*Physical activity*](https://www.who.int/news-room/fact-sheets/detail/physical-activity).
- ABESO. *Diretrizes brasileiras de obesidade 2016*. 4. ed. São Paulo: ABESO, 2016.
- PALMA, A. Exercício físico e saúde; sedentarismo e doença: epidemia, causalidade e moralidade. *Motriz – Revista de Educação Física*, 2009.
- FIGUEIREDO, A. E. B.; CECCON, R. F.; FIGUEIREDO, J. H. C. Doenças crônicas não transmissíveis e suas implicações na vida de idosos dependentes. *Ciência & Saúde Coletiva*, v. 26, 2021.

### Limites metodológicos

Os resultados são **descritivos**. O que se fundamenta na literatura são as variáveis e a forma de avaliação adotadas; o programa não afirma que seus resultados em si foram validados cientificamente.

---

## Autores

Estudantes do Curso Técnico em Informática, IFRS – Câmpus Rolante.

<!-- Adicione aqui os nomes e links dos perfis dos integrantes -->

---

## Licença

A definir.
