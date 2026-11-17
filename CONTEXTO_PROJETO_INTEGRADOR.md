# Projeto Integrador — Contexto oficial e especificação de referência

**Projeto vigente:** Gestão de Marcas — agente de apoio à priorização de prazos no WebSystem  
**Curso:** Ciência da Computação, 8º semestre — 2º semestre de 2026  
**Disciplinas:** Inteligência Artificial e Ciência de Dados  
**Objetivo deste arquivo:** prover ao Codex um contexto autocontido, fiel ao Marco 2 entregue e ao roteiro do Marco Final, distinguindo fatos documentados, hipóteses e decisões de implementação para o protótipo acadêmico.  
**Execução pretendida:** um dia, dois integrantes apresentando.  
**Estado:** PLANEJAMENTO — este arquivo não é evidência de implementação nem de desempenho.

## 1. Documentos-fonte e hierarquia de autoridade

1. **`Marco2_Documento_Padrao_Entrega-1.docx` (preenchido):** referência primária do escopo vigente, arquitetura proposta, modelo de ML, regras, integração e limitações.
2. **`Marco3_Documento_Roteiro_e_Avaliacao (1).docx`:** referência primária dos requisitos da apresentação final e dos cinco critérios de avaliação.
3. **`Marco2_Documento_Padrao_Entrega.docx` (modelo vazio):** requisitos formais originais do Marco 2, para cotejo.
4. **`PI_Catalogo_Problemas_Alunos.docx`:** critérios gerais de um bom PI, incluindo necessidade da integração de IA clássica e aprendizado estatístico.
5. **`Marco1_ClassificadordeRiscodeEntregas.docx`:** registro histórico de um **escopo abandonado** (entregas da Olist). **Não** usar seu dataset, baseline, métricas ou problema como resultados do projeto atual.

Os arquivos DOCX de origem podem não estar no repositório entregue ao Codex; **todo o contexto operacional necessário está resumido aqui**. Havendo conflito entre este documento e o Marco 2 preenchido, priorize o Marco 2; requisitos de avaliação do Marco Final têm prioridade para a apresentação. Toda simplificação de escopo deve ser explicitamente identificada como decisão do MVP, não como algo já implementado no Marco 2.

## 2. Enquadramento do projeto

O projeto originalmente tratava de previsão de atrasos em entregas de e-commerce com dados Olist, mas houve uma **mudança oficial de escopo**. O trabalho a continuar é o **Marco 2 de Gestão de Marcas**. Não reutilizar os 96.470 pedidos, os 8,11% de atraso, a matriz de confusão ou qualquer métrica do projeto Olist no produto atual.

**Problema atual:** uma equipe acompanha marcas e processos administrativos do INPI, com atos e prazos que precisam ser conferidos, acompanhados e priorizados. O sistema deve apoiar o trabalho humano com uma fila de prioridades e motivos auditáveis. A consulta à Revista da Propriedade Industrial (RPI) é semanal e **humana**; o projeto não presume leitura automática da RPI, integração autenticada com o INPI nem automação jurídica.

**Perguntas das duas disciplinas:**
- **Ciência de Dados / ML:** a partir de dados históricos disponíveis no momento da decisão, qual é a probabilidade de uma providência **não ser concluída dentro do prazo**?
- **IA clássica:** dadas as datas validadas, condições do responsável e a evidência probabilística disponível, **que prioridade operacional deve ser atribuída**, com justificativa compreensível, preservando a precedência dos prazos?

**Natureza da solução:** sistema de **apoio** à decisão, não executor automático de atos perante o INPI. A equipe continua responsável por conferir fatos, validar prazos, executar providências e registrar a conclusão.

## 3. O que o Marco 2 realmente comprova

O Marco 2 **documenta uma proposta de arquitetura e contrato de integração**. Ele **não comprova** que os módulos estejam implementados, que exista dataset histórico rotulado suficiente ou que modelos tenham sido treinados/testados. A carteira inicial mencionada é de **19 processos**, que **não equivalem a 19 exemplos independentes rotulados**. Um processo pode ter vários prazos correlacionados.

