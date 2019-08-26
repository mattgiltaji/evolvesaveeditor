# Tests for evolvesaveeditor.py
# run from evolvesaveeditor dir as:
#    python -m pytest tests/test_evolvesaveeditor.py

import os
import pytest
import copy

from evolvesaveeditor import EvolveSaveEditor as Ese

# paths to test files and such
current_dir = os.path.dirname(os.path.abspath(__file__))
test_data_dir = os.path.join(current_dir, "files")


@pytest.fixture
def unlocked_container_and_crate_json():
    return {"city": {"storage_yard": {"count": 1}, "warehouse": {"count": 1}}}


@pytest.fixture
def evolve_save_editor():
    return Ese()


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


class TestEvolveSaveEditorAdjustSaveData:
    def test_adjust_save_data_handles_empty_data(self, evolve_save_editor):
        evolve_save_editor.adjust_save_data()
        assert evolve_save_editor.save_data == {}

    def test_adjust_save_data_fills_resources(self, evolve_save_editor):
        test_input = {"resource": {
            "Money": {"name": "$", "display": True, "amount": 5, "crates": 0, "max": 2000, "stackable": False,
                      "containers": 0},
            "Food": {"name": "Food", "display": True, "amount": 240, "crates": 0, "max": 240, "stackable": True,
                     "containers": 0}}}
        expected = copy.deepcopy(test_input)
        expected["resource"]["Money"]["amount"] = 2000
        evolve_save_editor.save_data = test_input
        evolve_save_editor.adjust_save_data()
        assert evolve_save_editor.save_data == expected

    def test_adjust_save_data_stacks_resources(self, unlocked_container_and_crate_json, evolve_save_editor):
        test_input = unlocked_container_and_crate_json
        test_input["resource"] = {
            "Money": {"name": "$", "display": True, "amount": 2000, "crates": 0, "max": 2000, "stackable": False,
                      "containers": 0},
            "Stone": {"name": "Stone", "display": True, "amount": 240, "crates": 8, "max": 240, "stackable": True,
                      "containers": 4}}
        expected = copy.deepcopy(test_input)
        expected["resource"]["Stone"]["crates"] = evolve_save_editor.DEFAULT_STACK_AMOUNT
        expected["resource"]["Stone"]["containers"] = evolve_save_editor.DEFAULT_STACK_AMOUNT
        evolve_save_editor.save_data = test_input
        evolve_save_editor.adjust_save_data()
        assert evolve_save_editor.save_data == expected


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


