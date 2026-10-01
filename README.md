# Simulador de Rotina Saudável

Simulador em Python que recebe o perfil de rotina de uma pessoa com obesidade (atividade física, alimentação e estilo de vida) e gera **recomendações personalizadas** de rotina, alimentação e atividade física. O usuário também pode testar cenários ("e se eu praticasse atividade física 5 dias por semana?") e comparar os resultados.

> ⚠️ **Aviso:** este é um projeto educativo. Ele **não é um instrumento de diagnóstico** nem uma ferramenta clinicamente validada, e não substitui a avaliação de médico, nutricionista ou profissional de educação física.

---

## Como funciona

```
USUÁRIO
   ↓
QUESTIONÁRIO
   ↓
┌──────────┼──────────┐
↓          ↓          ↓
IPAQ   Saúde na Boa   PEVI
↓          ↓          ↓
atividade  alimentação  estilo de
física +   + hábitos    vida geral
sedentário
└──────────┼──────────┘
           ↓
   PERFIL DA ROTINA
           ↓
   RECOMENDAÇÕES PERSONALIZADAS
           ↓
   SIMULAÇÃO DE MUDANÇA
           ↓
   COMPARAÇÃO DOS RESULTADOS
```

O simulador **não gera uma nota única de saúde**. Cada metodologia avalia um aspecto da rotina e os resultados são mostrados separados:

| Módulo | Baseado em | Saída |
|---|---|---|
| Atividade física e sedentarismo | IPAQ | minutos de atividade por semana, frequência semanal e tempo sedentário |
| Alimentação e hábitos | Saúde na Boa | indicadores separados dos hábitos alimentares |
| Estilo de vida geral | PEVI | perfil por dimensão (alimentação, atividade física, comportamento preventivo, relacionamentos, controle do estresse) |

---

## Estrutura do projeto

```
simulador/
├── main.py             # interface e gerenciamento do fluxo
├── calculos.py         # cálculos dos indicadores e comparação de cenários
├── recomendacoes.py    # banco de recomendações e adequação ao perfil
└── modelos.py          # dataclasses e constantes (limiares, categorias)
```

- **`main.py`**: coleta as respostas, chama as demais funções, exibe os resultados e oferece o menu de simulação. É o único arquivo com entrada e saída (`input`/`print`).
- **`calculos.py`**: funções que transformam respostas em indicadores, preservando os indicadores originais dos instrumentos sempre que possível.
- **`recomendacoes.py`**: regras que associam características do perfil a recomendações, com linguagem adequada ao público.
- **`modelos.py`**: estrutura do perfil do usuário e constantes, como a meta de 150 minutos semanais de atividade física.

---

## Como executar

Requisitos: Python 3.10 ou superior.

```bash
git clone <url-do-repositorio>
cd simulador
python main.py
```

---

## Fundamentação científica

As perguntas e variáveis são adaptadas de instrumentos previamente estudados e validados para a população brasileira:

- **IPAQ** (versão brasileira): [estudo de validação](https://rbafs.org.br/RBAFS/article/view/931)
- **Saúde na Boa**: [estudo de reprodutibilidade e validade](https://rbafs.org.br/RBAFS/article/view/817)
- **PEVI** (Perfil do Estilo de Vida Individual): [estudo de validação](https://rbafs.org.br/RBAFS/article/view/778)

**Limites metodológicos:** as pontuações dos três instrumentos não são combinadas, e o simulador não afirma que seus resultados foram validados cientificamente. O que se fundamenta na literatura são as variáveis e a forma de avaliação adotadas; os resultados são descritivos, e a simulação de cenários mostra como os indicadores mudariam se os valores informados fossem diferentes.

---

## Status

🚧 Em desenvolvimento.

- [ ] Definir e adaptar as perguntas de cada módulo
- [ ] Implementar os cálculos em `calculos.py`
- [ ] Montar o banco de recomendações
- [ ] Implementar a interface e o modo de simulação
- [ ] Testar com perfis de exemplo

---

## Licença

A definir.