| Elemento | Condição no Marco 2 |
|---|---|
| Problema, premissas e módulos | Definidos conceitualmente |
| Arquitetura de 10 módulos | Diagramada e descrita, sem comprovação de execução |
| Representação de fatos e regras | Proposta: regras de produção e encadeamento para a frente |
| Interface entre ML e IA | Contrato JSON ilustrativo proposto |
| Base histórica suficiente | **Não comprovada** |
| Modelos treinados e baseline no escopo atual | **Não comprovados** |
| Métricas do modelo final | **Indisponíveis** |
| Implementação do WebSystem completo | Não comprovada e desnecessária para o MVP acadêmico |

**Regra de integridade acadêmica:** não afirmar que exemplos fictícios ou planos são experimentos realizados; não apresentar valores de probabilidade digitados manualmente como predições reais.

## 4. Arquitetura do Marco 2 — módulos originais

A arquitetura publicada no Marco 2 distingue, por cor, o sistema operacional de base (azul) da extensão acadêmica de IA/ML (amarelo). Os números originais são:

1. **Entrada humana:** planilha mestre dos processos e atos identificados na consulta humana semanal à RPI; registros conferidos.
2. **WebSystem — interface, autenticação e permissões:** recebe entradas e ações autorizadas, mostra a fila.
3. **API de domínio e validação:** valida carteira, titular, marca, processo, ato, prazo, situação, responsável, revisor e suplente.
4. **Persistência e histórico:** armazena carteira, prazos, providências e histórico/auditoria.
5. **Preparação de atributos:** forma *snapshot* no instante da decisão `t0`, com variáveis disponíveis então.
6. **Inferência de ML:** recebe atributos e modelo versionado; retorna probabilidade de atraso (0 a 1), versão e instante, ou indisponibilidade.
7. **IA clássica — motor de regras:** recebe fatos operacionais validados e, quando houver, risco do ML; emite prioridade, motivos e necessidade de revisão.
8. **Painel operacional:** apresenta vencidos, urgentes, próximos, filtros e justificativas.
9. **Decisão humana:** responsável/revisor/suplente confere, providencia e registra conclusão; a confirmação alimenta o histórico.
10. **Treino e avaliação offline:** recebe snapshots e desfechos maduros; treina, avalia e versiona o modelo fora da requisição operacional.

**Fluxos fundamentais:** 1→2→3↔4; 4→5→6→7→8→9→2, com 3→7 fornecendo fatos e datas validados; 4→10 alimenta treino, e 10 disponibiliza modelo versionado para 6 após validação.

### 4.1. Mapeamento para MVP acadêmico de um dia (decisão de implementação)

Implementar um protótipo **independente** e executável localmente, sem construir um WebSystem comercial inteiro:

| Módulo original | Implementação mínima proposta |
|---|---|
| 1, 3 e 4 | CSV/objetos tipados de **dados de demonstração**, validação de entradas e estado local; opcional registro simples das ações |
| 2 e 8 | Interface Streamlit ou CLI clara para demonstração, sem login real |
| 5 | Pipeline de preparação de atributos versionável |
| 6 | `predict_proba` de um classificador **treinado** ou status explícito `indisponivel` |
| 7 | Motor próprio de regras/fatos e inferência explicável |
| 9 | Aprovação/revisão **simulada na interface**, sempre exigindo humano; sem protocolar atos reais |
| 10 | Script reprodutível de treinamento/avaliação offline |

Esse recorte deve ser identificado como **protótipo acadêmico**, sem fingir a existência de uma integração real com WebSystem ou INPI.

## 5. Definição da tarefa de ML conforme Marco 2

**Unidade de predição:** uma providência/prazo (`prazo_id`) vinculada a um processo (`processo_id`).

**Instante de predição:** `t0`, primeira validação humana do prazo. A primeira versão prevê somente nesse instante: **não** alegar validade para atualizações diárias.

**Rótulo proposto (`y`):**
- `1`: a providência obrigatória termina **após** a data-limite, ou permanece aberta depois dessa data, quando o desfecho já pode ser confirmado;
- `0`: providência concluída **até** a data-limite;
- prazos cancelados, ainda não vencidos/sem desfecho maduro ou com resultado indeterminado **não recebem rótulo de treino**.

