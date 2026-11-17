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
