#!/usr/bin/env python

from clozegen.file_handler import parse_sentences, save_clozes_to_files
from clozegen.cloze_processor import clean_data, generator_frequency_counter, process_pairs, gen_clozes

def main():
    # Load and parse sentences
    pairs = parse_sentences()    
    # Clean and process data
    pairs = clean_data(pairs)
    freq_counter, freq_words = generator_frequency_counter(pairs)
    pairs = process_pairs(pairs, freq_counter)
    
    # Generate clozes and save to files
    clozes = gen_clozes(pairs, freq_counter, freq_words)
    save_clozes_to_files(clozes)

if __name__ == "__main__":
    main()