**Atributos citados no Marco 2 (disponíveis em `t0`):**
- `dias_restantes_t0` (calculados com data validada);
- `tipo_ato`;
- `situacao` do prazo/processo no instante de decisão;
- `prioridade_operacional_t0` (quando realmente existente antes da predição; não usar prioridade calculada depois pelo agente);
- `carga_prazos_abertos_responsavel_t0`;
- `responsavel_ausente_t0`.

Tratamentos de ausentes, codificação categórica e escala numérica devem ser ajustados **somente** no treino. IDs servem para ligação e auditoria, **não** como features. Não usar como atributo preditivo: data de conclusão, estado futuro, atraso observado, resultado do motor de regras, carga calculada após `t0` ou informação de etapa posterior; isso produziria **data leakage**.

**Modelos candidatos da seção 3:**
- Dummy majoritário (baseline mínimo);
- Regressão Logística regularizada (candidata preferencial, **não escolhida empiricamente**);
- Árvore de Decisão com poda;
- Random Forest;
- HistGradientBoosting.

**Métricas indicadas:** recall da classe atraso, precision, F1-score, PR-AUC por **Average Precision**, acurácia, matriz de confusão, Brier score e análise de calibração quando viável. Limiar deve ser decidido por validação e capacidade de revisão humana, nunca otimizado diretamente no teste. Registrar TP, FP, TN, FN e suporte das classes. Usar `average_precision_score` para PR-AUC/AP, distinguindo de integrais alternativas de curva precisão-revocação.

**Divisão dos dados:** preferência por avaliação temporal, mantendo processos relacionados fora de treino e teste simultaneamente. Se houver tamanho muito pequeno ou classe ausente, declarar que a métrica não pode ser estimada. Não forçar uma seleção de modelo sem evidência.

## 6. Ausência de dados reais: dois modos honestos

### 6.1. Modo A — regras determinísticas (obrigatório)

Pode funcionar com casos operacionais de demonstração e **sem** modelo treinado. `status = indisponivel`, `prob_atraso = null`; a inferência usa apenas fatos verificados. Essa operação já está prevista pelo Marco 2.

### 6.2. Modo B — ML experimental sintético (opcional, desejável para a banca)

Caso não seja fornecido histórico real rotulado, criar um dataset **sintético reprodutível** apenas para demonstrar a cadeia real: geração de exemplos com rótulo, preparo, treinamento, métricas obtidas por execução, carregamento do artefato, `predict_proba` e consumo automático das probabilidades pelo motor lógico. O componente **executa código real de ML**, mas sua validade é **somente técnica em dados artificiais**.

Regras para o gerador experimental:
- usar `seed` fixa e explicar como os cenários foram gerados;
- criar variações razoáveis nos atributos do `t0` e rótulos, sem embutir diretamente o desfecho como entrada;
- não derivar as prioridades do agente como atributos do modelo;
- evitar resultados artificialmente perfeitos, não manipular o teste para obter nota;
- **identificar em interface, relatório e slides** que dados e métricas são sintéticos e não demonstram eficácia com processos reais;
- considerar grupo por `processo_id` para evitar vazamento entre registros relacionados;
- reservar casos de demonstração separados dos exemplos do treino;
- se não houver inferência legítima disponível, mostrar indisponibilidade; nunca preencher `prob_atraso` com um número falso como se tivesse sido calculado pelo modelo.

Os 19 processos citados são referência de escopo de implantação, **não uma base rotulada disponível**. Não afirmar contato com cliente, equipe jurídica, dados do INPI ou validação de regras legais que não existiu.

## 7. Contrato de integração ML → IA, conforme Marco 2

O contrato proposto pela seção 2.1 do Marco 2 é um objeto JSON de inferência:

```json
{
  "schema_version": "1.0",
  "prazo_id": "PZ-001",
  "gerado_em": "2026-11-08T10:00:00-03:00",
  "modelo_versao": "logreg-candidata-v1",
  "status": "ok",
  "prob_atraso": 0.78
}
```

**Atenção:** o valor `0.78` e o identificador do modelo são **exemplo numérico do documento**, não inferência real. No MVP, `prob_atraso` precisa ser retornado por `predict_proba` quando `status=ok`; se não existir modelo treinado/validado ou dados mínimos, retornar:

