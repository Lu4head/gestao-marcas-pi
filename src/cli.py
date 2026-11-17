import argparse
import json
from datetime import date
from src.data.demo import cases, REFERENCE
from src.ml.inference import Predictor
from src.integration.service import evaluate


def main():
    parser = argparse.ArgumentParser(description='Demo acadêmica sintética IA + ML')
    parser.add_argument('--sem-ml', action='store_true')
    parser.add_argument('--data', type=date.fromisoformat, default=REFERENCE)
    args = parser.parse_args()
    predictor = None if args.sem_ml else Predictor()
    print(json.dumps([evaluate(p, args.data, predictor) for p in cases()], ensure_ascii=False, indent=2, allow_nan=False))


if __name__ == '__main__':
    main()
