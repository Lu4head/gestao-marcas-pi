import pandas as pd
import numpy as np
from src.data.synthetic import generate, split_temporal
from src.domain import FEATURES
from src.ml.train import metrics, select_threshold


def test_reproducible_generation_and_labels():
    a,b=generate(20),generate(20)
    pd.testing.assert_frame_equal(a,b)
    assert (a.y == (a.data_conclusao > a.data_limite).astype(int)).all()
    assert set(a.origem)=={'SINTETICO'}
    assert not {'prazo_id','processo_id','y','data_conclusao','desfecho_disponivel_em'} & set(FEATURES)


def test_split_has_no_process_or_temporal_leakage():
    train,val,test,purge=split_temporal(generate())
    assert not set(train.processo_id) & set(val.processo_id)
    assert not set(train.processo_id) & set(test.processo_id)
    assert not set(val.processo_id) & set(test.processo_id)
    assert train.desfecho_disponivel_em.max() < val.t0.min()
    assert val.desfecho_disponivel_em.max() < test.t0.min()
    assert sum(purge.values()) > 0


def test_transforms_fit_only_training_and_metrics_recompute(trained):
    root, report, predictor = trained
    train, _, _, _ = split_temporal(generate())
    prep = predictor.bundle['pipeline'].named_steps['preparo']
    scaler=prep.named_transformers_['numericas'].named_steps['escala']
    assert scaler.n_samples_seen_ == len(train)
    assert scaler.mean_[0] == np.mean(train.dias_restantes_t0)
    predictions=pd.read_csv(root/'docs/predicoes_teste_sintetico.csv')
    recalculated=metrics(predictions.y,predictions.prob_atraso,report['limiar_validacao'])
    for k in ['TP','FP','TN','FN','recall','f1','average_precision','brier']:
        assert np.isclose(recalculated[k],report['comparacao']['regressao_logistica'][k])


def test_undefined_precision_is_not_invented_zero():
    result=metrics([0,1], [0,0], .7)
    assert result['precision'] is None
    assert result['recall']==0