class TestEvolveSaveEditorStackResources:
    def test_stack_resources_does_not_update_when_stackables_not_unlocked(self):
        test_input = {
            "resource": {"Food": {"name": "Food", "amount": 10, "crates": 0, "stackable": True, "containers": 0}},
            "city": {}}
        expected = test_input
        actual = Ese.stack_resources(test_input, 1000)
        assert actual == expected

    def test_stack_resources_updates_only_crates_when_containers_not_unlocked(self):
        test_input = {
            "resource": {"Food": {"name": "Food", "amount": 13, "crates": 0, "stackable": True, "containers": 0}},
            "city": {"storage_yard": {"count": 1}}}
        expected = {
            "resource": {"Food": {"name": "Food", "amount": 13, "crates": 144, "stackable": True, "containers": 0}},
            "city": {"storage_yard": {"count": 1}}}
        actual = Ese.stack_resources(test_input, 144)
        assert actual == expected

    def test_stack_resources_updates_only_containers_when_crates_not_unlocked(self):
        test_input = {
            "resource": {"Food": {"name": "Food", "amount": 13, "crates": 0, "stackable": True, "containers": 0}},
            "city": {"warehouse": {"count": 1}}}
        expected = {
            "resource": {"Food": {"name": "Food", "amount": 13, "crates": 0, "stackable": True, "containers": 42}},
            "city": {"warehouse": {"count": 1}}}
        actual = Ese.stack_resources(test_input, 42)
        assert actual == expected

    def test_stack_resources_updates_only_when_positive_amount(self, unlocked_container_and_crate_json):
        test_input = unlocked_container_and_crate_json
        test_input["resource"] = {
            "Stone": {"name": "Stone", "amount": 0, "crates": 0, "stackable": True, "containers": 0}}
        expected = test_input
        actual = Ese.stack_resources(test_input, 240)
        assert actual == expected

    def test_stack_resources_does_not_update_unstackable_resources(self, unlocked_container_and_crate_json):
        test_input = unlocked_container_and_crate_json
        test_input["resource"] = {"RNA": {"name": "RNA", "amount": 44, "crates": 0, "containers": 0},
                                  "Oil": {"name": "Oil", "amount": 25, "crates": 0, "stackable": False,
                                          "containers": 0}}
        expected = test_input
        actual = Ese.stack_resources(test_input, 76)
        assert actual == expected

    def test_stack_resources_does_not_remove_extra_stackables(self, unlocked_container_and_crate_json):
        test_input = unlocked_container_and_crate_json
        test_input["resource"] = {
            "Furs": {"name": "Furs", "amount": 100, "crates": 30, "stackable": True, "containers": 30}}
        expected = test_input
        actual = Ese.stack_resources(test_input, 20)
        assert actual == expected

    def test_stack_resources_updates_stackables(self, unlocked_container_and_crate_json):
        test_input = unlocked_container_and_crate_json
        test_input["resource"] = {
            "Copper": {"name": "Copper", "amount": 12, "crates": 1, "stackable": True, "containers": 2}}
        expected = copy.deepcopy(test_input)
        expected["resource"]["Copper"]["crates"] = 1000
        expected["resource"]["Copper"]["containers"] = 1000
        actual = Ese.stack_resources(test_input, 1000)
        assert actual == expected


