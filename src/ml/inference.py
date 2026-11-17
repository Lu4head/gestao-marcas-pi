from pathlib import Path
import hashlib
import json
import math
from numbers import Real
import joblib
import pandas as pd
import sklearn
from src.domain import FEATURES
from src.integration.contract import unavailable, validate


class Predictor:
    """Carrega apenas o artefato local do projeto, verificando manifesto e versão."""
    def __init__(self, path=None):
        self.path = Path(path) if path else Path(__file__).resolve().parents[2]/'models/modelo_sintetico.joblib'
        self.bundle = None
        self.error = None
        try:
            manifest = json.loads(self.path.with_name('manifesto.json').read_text())
            if manifest['sha256'] != hashlib.sha256(self.path.read_bytes()).hexdigest():
                raise ValueError('Checksum do artefato diverge do manifesto')
            if manifest['sklearn'] != sklearn.__version__:
                raise ValueError('Versão sklearn diferente: retreine localmente')
            bundle = joblib.load(self.path)
            if bundle['features'] != FEATURES or bundle['origem'] != 'SINTETICO' or bundle['modelo_versao'] != manifest['modelo_versao']:
                raise ValueError('Metadados incompatíveis')
            if not callable(getattr(bundle['pipeline'], 'predict_proba', None)):
                raise ValueError('Artefato sem predict_proba')
            self.bundle = bundle
        except (OSError, ValueError, KeyError, TypeError, EOFError, ImportError, AttributeError, IndexError) as exc:
            self.error = f'{type(exc).__name__}: {exc}'

    def predict(self, prazo):
        payload = unavailable(prazo.prazo_id)
        if self.bundle is None:
            return payload
        features = prazo.features()
        if any(features[k] is None or features[k] == '' for k in FEATURES):
            return payload
        if any(not isinstance(features[k], Real) or not math.isfinite(features[k]) for k in FEATURES[:3]):
            return payload
        try:
            probabilities = self.bundle['pipeline'].predict_proba(pd.DataFrame([features])[FEATURES])
            classes = list(self.bundle['pipeline'].classes_)
            payload.update(status='ok', prob_atraso=float(probabilities[0, classes.index(1)]),
                           modelo_versao=self.bundle['modelo_versao'])
            return validate(payload, prazo.prazo_id)[0]
        except (ValueError, TypeError, KeyError, IndexError, AttributeError):
            return unavailable(prazo.prazo_id)
