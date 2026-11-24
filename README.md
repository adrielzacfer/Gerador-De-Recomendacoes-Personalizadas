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
| IPAQ (versão reduzida) | dias de atividade física na semana e minutos por dia |
| Saúde na Boa | dias por semana com frutas, verduras, salgadinhos, doces e refrigerante |
| PEVI | 15 respostas de 0 a 3, em 5 componentes |

Tipos de exercício reconhecidos: corrida e caminhada, musculação, futebol/futsal, alongamento, ciclismo, treinamento funcional, natação, pilates, vôlei/futevôlei e dança.

---

## Estrutura do repositório

```
Gerador-De-Recomendacoes-Personalizadas/
├── dados.py                  # variáveis do perfil, perguntas e o programa principal
├── recomendacoes.py          # banco de recomendações personalizadas
├── testes_recomendacoes.py   # testes do banco de recomendações
└── README.md
```

- **`dados.py`**: define todas as variáveis do perfil (com unidades e códigos de cada categoria) e as funções que coletam e validam cada resposta. A função `responder_tudo()` faz as perguntas na ordem, e rodar o arquivo mostra a introdução, as perguntas e as recomendações.
- No fim do `dados.py` ficam os três questionários, que guardam as respostas e são chamados depois das perguntas do perfil:
  - `ipaq()`: versão reduzida do IPAQ, com dias de atividade na semana e minutos por dia; calcula os minutos semanais;
  - `alimentacao()`: cinco perguntas do Saúde na Boa, em dias por semana (frutas, verduras, salgadinhos, doces e refrigerante);
  - `pevi()`: as 15 afirmações do PEVI em 5 componentes, com respostas de 0 a 3, totalizando até 45 pontos.

---

## Recomendações personalizadas

O banco de recomendações fica em `recomendacoes.py`. Ele usa os mesmos nomes das variáveis de `dados.py` e não altera as perguntas.

```python
import dados
import recomendacoes

perfil = recomendacoes.criar_perfil(dados)   # lê as variáveis de dados.py
print(recomendacoes.formatar(perfil))        # texto pronto para mostrar
```

Cada recomendação é criada com `criar_recomendacao` e tem:

| Campo | O que é |
|---|---|
| `condicao` | função que recebe o perfil e diz se a recomendação vale para a pessoa |
| `texto` | o que fazer, com uma meta pequena |
| `motivo` | por que isso ajuda, com o resultado do estudo e em quem ele foi feito |
| `fonte` | a referência do estudo, ou "Critério do projeto" quando o corte é nosso |
| `alternativas` | o que fazer se o caminho principal não servir |

Hoje o banco tem 16 recomendações, que usam estas respostas. O total de minutos do IPAQ entra na conta dos minutos de atividade por dia, junto com as perguntas do perfil.

| Recomendação | Resposta que dispara |
|---|---|
| Adaptar a atividade à dor | `DoresArticulacoes` ou `DoresMusculares` diferente de 0 |
| Começar a se mexer | menos de 30 minutos de atividade por dia |
| Chegar aos 60 minutos por dia | de 30 a 59 minutos de atividade por dia |
| Exercício em 3 dias da semana, com força | `FrequenciaExercicio` abaixo de 3, para quem já faz 30 minutos ou mais por dia |
| Subir a intensidade | `IntensidadeExercicio` leve, com as duas perguntas de dor respondidas "nenhuma" |
| Reduzir o tempo de tela | `TempoDeTela` acima de 3 horas |
| Dormir mais | menos de 8 horas de sono |
| Tirar as telas da hora de dormir | muita tela e pouco sono ao mesmo tempo |
| Observar o sono longo | mais de 10 horas de sono |
| Comer com calma | `TempoParaComer` abaixo de 45 minutos no dia |
| Trocar refrigerante por água | `RefrigeranteDias` de 3 ou mais (Saúde na Boa) |
| Mais dias com frutas e verduras | `FrutasDias` ou `VerdurasDias` abaixo de 5 (Saúde na Boa) |
| Menos salgadinhos | `SalgadinhosDias` de 3 ou mais (Saúde na Boa) |
| Doces em dias combinados | `DocesDias` de 4 ou mais (Saúde na Boa) |
| Tempo diário para relaxar | média do componente "controle do estresse" do PEVI abaixo de 1,5 |
| Atividades em grupo | média do componente "relacionamentos" do PEVI abaixo de 1,5 |

