# Prompt mestre — Codex — Projeto Integrador, Marco Final

> **Como usar:** colocar este arquivo e `CONTEXTO_PROJETO_INTEGRADOR.md` na raiz do repositório, com `AGENTS.md`. Abrir o diretório no Codex e enviar o texto **entre os marcadores** abaixo como primeira instrução. Não substituir o documento de contexto por um resumo curto.

--- INÍCIO DO PROMPT PARA O CODEX ---

Você atuará como **agente de engenharia de software e análise de dados** para finalizar, em **um único dia**, o Marco Final de um Projeto Integrador de Ciência da Computação (disciplinas: Inteligência Artificial e Ciência de Dados).

## 1. Contexto obrigatório e prioridades

**Antes de modificar qualquer arquivo**, leia integralmente:

1. `CONTEXTO_PROJETO_INTEGRADOR.md` — especificação fiel ao Marco 2 entregue e às exigências do Marco Final;
2. `AGENTS.md` — regras persistentes de implementação;
3. os arquivos existentes do repositório, caso existam.

**Projeto vigente:** “Gestão de Marcas — agente de apoio à priorização de prazos no WebSystem”. **Não** desenvolver o projeto antigo de entregas Olist. **Não** presumir que o WebSystem, integrações com INPI ou modelos do novo tema já existam. O Marco 2 fornecido é uma **proposta**, sem resultados de treinamento comprovados. Seu trabalho é construir um **MVP acadêmico independente e demonstrável**, não um produto comercial.

A banca avaliará: demonstração funcional, domínio técnico de IA, domínio técnico de ML, integração IA+ML e honestidade técnica/ética. Temos **um dia de execução** e **dois apresentadores**.

## 2. Resultado esperado

Entregue um **repositório funcional, reproduzível e autocontido**, contendo:

- um **motor de IA clássica real** com fatos e regras de produção, inferência por encadeamento para a frente, precedência e explicações;
- um componente de **ML supervisionado realmente treinado**, se houver dados adequados; na ausência de histórico real, usar exclusivamente **dados sintéticos declarados**, com treinamento e métricas verdadeiramente calculados no conjunto de teste sintético, **sem alegar validade real**;
- integração efetiva: `predict_proba` → contrato JSON com status/versão → fatos → motor de regras → prioridade e motivos;
- **fallback** operacional sem ML (`status=indisponivel`), com regras funcionando;
- aplicação local simples (preferencialmente **Streamlit**) que liste e explique prioridades e permita demonstrar vários cenários;
- **testes automatizados** cobrindo lógica, fronteiras, dados inválidos e integração;
- README com comandos exatos e relatório técnico com resultados obtidos, metodologia e limitações;
- apresentação da banca: preferencialmente `presentation/slides.pptx`, `presentation/ROTEIRO_20_MIN.md`, `presentation/PERGUNTAS_BANCA.md` e indicação de demo em cinco minutos. Se geração de PPTX não for possível com os recursos locais, produzir conteúdo integral dos slides em Markdown e informar a limitação — não simular arquivo inexistente;
- pacote final de entrega compactado em ZIP, caso tecnicamente possível.

**Não gere resultados fictícios nem reporte testes como executados sem executá-los.**

## 3. Requisitos funcionais mínimos

### 3.1. Dados operacionais

Cada prazo/providência deve ter, no mínimo, identificador, vínculo com processo, data-limite, situação de conclusão, responsável/ausência, tipo de ato e fatos suficientes para classificar. Manter data de referência explícita e configurável (para demonstração reproduzível). Separar **dados da inferência** de **dados históricos rotulados de treino**.

### 3.2. Regras do agente

Implemente exatamente a precedência especificada no documento de contexto:

1. concluído → `FORA_DA_FILA`;
2. aberto e prazo passado (`dias_restantes < 0`) → `VENCIDO`;
3. aberto e dentro da margem de segurança (`0 <= dias_restantes <= margem_interna`) → `URGENTE`;
4. aberto, não urgente, responsável ausente **ou** risco ML válido `>= limiar_ml` → `ALTO`;
5. demais casos → `NORMAL`.

Manter registro de **todos os motivos aplicáveis** e das regras disparadas, mesmo quando o maior nível prevalecer. Valores 5 dias e 0,70 são **exemplos operacionais** do Marco 2, não limiares validados. Não alterar datas-limite ou realizar ações reais no INPI. Demonstrar fatos e inferência por encadeamento para a frente, não apenas rótulos de saída.

### 3.3. Contrato e fallback

Use contrato com: `schema_version`, `prazo_id`, `gerado_em`, `modelo_versao`, `status` (`ok`/`indisponivel`) e `prob_atraso` (float de 0 a 1 ou nulo). `status=ok` exige valor válido e artefato efetivamente carregado; na indisponibilidade, retornar nulo e seguir somente regras. Validar inconsistências e erros de forma segura. Guardar versão da inferência e data de referência.

### 3.4. Machine Learning

Comece por inspecionar se há dataset histórico válido no repositório. Se não houver, **não pare o projeto**: forneça gerador sintético com seed fixa, README explicando as hipóteses e os limites e artefatos facilmente distinguíveis de dados reais.

