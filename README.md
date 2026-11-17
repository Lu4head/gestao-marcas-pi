# Gestão de Marcas — Projeto Integrador

Protótipo acadêmico independente de priorização de prazos. **Todos os dados e métricas são sintéticos. Não validado para uso jurídico/operacional.**

O motor usa fatos, regras de produção e encadeamento para a frente. A regressão logística realmente treinada entrega `predict_proba` por contrato JSON; sem artefato, a aplicação segue somente com regras. Nenhum componente consulta o INPI ou altera datas-limite.

## Início rápido

Extraia o ZIP, abra o terminal dentro de `gestao-marcas-pi` e use Python **3.12** (versão verificada: 3.12.14). As dependências listadas exigem Python 3.11 ou superior; outras versões de Python não foram verificadas nesta entrega.

```bash
python -m venv .venv
```

Ative no Windows PowerShell com `.venv\Scripts\Activate.ps1`, no CMD com `.venv\Scripts\activate.bat`, ou no Linux/macOS com `source .venv/bin/activate`.

```bash
python -m pip install -r requirements.txt
python -m src.ml.train
python -m pytest -q
python -m streamlit run app.py
```

Abra `http://localhost:8501`. No Windows, `py -3.12` pode substituir `python` na criação do ambiente. Se a execução de scripts do PowerShell estiver bloqueada, use o CMD ou execute `.venv\Scripts\python.exe` diretamente. A instalação requer rede; treino, inferência e aplicação usam apenas arquivos locais.

## Demonstração

A data inicial é **17/11/2026**. O painel oferece sete casos, inspeção do contrato, fatos e trilha; alternância ML/regras; configuração da margem e do limiar; e conclusão humana simulada. A simulação da conclusão dura só a sessão e pode ser restaurada.

A aba **Análise de prazos** reúne a tabela e a inspeção dos casos. A aba **Gráficos** mostra a distribuição de prioridades, os dias restantes por prazo e a probabilidade sintética de atraso em t0, quando disponível. Os gráficos consideram apenas a fila aberta e acompanham as configurações e conclusões da sessão. Sem ML, o gráfico de risco informa indisponibilidade.

`data/demo_prazos.csv` é um espelho legível dos cenários; a aplicação usa `src/data/demo.py` como fonte. Para modificar os casos permanentemente, edite esse módulo. A interface não oferece importação de planilhas reais.

```bash
python -m src.cli
python -m src.cli --sem-ml
python -m src.cli --data 2026-11-27
```

O CLI retorna JSON completo. A data de referência altera as regras, enquanto a previsão permanece no snapshot original de **t0**. Esta versão não prevê risco diário atualizado.

## Resultados verificados

- Dataset gerado: 3.600 prazos sintéticos de 1.200 processos; seed `20261117`.
- Após purga: 2133 treino, 687 validação, 720 teste.
- Regressão no teste, limiar escolhido na validação `0.25`: precision 51.2%, recall 76.5%, F1 0.6135, AP 0.6715.
- O painel inicia com **0,70**, o exemplo operacional do Marco 2. As métricas de 0,25 e 0,70 estão separadas em `docs/metricas.json`.
- O teste completo e o smoke test do servidor estão em `docs/RESULTADOS_EXECUCAO.md`, com logs originais ao lado.

## Conteúdo

| Caminho | Uso |
|---|---|
| `src/ia/engine.py` | Fatos, regras, agenda e precedência |
| `src/ml/train.py` | Geração, particionamento temporal, treino e avaliação |
| `src/ml/inference.py` | Carregamento do modelo e inferência real |
| `src/integration/` | Validação do contrato e orquestração |
| `tests/` | Regras T01–T12, pipeline, integração e painel |
| `docs/RELATORIO_TECNICO.md` | Metodologia, métricas e arquitetura |
| `presentation/slides.pptx` | Slides editáveis da apresentação |
| `presentation/ROTEIRO_20_MIN.md` | Fala de dois apresentadores e demo de cinco minutos |
| `presentation/PERGUNTAS_BANCA.md` | Preparação para dez minutos de defesa |

## Suposições e limites

Sem histórico real rotulado nos anexos, foi gerada uma simulação própria. A prioridade operacional prévia não foi fabricada como feature; os atributos utilizados estão no relatório. Não há login, banco de produção, API do WebSystem, consulta RPI/INPI, e-mail ou protocolo jurídico.

O arquivo `joblib` acompanha manifesto com hash e versão. Carregue apenas o artefato confiável deste pacote; `joblib` não é formato para uploads públicos. Se a versão de scikit-learn divergir, a aplicação entra em fallback; execute o treino no novo ambiente.

O Marco 2 documentava planejamento. O exemplo de 0,78 daquele documento continua ilustrativo; a execução atual usa probabilidades calculadas e não reutiliza dados/métricas do antigo projeto Olist.
