# Evidências de execução — 17/11/2026

Comandos executados no Linux com Python 3.12.14:

```bash
python -m pip install -r requirements.txt
python -m src.ml.train
python -m pytest -q
python -m src.cli
python -m src.cli --sem-ml
```

Instalação concluída; saída em `instalacao_stdout.txt`. Treino concluído com 3.600 linhas sintéticas geradas e modelo salvo. O relatório de métricas usa somente previsões realmente calculadas.

Saída da suíte final:

```text
................................................................         [100%]
=============================== warnings summary ===============================
../../../../opt/codex/runtimes/codex-primary-runtime/dependencies/python/lib/python3.12/site-packages/anyio/pytest_plugin.py:14
  /opt/codex/runtimes/codex-primary-runtime/dependencies/python/lib/python3.12/site-packages/anyio/pytest_plugin.py:14: PytestRemovedIn10Warning: _pytest.python.CallSpec2 has been renamed to CallSpec.
  The CallSpec2 alias will be removed in pytest 10.
  Update imports to use CallSpec instead.
  See https://docs.pytest.org/en/stable/deprecations.html#callspec2-renamed
    from _pytest.python import CallSpec2

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
64 passed, 1 warning in 0.97s
```

O aviso de depreciação provém do plugin anyio do ambiente de execução. A suíte inclui T01–T12, precedência, fronteiras, rejeição de contratos, fallback sem modelo/campos, hash corrompido, passagem real de predict_proba, validação do split e execução do painel por AppTest. AppTest verifica toggle de ML, confirmação humana e ausência de artefato.

Smoke test do servidor Streamlit via subprocesso local, porta 8502:

```json
{
  "status_http": 200,
  "resposta": "ok",
  "porta": 8502
}
```

A porta de smoke test difere do padrão de uso (8501). O processo foi encerrado após o teste. A execução HTTP testa inicialização do servidor; AppTest cobre execução e ações no script. O código inclui falhas e correções verificadas: a primeira execução de testes identificou seleção de botão por índice no teste de interface; a versão final usa chave estável e passou.

A inspeção visual do painel em navegador não foi concluída neste ambiente; a execução funcional foi coberta por AppTest.

Não foram verificados nesta execução: Windows nativo, abertura no aplicativo Microsoft PowerPoint, vídeo de reserva, integração com WebSystem/INPI, homologação operacional e desempenho com dados reais. As instruções Windows são fornecidas para reprodução, sem alegar teste naquele sistema.
