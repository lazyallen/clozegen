class Config:
    # File and directory path configurations
    FILE_SOURCE_DIR: str = "source"  # Directory containing source data files
    FILE_SOURCE_NAME: str = (
        "Sentence pairs in German-English.tsv"  # Name of the source TSV file
    )
    FILE_OUTPUT_DIR: str = "csv"  # Directory for output CSV files
    FILE_UNIT_SIZE: int = 100  # Number of items per output CSV unit file

    # Sentence processing configurations
    SENTENCE_MAX_WORDS: int = 10  # Maximum number of words allowed in a source sentence
    SENTENCE_CLOZE_LIMIT: int = (
        3  # Maximum number of times a word can be used for cloze tests
    )

    # Word frequency configurations
    WORD_FREQ_MIN_RANK: float = 0  # Minimum rank for word frequency selection
    WORD_FREQ_MAX_RANK: float = 2000  # Maximum rank for word frequency selection
    WORD_FREQ_TARGET: int = 500  # Target frequency for optimal word selection
    WORD_LENGTH_SHORT: int = 3  # Threshold for short words
    WORD_LENGTH_MEDIUM: int = 6  # Threshold for medium words
    WORD_LENGTH_NORMALIZER: float = 5.0  # Normalizer for word length scoring

    # Scoring weight configurations
    SCORE_FREQUENCY_WEIGHT: float = 0.5  # Weight for frequency-based scoring
    SCORE_LENGTH_WEIGHT: float = 0.3  # Weight for length-based scoring
    SCORE_POSITION_WEIGHT: float = 0.2  # Weight for position-based scoring

    # Text-to-Speech (TTS) configurations
    TTS_OUTPUT_DIR: str = "tts"  # Directory for TTS audio output files
    TTS_VOICE_ID: str = "de-DE-ConradNeural"  # Voice ID for TTS generation
    TTS_MAX_RETRIES: int = 3  # Maximum number of retry attempts for TTS generation
    TTS_RETRY_DELAY: float = 1.0  # Delay in seconds between retry attempts
    TTS_ENABLED: bool = False  # Whether to generate TTS audio files

    @staticmethod
    def update_config(**kwargs):
        for key, value in kwargs.items():
            if hasattr(Config, key):
                setattr(Config, key, value)

    # Word length thresholds for hints
    SHORT_WORD_LENGTH = 4
    MEDIUM_WORD_LENGTH = 8

    @staticmethod
    def get_hint_length(word: str) -> int:
        if len(word) <= Config.SHORT_WORD_LENGTH:
            return 1
        elif len(word) <= Config.MEDIUM_WORD_LENGTH:
            return 2
        return 3