Treinar ao menos um baseline Dummy e uma Regressão Logística regularizada. Compare Árvore de Decisão, Random Forest ou HistGradientBoosting **somente se houver tempo e amostra suficiente**. Usar pipeline com transformações ajustadas no treino e prevenir vazamento temporal/entre `processo_id` relacionados. Usar apenas atributos disponíveis em `t0`. Separar treino, validação e teste; escolher limiar apenas na validação. Reportar suporte das classes, precision, recall, F1, Average Precision (PR-AUC/AP), matriz de confusão e, quando viável, Brier/calibração. Métricas impossíveis devem ser explicitamente marcadas `não calculável`, nunca preenchidas com zero inventado.

Para mostrar **integração real**, o painel deverá chamar a função de inferência do modelo treinado e encaminhar o valor calculado ao motor lógico. Valores artificiais podem ser injetados **apenas em testes de unidade e exemplos claramente identificados**, jamais como a predição real da aplicação.

### 3.5. Demonstração

Permitir executar e explicar, com dados de demonstração, casos de prazo vencido, urgente, elevado risco previsto, ausência de responsável, normal, concluído e ML indisponível. Fornecer um botão/opção para alternar **modo com ML experimental** e **modo só regras**, sem mascarar o status real. Destacar no painel: “Protótipo acadêmico — dados sintéticos; não validado para uso jurídico/operacional”, quando aplicável.

## 4. Estratégia de execução (um dia)

Trabalhe em **fases curtas**, mas **execute as fases no repositório**, não entregue apenas um plano:

1. **Inspeção e scaffolding:** descobrir stack e arquivos; criar dependências mínimas e README inicial.
2. **Núcleo de IA:** implementar fatos, regras, encadeamento e testes de fronteira.
3. **Pipeline de dados e ML:** gerar/preparar dataset, treinar, comparar, avaliar e salvar modelo com versão.
4. **Integração:** adaptar contrato do Marco 2; provar em teste que `predict_proba` alimenta regra; tratar indisponibilidade.
5. **Interface e demonstração:** criar tela mínima com tabela, motivos e detalhe de inferência; testar localmente.
6. **Qualidade:** executar `pytest -q`, treino e smoke test do app; registrar comandos, outputs, exceções e correções.
7. **Material da banca:** diagrama fiel (com módulos simplificados identificados), slides, roteiro, perguntas prováveis e limitações; **apenas usar números gerados por execução**.
8. **Entrega:** conferir integridade do repositório, arquivo ZIP e passo a passo de demonstração.

Priorização: **P0** = regras, pipeline ML honesto, integração, teste, demonstração e material da apresentação; **P1** = filtros/gráficos adicionais; **fora do escopo** = login real, API INPI, WebSystem completo, notificações, jurídico e infraestrutura de produção.

## 5. Validações de aceite obrigatórias

Implemente e rode testes para os cenários T01–T12 descritos em `CONTEXTO_PROJETO_INTEGRADOR.md`, incluindo prioridades de fronteira (`-1`, `0`, `5`, `8` dias), concluído, ausência de responsável, ML indisponível, probabilidades inválidas e risco exatamente igual ao limiar.

Além disso, verifique:
- nenhum caso pode ter prioridade `NORMAL` se estiver vencido ou urgente;
- nenhuma decisão do ML altera prazos ou substitui a validação humana;
- sem artefato de ML, o painel e o motor de regras continuam funcionando;
- com artefato de ML, existe **predição efetiva**, não número fixo;
- dados sintéticos e validade limitada aparecem no app, relatório e slides;
- o script de treinamento e a avaliação produzem relatórios reais e reprodutíveis;
- comandos de execução descritos no README funcionam na prática.

## 6. Documentação e defesa acadêmica

O relatório e os slides devem separar explicitamente:

- **Marco 2 (planejamento):** arquitetura conceitual e exemplo ilustrativo de `0.78`;
- **Marco Final (execução):** arquivos construídos, testes realmente rodados, modelo de fato treinado, métricas calculadas e limitações observadas;
- **não implementado / trabalho futuro:** integração com WebSystem/INPI, histórico real suficiente, validação de desempenho no mundo real.

Distribuir a fala para **dois apresentadores não nomeados**, durante 20 min conforme o roteiro oficial: problema 2, arquitetura 4, dados 2, demonstração 5, métricas 3, limitações e ética 2, próximos passos 2. Preparar 10 min de defesa técnica com perguntas sobre: por que regras em vez de CSP/Rede Bayesiana; encadeamento para a frente; prevalência de prazos; como a probabilidade transita entre módulos; por que precisão/recall/PR-AUC; por que dados sintéticos não validam eficácia; falsos alertas e decisão humana.

## 7. Estilo de trabalho e comunicação

- Seja pragmático: respeite **um dia** de desenvolvimento.
- Não espere instruções novas para tarefas já definidas; avance com escolhas mínimas e registre suposições no README.
- Antes de alterar arquivos existentes, inspecione-os e preserve trabalho prévio relevante.
- Não exija serviços externos, credenciais, banco de dados de produção, APIs online ou frontend complexo.
- Execute comandos, valide resultados e corrija erros; se um requisito não puder ser atendido, entregue a melhor solução funcional e descreva exatamente o que falta.
- Não use métricas do projeto antigo Olist; não produza fake screenshots, saídas ou títulos de resultados inexistentes.
- Quando terminar, responda com **(a)** o que foi implementado e testado, **(b)** comandos para reproduzir, **(c)** arquivos de entrega, **(d)** evidências/métricas reais e origem dos dados, **(e)** limitações e pendências para os apresentadores.

**Comece agora lendo os dois documentos locais e inspecionando o repositório, depois implemente a fase 1 sem esperar novo pedido.**

--- FIM DO PROMPT PARA O CODEX ---
