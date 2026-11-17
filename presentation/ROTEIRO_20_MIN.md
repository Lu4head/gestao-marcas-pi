# Roteiro de apresentação — 20 minutos

Dois apresentadores, identificados como **Apresentador 1** e **Apresentador 2**. Os nomes serão associados pela equipe. Preparar mais dez minutos para defesa técnica. Abrir o painel e testar os dois modos antes de começar; manter `docs/demo_ml.json` como evidência complementar caso a interface falhe.

| Tempo | Slide | Apresentador | Tema |
|---|---:|---|---|
| 00:00–00:30 | 1 | 1 | Identificação e objetivo |
| 00:30–02:00 | 2 | 1 | Problema |
| 02:00–03:30 | 3 | 1 | Arquitetura completa e recorte local |
| 03:30–05:00 | 4 | 1 | IA clássica |
| 05:00–06:00 | 5 | 1 | Contrato de integração |
| 06:00–08:00 | 6 | 2 | Dados e treinamento |
| 08:00–10:30 | 7, painel | 1 | Demonstração: datas, fatos e risco |
| 10:30–13:00 | 7, painel | 2 | Demonstração: fallback e revisão |
| 13:00–14:30 | 8 | 2 | Modelos e métricas |
| 14:30–16:00 | 9 | 2 | Matriz de confusão e limiar |
| 16:00–18:00 | 10 | 1 | Limitações e ética |
| 18:00–20:00 | 11 | 2 | Próximos passos |

## Fala-base e pontos de domínio

### Slides 1 e 2 — problema (2 min)

“Nosso projeto atual trata da organização de prazos de marcas. A consulta à RPI e a conferência das datas continuam humanas. O desafio é ordenar providências e explicar por que cada uma merece atenção. Datas identificam urgências objetivas; uma estimativa estatística pode antecipar risco antes da urgência. O protótipo combina essas informações em uma fila auditável.”

Explicar que o Marco 2 descrevia arquitetura e que agora existe implementação independente. O tema anterior de entregas foi abandonado; não reaproveitamos suas métricas. Destacar dados sintéticos logo no início.

### Slide 3 — arquitetura (1 min 30 s)

Explicar entrada humana, interface, validação e armazenamento como base; snapshot t0, inferência e regras como caminho de priorização; painel e decisão humana como saída; treino offline como fluxo separado. No MVP, CSV/objetos substituem persistência de produção e Streamlit reúne interface e painel. Não existe integração com o WebSystem nesta entrega.

### Slide 4 — IA clássica (1 min 30 s)

“A memória inicia com fatos operacionais. Uma regra deriva prazo aberto; outra pode derivar risco acima do limiar; isso habilita uma regra posterior que deriva candidato ALTO. Repetimos a agenda até não surgir um fato novo. Depois aplicamos a precedência. Concluídos saem; vencido e urgente sempre prevalecem sobre o ML.”

Mostrar que ausência e risco ficam nos motivos mesmo quando a data define VENCIDO. A agenda e os ciclos são a evidência de encadeamento, que será aberta no painel.

### Slide 5 — integração (1 min)

“O modelo carregado calcula predict_proba. O JSON entrega probabilidade, status, ID, versão e timestamp. A validação confere o vínculo e os limites. Só um contrato válido vira fato de risco. Sem modelo ou com probabilidade inválida, o contrato vira indisponível, com nulo; as regras permanecem.”

O exemplo mostrado no slide usa 0.824111, calculado nesta execução, e não o 0,78 ilustrativo do planejamento.

### Slide 6 — dados (2 min)

“Não recebemos histórico real rotulado. Geramos 3.600 prazos sintéticos com seed fixa. Simulamos carga, dias, ausência e tipos de ato; sorteamos atrasos com ruído e construímos datas coerentes. Isso valida a cadeia técnica, sem medir desempenho real.”

Explicar cinco features, IDs fora do modelo, divisão temporal por processo, purga de 60 exemplos e transformações ajustadas apenas no treino. A regressão aprende uma relação favorecida pelo gerador; a avaliação não prova comportamento da carteira real.

## Demonstração real — 5 minutos

Preparação: `python -m streamlit run app.py`; referência 17/11/2026, margem 5, limiar 0,70, ML ligado. Restaurar cenários e fechar expansores antes de apresentar.

| Tempo de demo | Quem | Ação | O que explicar |
|---|---|---|---|
| 00:00–00:45 | 1 | Mostrar D01, D02 e D03 | Vencido, hoje e fronteira de cinco dias; datas dominam |
| 00:45–01:30 | 1 | Selecionar D04-RISCO | 82.4% calculado, oito dias, ALTO por ML |
| 01:30–02:30 | 1 | Abrir fatos e encadeamento | JSON, R2, R6, R7, ciclos e resolução; data-limite intacta |
| 02:30–03:15 | 2 | Desligar ML | D04 vira NORMAL; status indisponível/nulo; vencidos e urgentes continuam |
| 03:15–04:00 | 2 | Mostrar D05, D06 e D07 | ALTO por ausência; NORMAL; concluído fora da fila |
| 04:00–05:00 | 2 | Ligar ML, selecionar D04, confirmar conclusão simulada | Sai da fila por ação humana; auditar e baixar JSON; restaurar |

Se o modelo não carregar, explicar o diagnóstico e executar `python -m src.ml.train`. Se a interface falhar, executar `python -m src.cli` e `python -m src.cli --sem-ml` ao vivo; ambos executam a mesma lógica. Os JSON salvos são evidência anterior, não devem ser apresentados como execução ao vivo. A equipe pode gravar um vídeo de reserva; nenhum vídeo acompanha esta entrega.

### Slides 8 e 9 — resultados (3 min)

“No teste sintético de 720 exemplos, o Dummy identifica zero atrasos. A regressão, com limiar 0,25 escolhido na validação, encontra 173 dos 226 atrasos: recall 76.5%. Ela também produz 165 falsos alarmes, com precision 51.2%. AP 0.6715 avalia o ranking ao longo dos limiares.”

Explicar 53 falsos negativos e o Brier. Comparar com 0,70: menos alarmes, mas recall 16.8%. A interface inicia com 0,70 para reproduzir o exemplo do planejamento; 0,25 é o experimento de validação. Ajustar no painel se houver tempo, sem sugerir regra jurídica.

### Slide 10 — limitações e ética (2 min)

Não há validação real nem integração INPI. Há risco de alarme excessivo e atraso não sinalizado pelo ML. Os fatos dependem de conferência humana. A probabilidade é de t0, não uma previsão diária. A confirmação na tela é uma simulação; ninguém protocolou atos ou homologou a solução.

### Slide 11 — próximos passos (2 min)

Definir coleta de snapshots reais, rótulo e maturidade; preservar separação temporal e por processo. Comparar regras isoladas e integração com a carga efetiva da equipe. Validar margem e limiar, calibrar o modelo, medir utilidade antes de integrar ao WebSystem. Encerrar com o que já funciona: regras explicáveis, predição real de um modelo sintético e fallback.