```json
{
  "schema_version": "1.0",
  "prazo_id": "PZ-001",
  "gerado_em": "2026-11-08T10:00:00-03:00",
  "modelo_versao": null,
  "status": "indisponivel",
  "prob_atraso": null
}
```

**Fatos validados entregues em paralelo**, e não inferidos do ML: `data_referencia`, `data_limite`, `dias_restantes`, `concluido`, `responsavel_ausente` e outros metadados necessários. Não aceitar `prob_atraso` fora de `[0,1]` ou status contraditórios como predição válida. Datas de referência devem ser parametrizáveis para testes reprodutíveis; usar ISO 8601 e datas locais sem conversões silenciosas.

## 8. IA clássica — regras e encadeamento para a frente

**Técnica explicitada pelo Marco 2:** representação de fatos e regras de produção, com inferência lógica por **encadeamento para a frente**. Não chamar simplesmente uma sequência opaca de `if/else` de motor de inferência sem demonstrar fatos, disparo de regras e justificativas. Uma implementação compacta com `Rule`, `Fact`, agenda de disparos e trilha de regras é suficiente.

**Fatos exemplificativos do documento:** `prazo_aberto(P)`, `dias_restantes(P,D)`, `responsavel_ausente(P)` e `risco_ml(P,Q)`.

**Precedência estabelecida:** `VENCIDO > URGENTE > ALTO > NORMAL`; `CONCLUIDO` fica fora da fila. Concretização do exemplo didático:

1. Se concluído, retirar da fila operacional (`FORA_DA_FILA`/`CONCLUIDO`); essa condição prevalece mesmo se a data já passou.
2. Se ainda aberto e `dias_restantes < 0`, `VENCIDO`.
3. Se aberto e `0 <= dias_restantes <= margem_interna`, `URGENTE`.
4. Se aberto, não vencido e não urgente, com `responsavel_ausente = true` **ou** (`status=ok` e `prob_atraso >= limiar_ml`), `ALTO`.
5. Caso contrário, `NORMAL`.
6. Registrar **todos os motivos aplicáveis** no relatório de inferência, mesmo quando a maior precedência determina a categoria.
7. Nenhuma saída de ML pode rebaixar `VENCIDO` ou `URGENTE`, alterar data-limite, declarar conclusão automática ou gerar atos jurídicos.

**Parâmetros meramente ilustrativos do Marco 2:** `margem_interna=5 dias` e `limiar_ml=0.70`. Expor como configuração de demonstração, não atribuir aprovação jurídica ou calibração experimental a esses valores. No exemplo da seção 2.1, faltam oito dias e probabilidade ilustrativa de 78%: prioridade ALTO, motivo `RISCO_ML_ACIMA_LIMIAR`; data-limite permanece intacta.

**Justificativa da técnica:** regras de produção são rastreáveis, auditáveis, têm precedência operacional explícita e preservam vencidos/urgentes mesmo que o ML falhe. O Marco 2 não escolhe CSP ou Redes Bayesianas e considera distribuição de tarefas sob restrições um problema futuro.

## 9. Casos de teste mínimos exigidos para a demonstração

Usar `data_referencia` fixa em testes e construir casos separados (valores de probabilidades abaixo são **entradas controladas de teste do motor**, não saídas ML, a menos que produzidos em execução real):

| ID | Condição | Esperado |
|---|---|---|
| T01 | aberto, dias_restantes = -1, risco = 0.05 | VENCIDO |
| T02 | aberto, dias_restantes = 0 | URGENTE |
| T03 | aberto, dias_restantes = 5 | URGENTE |
| T04 | aberto, dias_restantes = 8, risco ML = 0.78, `status=ok` | ALTO, motivo risco |
| T05 | aberto, dias_restantes = 8, sem responsável, ML indisponível | ALTO, motivo responsável |
| T06 | aberto, dias_restantes = 20, risco 0.15 | NORMAL |
| T07 | concluído, dias_restantes = -10 | FORA_DA_FILA |
| T08 | aberto, dias_restantes = 3, risco ML alto | URGENTE; ML não rebaixa a urgência |
| T09 | aberto, dias_restantes = 12, `status=indisponivel` | NORMAL se houver responsável |
| T10 | probabilidade inválida (<0, >1, NaN), status contraditório | Rejeitar inferência e fazer fallback |
| T11 | risco exatamente igual a limiar, prazo não urgente | ALTO (comparação `>=`) |
| T12 | dado mínimo ausente ou modelo ausente | ML indisponível; regras ainda funcionam quando há dados operacionais suficientes |

