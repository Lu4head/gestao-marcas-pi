from dataclasses import replace
import pandas as pd
import pytest
from src.data.demo import cases, REFERENCE
from src.integration.service import evaluate
from src.ml.inference import Predictor
from src.domain import FEATURES


def test_real_predict_proba_reaches_engine(trained):
    root, report, predictor = trained
    assert predictor.bundle is not None, predictor.error
    p = cases()[3]
    actual = predictor.bundle['pipeline'].predict_proba(pd.DataFrame([p.features()])[FEATURES])[0,1]
    r = evaluate(p, REFERENCE, predictor)
    assert r['ml']['prob_atraso'] == pytest.approx(actual)
    assert r['fatos_iniciais']['risco_ml'] == pytest.approx(actual)
    assert r['ml']['prazo_id'] == p.prazo_id
    assert r['ml']['modelo_versao'] == report['modelo_versao']
    assert r['ml']['gerado_em']
    assert ('RISCO_ML_ACIMA_LIMIAR' in r['motivos']) == (actual >= .7)
    low = evaluate(cases()[5], REFERENCE, predictor)
    assert actual != low['ml']['prob_atraso']


def test_T12_missing_model_and_minimum_features(trained, tmp_path):
    p = cases()[3]
    missing = Predictor(tmp_path/'inexistente.joblib')
    assert missing.bundle is None
    for predictor, item in [(missing,p), (trained[2],replace(p,carga_prazos_abertos_responsavel_t0=None))]:
        r = evaluate(item, REFERENCE, predictor)
        assert r['ml']['prob_atraso'] is None
        assert r['ml']['status']=='indisponivel'
        assert r['prioridade']=='NORMAL'
    assert evaluate(cases()[0], REFERENCE, missing)['prioridade']=='VENCIDO'


def test_corrupt_model_falls_back(trained, tmp_path):
    root = trained[0]
    (tmp_path/'manifesto.json').write_bytes((root/'models/manifesto.json').read_bytes())
    path = tmp_path/'modelo_sintetico.joblib'; path.write_bytes(b'corrompido')
    predictor = Predictor(path)
    assert predictor.bundle is None and 'Checksum' in predictor.error


def test_reference_changes_only_rules(trained):
    from datetime import timedelta
    p = cases()[3]
    a = evaluate(p,REFERENCE,trained[2]); b = evaluate(p,REFERENCE+timedelta(days=10),trained[2])
    assert a['ml']['prob_atraso'] == b['ml']['prob_atraso']
    assert b['prioridade']=='VENCIDO'
    assert a['data_limite']==b['data_limite']
