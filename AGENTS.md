# Instruções locais para o Codex — Projeto Integrador, Marco Final

## Leitura obrigatória

Leia `CONTEXTO_PROJETO_INTEGRADOR.md` integralmente antes de implementar qualquer coisa. O contexto representa o **Marco 2 vigente (Gestão de Marcas)**; o antigo Marco 1 de entregas/Olist foi abandonado. Execute as tarefas do `PROMPT_MESTRE_CODEX.md` quando solicitado.

## Princípios inegociáveis

- Construir **protótipo acadêmico independente** para um dia, não WebSystem comercial.
- O Marco 2 **não comprova** modelos treinados, métricas ou sistema pronto. Não afirmar o contrário.
- Não inventar histórico, métricas, testes, nomes de apresentadores, homologação ou integrações INPI.
- Se dados reais não existirem, usar **dados sintéticos claramente identificados**, sem reivindicar validade operacional.
- Para modo ML, gerar probabilidade com **`predict_proba` de modelo treinado**; para modo sem ML, devolver `indisponivel` e `null`, nunca valor fabricado.
- Representar **fatos e regras de produção com encadeamento para a frente**, justificativas e rastreamento de inferência.
- Precedência: `CONCLUIDO` fora da fila; depois `VENCIDO > URGENTE > ALTO > NORMAL`.
- As regras operacionais **não criam nem alteram prazos legais**, e decisões continuam humanas.
- Isolar testes de unidade com probabilidades controladas dos testes de integração reais.
- Prevenir data leakage; IDs não são features; ajustar transformadores apenas no treino.
- Sempre executar os testes e registrar resultados verdadeiros; se não executou, marcar explicitamente não verificado.
- Priorizar funcionamento/integração/testes sobre UI sofisticada.

## Critérios de entrega

A avaliação final inclui demonstração real, domínio técnico de IA, domínio técnico de ML, integração funcional IA+ML e honestidade técnica/ética. Preparar 20 min de apresentação + 10 min de perguntas, para dois apresentadores.

## Comandos-alvo (adaptar se estrutura existente diferir)

```bash
python -m pip install -r requirements.txt
python -m src.ml.train
pytest -q
streamlit run app.py
```

Não fingir que esses comandos já foram executados até confirmá-los. Criar `README.md` com o fluxo verificado e documentar limitações no `docs/RELATORIO_TECNICO.md`.
