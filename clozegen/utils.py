import re

# Constants
WORD_BOUNDARY: re.Pattern[str] = re.compile(r"[\s,\.!?\"]")


def words(line: str) -> list[str]:
    word_list = [w.strip() for w in re.split(WORD_BOUNDARY, line) if w.strip()]
    word_list = [w for w in word_list if not w.isdigit()]
    return word_list
