"""streamlit run app.py -- dados exclusivamente de demonstração."""
import json
from dataclasses import replace
from pathlib import Path
from datetime import datetime, timezone
import pandas as pd
import streamlit as st
from src.data.demo import cases, REFERENCE
from src.ml.inference import Predictor
from src.integration.service import evaluate
from src.ia.engine import Config

st.set_page_config(page_title='Gestão de Marcas | PI', page_icon='📋', layout='wide')
st.title('Gestão de Marcas')
st.caption('Projeto Integrador · IA clássica e Ciência de Dados · Marco Final')
st.warning('Protótipo acadêmico — dados sintéticos; não validado para uso jurídico/operacional. A decisão continua humana.')
predictor = Predictor()
with st.sidebar:
    st.header('Demonstração')
    reference = st.date_input('Data de referência', REFERENCE, min_value=REFERENCE)
    use_ml = st.toggle('ML experimental sintético', value=True)
    margin = st.number_input('Margem interna (dias)', min_value=0, max_value=30, value=5, step=1)
    threshold = st.number_input('Limiar de risco ML', min_value=0., max_value=1., value=.70, step=.05, format='%.3f')
    st.caption('5 dias e 0,70 são parâmetros ilustrativos do Marco 2. Não definem prazos legais.')
    if predictor.bundle:
        st.caption(f"Limiar obtido na validação sintética: {predictor.bundle['limiar_validacao']:.3f}. O painel inicia com o exemplo 0,70.")
    st.caption('A probabilidade usa o snapshot fixo de t0. Alterar a referência só atualiza as regras de prazo.')
    st.button('Restaurar cenários', key='restaurar', on_click=lambda: (st.session_state.pop('concluidos', None), st.session_state.pop('auditoria', None)))
if not use_ml:
    st.info('Modo somente regras: status=indisponivel e prob_atraso=null.')
elif predictor.bundle is None:
    st.info('Modelo indisponível. As regras continuam funcionando. Execute: python -m src.ml.train')
    if predictor.error:
        with st.expander('Diagnóstico do modelo'):
            st.code(predictor.error)
else:
    st.caption(f"Modelo carregado: {predictor.bundle['modelo_versao']} · Probabilidades calculadas por predict_proba")

config = Config(int(margin), float(threshold))
closed = st.session_state.setdefault('concluidos', set())
audit = st.session_state.setdefault('auditoria', [])
prazos = [replace(p, concluido=True) if p.prazo_id in closed else p for p in cases()]
results = [evaluate(p, reference, predictor if use_ml else None, config) for p in prazos]
rank = {x:i for i,x in enumerate(['VENCIDO','URGENTE','ALTO','NORMAL','FORA_DA_FILA'])}
results.sort(key=lambda r:(rank[r['prioridade']], r['dias_restantes'], r['prazo_id']))
cols = st.columns(4)
for col, label in zip(cols, ['VENCIDO','URGENTE','ALTO','NORMAL']):
    col.metric(label, sum(r['prioridade']==label for r in results))
rows = [dict(Prazo=r['prazo_id'], Prioridade=r['prioridade'], Dias=r['dias_restantes'],
             Risco_ML=r['ml']['prob_atraso'], Status_ML=r['ml']['status'], Motivos=', '.join(r['motivos'])) for r in results]
