# Tests for evolvesaveeditor.py
# run from evolvesaveeditor dir as:
#    python -m pytest tests/test_evolvesaveeditor.py

import os
import pytest

from evolvesaveeditor import EvolveSaveEditor as Ese

# paths to test files and such
current_dir = os.path.dirname(os.path.abspath(__file__))
test_data_dir = os.path.join(current_dir, "files")


class TestEvolveSaveEditorLZString:
    # noinspection SpellCheckingInspection
    @pytest.mark.parametrize(("test_input", "expected"), [
        ("taste", r"C4QwzsCmQ===")
    ])
    def test_compress_lz_string_can_compress_correctly(self, test_input, expected):
        actual = Ese.compress_lz_string(test_input)
        assert actual == expected

    # noinspection SpellCheckingInspection
    @pytest.mark.parametrize(("test_input", "expected"), [
        (r"C4QwzsCmQ===", "taste")
    ])
    def test_decompress_lz_string_can_decompress_valid_text(self, test_input, expected):
        actual = Ese.decompress_lz_string(test_input)
        assert actual == expected

    def test_decompress_lz_string_returns_none_on_invalid_text(self):
        actual = Ese.decompress_lz_string(r"potato")
        assert actual is None


class TestEvolveSaveEditorAdjustPrestigeCurrency:
    def test_adjust_prestige_currency_can_add_all_currencies(self):
        test_input = {
            "race": {"species": "test", "Plasmid": {"count": 123}, "Phage": {"count": 456}, "Dark": {"count": 7.8}},
            "stats": {"plasmid": 3000, "phage": 2000}}
        expected = {
            "race": {"species": "test", "Plasmid": {"count": 1234}, "Phage": {"count": 1456}, "Dark": {"count": 107.8}},
            "stats": {"plasmid": 4111, "phage": 3000}}

        actual = Ese.adjust_prestige_currency(test_input, {"Plasmid": 1234, "Phage": 1456, "Dark": 107.8})
        assert actual == expected

    def test_adjust_prestige_currency_adds_no_currencies_if_all_zero(self):
        test_input = {"race": {"species": "test", "Plasmid": {"count": 0}, "Phage": {"count": 0}, "Dark": {"count": 0}},
                      "stats": {"plasmid": 0, "phage": 0}}
        expected = {"race": {"species": "test", "Plasmid": {"count": 0}, "Phage": {"count": 0}, "Dark": {"count": 0}},
                    "stats": {"plasmid": 0, "phage": 0}}

        actual = Ese.adjust_prestige_currency(test_input, {"Plasmid": 3000, "Phage": 2000, "Dark": 1000})
        assert actual == expected

    def test_adjust_prestige_currency_does_not_reduce_currency(self):
        test_input = {
            "race": {"species": "test", "Plasmid": {"count": 4000}, "Phage": {"count": 3000}, "Dark": {"count": 2000}},
            "stats": {"plasmid": 4000, "phage": 3000}}
        expected = {
            "race": {"species": "test", "Plasmid": {"count": 4000}, "Phage": {"count": 3000}, "Dark": {"count": 2000}},
            "stats": {"plasmid": 4000, "phage": 3000}}

        actual = Ese.adjust_prestige_currency(test_input, {"Plasmid": 3000, "Phage": 2000, "Dark": 1000})
        assert actual == expected


class TestEvolveSaveEditorFillResources:
    def test_fill_resources_skips_broken_elements(self):
        test_input = {"resource": {
            "RNA": {"name": "RNA", "max": 100},
            "DNA": {"name": "DNA", "amount": 0},
            "FAKE": {"name": "FAKE", "amount": 0, "max": 2000}}}
        expected = {"resource": {
            "RNA": {"name": "RNA", "max": 100},
            "DNA": {"name": "DNA", "amount": 0},
            "FAKE": {"name": "FAKE", "amount": 2000, "max": 2000}}}
        actual = Ese.fill_resources(test_input, 10000)
        assert actual == expected

    def test_fill_resources_fills_to_max(self):
        test_input = {"resource": {
            "RNA": {"name": "RNA", "display": True, "amount": 0, "crates": 0, "diff": 0, "delta": 0, "max": 100,
                    "rate": 1, "containers": 0},
            "DNA": {"name": "DNA", "display": False, "amount": 0, "crates": 0, "diff": 0, "delta": 0, "max": 100,
                    "rate": 1, "containers": 0}}}
        expected = {"resource": {
            "RNA": {"name": "RNA", "display": True, "amount": 100, "crates": 0, "diff": 0, "delta": 0, "max": 100,
                    "rate": 1, "containers": 0},
            "DNA": {"name": "DNA", "display": False, "amount": 100, "crates": 0, "diff": 0, "delta": 0, "max": 100,
                    "rate": 1, "containers": 0}}}
        actual = Ese.fill_resources(test_input, 10000)
        assert actual == expected

    def test_fill_resources_sets_unbounded_resources_to_amount(self):
        test_input = {"resource": {"MAGIC": {"name": "MAGIC", "amount": 0, "max": -1}}}
        expected = {"resource": {"MAGIC": {"name": "MAGIC", "amount": 20000, "max": -1}}}
        actual = Ese.fill_resources(test_input, 20000)
        assert actual == expected
