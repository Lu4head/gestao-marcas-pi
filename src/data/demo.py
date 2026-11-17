from datetime import date
from src.domain import Prazo

REFERENCE = date(2026, 11, 17)


def cases():
    def make(id, deadline, t0, load, absent=False, closed=False, act='ACOMPANHAMENTO'):
        return Prazo(id, 'DEMO-'+id, date.fromisoformat(deadline), date.fromisoformat(t0),
                     closed, None if absent else 'Equipe demonstrativa', absent, act,
                     carga_prazos_abertos_responsavel_t0=load, responsavel_ausente_t0=absent)
    return [
        make('D01-VENCIDO', '2026-11-16', '2026-11-01', 8),
        make('D02-HOJE', '2026-11-17', '2026-11-02', 10),
        make('D03-MARGEM', '2026-11-22', '2026-11-10', 7),
        make('D04-RISCO', '2026-11-25', '2026-11-17', 60, act='EXIGENCIA'),
        make('D05-AUSENTE', '2026-11-29', '2026-11-17', 10, absent=True),
        make('D06-NORMAL', '2026-12-17', '2026-11-17', 2),
        make('D07-CONCLUIDO', '2026-11-07', '2026-11-01', 30, closed=True),
    ]
