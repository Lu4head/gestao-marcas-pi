import pytest
from src.ml.train import run
from src.ml.inference import Predictor


@pytest.fixture(scope='session')
def trained(tmp_path_factory):
    root = tmp_path_factory.mktemp('treino')
    report = run(root)
    return root, report, Predictor(root/'models/modelo_sintetico.joblib')
