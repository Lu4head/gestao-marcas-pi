"""Contrato não confiável: inconsistências sempre levam ao modo só regras."""
from datetime import datetime, timezone
from numbers import Real
import math


def unavailable(prazo_id):
    return dict(schema_version='1.0', prazo_id=prazo_id,
                gerado_em=datetime.now(timezone.utc).isoformat(), modelo_versao=None,
                status='indisponivel', prob_atraso=None)


def validate(payload, prazo_id):
    if not isinstance(payload, dict):
        return unavailable(prazo_id), 'Contrato ausente ou inválido'
    try:
        if payload['schema_version'] != '1.0' or payload['prazo_id'] != prazo_id:
            raise ValueError('Versão ou vínculo inválido')
        dt = datetime.fromisoformat(payload['gerado_em'])
        if dt.tzinfo is None:
            raise ValueError('Timestamp sem timezone')
        q, status, version = payload['prob_atraso'], payload['status'], payload['modelo_versao']
        if status == 'ok':
            if not (isinstance(q, Real) and not isinstance(q, bool) and math.isfinite(q) and 0 <= q <= 1):
                raise ValueError('Probabilidade inválida')
            if not (isinstance(version, str) and version.strip()):
                raise ValueError('Versão ausente')
        else:
            if not (status == 'indisponivel' and q is None and version is None):
                raise ValueError('Indisponibilidade contraditória')
        return dict(payload), None
    except (AssertionError, KeyError, TypeError, ValueError, OverflowError):
        return unavailable(prazo_id), 'Inferência rejeitada: contrato inconsistente'