Testes de integração devem conferir que a probabilidade **efetivamente gerada por modelo carregado** é a que chega à IA, com `prazo_id`, versão, timestamp e motivos consistentes. Separar teste de regras com entradas fixas do teste ponta a ponta com `predict_proba`.

## 10. Requisitos éticos, técnicos e de segurança

- Não automatizar consulta à RPI, integração INPI, petições, emissão de GRU, peças jurídicas, decisões jurídicas ou atendimento externo.
- Não transformar configurações operacionais de demonstração em prazos jurídicos oficiais.
- A decisão sobre providências continua humana; interface deve ressaltar o caráter consultivo.
- Evitar dados pessoais identificáveis no dataset sintético ou nos slides; dados do titular não são necessários como features de ML.
- Registrar versão de dados/modelo, timestamp, parâmetros e motivos de cada classificação quando viável.
- Não inventar histórico, métricas, avaliações, testes executados ou homologação com equipe externa.
- Declarar o risco de alarmes falsos, falsos negativos, mudança de operação, baixa calibração, viés, dados incompletos e desatualização da conferência humana.
- A execução local deve funcionar sem credenciais, APIs externas, chaves privadas ou dependência de rede após instalação das bibliotecas.

## 11. Entregáveis acadêmicos do Marco Final

A ficha de avaliação do documento oficial tem **cinco critérios de 0 a 2 pontos**:

1. **Demonstração funcional:** agente rodando de verdade, ao vivo ou vídeo gravado, não slides estáticos.
2. **Domínio técnico de IA:** defender regras de produção, representação e encadeamento para a frente.
3. **Domínio técnico de ML:** defender modelagem, métricas e limitações do modelo treinado, se houver.
4. **Integração IA + ML:** conexão funcional e visível, não apenas diagrama.
5. **Honestidade técnica e ética:** limitações e riscos expostos sem inflar resultados.

**Formato da banca:** 20 min de apresentação + 10 min de perguntas. Estrutura sugerida:

| Bloco | Minutos |
|---|---:|
| Problema | 2 |
| Arquitetura completa, IA e ML e integração | 4 |
| Dataset e pré-processamento | 2 |
| Demonstração real | 5 |
| Resultados e métricas | 3 |
| Limitações e ética | 2 |
| Próximos passos | 2 |

A apresentação será realizada por **dois apresentadores**, identificados no roteiro como Apresentador 1 e Apresentador 2.

**Não existe no roteiro oficial exigência explícita de um novo relatório escrito obrigatório.** É prudente produzir `README.md`, resultados reprodutíveis e relatório técnico curto como documentação de apoio, além dos slides e projeto executável. Não afirmar que um novo arquivo DOCX/PDF escrito é exigido pela banca sem confirmação.

## 12. Escopo de desenvolvimento recomendado para um dia — novas decisões, não fatos do Marco 2

**P0 — imprescindível:**
1. Repositório Python executável, dados demonstrativos e configuração fixa/reprodutível;
2. Motor lógico com fatos/regras e explicações, testes de fronteira e fallback;
3. Treino reprodutível de ML sintético **se não houver histórico real**, com artefato e métricas reais **sobre dados sintéticos**, identificadas como tal;
4. Integração real via `predict_proba` → contrato JSON → fatos/regra → prioridade;
5. Visualização simples que permita demonstrar vencidos, urgentes, altos e normais;
6. Testes automatizados e ensaio de ponta a ponta;
7. Slides, roteiro e relatório de limitações.

**P1 — se sobrar tempo:** filtros de painel, gráficos extras, comparação modo regras vs. experimental, histórico simples de revisões, vídeo reserva.

