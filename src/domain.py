"""Dados operacionais imutáveis; o snapshot t0 não acompanha a data do painel."""
from dataclasses import dataclass, asdict
from datetime import date
from numbers import Real
import math

NUMERIC = ['dias_restantes_t0', 'carga_prazos_abertos_responsavel_t0', 'responsavel_ausente_t0']
CATEGORICAL = ['tipo_ato', 'situacao_t0']
FEATURES = NUMERIC + CATEGORICAL


@dataclass(frozen=True)
class Prazo:
    prazo_id: str
    processo_id: str
    data_limite: date
    t0: date
    concluido: bool
    responsavel: str | None
    responsavel_ausente: bool
    tipo_ato: str
    situacao_t0: str = 'ABERTO'
    carga_prazos_abertos_responsavel_t0: float | None = None
    responsavel_ausente_t0: bool | None = None

    def __post_init__(self):
        if not all(isinstance(s, str) and s.strip() for s in [self.prazo_id, self.processo_id, self.tipo_ato]):
            raise ValueError('Identificadores e tipo de ato são obrigatórios')
        if type(self.data_limite) is not date or type(self.t0) is not date:
            raise ValueError('Datas devem ser date, sem conversão silenciosa')
        if self.t0 > self.data_limite:
            raise ValueError('Snapshot t0 posterior ao prazo não é suportado pelo ML desta versão')
        if type(self.concluido) is not bool or type(self.responsavel_ausente) is not bool:
            raise ValueError('Indicadores operacionais devem ser booleanos')
        if self.responsavel is not None and not isinstance(self.responsavel, str):
            raise ValueError('Responsável deve ser texto ou nulo')
        if self.responsavel_ausente_t0 is not None and type(self.responsavel_ausente_t0) is not bool:
            raise ValueError('Ausência t0 deve ser booleana ou nula')
        x = self.carga_prazos_abertos_responsavel_t0
        if x is not None and (isinstance(x, bool) or not isinstance(x, Real) or not math.isfinite(x) or x < 0):
            raise ValueError('Carga t0 deve ser finita e não negativa')

    def features(self):
        return dict(dias_restantes_t0=(self.data_limite-self.t0).days,
                    carga_prazos_abertos_responsavel_t0=self.carga_prazos_abertos_responsavel_t0,
                    responsavel_ausente_t0=None if self.responsavel_ausente_t0 is None else int(self.responsavel_ausente_t0),
                    tipo_ato=self.tipo_ato, situacao_t0=self.situacao_t0)

    def serializable(self):
        return {k: v.isoformat() if isinstance(v, date) else v for k, v in asdict(self).items()}