frame = pd.DataFrame(rows)
analysis_tab, charts_tab = st.tabs(['Análise de prazos', 'Gráficos'])
with analysis_tab:
    st.dataframe(frame, hide_index=True, width='stretch',
                 column_config={'Risco_ML': st.column_config.NumberColumn('Risco sintético em t0', format='percent')})
    selected = st.selectbox('Inspecionar prazo', [r['prazo_id'] for r in results])
    r = next(r for r in results if r['prazo_id']==selected)
    p = next(p for p in prazos if p.prazo_id==selected)
    st.subheader(f"{r['prioridade']} · {selected}")
    st.write('**Motivos:** '+', '.join(r['motivos']))
    a,b = st.columns(2)
    with a:
        st.write('**Snapshot de ML em t0**')
        st.json(dict(t0=p.t0.isoformat(), **p.features()))
    with b:
        st.write('**Contrato ML → IA**')
        st.json(r['ml'])
    with st.expander('Fatos e encadeamento para a frente', expanded=False):
        st.write('Fatos iniciais'); st.json(r['fatos_iniciais'])
        for step in r['trilha']:
            st.write(f"Ciclo {step['ciclo']} · {step['regra']} · {step['descricao']}")
            st.json(step)
        st.write('Fatos no ponto fixo'); st.json(r['fatos_finais'])
    with st.expander('Revisão humana simulada'):
        st.caption('A confirmação muda apenas esta sessão local de demonstração. Datas-limite permanecem intactas.')
        if st.button('Confirmar conclusão simulada', key='confirmar', disabled=p.concluido):
            closed.add(selected)
            audit.append(dict(prazo_id=selected, acao='CONCLUSAO_SIMULADA', autor='Usuário da sessão demonstrativa',
                              instante=datetime.now(timezone.utc).isoformat(), inferencia=r))
            st.rerun()
        st.json(audit)
    st.download_button('Baixar evidência desta execução (JSON)',
                       json.dumps(dict(origem='SINTETICO', resultados=results, revisoes=audit), ensure_ascii=False, indent=2, allow_nan=False),
                       file_name='evidencia_demo_sintetica.json', mime='application/json')
    with st.expander('Resultados do treino sintético'):
        path = Path(__file__).parent/'docs/metricas.json'
        if path.exists():
            st.json(json.loads(path.read_text()))
        else:
            st.write('Relatório ainda não gerado.')

with charts_tab:
    st.subheader('Panorama dos prazos analisados')
    st.caption(
        f'Dados sintéticos da sessão · Referência: {reference:%d/%m/%Y}. '
        'Os gráficos acompanham os parâmetros e as conclusões simuladas.'
    )
    active = frame.loc[frame['Prioridade'] != 'FORA_DA_FILA'].copy()
    completed_count = len(frame) - len(active)
    st.write(f'{len(frame)} prazos analisados · {len(active)} na fila · {completed_count} concluídos fora da fila')

    st.subheader('Distribuição de prioridades')
    priority_counts = (
        active['Prioridade'].value_counts()
        .reindex(['VENCIDO', 'URGENTE', 'ALTO', 'NORMAL'], fill_value=0)
        .rename_axis('Prioridade').reset_index(name='Quantidade')
    )
    st.bar_chart(
        priority_counts, x='Prioridade', y='Quantidade', sort=False,
        x_label='Prioridade operacional', y_label='Quantidade de prazos',
        height=280, width='stretch',
    )
    st.caption('Somente prazos abertos. Concluídos ficam fora da fila operacional.')

    if active.empty:
        st.info('Todos os prazos estão concluídos. Restaure os cenários para visualizar a fila novamente.')
    else:
        st.subheader('Dias até o vencimento')
        st.bar_chart(
            active, x='Prazo', y='Dias', horizontal=True, sort=False,
            x_label='Prazo', y_label='Dias restantes',
            height=320, width='stretch',
        )
        st.caption('Valores negativos indicam vencimento passado; zero indica vencimento na data de referência.')

        st.subheader('Risco de atraso estimado pelo ML em t0')
        risk = active.loc[(active['Status_ML'] == 'ok') & active['Risco_ML'].notna(), ['Prazo', 'Risco_ML']].copy()
        if risk.empty:
            st.info('Risco ML indisponível para os prazos da fila. Nenhuma probabilidade foi atribuída.')
        else:
            risk['Probabilidade (%)'] = risk['Risco_ML'] * 100
            st.bar_chart(
                risk, x='Prazo', y='Probabilidade (%)', horizontal=True, sort=False,
                x_label='Prazo', y_label='Probabilidade de atraso (%)',
                height=320, width='stretch',
            )
            st.caption(
                f'Inferência experimental em dados sintéticos, sem validação operacional. '
                f'Limiar configurado: {threshold:.0%}. '
                f'Cobertura: {len(risk)} de {len(active)} prazos abertos. '
                'Probabilidades indisponíveis são omitidas. A estimativa permanece no snapshot de t0; '
                'alterar a data de referência não recalcula o risco diário.'
            )