class TestEvolveSaveEditorAdjustBuildings:
    def test_adjust_buildings_can_handle_no_buildings(self):
        test_input = {"city": {}, "space": {}, "interstellar": {}, "portal": {}}
        expected = test_input
        actual = Ese.adjust_buildings(test_input, Ese.BuildingAmountsParam())
        assert actual == expected

    def test_adjust_buildings_skips_zero_and_no_count_buildings(self):
        test_input = {"city": {"biome": "oceanic", "university": {"count": 0}, "rock_quarry": {"count": 1}, },
                      "space": {}, "interstellar": {}, "portal": {}}
        expected = {"city": {"biome": "oceanic", "university": {"count": 0},
                             "rock_quarry": {"count": Ese.BuildingAmountsParam().boost}, }, "space": {},
                    "interstellar": {}, "portal": {}}
        actual = Ese.adjust_buildings(test_input, Ese.BuildingAmountsParam())
        assert actual == expected

    def test_adjust_buildings_will_not_lower_building_count(self):
        test_input = {"city": {"university": {"count": 100000000}}, "space": {}, "interstellar": {}, "portal": {}}
        expected = test_input
        actual = Ese.adjust_buildings(test_input, Ese.BuildingAmountsParam())
        assert actual == expected

    def test_adjust_buildings_special_goes_to_proper_limits(self):
        test_input = {"city": {}, "space": {"swarm_control": {"count": 50}, "swarm_satellite": {"count": 3},
                                            "world_collider": {"count": 1}},
                      "interstellar": {"dyson": {"count": 2}, "stellar_engine": {"count": 4}}, "portal": {}}
        expected = {"city": {}, "space": {"swarm_control": {"count": Ese.BuildingAmountsParam().support},
                                          "swarm_satellite": {"count": Ese.BuildingAmountsParam().support * 6},
                                          "world_collider": {"count": 1858}},
                    "interstellar": {"dyson": {"count": 99}, "stellar_engine": {"count": 99}}, "portal": {}}
        actual = Ese.adjust_buildings(test_input, Ese.BuildingAmountsParam())
        assert actual == expected

    def test_adjust_buildings_boost_type(self):
        test_input = {"city": {"temple": {"count": 10}}, "space": {"ziggurat": {"count": 5}},
                      "interstellar": {"processing": {"count": 4}}, "portal": {"turret": {"count": 3}}}
        count = 9000
        amounts = Ese.BuildingAmountsParam()
        amounts.boost = count
        expected = {"city": {"temple": {"count": count}}, "space": {"ziggurat": {"count": count}},
                    "interstellar": {"processing": {"count": count}}, "portal": {"turret": {"count": count}}}
        actual = Ese.adjust_buildings(test_input, amounts)
        assert actual == expected

    def test_adjust_buildings_housing_type(self):
        test_input = {"city": {"basic_housing": {"count": 6}}, "space": {}, "interstellar": {"habitat": {"count": 4}},
                      "portal": {}}
        count = 90210
        amounts = Ese.BuildingAmountsParam()
        amounts.housing = count
        expected = {"city": {"basic_housing": {"count": count}}, "space": {},
                    "interstellar": {"habitat": {"count": count}}, "portal": {}}
        actual = Ese.adjust_buildings(test_input, amounts)
        assert actual == expected

    def test_adjust_buildings_job_type(self):
        test_input = {"city": {"bank": {"count": 73}}, "space": {"living_quarters": {"count": 15}},
                      "interstellar": {}, "portal": {"carport": {"count": 20}}}
        count = 925
        amounts = Ese.BuildingAmountsParam()
        amounts.job = count
        expected = {"city": {"bank": {"count": count}}, "space": {"living_quarters": {"count": count}},
                    "interstellar": {}, "portal": {"carport": {"count": count}}}
        actual = Ese.adjust_buildings(test_input, amounts)
        assert actual == expected

    def test_adjust_buildings_morale_job_type(self):
        test_input = {"city": {"amphitheatre": {"count": 15}, "casino": {"count": 7}}, "space": {}, "interstellar": {},
                      "portal": {}}
        count = 420
        amounts = Ese.BuildingAmountsParam()
        amounts.morale_job = count
        expected = {"city": {"amphitheatre": {"count": count}, "casino": {"count": count}}, "space": {},
                    "interstellar": {}, "portal": {}}
        actual = Ese.adjust_buildings(test_input, amounts)
        assert actual == expected

    def test_adjust_buildings_power_generator_type(self):
        test_input = {"city": {"oil_power": {"count": 2}}, "space": {"geothermal": {"count": 4}},
                      "interstellar": {"fusion": {"count": 6}}, "portal": {}}
        count = 321
        amounts = Ese.BuildingAmountsParam()
        amounts.power_generator = count
        expected = {"city": {"oil_power": {"count": count}}, "space": {"geothermal": {"count": count}},
                    "interstellar": {"fusion": {"count": count}}, "portal": {}}
        actual = Ese.adjust_buildings(test_input, amounts)
        assert actual == expected

    def test_adjust_buildings_production_type(self):
        test_input = {"city": {"oil_well": {"count": 7}}, "space": {"elerium_ship": {"count": 8}},
                      "interstellar": {"g_factory": {"count": 9}}, "portal": {}}
        count = 180
        amounts = Ese.BuildingAmountsParam()
        amounts.production = count
        expected = {"city": {"oil_well": {"count": count}}, "space": {"elerium_ship": {"count": count}},
                    "interstellar": {"g_factory": {"count": count}}, "portal": {}}
        actual = Ese.adjust_buildings(test_input, amounts)
        assert actual == expected

    def test_adjust_buildings_storage_type(self):
        test_input = {"city": {"shed": {"count": 4}}, "space": {"elerium_contain": {"count": 5}},
                      "interstellar": {"warehouse": {"count": 6}}, "portal": {"sensor_drone": {"count": 7}}}
        count = 1024
        amounts = Ese.BuildingAmountsParam()
        amounts.storage = count
        expected = {"city": {"shed": {"count": count}}, "space": {"elerium_contain": {"count": count}},
                    "interstellar": {"warehouse": {"count": count}}, "portal": {"sensor_drone": {"count": count}}}
        actual = Ese.adjust_buildings(test_input, amounts)
        assert actual == expected

    def test_adjust_buildings_support_type(self):
        test_input = {"city": {}, "space": {"nav_beacon": {"count": 1}}, "interstellar": {"starport": {"count": 2}},
                      "portal": {}}
        count = 1800
        amounts = Ese.BuildingAmountsParam()
        amounts.support = count
        expected = {"city": {}, "space": {"nav_beacon": {"count": count}},
                    "interstellar": {"starport": {"count": count}}, "portal": {}}
        actual = Ese.adjust_buildings(test_input, amounts)
        assert actual == expected


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

    def test_update_prestige_currency_value_skips_missing_currencies(self):
        test_input = {
            "race": {"species": "test", "Plasmid": {"count": 1}, "Phage": {"count": 2}, "Dark": {"count": 3}},
            "stats": {"plasmid": 4, "phage": 5}}
        expected = test_input
        actual_data, actual_added = Ese._update_prestige_currency_value(test_input, "fake", 1000)
        assert actual_data == expected
        assert actual_added == 0


