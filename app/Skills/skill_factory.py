from Skills.skills.colapso_ortografico import ColapsoOrtografico
from Skills.skills.corrente_combos import CorrenteDeCombos
from Skills.skills.disruptor_semantico import DisruptorSemantico
from Skills.skills.ditador_palavras import DitadorDePalavras
from Skills.skills.eco_palavras import EcoDePalavras
from Skills.skills.explosao_verbo import ExplosaoDeVerbos
from Skills.skills.mimetismo import Mimetismo
from Skills.skills.palavra_proibida import PalavraProibida
from Skills.skills.ritual_palavras import RitualDasPalavras
from Skills.skills.roubo_vocabulario import RouboDeVocabulario

skill_classes = {
    "colapso_ortografico": ColapsoOrtografico,
    "corrente_combos": CorrenteDeCombos,
    "disruptor_semantico": DisruptorSemantico,
    "ditador_palavras": DitadorDePalavras,
    "eco_palavras": EcoDePalavras,
    "explosao_verbo": ExplosaoDeVerbos,
    "mimetismo": Mimetismo,
    "palavra_proibida": PalavraProibida,
    "ritual_palavras": RitualDasPalavras,
    "roubo_vocabulario": RouboDeVocabulario,
}

def create_skill(name, image=None):
    cls = skill_classes.get(name)
    if cls:
        skill = cls()
        if image:
            skill.image = image
        return skill
    raise ValueError(f"Skill '{name}' não encontrada na fábrica.")
