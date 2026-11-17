"""Treino offline reprodutível: python -m src.ml.train."""
from pathlib import Path
import hashlib
import json
import platform
from datetime import datetime, timezone
import joblib
import numpy as np
import pandas as pd
import sklearn
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.dummy import DummyClassifier
from sklearn.metrics import confusion_matrix, average_precision_score, brier_score_loss, accuracy_score
from sklearn.calibration import calibration_curve
from src.domain import NUMERIC, CATEGORICAL, FEATURES
from src.data.synthetic import generate, split_temporal, SEED

ROOT = Path(__file__).resolve().parents[2]


def pipeline(estimator):
    prep = ColumnTransformer([
        ('numericas', Pipeline([('imputacao', SimpleImputer(strategy='median')), ('escala', StandardScaler())]), NUMERIC),
        ('categorias', Pipeline([('imputacao', SimpleImputer(strategy='most_frequent')), ('onehot', OneHotEncoder(handle_unknown='ignore'))]), CATEGORICAL),
    ])
    return Pipeline([('preparo', prep), ('classificador', estimator)])


def metrics(y, probs, threshold):
    pred = np.asarray(probs) >= threshold
    tn, fp, fn, tp = [int(x) for x in confusion_matrix(y, pred, labels=[0, 1]).ravel()]
    ratio = lambda a, b: a/b if b else None
    return dict(limiar=float(threshold), suporte={'0': tn+fp, '1': tp+fn},
                TN=tn, FP=fp, FN=fn, TP=tp,
                precision=ratio(tp, tp+fp), recall=ratio(tp, tp+fn),
                f1=ratio(2*tp, 2*tp+fp+fn),
                average_precision=float(average_precision_score(y, probs)) if len(set(y))==2 else None,
                brier=float(brier_score_loss(y, probs)), acuracia=float(accuracy_score(y, pred)),
                fracao_alertas=float(np.mean(pred)))


def select_threshold(y, p):
    # Orçamento ilustrativo de até 45% de alertas; maximiza F2 só na validação.
    candidates = []
    for threshold in np.arange(.10, .91, .025):
        m = metrics(y, p, threshold)
        f2 = 5*m['TP']/(5*m['TP']+4*m['FN']+m['FP']) if (m['TP']+m['FN']+m['FP']) else 0
        if m['fracao_alertas'] <= .45:
            candidates.append((f2, float(threshold)))
    return max(candidates)[1] if candidates else .5


def run(root=ROOT):
    root = Path(root)
    for name in ['data', 'models', 'docs']:
        (root/name).mkdir(parents=True, exist_ok=True)
    df = generate()
    dataset = root/'data/synthetic_train.csv'
    df.to_csv(dataset, index=False)
    train, val, test, purge = split_temporal(df)
    for part in [train, val, test]:
        if set(part.y) != {0, 1}:
            raise ValueError('Partição sem ambas as classes: avaliação adiada')
    # Escolha arquitetural fixa: regressão regularizada. Não há busca no teste.
    models = {'dummy_majoritario': pipeline(DummyClassifier(strategy='most_frequent')),
              'regressao_logistica': pipeline(LogisticRegression(C=1.0, max_iter=1000, random_state=SEED))}
    for model in models.values():
        model.fit(train[FEATURES], train.y)
    chosen = models['regressao_logistica']
    threshold = select_threshold(val.y, chosen.predict_proba(val[FEATURES])[:, 1])
    report = dict(origem='SINTETICO', seed=SEED, dataset_sha256=hashlib.sha256(dataset.read_bytes()).hexdigest(),
                  features=FEATURES, purga=purge, criterio_limiar='Maximizar F2 com fração de alertas <= 0.45 na validação (orçamento ilustrativo)',
                  modelo_escolhido='regressao_logistica', limiar_validacao=threshold,
                  versoes={'python': platform.python_version(), 'sklearn': sklearn.__version__, 'numpy': np.__version__, 'pandas': pd.__version__},
                  particoes={}, comparacao={}, validade='Demonstração técnica sintética; sem validação jurídica ou operacional')
    for name, part in zip(['treino', 'validacao', 'teste'], [train, val, test]):
        report['particoes'][name] = dict(n=len(part), processos=int(part.processo_id.nunique()), inicio_t0=part.t0.min(),
                                       fim_t0=part.t0.max(), fim_desfecho=part.desfecho_disponivel_em.max(),
                                       suporte={str(int(k)): int(v) for k, v in part.y.value_counts().items()})
    for name, model in models.items():
        probs = model.predict_proba(test[FEATURES])[:, 1]
        report['comparacao'][name] = metrics(test.y, probs, threshold)
    report['logistica_limiar_ilustrativo_070'] = metrics(test.y, chosen.predict_proba(test[FEATURES])[:, 1], .70)
    report['validacao_logistica'] = metrics(val.y, chosen.predict_proba(val[FEATURES])[:, 1], threshold)
    ptest = chosen.predict_proba(test[FEATURES])[:, 1]
    observed, predicted = calibration_curve(test.y, ptest, n_bins=5, strategy='quantile')
    report['calibracao_teste'] = [dict(media_prevista=float(p), frequencia_observada=float(o)) for p, o in zip(predicted, observed)]
    # Comparação técnica no snapshot t0; sem simular que alertas evitariam atrasos.
    by_rules = (test.dias_restantes_t0 <= 5) | (test.responsavel_ausente_t0 == 1)
    integrated = by_rules | (ptest >= threshold)
    report['comparacao_priorizacao_t0'] = {'somente_regras': metrics(test.y, by_rules.astype(float), .5),
                                         'regras_com_ml': metrics(test.y, integrated.astype(float), .5)}
    # AP/Brier sobre rótulos duros não são medidas de probabilidade do agente.
    for m in report['comparacao_priorizacao_t0'].values():
        m.pop('average_precision'); m.pop('brier')
    output = root/'models/modelo_sintetico.joblib'
    version = 'logreg-sintetica-v1-'+report['dataset_sha256'][:10]
    joblib.dump(dict(pipeline=chosen, modelo_versao=version, origem='SINTETICO', features=FEATURES,
                     sklearn=sklearn.__version__, limiar_validacao=threshold), output)
    report['modelo_versao'] = version
    manifest = dict(modelo_versao=version, origem='SINTETICO', arquivo=output.name,
                    sha256=hashlib.sha256(output.read_bytes()).hexdigest(), sklearn=sklearn.__version__,
                    limiar_validacao=threshold, gerado_em=datetime.now(timezone.utc).isoformat())
    (root/'models/manifesto.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False)+'\n')
    (root/'docs/metricas.json').write_text(json.dumps(report, indent=2, ensure_ascii=False, allow_nan=False)+'\n')
    test_out = test[['prazo_id', 'processo_id', 'y']].copy()
    test_out['prob_atraso'] = ptest
    test_out['predicao'] = (ptest >= threshold).astype(int)
    test_out.to_csv(root/'docs/predicoes_teste_sintetico.csv', index=False)
    split = pd.concat([part[['prazo_id', 'processo_id']].assign(particao=name) for name, part in zip(['treino','validacao','teste'],[train,val,test])])
    split.to_csv(root/'docs/particoes.csv', index=False)
    return report


if __name__ == '__main__':
    report = run()
    print(json.dumps({k: report[k] for k in ['origem','modelo_versao','particoes','purga','limiar_validacao','comparacao']}, indent=2, ensure_ascii=False))
