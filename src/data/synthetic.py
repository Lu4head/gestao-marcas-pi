"""Simulação técnica, sem origem INPI e sem validade empírica no domínio."""
from datetime import date, timedelta
import numpy as np
import pandas as pd

SEED = 20261117


def generate(n_processos=1200, seed=SEED):
    rng = np.random.default_rng(seed)
    rows = []
    for g in range(n_processos):
        latent = rng.normal(0, .5)  # correlação oculta entre prazos do mesmo processo
        for j in range(3):
            t0 = date(2019, 1, 1) + timedelta(days=g*2+j)
            days = int(rng.integers(1, 36))
            load = int(rng.integers(0, 61))
            absent = int(rng.random() < .16)
            act = str(rng.choice(['EXIGENCIA', 'MANIFESTACAO', 'PAGAMENTO', 'ACOMPANHAMENTO']))
            effect = {'EXIGENCIA': .9, 'MANIFESTACAO': .4, 'PAGAMENTO': .1, 'ACOMPANHAMENTO': -.3}[act]
            z = -2.6 - .07*days + .065*load + 1.0*absent + effect + latent + rng.normal(0, .6)
            y = int(rng.random() < 1/(1+np.exp(-z)))
            deadline = t0 + timedelta(days=days)
            completed = deadline + timedelta(days=int(rng.integers(1, 10)) if y else -int(rng.integers(0, days+1)))
            # Desfecho conservador: conhecido só após prazo e conclusão.
            mature = max(deadline, completed) + timedelta(days=1)
            rows.append(dict(origem='SINTETICO', processo_id=f'SYN-{g:04d}', prazo_id=f'SYN-{g:04d}-{j}',
                             t0=t0.isoformat(), data_limite=deadline.isoformat(), data_conclusao=completed.isoformat(),
                             desfecho_disponivel_em=mature.isoformat(), dias_restantes_t0=days,
                             carga_prazos_abertos_responsavel_t0=load, responsavel_ausente_t0=absent,
                             tipo_ato=act, situacao_t0='ABERTO', y=y))
    return pd.DataFrame(rows)


def split_temporal(df):
    groups = df.groupby('processo_id').t0.min().sort_values()
    n = len(groups)
    partitions = [set(groups.index[:int(n*.6)]), set(groups.index[int(n*.6):int(n*.8)]), set(groups.index[int(n*.8):])]
    raw = [df[df.processo_id.isin(gs)].copy() for gs in partitions]
    # Purga impede usar no treino rótulos conhecidos apenas depois da validação/teste.
    train = raw[0][raw[0].desfecho_disponivel_em < raw[1].t0.min()].copy()
    val = raw[1][raw[1].desfecho_disponivel_em < raw[2].t0.min()].copy()
    test = raw[2]
    return train, val, test, dict(treino=len(raw[0])-len(train), validacao=len(raw[1])-len(val))
