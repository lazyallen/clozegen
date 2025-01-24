from dataclasses import dataclass


@dataclass(frozen=True)
class Pair:
    source: str
    source_words: list[str]
    target: str
    target_words: list[str]

    def dump(self):
        print(f"\tsource={self.source}")
        print(f"\tsource_words={self.source_words}")
        print(f"\ttarget={self.target}")
        print(f"\ttarget_words={self.target_words}")


@dataclass(frozen=True)
class Cloze:
    cloze_word: str
    source: str
    source_cloze: str
    target: str
    hint: str
    freq: int
    score: float
    audio_file: str