**Filtro por dor.** Para cada dor relatada, alguns dos dez tipos de exercício deixam de ser sugeridos. Com dor em qualquer articulação (joelho, coluna, quadril, artrite, artrose) saem os exercícios de impacto e de carga: futebol, vôlei, treinamento funcional, musculação e dança, e a corrida vira caminhada. Cada dor muscular tira os exercícios que mais exigem daquela região. Alongamento e pilates nunca saem. É uma regra de precaução do projeto, não um tratamento, e vale ser revisada pelo orientador de Educação Física. Quem já pratica um esporte que saiu da lista é orientado a adaptar com o professor, não a largar.

**O texto gerado** começa com as respostas da pessoa e diz quais temas ficaram sem avaliação por falta de resposta. Assim, um perfil com poucas respostas não parece "tudo certo".

**Limites.**

- Os minutos de atividade por dia são o maior valor entre `TempoAtividadeFisica` e a média semanal de `TempoExercicioFisico` vezes `FrequenciaExercicio`. É um critério do projeto.
- Os cortes de 30 minutos de atividade e de 45 minutos para comer são critérios do projeto. Os de 60 minutos de atividade, 8 a 10 horas de sono e 2 a 3 horas de tela vêm das fontes citadas.
- A alimentação é avaliada por frequência: em quantos dias da semana a pessoa come frutas, verduras, doces e salgadinhos e toma refrigerante. O programa não pergunta quantidade nem monta cardápio. Os cortes em dias por semana (3, 4 ou 5 dias) são critérios do projeto, assim como o corte de 1,5 na média de cada componente do PEVI.
- Não há recomendação sobre IMC nem sobre os horários das refeições. Para adolescentes o IMC precisa ser comparado por idade e sexo, e não encontramos fonte conferida para os horários.
- Os três questionários entram em versões adaptadas, e o programa diz isso no próprio texto que gera. O IPAQ tem só duas perguntas (dias e minutos), então dá o total de minutos na semana e não a classificação oficial; ele foi validado em adultos de 18 a 65 anos. Do Saúde na Boa entram cinco perguntas de alimentação, com a redação do questionário. O PEVI entra com as 15 afirmações do instrumento, três delas adaptadas para adolescentes (álcool, trânsito e trabalho/estudos); a redação original está nos comentários do `dados.py`.
- As dicas práticas são orientação de bom senso. A referência de cada recomendação sustenta o motivo, não cada dica.

Para conferir que nada quebrou depois de uma mudança:

```bash
python testes_recomendacoes.py
```

---

## Como executar

**Requisitos:** Python 3.10 ou superior (sem dependências externas).

```bash
git clone https://github.com/<seu-usuario>/Gerador-De-Recomendacoes-Personalizadas.git
cd Gerador-De-Recomendacoes-Personalizadas
python dados.py
```

---

## Status do desenvolvimento

🚧 **Em desenvolvimento.**

- [x] Definição das variáveis e unidades de medida
- [x] Protótipos dos módulos IPAQ, Saúde na Boa e PEVI
- [x] Finalizar a coleta e a validação das respostas do perfil e dos três questionários
- [ ] Implementar a classificação oficial do IPAQ (exige separar caminhada, atividade moderada e vigorosa; hoje o programa só soma os minutos da semana)
- [x] Montar o banco de recomendações com base em artigos científicos
- [x] Implementar as regras de personalização (limitações físicas, rotina, nível de atividade)
- [x] Fluxo completo no terminal (`python dados.py`): introdução, perguntas e recomendações
- [x] Guardar as respostas de IPAQ (versão reduzida), Saúde na Boa e PEVI e usá-las nas recomendações
- [x] Testes do banco de recomendações com perfis de exemplo

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
