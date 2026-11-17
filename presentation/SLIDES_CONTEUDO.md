## 1. Gestão de Marcas

- Priorização de prazos com IA e ML
- Projeto Integrador · Ciência da Computação · 2026

**Notas:** 00:00–00:30 · Apresentador 1. Protótipo acadêmico com dados sintéticos; explicar o objetivo.

## 2. Priorização de providências

- Datas conferidas definem urgências
- O ML estima risco no instante t0
- As regras geram uma fila explicável
- A decisão continua humana

**Notas:** 00:30–02:00 · Apresentador 1. Fonte: Marco2_Documento_Padrao_Entrega-1.docx, seções 1 e 2. Consulta RPI humana; sem integração INPI. Tema antigo Olist abandonado.

## 3. Arquitetura do agente

Módulos agrupados no MVP: 1/3/4 dados e validação; 5 snapshot t0; 6 inferência ML; 7 fatos e regras; 2/8 interface e painel; 9 decisão humana; 10 treino offline. Dados fornecem atributos ao modelo e fatos às regras. A inferência alimenta as regras, que alimentam painel e decisão humana; o treino offline fornece o artefato à inferência. A confirmação humana retorna aos dados. Diagrama completo e tabela de mapeamento no relatório técnico.

**Notas:** 02:00–03:30 · Apresentador 1. Diagrama conceitual dos dez módulos do Marco 2; os fluxos foram preservados. MVP: CSV/objetos, Python e Streamlit; sem API, autenticação ou banco de produção. Fonte: Marco2_Documento_Padrao_Entrega-1.docx, seção 1.2; src/.

## 4. Fatos e regras de produção

| Condição | Resultado |
|---|---|
| Concluído | FORA_DA_FILA |
| Aberto, dias < 0 | VENCIDO |
| Aberto, 0 ≤ dias ≤ margem | URGENTE |
| Fora da margem, ausência ou risco ≥ limiar | ALTO |
| Demais abertos | NORMAL |

Memória de fatos, agenda, novos fatos e ponto fixo.

**Notas:** 03:30–05:00 · Apresentador 1. Prazo aberto e risco elevado derivam fatos em ciclos diferentes. A agenda chega a ponto fixo antes de resolver prioridade. Motivos adicionais ficam registrados. Fonte: src/ia/engine.py; docs/demo_ml.json.

## 5. Contrato ML e IA

```json
{
  "schema_version": "1.0",
  "prazo_id": "D04-RISCO",
  "gerado_em": "2026-11-17T10:58:33.520893+00:00",
  "modelo_versao": "logreg-sintetica-v1-6fd088eae9",
  "status": "ok",
  "prob_atraso": 0.8241107932764514
}
```

Risco vira motivo e candidato ALTO. Fallback: status indisponivel, prob_atraso null.

**Notas:** 05:00–06:00 · Apresentador 1. JSON real desta execução: docs/demo_ml.json, D04-RISCO. predict_proba do modelo carregado alimenta fato risco_ml; R6 deriva motivo, R7 deriva ALTO. Falha: indisponivel/null. Nenhuma data se altera.

## 6. Dados sintéticos e avaliação

3.600 prazos, 1.200 processos, seed 20261117.

| Partição | Prazos | Processos | Classe 0 | Classe 1 | t0 |
|---|---:|---:|---:|---:|---|
| treino | 2133 | 716 | 1543 | 590 | 2019-01-01 a 2022-12-03 |
| validacao | 687 | 235 | 516 | 171 | 2022-12-11 a 2024-03-29 |
| teste | 720 | 240 | 494 | 226 | 2024-04-04 a 2025-07-28 |

Divisão temporal por processo; purga de 60 desfechos. Features t0: dias, carga, ausência, ato e situação. Fit só no treino.

**Notas:** 06:00–08:00 · Apresentador 2. Fonte: docs/metricas.json e src/data/synthetic.py. 3.600 prazos de 1.200 processos. Gerador logístico com ruído favorece logística; sem validade real. Features t0: dias, carga, ausência, ato e situação; IDs fora. Partição temporal por processo, purga de 60 desfechos, fit apenas no treino. Referência técnica: https://scikit-learn.org/stable/common_pitfalls.html

## 7. Demonstração funcional

- Vencidos, urgentes e fronteira de 5 dias
- D04: predição real e trilha R2 / R6 / R7
- ML desligado: indisponível e regras ativas
- Ausência, normal e concluído fora da fila
- Conclusão humana simulada e evidência JSON

**Notas:** 08:00–13:00 · Apresentador 1 até 10:30; Apresentador 2 até 13:00. Abrir painel; referência 17/11/2026, margem 5, limiar 0,70. Seguir ROTEIRO_20_MIN.md. Fonte: src/data/demo.py e docs/demo_ml.json.

## 8. Resultados no teste sintético

Teste sintético de 720 prazos. Limiar 0,25 na validação.

| Modelo | Precision | Recall | F1 | AP | Brier |
|---|---:|---:|---:|---:|---:|
| dummy_majoritario | não calculável | 0.0% | 0.0000 | 0.3139 | 0.3139 |
| regressao_logistica | 51.2% | 76.5% | 0.6135 | 0.6715 | 0.1624 |

Precision do Dummy não é calculável porque não há positivos previstos.

**Notas:** 13:00–14:30 · Apresentador 2. Fonte: docs/metricas.json. Limiar 0,25 escolhido na validação por F2 e orçamento ilustrativo de 45% de alertas. No teste, alertas 46,9%. Dummy precision não calculável por zero positivos previstos. AP usa average_precision_score. Resultados apenas sintéticos.

## 9. Erros e escolha do limiar

| Real / Previsto | No prazo | Atraso |
|---|---:|---:|
| No prazo | 329 (TN) | 165 (FP) |
| Atraso | 53 (FN) | 173 (TP) |

Limiar 0,25: precision 51,2%, recall 76,5%. Limiar 0,70: precision 90,5%, recall 16,8%. Mais sensibilidade exige maior carga de revisão.

**Notas:** 14:30–16:00 · Apresentador 2. Fonte: docs/metricas.json. 173 TP, 165 FP, 53 FN, 329 TN no limiar 0,25. Comparar precision/recall com 0,70, o padrão inicial da interface. Regras+ML no teste sintético aumenta recall e também a carga de revisão. Não inferir redução de atrasos.

## 10. Limitações e ética

- Métricas restritas à simulação
- Falsos alertas e riscos não detectados
- Dependência de conferência humana
- Probabilidade t0; sem reavaliação diária
- Sem validação operacional ou jurídica

**Notas:** 16:00–18:00 · Apresentador 1. Fonte: docs/LIMITACOES_ETICA.md. Sem WebSystem/INPI real; datas imutáveis; conclusão simulada; não apresentar homologação inexistente.

## 11. Próximos passos

- Coleta de snapshots e desfechos reais
- Validação temporal e calibração
- Comparação com as regras e carga da equipe
- Definição de parâmetros com responsáveis
- Integração ao WebSystem após validação

**Notas:** 18:00–20:00 · Apresentador 2. Plano futuro, não resultado entregue. Coletar histórico com rótulos maduros e governança; avaliar benefício sobre controle determinístico antes da adoção. Reservar 10 minutos para perguntas.
