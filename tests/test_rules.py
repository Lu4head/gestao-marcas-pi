"""T01–T12: probabilidades controladas exclusivamente para testes de regras."""
from dataclasses import replace
from datetime import date, timedelta
import pytest
from src.domain import Prazo
from src.ia.engine import classify, Config
from src.integration.contract import unavailable

REF = date(2026, 11, 17)


def prazo(days, absent=False, closed=False):
    return Prazo('TESTE', 'PROC-TESTE', REF+timedelta(days=days), REF-timedelta(days=50),
                 closed, None if absent else 'Responsável teste', absent, 'EXIGENCIA',
                 carga_prazos_abertos_responsavel_t0=10, responsavel_ausente_t0=False)


def controlled(prob):
    p = unavailable('TESTE')
    if prob is not None:
        p.update(status='ok', prob_atraso=prob, modelo_versao='ENTRADA_CONTROLADA_TESTE')
    return p


@pytest.mark.parametrize('id,days,q,absent,closed,expected', [
    ('T01',-1,.05,False,False,'VENCIDO'), ('T02',0,None,False,False,'URGENTE'),
    ('T03',5,None,False,False,'URGENTE'), ('T04',8,.78,False,False,'ALTO'),
    ('T05',8,None,True,False,'ALTO'), ('T06',20,.15,False,False,'NORMAL'),
    ('T07',-10,.95,True,True,'FORA_DA_FILA'), ('T08',3,.95,False,False,'URGENTE'),
    ('T09',12,None,False,False,'NORMAL'), ('T11',8,.70,False,False,'ALTO'),
])
def test_required(id, days, q, absent, closed, expected):
    p = prazo(days, absent, closed)
    r = classify(p, REF, controlled(q))
    assert r['prioridade'] == expected
    assert r['data_limite'] == p.data_limite.isoformat()
    if id in ['T04', 'T08', 'T11']:
        assert 'RISCO_ML_ACIMA_LIMIAR' in r['motivos']
    if id == 'T05':
        assert 'RESPONSAVEL_AUSENTE' in r['motivos']


@pytest.mark.parametrize('key,value', [('prob_atraso',-.1), ('prob_atraso',1.1), ('prob_atraso',float('nan')),
    ('prob_atraso',float('inf')), ('prob_atraso',True), ('prob_atraso','0.9'),
    ('status','indisponivel'), ('schema_version','2'), ('prazo_id','OUTRO'),
    ('gerado_em','ontem'), ('gerado_em','2026-11-17T12:00:00'), ('modelo_versao',None)])
def test_T10_invalid_contract(key, value):
    payload = controlled(.95); payload[key] = value
    r = classify(prazo(12), REF, payload)
    assert r['prioridade'] == 'NORMAL'
    assert r['ml']['status'] == 'indisponivel' and r['ml']['prob_atraso'] is None
    assert r['aviso']


def test_trace_records_all_reasons_and_multiple_cycles():
    r = classify(prazo(-1, True), REF, controlled(.99))
    assert r['prioridade'] == 'VENCIDO'
    assert set(r['motivos']) == {'PRAZO_VENCIDO','RESPONSAVEL_AUSENTE','RISCO_ML_ACIMA_LIMIAR'}
    assert max(s['ciclo'] for s in r['trilha']) >= 3
    r2 = classify(prazo(12), REF, controlled(.99))
    assert any(s['regra']=='R7' and 'motivo_RISCO_ML_ACIMA_LIMIAR' in s['fatos_consultados'] for s in r2['trilha'])


@pytest.mark.parametrize('days', range(-20,6))
def test_never_normal_when_overdue_or_urgent(days):
    for q in [None, 0., 1.]:
        assert classify(prazo(days), REF, controlled(q))['prioridade'] in {'VENCIDO','URGENTE'}


@pytest.mark.parametrize('kwargs', [{'margem_interna':-1}, {'margem_interna':1.5}, {'limiar_ml':float('nan')}, {'limiar_ml':1.01}])
def test_bad_configuration(kwargs):
    with pytest.raises(ValueError): Config(**kwargs)


def test_bad_operational_data():
    with pytest.raises(ValueError): replace(prazo(10), data_limite=None)
    with pytest.raises(ValueError): replace(prazo(10), concluido='false')
    with pytest.raises(ValueError): replace(prazo(10), prazo_id='')
    with pytest.raises(ValueError): classify(prazo(10), REF-timedelta(days=51), controlled(None))
