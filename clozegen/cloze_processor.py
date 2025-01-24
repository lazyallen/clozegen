import asyncio
import os
import re
import statistics
from collections import Counter

from tqdm import tqdm

from .config import Config
from .logger import logger
from .models import Cloze, Pair
from .tts_generator import TTS_DIR, generate_audio_filename, generate_tts

# Constants
WORD_BOUNDARY: re.Pattern[str] = re.compile(r"[\s,\.!?\"]")


def avg_freq(words: list[str], tbl: Counter[str]) -> float:
    return sum(tbl[w] for w in words) / len(words)


def sort_pairs(pairs: list[Pair], freq_counter: Counter[str]) -> list[Pair]:
    def score_sentence(p: Pair) -> float:
        base_score = avg_freq(p.target_words, freq_counter)
        length_penalty = 1.0 / (1 + len(p.target_words))
        freq_variance = (
            statistics.variance([freq_counter[w] for w in p.target_words])
            if len(p.target_words) > 1
            else 0
        )
        return base_score * length_penalty * (1 + freq_variance)

    return sorted(pairs, key=score_sentence, reverse=True)


def clean_data(pairs: list[Pair]) -> list[Pair]:
    def strip_punctuation(text: str) -> str:
        trans_table = str.maketrans("", "", "!.,")
        return text.translate(trans_table).strip()

    result: list[Pair] = []
    appeared: set[str] = set()
    skipped: int = 0

    for pair in pairs:
        stripped: str = strip_punctuation(pair.source)
        if stripped in appeared:
            skipped += 1
            continue
        result.append(pair)
        appeared.add(stripped)

    logger.info(
        f"Deduplication completed: skipped {skipped} duplicate sentences, {len(result)} unique sentences remaining"
    )
    return result


def select_cloze_word(
    words: list[str], freq_counter: Counter[str]
) -> tuple[str, float]:
    logger.debug(
        f"Starting to select the best cloze word from word list, word count: {len(words)}"
    )

    def score_word(word: str) -> float:
        freq = freq_counter[word]
        freq_score = 1.0 / (1 + abs(freq - Config.WORD_FREQ_TARGET))
        length_score = min(len(word) / Config.WORD_LENGTH_NORMALIZER, 1.0)
        word_index = words.index(word)
        position_score = 1.0 - abs(word_index / len(words) - 0.5)
        return (
            freq_score * Config.SCORE_FREQUENCY_WEIGHT
            + length_score * Config.SCORE_LENGTH_WEIGHT
            + position_score * Config.SCORE_POSITION_WEIGHT
        )

    best_word = max(words, key=score_word)
    best_score = score_word(best_word)
    logger.debug(
        f"Cloze word selection completed: {best_word}, score: {best_score:.2f}"
    )
    return best_word, best_score


def get_word_hint(word: str) -> str:
    hint_length = Config.get_hint_length(word)
    hint_letters = word[:hint_length]
    return (
        f"First {hint_length} letter{'s' if hint_length > 1 else ''}: {hint_letters}..."
    )


def generate_audio_for_source(source: str) -> str:
    if not Config.TTS_ENABLED:
        return ""
    audio_filename = generate_audio_filename(source)
    audio_path = os.path.join(TTS_DIR, audio_filename)
    if not os.path.exists(audio_path):
        asyncio.run(generate_tts(source, audio_path))
    return audio_filename


def gen_clozes(
    pairs: list[Pair], freq_counter: Counter[str], freq_words: set[str]
) -> list[Cloze]:
    logger.info(
        f"Starting to generate cloze tests, sentence count: {len(pairs)}, high-frequency words count: {len(freq_words)}"
    )

    clozes: list[Cloze] = []
    handled_count: Counter[str] = Counter()
    skipped_limit: int = 0

    for pair in tqdm(pairs, desc="Generating cloze tests", unit="sentence"):
        source_words = pair.source_words
        cloze_word, score = select_cloze_word(source_words, freq_counter)
        if handled_count[cloze_word] == Config.SENTENCE_CLOZE_LIMIT:
            skipped_limit += 1
        elif cloze_word not in freq_words:
            continue
        else:
            hint = get_word_hint(cloze_word)
            cloze_text = "{{1::" + cloze_word + "}}"
            source = pair.source

            audio_filename = generate_audio_for_source(source)

            cloze = Cloze(
                source=source,
                source_cloze=source.replace(cloze_word, cloze_text),
                target=pair.target,
                hint=hint,
                cloze_word=cloze_word,
                freq=freq_counter[cloze_word],
                score=score,
                audio_file=audio_filename,
            )
            clozes.append(cloze)
            handled_count.update({cloze_word: 1})

    logger.info(
        f"Skipped {skipped_limit} clozes because the word appeared too many times."
    )
    return clozes


def do_gen_freq_counter(sentences: list[list[str]]) -> Counter[str]:
    freq_counter: Counter[str] = Counter()
    for sentence in sentences:
        freq_counter.update(sentence)
    logger.info(f"Found {len(freq_counter)} frequency words.")
    return freq_counter


def get_most_frequent_words(c: Counter, min_freq: float, max_freq: float) -> set[str]:
    all_words = c.most_common()
    return set([word for word, freq in all_words[min_freq:max_freq]])


def generator_frequency_counter(pairs: list[Pair]) -> tuple[Counter[str], set[str]]:
    logger.info("Starting to generate word frequency statistics")
    counter = do_gen_freq_counter([pair.source_words for pair in pairs])
    freq_words = get_most_frequent_words(
        counter, Config.WORD_FREQ_MIN_RANK, Config.WORD_FREQ_MAX_RANK
    )
    return counter, freq_words


def process_pairs(pairs: list[Pair], freq_counter: Counter[str]) -> list[Pair]:
    logger.info("Sorting started.")
    pairs = sort_pairs(pairs, freq_counter)
    logger.info("Sorting completed.")

    return pairs