class TestEvolveSaveEditorAdjustArpaResearch:
    def test_adjust_arpa_research_can_handle_no_research(self):
        test_input = {"arpa": {}}
        expected = test_input
        actual = Ese.adjust_arpa_research(test_input)
        assert actual == expected

    def test_adjust_arpa_research_skips_broken_nodes(self):
        test_input = {"arpa": {"sequence": {"progress": 0}, "launch_facility": {"rank": 0}, "lhc": {"rank": 10}}}
        expected = test_input
        actual = Ese.adjust_arpa_research(test_input)
        assert actual == expected

    def test_adjust_arpa_research_does_not_update_launch_facility_past_rank_1(self):
        test_input = {"arpa": {"launch_facility": {"complete": 0, "rank": 1}}}
        expected = test_input
        actual = Ese.adjust_arpa_research(test_input)
        assert actual == expected

    def test_adjust_arpa_research_updates_initial_launch_facility(self):
        test_input = {"arpa": {"launch_facility": {"complete": 0, "rank": 0}}}
        expected = {"arpa": {"launch_facility": {"complete": 99, "rank": 0}}}
        actual = Ese.adjust_arpa_research(test_input)
        assert actual == expected

    def test_adjust_arpa_research_updates_genetic_sequencing(self):
        test_input = {"arpa": {"sequence": {"max": 850000, "progress": 1500}}}
        expected = {"arpa": {"sequence": {"max": 850000, "progress": 849995}}}
        actual = Ese.adjust_arpa_research(test_input)
        assert actual == expected

    def test_adjust_arpa_research_only_increases_genetic_sequencing_completion(self):
        test_input = {"arpa": {"sequence": {"max": 9000, "progress": 8999}}}
        expected = test_input
        actual = Ese.adjust_arpa_research(test_input)
        assert actual == expected

    def test_adjust_arpa_research_updates_lhc(self):
        test_input = {"arpa": {"lhc": {"complete": 0, "rank": 0}}}
        expected = {"arpa": {"lhc": {"complete": 99, "rank": 0}}}
        actual = Ese.adjust_arpa_research(test_input)
        assert actual == expected

    def test_adjust_arpa_research_updates_stock_exchange(self):
        test_input = {"arpa": {"stock_exchange": {"complete": 0, "rank": 15}}}
        expected = {"arpa": {"stock_exchange": {"complete": 99, "rank": 15}}}
        actual = Ese.adjust_arpa_research(test_input)
        assert actual == expected

    def test_adjust_arpa_research_updates_monument(self):
        test_input = {"arpa": {"monument": {"complete": 0, "rank": 68}}}
        expected = {"arpa": {"monument": {"complete": 99, "rank": 68}}}
        actual = Ese.adjust_arpa_research(test_input)
        assert actual == expected
