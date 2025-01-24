import csv
from dataclasses import fields

from .config import Config
from .logger import logger
from .models import Cloze, Pair
from .utils import words


def parse_sentences() -> list[Pair]:
    logger.info(f"Start parsing sentence file: {Config.FILE_SOURCE_NAME}")
    pairs: list[Pair] = []
    with open(f"{Config.FILE_SOURCE_DIR}/{Config.FILE_SOURCE_NAME}", "r") as stream:
        reader = csv.reader(stream, delimiter="\t")
        for row in reader:
            source: str = row[1].strip().lower()
            target: str = row[3].strip().lower()
            source_words: list[str] = words(source)
            target_words: list[str] = words(target)
            if len(source_words) > Config.SENTENCE_MAX_WORDS:
                logger.debug(
                    f"Skipping sentence due to length, word count: {len(source_words)}"
                )
                continue
            if (not source_words) or (not target_words):
                logger.debug(
                    f"Skipping empty sentence, source_words: {len(source_words)}, target_words: {len(target_words)}"
                )
                continue
            pair: Pair = Pair(
                source=source,
                source_words=source_words,
                target=target,
                target_words=target_words,
            )
            pairs.append(pair)
    logger.info(f"Found {len(pairs):,} sentences.")
    return pairs


def group_unit(lst: list, n: int) -> list[list]:
    if n <= 0:
        raise ValueError("Group size must be greater than 0")
    if not lst:
        return []

    return [lst[i : i + n] for i in range(0, len(lst), n)]


def save_clozes_to_files(clozes: list[Cloze]) -> None:
    logger.info(f"Start saving cloze tests, total count: {len(clozes)}")
    units: list[list[Cloze]] = group_unit(clozes, Config.FILE_UNIT_SIZE)
    logger.info(
        f"Will generate {len(units)} practice units, each containing {Config.FILE_UNIT_SIZE} sentences."
    )

    for unit_id, unit in enumerate(units):
        output_file = f"{Config.FILE_OUTPUT_DIR}/cloze_{unit_id}.csv"
        logger.info(f"Saving unit {unit_id + 1}/{len(units)} to file: {output_file}")
        with open(output_file, "w") as stream:
            writer = csv.writer(
                stream,
                delimiter=",",
                quotechar='"',
                quoting=csv.QUOTE_ALL,
                lineterminator="\n",
            )
            # Write field names as header
            writer.writerow([field.name for field in fields(Cloze)])
            # Write field values
            for cloze in unit:
                writer.writerow(
                    [
                        cloze.cloze_word,
                        cloze.source,
                        cloze.source_cloze,
                        cloze.target,
                        cloze.hint,
                        cloze.freq,
                        cloze.score,
                        cloze.audio_file,
                    ]
                )
