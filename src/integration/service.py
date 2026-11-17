from src.ia.engine import classify, Config
from src.integration.contract import unavailable


def evaluate(prazo, referencia, predictor=None, config=Config()):
    payload = predictor.predict(prazo) if predictor else unavailable(prazo.prazo_id)
    return classify(prazo, referencia, payload, config)
