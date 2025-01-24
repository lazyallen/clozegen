import unittest
from unittest.mock import patch, mock_open
import os
from collections import Counter

from clozegen.models import Pair, Cloze
from clozegen.file_handler import parse_sentences, save_clozes_to_files, group_unit
from clozegen.cloze_processor import (
    clean_data,
    generator_frequency_counter,
    process_pairs,
    gen_clozes,
    select_cloze_word,
    get_word_hint
)
from clozegen.config import Config

class TestClozegen(unittest.TestCase):
    def setUp(self):
        # 设置测试数据
        self.test_pairs = [
            Pair(
                source="ich bin ein student.",
                source_words=["ich", "bin", "ein", "student"],
                target="i am a student.",
                target_words=["i", "am", "a", "student"]
            ),
            Pair(
                source="das ist ein buch.",
                source_words=["das", "ist", "ein", "buch"],
                target="this is a book.",
                target_words=["this", "is", "a", "book"]
            )
        ] * 50  # 生成100条测试数据

    def test_group_unit(self):
        """测试分组功能"""
        test_list = list(range(10))
        result = group_unit(test_list, 3)
        self.assertEqual(result, [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]])

    @patch('builtins.open', new_callable=mock_open, read_data='col1\tcol2\tcol3\tcol4\n1\tich bin\t3\ti am')
    def test_parse_sentences(self, mock_file):
        """测试句子解析功能"""
        pairs = parse_sentences()
        self.assertTrue(len(pairs) > 0)
        self.assertIsInstance(pairs[0], Pair)

    def test_clean_data(self):
        """测试数据清洗功能"""
        cleaned_pairs = clean_data(self.test_pairs)
        self.assertLess(len(cleaned_pairs), len(self.test_pairs))

    def test_generator_frequency_counter(self):
        """测试词频统计功能"""
        counter, freq_words = generator_frequency_counter(self.test_pairs)
        self.assertIsInstance(counter, Counter)
        self.assertIsInstance(freq_words, set)
        self.assertTrue(len(counter) > 0)

    def test_process_pairs(self):
        """测试句子处理功能"""
        counter = Counter()
        for pair in self.test_pairs:
            counter.update(pair.source_words)
        processed_pairs = process_pairs(self.test_pairs, counter)
        self.assertEqual(len(processed_pairs), len(self.test_pairs))

    def test_select_cloze_word(self):
        """测试完形填空词选择功能"""
        words = ["ich", "bin", "ein", "student"]
        counter = Counter(words)
        word, score = select_cloze_word(words, counter)
        self.assertIn(word, words)
        self.assertIsInstance(score, float)

    def test_get_word_hint(self):
        """测试提示生成功能"""
        hint = get_word_hint("student")
        self.assertTrue(hint.startswith("First"))

    def test_gen_clozes(self):
        """测试完形填空生成功能"""
        counter = Counter()
        for pair in self.test_pairs:
            counter.update(pair.source_words)
        freq_words = set(word for word, _ in counter.most_common(100))
        clozes = gen_clozes(self.test_pairs, counter, freq_words)
        self.assertTrue(len(clozes) > 0)
        self.assertIsInstance(clozes[0], Cloze)

    @patch('builtins.open', new_callable=mock_open)
    def test_save_clozes_to_files(self, mock_file):
        """测试完形填空保存功能"""
        clozes = [
            Cloze(
                cloze_word="student",
                source="ich bin ein student",
                source_cloze="ich bin ein {1::student}",
                target="i am a student",
                hint="First 2 letters: st...",
                freq=1,
                score=0.5,
                audio_file=""
            )
        ] * 100
        save_clozes_to_files(clozes)
        mock_file.assert_called()

if __name__ == '__main__':
    unittest.main()