"""Atualiza documentação a partir das evidências reais salvas pelo treino/testes."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]


def build():
    m=json.loads((ROOT/'docs/metricas.json').read_text())
    demo=json.loads((ROOT/'docs/demo_ml.json').read_text())
    q=next(r for r in demo if r['prazo_id']=='D04-RISCO')
    model=m['comparacao']['regressao_logistica']
    base=m['comparacao']['dummy_majoritario']
    pct=lambda x: 'não calculável' if x is None else f'{x*100:.1f}%'
    n=lambda x: 'não calculável' if x is None else f'{x:.4f}'
    def write(path, text):
        (ROOT/path).write_text(text.strip()+'\n')
    write('README.md', f'''
# Gestão de Marcas — Projeto Integrador

Protótipo acadêmico independente de priorização de prazos. **Todos os dados e métricas são sintéticos. Não validado para uso jurídico/operacional.**

O motor usa fatos, regras de produção e encadeamento para a frente. A regressão logística realmente treinada entrega `predict_proba` por contrato JSON; sem artefato, a aplicação segue somente com regras. Nenhum componente consulta o INPI ou altera datas-limite.

## Início rápido

Extraia o ZIP, abra o terminal dentro de `gestao-marcas-pi` e use Python **3.12** (versão verificada: {m['versoes']['python']}). As dependências listadas exigem Python 3.11 ou superior; outras versões de Python não foram verificadas nesta entrega.

```bash
python -m venv .venv
```

Ative no Windows PowerShell com `.venv\\Scripts\\Activate.ps1`, no CMD com `.venv\\Scripts\\activate.bat`, ou no Linux/macOS com `source .venv/bin/activate`.

```bash
python -m pip install -r requirements.txt
python -m src.ml.train
python -m pytest -q
python -m streamlit run app.py
```

Abra `http://localhost:8501`. No Windows, `py -3.12` pode substituir `python` na criação do ambiente. Se a execução de scripts do PowerShell estiver bloqueada, use o CMD ou execute `.venv\\Scripts\\python.exe` diretamente. A instalação requer rede; treino, inferência e aplicação usam apenas arquivos locais.

## Demonstração

A data inicial é **17/11/2026**. O painel oferece sete casos, inspeção do contrato, fatos e trilha; alternância ML/regras; configuração da margem e do limiar; e conclusão humana simulada. A simulação da conclusão dura só a sessão e pode ser restaurada.

`data/demo_prazos.csv` é um espelho legível dos cenários; a aplicação usa `src/data/demo.py` como fonte. Para modificar os casos permanentemente, edite esse módulo. A interface não oferece importação de planilhas reais.

```bash
python -m src.cli
python -m src.cli --sem-ml
python -m src.cli --data 2026-11-27
```

O CLI retorna JSON completo. A data de referência altera as regras, enquanto a previsão permanece no snapshot original de **t0**. Esta versão não prevê risco diário atualizado.

## Resultados verificados

- Dataset gerado: 3.600 prazos sintéticos de 1.200 processos; seed `{m['seed']}`.
- Após purga: {m['particoes']['treino']['n']} treino, {m['particoes']['validacao']['n']} validação, 720 teste.
- Regressão no teste, limiar escolhido na validação `{m['limiar_validacao']:.2f}`: precision {pct(model['precision'])}, recall {pct(model['recall'])}, F1 {n(model['f1'])}, AP {n(model['average_precision'])}.
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
''')
    partitions='\n'.join(f"| {name} | {v['n']} | {v['processos']} | {v['suporte'].get('0',0)} | {v['suporte'].get('1',0)} | {v['inicio_t0']} a {v['fim_t0']} |" for name,v in m['particoes'].items())
    comparison='\n'.join(f"| {name} | {pct(v['precision'])} | {pct(v['recall'])} | {n(v['f1'])} | {n(v['average_precision'])} | {n(v['brier'])} |" for name,v in m['comparacao'].items())
    write('docs/RELATORIO_TECNICO.md', f'''
# Relatório técnico — Gestão de Marcas

## Problema e status da entrega

Organizar a fila de providências de marcas a partir de datas conferidas e informações do responsável. O componente lógico decide a prioridade; o ML estima a chance de a providência não ser concluída no prazo, no instante da primeira validação humana (t0).

O Marco 2 era uma proposta de arquitetura, com 19 processos previstos e sem dataset rotulado ou experimentos comprovados no tema atual. O Marco Final implementa um **protótipo acadêmico independente** em Python/Streamlit. Dados, nomes de processos e rótulos são **sintéticos**. Não há evidência de eficácia jurídica ou operacional.

## Arquitetura e módulos

O desenho conceitual do Marco 2 contém dez módulos. O fluxo abaixo preserva as relações; as funções de API, persistência e autenticação são simplificadas no MVP.

```mermaid
flowchart TD
 M1["1 · Entrada humana"] --> M2["2 · Interface"]
 M2 --> M3["3 · Validação de domínio"]
 M3 <--> M4["4 · Persistência e histórico"]
 M4 --> M5["5 · Snapshot de atributos"]
 M5 --> M6["6 · Inferência ML"]
 M3 --> M7["7 · Motor de regras"]
 M6 --> M7
 M7 --> M8["8 · Painel"]
 M8 --> M9["9 · Decisão humana"]
 M9 --> M2
 M4 --> M10["10 · Treino offline"]
 M10 --> M6
```

| Módulos do Marco 2 | Realização neste MVP |
|---|---|
| 1, 3, 4 | Cenários em objetos/CSV; validação tipada; arquivos locais; auditoria de revisão na sessão |
| 2, 8 | Streamlit, sem login; tabela, parâmetros e inspeção |
| 5 | Snapshot t0 preservado; atributos selecionados explicitamente |
| 6 | Pipeline scikit-learn carregado e `predict_proba` |
| 7 | Fatos, regras de produção, agenda e ponto fixo |
| 9 | Confirmação humana simulada; registro com autoria demonstrativa |
| 10 | Treino offline versionado com manifesto, métricas e predições |

## Representação e inferência de IA

`Fact` representa uma proposição derivável e seu valor. A memória de trabalho inicia com conclusão, dias restantes, ausência e status do ML; o contrato válido acrescenta `risco_ml`. `Rule` contém condição, efeitos e identificador. A agenda seleciona regras habilitadas, cada uma disparando uma vez; os efeitos entram na memória e habilitam o ciclo seguinte. A execução termina no ponto fixo. Só então a resolução escolhe o candidato de maior precedência.

Exemplo real da demo: a regra R2 deriva `prazo_aberto`; R6 usa o risco {q['ml']['prob_atraso']:.6f} calculado pelo modelo e deriva um motivo; R7 usa esse motivo em um ciclo posterior e deriva `candidato_ALTO`. O painel mostra memória inicial/final, fatos consultados, efeitos, ciclos e resolução. Não há apenas uma classificação opaca.

| Condição | Prioridade |
|---|---|
| Concluído | FORA_DA_FILA |
| Aberto e dias < 0 | VENCIDO |
| Aberto e 0 ≤ dias ≤ margem | URGENTE |
| Aberto fora da margem e ausência ou risco ≥ limiar | ALTO |
| Demais abertos | NORMAL |

A ausência e o risco podem aparecer como motivos adicionais mesmo em vencidos/urgentes; a precedência permanece intacta. Em concluídos, as regras de ação não disparam. O limiar padrão 0,70 e a margem de cinco dias são configurações ilustrativas, sem aprovação jurídica presumida. Datas-limite permanecem imutáveis.

Regras foram escolhidas pela rastreabilidade e precedência. CSP seria adequado a alocação sob restrições, fora do objetivo atual. Uma rede bayesiana exigiria estrutura e probabilidades condicionais sem suporte no material disponível.

## Dados e rótulo

Gerador: `src/data/synthetic.py`, seed {m['seed']}, 1.200 processos com três prazos cada. Datas t0 simuladas de 2019 a 2025, com intervalo entre processos. Dias restantes variam de 1 a 35; carga de 0 a 60; ausência t0 tem probabilidade de 16%; quatro tipos de ato.

O gerador calcula uma probabilidade latente logística: `z = -2.6 - 0.07*dias + 0.065*carga + ausencia + efeito_ato + efeito_processo + ruido`. Efeito de processo segue Normal(0, 0,5); ruído segue Normal(0, 0,6). Os efeitos de ato são 0,9 para exigência, 0,4 manifestação, 0,1 pagamento e -0,3 acompanhamento. O rótulo nasce de Bernoulli(sigmoid(z)); depois são criadas datas de conclusão consistentes com y. Esses números são hipóteses de simulação, sem estimativa empírica do domínio.

`y=1` corresponde a conclusão posterior à data-limite; `y=0` a conclusão até a data-limite. Todos os exemplos gerados têm desfecho maduro. A base real futura também precisaria tratar abertos vencidos, cancelamentos e casos indeterminados; este gerador simula somente conclusões conhecidas.

Features: `{', '.join(m['features'])}`. `situacao_t0` é constante ABERTO nesta simulação; não agrega sinal, mas mantém o campo de contrato. A prioridade operacional prévia é omitida por não existir histórico independente. Identificadores, conclusão, maturidade do desfecho e y ficam fora das features.

Os sete cenários da interface são separados dos exemplos de treino, usam IDs DEMO e não foram usados para seleção de limiar ou ajuste de modelo. Uma data de referência posterior a t0 só muda regras; a previsão continua sendo a original de t0.

## Particionamento e prevenção de vazamento

Processos ordenados pelo primeiro t0: 60% dos grupos candidatos a treino, 20% validação e 20% teste. Nenhum processo atravessa partições. A purga elimina do treino os exemplos cujo desfecho ainda não estaria disponível antes da validação, e da validação aqueles não maduros antes do teste: {m['purga']['treino']} e {m['purga']['validacao']} exclusões, respectivamente.

| Partição | Prazos | Processos após purga | Classe 0 | Classe 1 | Intervalo t0 |
|---|---:|---:|---:|---:|---|
{partitions}

Pipeline: imputação mediana e StandardScaler para números; imputação por moda e OneHotEncoder com categorias desconhecidas ignoradas para categorias; LogisticRegression regularizada L2, C=1, max_iter=1000. Os transformadores são ajustados apenas no treino. Não há dados ausentes no gerador atual; a inferência exige todos os campos mínimos, caso contrário usa fallback.

## Seleção e avaliação

Comparação implementada: Dummy majoritário e regressão logística. Árvore, Random Forest e HistGradientBoosting permanecem candidatos futuros; não foram treinados nesta entrega. A regressão foi uma escolha arquitetural simples fixada antes da avaliação do teste. Não houve busca de hiperparâmetros nem promoção para produção.

O limiar **{m['limiar_validacao']:.2f}** foi escolhido somente na validação, maximizando F2 sob um orçamento ilustrativo de até 45% de alertas. Não representa capacidade real da equipe. O teste permaneceu fora desse ajuste; nele a fração de alertas foi {pct(model['fracao_alertas'])}, mostrando que o orçamento de validação não garante a mesma carga em períodos posteriores.

| Modelo no teste sintético | Precision | Recall | F1 | AP | Brier |
|---|---:|---:|---:|---:|---:|
{comparison}

Precision do Dummy é não calculável porque ele não prevê positivos; recall e F1 são calculáveis e iguais a zero. AP do Dummy coincide com a prevalência do teste ({pct(base['average_precision'])}). AP usa `average_precision_score`, sem interpolação trapezoidal. O Brier menor favorece a regressão neste experimento, mas não constitui validação de calibração real. Cinco faixas de calibração por quantis estão no JSON; não houve recalibração nem intervalo de confiança nesta versão.

Matriz de confusão da regressão no limiar {m['limiar_validacao']:.2f}: **TN={model['TN']}, FP={model['FP']}, FN={model['FN']}, TP={model['TP']}**. Precision=TP/(TP+FP); recall=TP/(TP+FN); F1=2TP/(2TP+FP+FN). Há 226 atrasos e 494 conclusões pontuais no teste de 720 exemplos.

O painel inicia com **0,70**, para reproduzir o exemplo operacional do Marco 2. Nesse limiar a regressão atinge precision {pct(m['logistica_limiar_ilustrativo_070']['precision'])}, recall {pct(m['logistica_limiar_ilustrativo_070']['recall'])} e F1 {n(m['logistica_limiar_ilustrativo_070']['f1'])}. Aumentar o limiar reduz alarmes e perde atrasos. As métricas principais da tabela acima pertencem ao limiar 0,25.

## Regras versus integração

Comparação técnica no snapshot t0 do teste, com alerta definido como URGENTE ou ALTO: regras isoladas (margem 5 ou ausência) versus as mesmas regras acrescidas de ML ≥ 0,25. A rotina usa as condições equivalentes às regras para snapshots abertos, com dias ≥ 1; não avalia uma simulação longitudinal de intervenções.

| Modo | Recall | Precision | Alertas | Falsos positivos |
|---|---:|---:|---:|---:|
| Regras | {pct(m['comparacao_priorizacao_t0']['somente_regras']['recall'])} | {pct(m['comparacao_priorizacao_t0']['somente_regras']['precision'])} | {pct(m['comparacao_priorizacao_t0']['somente_regras']['fracao_alertas'])} | {m['comparacao_priorizacao_t0']['somente_regras']['FP']} |
| Regras + ML | {pct(m['comparacao_priorizacao_t0']['regras_com_ml']['recall'])} | {pct(m['comparacao_priorizacao_t0']['regras_com_ml']['precision'])} | {pct(m['comparacao_priorizacao_t0']['regras_com_ml']['fracao_alertas'])} | {m['comparacao_priorizacao_t0']['regras_com_ml']['FP']} |

O experimento detecta mais rótulos sintéticos de atraso e também aumenta trabalho de revisão e alarmes falsos. Não demonstra que a equipe evitaria atrasos, nem justifica adoção operacional. O gerador favorece relações compatíveis com a logística, o que limita a comparação e precisa ser dito à banca.

## Integração e fallback

Contrato real salvo em `docs/demo_ml.json`; exemplo executado:

```json
{json.dumps(q['ml'],ensure_ascii=False,indent=2)}
```

O carregador verifica hash, versão de scikit-learn, origem e features do artefato local. `status=ok` só nasce de `predict_proba` com bundle carregado. O validador rejeita probabilidades fora do intervalo, NaN/infinito, booleanos, status contraditórios, identificador incorreto, versão ausente e timestamp sem timezone. Erros viram indisponibilidade com probabilidade nula; o motor usa fatos operacionais. Regras recebem probabilidades controladas apenas em testes unitários, separados da integração real.

Modelo: `{m['modelo_versao']}`. Dataset SHA-256: `{m['dataset_sha256']}`. Versões e hash do artefato estão em `models/manifesto.json`; cada classificação registra referência, data-limite, parâmetros, versão, motivos e timestamp de inferência.

## Evidências, limitações e próximos passos

Os logs e resultados reais ficam em `RESULTADOS_EXECUCAO.md`, `pytest_stdout.txt`, `treino_stdout.json`, `metricas.json`, `predicoes_teste_sintetico.csv`, `particoes.csv` e os dois JSON de demonstração. O painel permite registrar e baixar uma revisão simulada; não há homologação externa.

Limites: sem histórico real; gerador conhecido e pouco representativo; ausência de validação jurídica; baixa portabilidade entre versões de artefato; sem autenticação e persistência multiusuário; falta de estimativa de incerteza por grupos; ausência de atualização diária do risco. Erros humanos na conferência podem comprometer toda a fila.

Próximos passos: coletar snapshots e desfechos reais com governança; validar maturidade e correlação por processo; avaliar em período posterior e recalibrar; escolher margem e limiar com capacidade da equipe; avaliar benefício sobre regras isoladas; só então projetar integração com WebSystem.

## Referências

- Marco 2 preenchido: `Marco2_Documento_Padrao_Entrega-1.docx` (arquitetura e integração propostas).
- Roteiro final: `Marco3_Documento_Roteiro_e_Avaliacao (1).docx` (demonstração real e cinco critérios).
- Catálogo de PI e modelos de entrega, usados como requisitos acadêmicos.
- [scikit-learn — prevenção de vazamento e pipelines](https://scikit-learn.org/stable/common_pitfalls.html).
- [Streamlit — AppTest](https://docs.streamlit.io/develop/api-reference/app-testing/st.testing.v1.apptest).

O Marco 1 de entregas/Olist é apenas histórico do tema abandonado; seus dados e resultados não foram usados.
''')
    log=(ROOT/'docs/pytest_stdout.txt').read_text()
    health=(ROOT/'docs/servidor_health.json').read_text() if (ROOT/'docs/servidor_health.json').exists() else 'Não verificado'
    write('docs/RESULTADOS_EXECUCAO.md', f'''
# Evidências de execução — 17/11/2026

Comandos executados no Linux com Python {m['versoes']['python']}:

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
{log.strip()}
```

O aviso de depreciação provém do plugin anyio do ambiente de execução. A suíte inclui T01–T12, precedência, fronteiras, rejeição de contratos, fallback sem modelo/campos, hash corrompido, passagem real de predict_proba, validação do split e execução do painel por AppTest. AppTest verifica toggle de ML, confirmação humana e ausência de artefato.

Smoke test do servidor Streamlit via subprocesso local, porta 8502:

```json
{health.strip()}
```

A porta de smoke test difere do padrão de uso (8501). O processo foi encerrado após o teste. A execução HTTP testa inicialização do servidor; AppTest cobre execução e ações no script. O código inclui falhas e correções verificadas: a primeira execução de testes identificou seleção de botão por índice no teste de interface; a versão final usa chave estável e passou.

Não foram verificados nesta execução: Windows nativo, abertura no aplicativo Microsoft PowerPoint, vídeo de reserva, integração com WebSystem/INPI, homologação operacional e desempenho com dados reais. As instruções Windows são fornecidas para reprodução, sem alegar teste naquele sistema.
''')
    write('docs/LIMITACOES_ETICA.md', '''
# Limitações e ética

- Todos os dados, rótulos e exemplos são sintéticos. Métricas medem execução técnica sobre uma distribuição inventada, sem demonstrar eficácia em processos reais.
- O gerador usa uma relação logística conhecida; o desempenho da regressão depende dessa hipótese. Não há prova de generalização para a carteira real.
- Os 19 processos citados no planejamento não constituem dataset rotulado disponível, nem foram importados nesta entrega.
- O risco pertence a t0. Mudar a data do painel atualiza as regras, preservando a previsão t0; reavaliação diária demandaria outro estudo.
- Margem e limiar são operacionais, não prazos legais. ML nunca altera data-limite, conclui uma providência sozinho ou decide ato jurídico.
- Alarmes falsos consomem revisão humana. Falsos negativos podem deixar riscos sem destaque; datas vencidas/urgentes continuam com precedência.
- O painel usa cenários fixos e estado por sessão. Não possui login, banco de produção, integração INPI/RPI ou envio de notificações.
- A confirmação de conclusão é simulada. O responsável continua obrigado a conferir fatos e decidir; não há homologação de equipe externa.
- Não há informações pessoais de titulares ou números reais de processos nos dados de ML.
- Antes de adoção, coletar histórico com finalidade e acesso definidos, validar rótulos e maturidade, medir calibração e benefício sobre regras isoladas e revisar vieses e mudanças de operação.
''')
    write('presentation/ROTEIRO_20_MIN.md', f'''
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

O exemplo mostrado no slide usa {q['ml']['prob_atraso']:.6f}, calculado nesta execução, e não o 0,78 ilustrativo do planejamento.

### Slide 6 — dados (2 min)

“Não recebemos histórico real rotulado. Geramos 3.600 prazos sintéticos com seed fixa. Simulamos carga, dias, ausência e tipos de ato; sorteamos atrasos com ruído e construímos datas coerentes. Isso valida a cadeia técnica, sem medir desempenho real.”

Explicar cinco features, IDs fora do modelo, divisão temporal por processo, purga de 60 exemplos e transformações ajustadas apenas no treino. A regressão aprende uma relação favorecida pelo gerador; a avaliação não prova comportamento da carteira real.

## Demonstração real — 5 minutos

Preparação: `python -m streamlit run app.py`; referência 17/11/2026, margem 5, limiar 0,70, ML ligado. Restaurar cenários e fechar expansores antes de apresentar.

| Tempo de demo | Quem | Ação | O que explicar |
|---|---|---|---|
| 00:00–00:45 | 1 | Mostrar D01, D02 e D03 | Vencido, hoje e fronteira de cinco dias; datas dominam |
| 00:45–01:30 | 1 | Selecionar D04-RISCO | {q['ml']['prob_atraso']*100:.1f}% calculado, oito dias, ALTO por ML |
| 01:30–02:30 | 1 | Abrir fatos e encadeamento | JSON, R2, R6, R7, ciclos e resolução; data-limite intacta |
| 02:30–03:15 | 2 | Desligar ML | D04 vira NORMAL; status indisponível/nulo; vencidos e urgentes continuam |
| 03:15–04:00 | 2 | Mostrar D05, D06 e D07 | ALTO por ausência; NORMAL; concluído fora da fila |
| 04:00–05:00 | 2 | Ligar ML, selecionar D04, confirmar conclusão simulada | Sai da fila por ação humana; auditar e baixar JSON; restaurar |

Se o modelo não carregar, explicar o diagnóstico e executar `python -m src.ml.train`. Se a interface falhar, executar `python -m src.cli` e `python -m src.cli --sem-ml` ao vivo; ambos executam a mesma lógica. Os JSON salvos são evidência anterior, não devem ser apresentados como execução ao vivo. A equipe pode gravar um vídeo de reserva; nenhum vídeo acompanha esta entrega.

### Slides 8 e 9 — resultados (3 min)

“No teste sintético de 720 exemplos, o Dummy identifica zero atrasos. A regressão, com limiar 0,25 escolhido na validação, encontra 173 dos 226 atrasos: recall {pct(model['recall'])}. Ela também produz 165 falsos alarmes, com precision {pct(model['precision'])}. AP {n(model['average_precision'])} avalia o ranking ao longo dos limiares.”

Explicar 53 falsos negativos e o Brier. Comparar com 0,70: menos alarmes, mas recall {pct(m['logistica_limiar_ilustrativo_070']['recall'])}. A interface inicia com 0,70 para reproduzir o exemplo do planejamento; 0,25 é o experimento de validação. Ajustar no painel se houver tempo, sem sugerir regra jurídica.

### Slide 10 — limitações e ética (2 min)

Não há validação real nem integração INPI. Há risco de alarme excessivo e atraso não sinalizado pelo ML. Os fatos dependem de conferência humana. A probabilidade é de t0, não uma previsão diária. A confirmação na tela é uma simulação; ninguém protocolou atos ou homologou a solução.

### Slide 11 — próximos passos (2 min)

Definir coleta de snapshots reais, rótulo e maturidade; preservar separação temporal e por processo. Comparar regras isoladas e integração com a carga efetiva da equipe. Validar margem e limiar, calibrar o modelo, medir utilidade antes de integrar ao WebSystem. Encerrar com o que já funciona: regras explicáveis, predição real de um modelo sintético e fallback.
''')
    write('presentation/PERGUNTAS_BANCA.md', f'''
# Defesa técnica — preparação para 10 minutos

1. **Qual é a IA clássica?** Fatos e regras de produção com encadeamento para a frente. A memória de trabalho recebe efeitos que habilitam regras em ciclos posteriores; a trilha documenta cada disparo. A resolução no ponto fixo aplica precedência.

2. **Por que não CSP?** O problema atual é classificar prioridades por condições operacionais, sem distribuir pessoas sob capacidade/restrições. Um CSP pode ser estudado quando houver alocação de tarefas.

3. **Por que não rede bayesiana?** Não temos estrutura causal nem probabilidades condicionais validadas. O modelo tabular é um experimento separado e regras preservam precedência de datas.

4. **O ML pode rebaixar urgentes?** Não. Apenas acrescenta motivo de risco e pode elevar um aberto fora da margem a ALTO. VENCIDO e URGENTE prevalecem. Concluídos saem da fila.

5. **Como a integração é comprovada?** O teste carrega o pipeline, calcula predict_proba, compara com o JSON e com o fato risco_ml usado pelo motor. O painel mostra a probabilidade e a versão. Desligar o ML remove o fato; não o substitui por uma constante.

6. **De onde vêm os dados?** Do gerador sintético com seed {m['seed']}. São 1.200 processos e 3.600 prazos, com correlação por processo e ruído. Não são dados do INPI nem dos 19 processos citados na proposta.

7. **Qual é o alvo?** Providência concluída após a data-limite, y=1; no prazo, y=0. O gerador usa apenas conclusões conhecidas. Na coleta real, abertos vencidos também podem ser positivos após maturidade; cancelados e indeterminados devem ser excluídos.

8. **Como evitamos vazamento?** IDs e desfechos não entram nas features; processos não atravessam partições; treino antecede validação e teste; purgamos desfechos conhecidos tarde; imputação, escala e categorias são ajustadas só no treino. A previsão usa o snapshot t0.

9. **Por que regressão logística?** Classificação binária leve, regularização e coeficientes inspecionáveis. Foi uma escolha de projeto anterior à avaliação, comparada com Dummy. Não alegamos seleção entre todos os modelos do Marco 2.

10. **Como foi escolhido o limiar?** Na validação, maximizando F2 com até 45% de alertas, um orçamento hipotético. Resultado: {m['limiar_validacao']:.2f}. O teste não ajustou esse parâmetro. O painel começa em 0,70, valor ilustrativo do Marco 2, e permite alterá-lo.

11. **Por que precision, recall, F1 e AP?** Recall mede atrasos encontrados; precision mede quantos alertas correspondem a atrasos; F1 resume os dois; AP mede ordenação sem depender de um único limiar. Acurácia isolada pode recompensar a maioria. Brier avalia erro quadrático das probabilidades.

12. **Quantos erros ocorreram?** No limiar 0,25: TP={model['TP']}, FP={model['FP']}, FN={model['FN']}, TN={model['TN']}. Encontramos {pct(model['recall'])} dos atrasos sintéticos; {pct(model['precision'])} dos alertas eram positivos. Esses resultados não estimam os erros reais da equipe.

13. **O ML melhora as regras?** Na simulação, integrar risco ≥ 0,25 aumenta recall de 44,2% para 84,5%, mas alertas sobem de 28,6% para 56,5% e há mais falsos positivos. Isso mostra o custo de revisão, não comprova utilidade operacional nem redução causal de atrasos.

14. **A probabilidade é calibrada?** Calculamos Brier e cinco faixas de calibração no teste sintético. Há discrepâncias. Não houve recalibração nem validação real; 82,4% no demo não pode ser interpretado como frequência confiável em processos jurídicos.

15. **Dados sintéticos são suficientes?** Para provar que geração, treino, predição e regras executam, sim. Para afirmar eficácia real, não. O gerador inventa a distribuição e favorece relações que a logística consegue aprender. Precisamos de coleta e validação independentes.

16. **O que acontece sem modelo?** status indisponível e probabilidade nula; continuam regras de datas e ausência. Entradas operacionais inválidas são rejeitadas, não classificadas como normais silenciosamente.

17. **Por que não atualizar risco todos os dias?** O estudo define predição em t0. Atualizações diárias precisam de snapshots, rótulos e avaliação adequados. Hoje só os fatos temporais das regras mudam com a referência.

18. **Qual dano poderia ocorrer?** Um dado de prazo errado, falso negativo ou excesso de alarmes pode prejudicar a organização. O protótipo preserva datas, mostra motivos e exige decisão humana; isso não substitui validação de operação e segurança.

19. **O que não foi implementado?** Integração WebSystem/INPI, login real, persistência multiusuário, leitura RPI, protocolo, e-mail, vídeo de reserva e validação com histórico real. O arquivo de suporte não é apresentado como novo relatório formal obrigatório do roteiro.

20. **Como reproduzir?** Instalar requirements, treinar, rodar pytest e abrir Streamlit; seed, partições, hash, modelo, métricas e predições acompanham o pacote. Artefatos devem ser confiáveis; joblib não aceita uploads públicos seguros.
''')
    slides=[
        dict(title='Gestão de Marcas',kind='cover',body=['Priorização de prazos com IA e ML','Projeto Integrador · Ciência da Computação · 2026'],note='00:00–00:30 · Apresentador 1. Protótipo acadêmico com dados sintéticos; explicar o objetivo.'),
        dict(title='Priorização de providências',kind='text',body=['Datas conferidas definem urgências','O ML estima risco no instante t0','As regras geram uma fila explicável','A decisão continua humana'],note='00:30–02:00 · Apresentador 1. Fonte: Marco2_Documento_Padrao_Entrega-1.docx, seções 1 e 2. Consulta RPI humana; sem integração INPI. Tema antigo Olist abandonado.'),
        dict(title='Arquitetura do agente',kind='architecture',body=[],note='02:00–03:30 · Apresentador 1. Diagrama conceitual dos dez módulos do Marco 2; os fluxos foram preservados. MVP: CSV/objetos, Python e Streamlit; sem API, autenticação ou banco de produção. Fonte: Marco2_Documento_Padrao_Entrega-1.docx, seção 1.2; src/.'),
        dict(title='Fatos e regras de produção',kind='rules',body=[],note='03:30–05:00 · Apresentador 1. Prazo aberto e risco elevado derivam fatos em ciclos diferentes. A agenda chega a ponto fixo antes de resolver prioridade. Motivos adicionais ficam registrados. Fonte: src/ia/engine.py; docs/demo_ml.json.'),
        dict(title='Contrato ML e IA',kind='contract',body=[],note='05:00–06:00 · Apresentador 1. JSON real desta execução: docs/demo_ml.json, D04-RISCO. predict_proba do modelo carregado alimenta fato risco_ml; R6 deriva motivo, R7 deriva ALTO. Falha: indisponivel/null. Nenhuma data se altera.'),
        dict(title='Dados sintéticos e avaliação',kind='data',body=[],note='06:00–08:00 · Apresentador 2. Fonte: docs/metricas.json e src/data/synthetic.py. 3.600 prazos de 1.200 processos. Gerador logístico com ruído favorece logística; sem validade real. Features t0: dias, carga, ausência, ato e situação; IDs fora. Partição temporal por processo, purga de 60 desfechos, fit apenas no treino. Referência técnica: https://scikit-learn.org/stable/common_pitfalls.html'),
        dict(title='Demonstração funcional',kind='text',body=['Vencidos, urgentes e fronteira de 5 dias','D04: predição real e trilha R2 / R6 / R7','ML desligado: indisponível e regras ativas','Ausência, normal e concluído fora da fila','Conclusão humana simulada e evidência JSON'],note='08:00–13:00 · Apresentador 1 até 10:30; Apresentador 2 até 13:00. Abrir painel; referência 17/11/2026, margem 5, limiar 0,70. Seguir ROTEIRO_20_MIN.md. Fonte: src/data/demo.py e docs/demo_ml.json.'),
        dict(title='Resultados no teste sintético',kind='metrics',body=[],note='13:00–14:30 · Apresentador 2. Fonte: docs/metricas.json. Limiar 0,25 escolhido na validação por F2 e orçamento ilustrativo de 45% de alertas. No teste, alertas 46,9%. Dummy precision não calculável por zero positivos previstos. AP usa average_precision_score. Resultados apenas sintéticos.'),
        dict(title='Erros e escolha do limiar',kind='confusion',body=[],note='14:30–16:00 · Apresentador 2. Fonte: docs/metricas.json. 173 TP, 165 FP, 53 FN, 329 TN no limiar 0,25. Comparar precision/recall com 0,70, o padrão inicial da interface. Regras+ML no teste sintético aumenta recall e também a carga de revisão. Não inferir redução de atrasos.'),
        dict(title='Limitações e ética',kind='text',body=['Métricas restritas à simulação','Falsos alertas e riscos não detectados','Dependência de conferência humana','Probabilidade t0; sem reavaliação diária','Sem validação operacional ou jurídica'],note='16:00–18:00 · Apresentador 1. Fonte: docs/LIMITACOES_ETICA.md. Sem WebSystem/INPI real; datas imutáveis; conclusão simulada; não apresentar homologação inexistente.'),
        dict(title='Próximos passos',kind='text',body=['Coleta de snapshots e desfechos reais','Validação temporal e calibração','Comparação com as regras e carga da equipe','Definição de parâmetros com responsáveis','Integração ao WebSystem após validação'],note='18:00–20:00 · Apresentador 2. Plano futuro, não resultado entregue. Coletar histórico com rótulos maduros e governança; avaliar benefício sobre controle determinístico antes da adoção. Reservar 10 minutos para perguntas.'),
    ]
    write('presentation/slides.json', json.dumps(slides,ensure_ascii=False,indent=2))
    supplements={
        'architecture': '''Módulos agrupados no MVP: 1/3/4 dados e validação; 5 snapshot t0; 6 inferência ML; 7 fatos e regras; 2/8 interface e painel; 9 decisão humana; 10 treino offline. Dados fornecem atributos ao modelo e fatos às regras. A inferência alimenta as regras, que alimentam painel e decisão humana; o treino offline fornece o artefato à inferência. A confirmação humana retorna aos dados. Diagrama completo e tabela de mapeamento no relatório técnico.''',
        'rules': '''| Condição | Resultado |
|---|---|
| Concluído | FORA_DA_FILA |
| Aberto, dias < 0 | VENCIDO |
| Aberto, 0 ≤ dias ≤ margem | URGENTE |
| Fora da margem, ausência ou risco ≥ limiar | ALTO |
| Demais abertos | NORMAL |

Memória de fatos, agenda, novos fatos e ponto fixo.''',
        'contract': '```json\n'+json.dumps(q['ml'],ensure_ascii=False,indent=2)+'\n```\n\nRisco vira motivo e candidato ALTO. Fallback: status indisponivel, prob_atraso null.',
        'data': '3.600 prazos, 1.200 processos, seed 20261117.\n\n| Partição | Prazos | Processos | Classe 0 | Classe 1 | t0 |\n|---|---:|---:|---:|---:|---|\n'+partitions+'\n\nDivisão temporal por processo; purga de 60 desfechos. Features t0: dias, carga, ausência, ato e situação. Fit só no treino.',
        'metrics': 'Teste sintético de 720 prazos. Limiar 0,25 na validação.\n\n| Modelo | Precision | Recall | F1 | AP | Brier |\n|---|---:|---:|---:|---:|---:|\n'+comparison+'\n\nPrecision do Dummy não é calculável porque não há positivos previstos.',
        'confusion': '| Real / Previsto | No prazo | Atraso |\n|---|---:|---:|\n| No prazo | 329 (TN) | 165 (FP) |\n| Atraso | 53 (FN) | 173 (TP) |\n\nLimiar 0,25: precision 51,2%, recall 76,5%. Limiar 0,70: precision 90,5%, recall 16,8%. Mais sensibilidade exige maior carga de revisão.',
    }
    write('presentation/SLIDES_CONTEUDO.md','\n\n'.join(f"## {i+1}. {s['title']}\n\n"+'\n'.join('- '+x for x in s['body'])+supplements.get(s['kind'],'')+f"\n\n**Notas:** {s['note']}" for i,s in enumerate(slides)))


if __name__=='__main__': build()
