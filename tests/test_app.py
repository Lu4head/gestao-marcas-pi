from pathlib import Path
import pyarrow as pa
from streamlit.testing.v1 import AppTest

APP=Path(__file__).resolve().parents[1]/'app.py'


def chart_frame(chart):
    return pa.ipc.open_stream(chart.proto.datasets[0].data.data).read_all().to_pandas()


def test_panel_ml_toggle_and_human_confirmation():
    app=AppTest.from_file(str(APP), default_timeout=30).run()
    assert not app.exception
    assert len(app.dataframe[0].value)==7
    assert [tab.label for tab in app.tabs] == ['Análise de prazos', 'Gráficos']
    charts = app.tabs[1].get('vega_lite_chart')
    assert len(charts) == 3
    assert chart_frame(charts[0]).set_index('Prioridade').Quantidade.to_dict() == {
        'VENCIDO': 1, 'URGENTE': 2, 'ALTO': 2, 'NORMAL': 1,
    }
    assert 'D07-CONCLUIDO' not in set(chart_frame(charts[1]).Prazo)
    risks = chart_frame(charts[2]).set_index('Prazo')['Probabilidade (%)']
    expected = app.dataframe[0].value.set_index('Prazo').loc[risks.index, 'Risco_ML'] * 100
    assert risks.to_dict() == expected.to_dict()
    app.toggle[0].set_value(False).run()
    assert not app.exception
    assert set(app.dataframe[0].value.Status_ML)=={'indisponivel'}
    assert len(app.tabs[1].get('vega_lite_chart')) == 2
    assert any('Risco ML indisponível' in info.value for info in app.tabs[1].info)
    app.selectbox[0].select('D04-RISCO').run()
    app.button(key='confirmar').click().run()
    assert not app.exception
    row=app.dataframe[0].value.set_index('Prazo').loc['D04-RISCO']
    assert row.Prioridade=='FORA_DA_FILA'
    charts = app.tabs[1].get('vega_lite_chart')
    assert chart_frame(charts[0]).Quantidade.sum() == 5
    assert 'D04-RISCO' not in set(chart_frame(charts[1]).Prazo)
    app.button(key='restaurar').click().run()
    assert not app.exception
    assert chart_frame(app.tabs[1].get('vega_lite_chart')[0]).Quantidade.sum() == 6


def test_panel_missing_artifact(monkeypatch, tmp_path):
    import src.ml.inference as inference
    real = inference.Predictor
    monkeypatch.setattr(inference, 'Predictor', lambda: real(tmp_path/'ausente.joblib'))
    app=AppTest.from_file(str(APP), default_timeout=30).run()
    assert not app.exception
    assert set(app.dataframe[0].value.Status_ML)=={'indisponivel'}
    assert app.metric[0].value=='1'
    assert len(app.tabs[1].get('vega_lite_chart')) == 2


def test_charts_reference_changes_and_empty_queue():
    from datetime import timedelta
    from src.data.demo import cases, REFERENCE

    app = AppTest.from_file(str(APP), default_timeout=30).run()
    days_before = chart_frame(app.tabs[1].get('vega_lite_chart')[1]).set_index('Prazo').Dias
    app.date_input[0].set_value(REFERENCE + timedelta(days=10)).run()
    assert not app.exception
    days_after = chart_frame(app.tabs[1].get('vega_lite_chart')[1]).set_index('Prazo').Dias
    assert (days_before - days_after).eq(10).all()
    app.session_state['concluidos'] = {p.prazo_id for p in cases()}
    app.run()
    assert not app.exception
    charts = app.tabs[1].get('vega_lite_chart')
    assert len(charts) == 1
    assert chart_frame(charts[0]).Quantidade.sum() == 0
    assert any('Todos os prazos estão concluídos' in info.value for info in app.tabs[1].info)
