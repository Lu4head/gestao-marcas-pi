"""Regras de produção monotônicas, agenda e ponto fixo antes da resolução."""
from dataclasses import dataclass
from datetime import date
import math
from src.integration.contract import validate


@dataclass(frozen=True)
class Config:
    margem_interna: int = 5
    limiar_ml: float = .70

    def __post_init__(self):
        if type(self.margem_interna) is not int or self.margem_interna < 0:
            raise ValueError('Margem deve ser inteiro não negativo')
        if isinstance(self.limiar_ml, bool) or not isinstance(self.limiar_ml, (int, float)) or not math.isfinite(self.limiar_ml) or not 0 <= self.limiar_ml <= 1:
            raise ValueError('Limiar deve estar entre zero e um')


@dataclass(frozen=True)
class Fact:
    nome: str
    valor: object = True


@dataclass(frozen=True)
class Rule:
    id: str
    descricao: str
    condicao: object
    efeitos: tuple


def classify(prazo, referencia: date, payload, config=Config()):
    if type(referencia) is not date or referencia < prazo.t0:
        raise ValueError('Referência deve ser date e não pode anteceder t0')
    ml, warning = validate(payload, prazo.prazo_id)
    d = (prazo.data_limite-referencia).days
    facts = {'concluido': prazo.concluido, 'dias_restantes': d,
             'responsavel_ausente': prazo.responsavel_ausente or not (prazo.responsavel or '').strip(),
             'ml_status': ml['status']}
    if ml['status'] == 'ok':
        facts['risco_ml'] = ml['prob_atraso']
    initial = dict(facts)
    rules = [
        Rule('R1', 'Concluído sai da fila', lambda f: f['concluido'], (Fact('candidato_FORA_DA_FILA'), Fact('motivo_CONCLUIDO'))),
        Rule('R2', 'Aberto permite avaliar condições', lambda f: not f['concluido'], (Fact('prazo_aberto'),)),
        Rule('R3', 'Aberto com data passada', lambda f: f.get('prazo_aberto') and f['dias_restantes'] < 0, (Fact('candidato_VENCIDO'), Fact('motivo_PRAZO_VENCIDO'))),
        Rule('R4', 'Aberto dentro da margem interna', lambda f: f.get('prazo_aberto') and 0 <= f['dias_restantes'] <= config.margem_interna, (Fact('candidato_URGENTE'), Fact('motivo_MARGEM_INTERNA'))),
        Rule('R5', 'Responsável ausente ou não designado', lambda f: f.get('prazo_aberto') and f['responsavel_ausente'], (Fact('motivo_RESPONSAVEL_AUSENTE'),)),
        Rule('R6', 'Probabilidade válida atinge o limiar', lambda f: f.get('prazo_aberto') and 'risco_ml' in f and f['risco_ml'] >= config.limiar_ml, (Fact('motivo_RISCO_ML_ACIMA_LIMIAR'),)),
        Rule('R7', 'Risco ou ausência fora da urgência', lambda f: f.get('prazo_aberto') and f['dias_restantes'] > config.margem_interna and (f.get('motivo_RESPONSAVEL_AUSENTE') or f.get('motivo_RISCO_ML_ACIMA_LIMIAR')), (Fact('candidato_ALTO'),)),
        Rule('R8', 'Aberto admite prioridade padrão', lambda f: f.get('prazo_aberto'), (Fact('candidato_NORMAL'),)),
    ]
    trace, fired, cycle = [], set(), 0
    while True:
        # Agenda calculada antes de disparar: fatos derivados habilitam o próximo ciclo.
        agenda = [r for r in rules if r.id not in fired and r.condicao(facts)]
        if not agenda:
            break
        cycle += 1
        for rule in agenda:
            before = dict(facts)
            for fact in rule.efeitos:
                facts[fact.nome] = fact.valor
            fired.add(rule.id)
            trace.append(dict(ciclo=cycle, regra=rule.id, descricao=rule.descricao,
                              fatos_consultados=before, fatos_adicionados={f.nome: f.valor for f in rule.efeitos}))
    precedence = ['FORA_DA_FILA', 'VENCIDO', 'URGENTE', 'ALTO', 'NORMAL']
    priority = next(p for p in precedence if facts.get('candidato_'+p))
    reasons = [k.removeprefix('motivo_') for k in facts if k.startswith('motivo_')]
    if priority == 'NORMAL':
        reasons.append('SEM_GATILHOS_DE_ELEVACAO')
    trace.append(dict(ciclo=cycle+1, regra='RESOLUCAO', descricao='Precedência entre candidatos no ponto fixo', prioridade=priority))
    return dict(prazo_id=prazo.prazo_id, processo_id=prazo.processo_id,
                data_referencia=referencia.isoformat(), data_limite=prazo.data_limite.isoformat(),
                dias_restantes=d, prioridade=priority, motivos=reasons,
                revisao_humana=not prazo.concluido, regras_versao='regras-v1',
                parametros=dict(margem_interna=config.margem_interna, limiar_ml=config.limiar_ml),
                ml=ml, aviso=warning, fatos_iniciais=initial, fatos_finais=facts, trilha=trace)
