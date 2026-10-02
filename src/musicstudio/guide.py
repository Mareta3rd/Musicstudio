from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class GuideQuestion:
    id: str
    text: str
    purpose: str
    optional: bool = False


@dataclass
class GuideSession:
    phase: str = "idea"
    answers: dict[str, str] = field(default_factory=dict)


QUESTIONS: tuple[GuideQuestion, ...] = (
    GuideQuestion("intent", "¿Qué quieres que haga sentir o contar esta obra?", "emotional intent"),
    GuideQuestion("format", "¿Estamos creando un single, una miniobra de 3 temas, un EP, un LP, un directo o un unplugged?", "release format"),
    GuideQuestion("world", "¿Qué universo sonoro imaginas? Piensa en lugares, texturas, época o imágenes, no solo en géneros.", "sonic world"),
    GuideQuestion("reference", "¿Hay una canción, artista, sonido o referencia que debamos estudiar? ¿Qué parte te interesa exactamente?", "reference", optional=True),
    GuideQuestion("voice", "¿Hay voz? ¿Quién parece hablar, a quién y con qué actitud?", "vocal identity", optional=True),
    GuideQuestion("energy", "¿Cómo quieres que evolucione la energía: estable, creciente, quebrada, de calma a explosión u otra forma?", "energy arc"),
    GuideQuestion("signature", "¿Qué detalle quieres que haga reconocible esta obra en diez segundos?", "signature"),
    GuideQuestion("visual", "¿Qué imagen, color, lugar o símbolo debería acompañarla visualmente?", "visual identity", optional=True),
    GuideQuestion("constraint", "¿Qué NO quieres que ocurra?", "negative constraint", optional=True),
)


class CreativeGuide:
    def start(self) -> GuideSession:
        return GuideSession()

    def next_question(self, session: GuideSession) -> GuideQuestion | None:
        for question in QUESTIONS:
            if question.id not in session.answers:
                return question
        return None

    def answer(self, session: GuideSession, question_id: str, answer: str) -> GuideQuestion | None:
        if not question_id or question_id not in {q.id for q in QUESTIONS}:
            raise KeyError(f"Unknown guide question: {question_id}")
        answer = " ".join(answer.strip().split())
        if not answer:
            raise ValueError("Guide answer cannot be empty")
        session.answers[question_id] = answer
        return self.next_question(session)

    def brief(self, session: GuideSession) -> str:
        lines = ["MUSICSTUDIO CREATIVE BRIEF"]
        labels = {q.id: q.purpose for q in QUESTIONS}
        for key, value in session.answers.items():
            lines.append(f"{labels[key]}: {value}")
        return "\n".join(lines)