**Fora do escopo de um dia:** login, controle de acesso comercial, banco de dados de produção, implantação WebSystem, integração real INPI, workflow jurídico, notificações por e-mail, painéis administrativos completos, inferência contínua diária, garantia de desempenho operacional.

**Stack sugerida (não é decisão oficial):** Python 3.11+, pandas, numpy, scikit-learn, Streamlit, pytest, joblib, matplotlib (se útil). Usar dependências mínimas e execução local; um arquivo CSV simples atende ao demo. Não aumentar escopo com Django/FastAPI/Oracle ou banco de dados se não necessário.

## 13. Estrutura de repositório esperada (sugestão)

```text
gestao-marcas-pi/
├── AGENTS.md                        # Instruções locais para o Codex
├── CONTEXTO_PROJETO_INTEGRADOR.md   # Este documento
├── README.md                        # Requisitos e comandos de execução
├── requirements.txt
├── app.py                           # Streamlit; CLI também pode ser disponibilizada
├── data/
│   ├── synthetic_train.csv
│   └── demo_prazos.csv
├── models/                          # Artefatos versionados e manifesto
├── src/
│   ├── data/                        # geração, validação, features
│   ├── ml/                          # treino, avaliação, inferência
│   ├── ia/                          # fatos, regras, motor de inferência
│   └── integration/                 # contrato, orquestração
├── tests/
│   ├── test_rules.py
│   ├── test_integration.py
│   └── test_ml_pipeline.py
├── docs/
│   ├── RELATORIO_TECNICO.md
│   ├── RESULTADOS_EXECUCAO.md
│   └── LIMITACOES_ETICA.md
└── presentation/
    ├── ROTEIRO_20_MIN.md
    ├── PERGUNTAS_BANCA.md
    └── slides.pptx                   # Se houver suporte para criação
```

Este é um **alvo**. Caso haja estrutura já existente, o Codex deve preservá-la e adaptar-se. Não é necessário preencher arquivos vazios para simular completude.

## 14. Critérios de aceite para concluir o MVP

- [ ] Instalação e execução documentadas e verificadas;
- [ ] Dataset de origem declarada: real (se houver) ou sintético;
- [ ] Fonte e maturidade dos rótulos compreendidas; sem vazamento conhecido;
- [ ] Pipeline de ML treinado e artefato carregado **se o modo ML estiver habilitado**;
- [ ] Métricas extraídas de execução, com origem dos dados claramente indicada;
- [ ] Modo regras funciona **sem** modelo, sem probabilidades fictícias;
- [ ] Motor de inferência retorna prioridade e todos os motivos aplicáveis;
- [ ] Integração recebe `predict_proba` real e não valores fixos disfarçados;
- [ ] Regras mantêm precedência e nunca alteram datas-limite;
- [ ] Testes mínimos executados, status reportado corretamente;
- [ ] Aplicação local inicia e permite demonstrar casos variados;
- [ ] Slides e roteiro de 20 min produzidos, com 5 min de demonstração;
- [ ] Riscos e limitações expostos, incluindo falta de validação real do ML;
- [ ] Dois apresentadores têm tarefas de fala atribuídas.

## 15. Ordem de implementação recomendada ao Codex

1. Ler `CONTEXTO_PROJETO_INTEGRADOR.md` e `AGENTS.md`.
2. Inspecionar arquivos existentes; não sobrescrever sem avaliar.
3. Implementar **fatos, regras e testes** primeiro para garantir núcleo demonstrável.
4. Implementar dataset sintético **somente se dados reais não estiverem no repositório**; geração com seed e origem evidente.
5. Implementar treino, split seguro, métricas e inferência versionada.
6. Integrar inferência ao motor lógico e validar fallback.
7. Construir Streamlit simples e determinístico para demonstração.
8. Executar testes, salvar outputs reais e corrigir bugs.
9. Escrever documentação, criar slides/roteiro usando apenas resultados verificados.
10. Finalizar um pacote de entrega fácil de abrir e executar.

**Princípio final:** um agente acadêmico simples, rodando, com IA clássica real, componente de ML real (mesmo que experimental com dados artificiais) e limitações honestas é mais defensável do que prometer um WebSystem inteiro.
