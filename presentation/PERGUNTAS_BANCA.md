# Defesa técnica — preparação para 10 minutos

1. **Qual é a IA clássica?** Fatos e regras de produção com encadeamento para a frente. A memória de trabalho recebe efeitos que habilitam regras em ciclos posteriores; a trilha documenta cada disparo. A resolução no ponto fixo aplica precedência.

2. **Por que não CSP?** O problema atual é classificar prioridades por condições operacionais, sem distribuir pessoas sob capacidade/restrições. Um CSP pode ser estudado quando houver alocação de tarefas.

3. **Por que não rede bayesiana?** Não temos estrutura causal nem probabilidades condicionais validadas. O modelo tabular é um experimento separado e regras preservam precedência de datas.

4. **O ML pode rebaixar urgentes?** Não. Apenas acrescenta motivo de risco e pode elevar um aberto fora da margem a ALTO. VENCIDO e URGENTE prevalecem. Concluídos saem da fila.

5. **Como a integração é comprovada?** O teste carrega o pipeline, calcula predict_proba, compara com o JSON e com o fato risco_ml usado pelo motor. O painel mostra a probabilidade e a versão. Desligar o ML remove o fato; não o substitui por uma constante.

6. **De onde vêm os dados?** Do gerador sintético com seed 20261117. São 1.200 processos e 3.600 prazos, com correlação por processo e ruído. Não são dados do INPI nem dos 19 processos citados na proposta.

7. **Qual é o alvo?** Providência concluída após a data-limite, y=1; no prazo, y=0. O gerador usa apenas conclusões conhecidas. Na coleta real, abertos vencidos também podem ser positivos após maturidade; cancelados e indeterminados devem ser excluídos.

8. **Como evitamos vazamento?** IDs e desfechos não entram nas features; processos não atravessam partições; treino antecede validação e teste; purgamos desfechos conhecidos tarde; imputação, escala e categorias são ajustadas só no treino. A previsão usa o snapshot t0.

9. **Por que regressão logística?** Classificação binária leve, regularização e coeficientes inspecionáveis. Foi uma escolha de projeto anterior à avaliação, comparada com Dummy. Não alegamos seleção entre todos os modelos do Marco 2.

10. **Como foi escolhido o limiar?** Na validação, maximizando F2 com até 45% de alertas, um orçamento hipotético. Resultado: 0.25. O teste não ajustou esse parâmetro. O painel começa em 0,70, valor ilustrativo do Marco 2, e permite alterá-lo.

11. **Por que precision, recall, F1 e AP?** Recall mede atrasos encontrados; precision mede quantos alertas correspondem a atrasos; F1 resume os dois; AP mede ordenação sem depender de um único limiar. Acurácia isolada pode recompensar a maioria. Brier avalia erro quadrático das probabilidades.

12. **Quantos erros ocorreram?** No limiar 0,25: TP=173, FP=165, FN=53, TN=329. Encontramos 76.5% dos atrasos sintéticos; 51.2% dos alertas eram positivos. Esses resultados não estimam os erros reais da equipe.

13. **O ML melhora as regras?** Na simulação, integrar risco ≥ 0,25 aumenta recall de 44,2% para 84,5%, mas alertas sobem de 28,6% para 56,5% e há mais falsos positivos. Isso mostra o custo de revisão, não comprova utilidade operacional nem redução causal de atrasos.

14. **A probabilidade é calibrada?** Calculamos Brier e cinco faixas de calibração no teste sintético. Há discrepâncias. Não houve recalibração nem validação real; 82,4% no demo não pode ser interpretado como frequência confiável em processos jurídicos.

15. **Dados sintéticos são suficientes?** Para provar que geração, treino, predição e regras executam, sim. Para afirmar eficácia real, não. O gerador inventa a distribuição e favorece relações que a logística consegue aprender. Precisamos de coleta e validação independentes.

16. **O que acontece sem modelo?** status indisponível e probabilidade nula; continuam regras de datas e ausência. Entradas operacionais inválidas são rejeitadas, não classificadas como normais silenciosamente.

17. **Por que não atualizar risco todos os dias?** O estudo define predição em t0. Atualizações diárias precisam de snapshots, rótulos e avaliação adequados. Hoje só os fatos temporais das regras mudam com a referência.

18. **Qual dano poderia ocorrer?** Um dado de prazo errado, falso negativo ou excesso de alarmes pode prejudicar a organização. O protótipo preserva datas, mostra motivos e exige decisão humana; isso não substitui validação de operação e segurança.

19. **O que não foi implementado?** Integração WebSystem/INPI, login real, persistência multiusuário, leitura RPI, protocolo, e-mail, vídeo de reserva e validação com histórico real. O arquivo de suporte não é apresentado como novo relatório formal obrigatório do roteiro.

20. **Como reproduzir?** Instalar requirements, treinar, rodar pytest e abrir Streamlit; seed, partições, hash, modelo, métricas e predições acompanham o pacote. Artefatos devem ser confiáveis; joblib não aceita uploads públicos seguros.
