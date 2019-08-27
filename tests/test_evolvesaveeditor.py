# Tests for evolvesaveeditor.py
# run from evolvesaveeditor dir as:
#    python -m pytest tests/test_evolvesaveeditor.py

import copy
import filecmp
import os

import pytest

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


@pytest.yield_fixture
def temp_file(tmpdir):
    filepath = os.path.join(tmpdir, "temp.txt")
    yield filepath
    try:
        os.remove(filepath)
    except OSError:
        pass


class TestEvolveSaveEditorSaveLoadFile:
    # noinspection SpellCheckingInspection
    def test_save_data_to_file_handles_start_file(self, evolve_save_editor, tmpdir):
        test_input = {"seed": 2953, "resource": {
            "RNA": {"name": "RNA", "display": True, "amount": 0, "crates": 0, "diff": 0, "delta": 0, "max": 100,
                    "rate": 1, "containers": 0},
            "DNA": {"name": "DNA", "display": False, "amount": 0, "crates": 0, "diff": 0, "delta": 0, "max": 100,
                    "rate": 1, "containers": 0}}, "evolution": {}, "tech": {}, "city": {
            "morale": {"current": 0, "unemployed": 0, "stress": 0, "entertain": 0, "leadership": 0, "season": 0,
                       "weather": 0, "warmonger": 0, "tax": 0},
            "calendar": {"day": 0, "year": 0, "season": 0, "weather": 2, "temp": 1, "moon": 0, "wind": 0, "orbit": 365},
            "powered": False, "power": 0, "biome": "grassland", "geology": {},
            "market": {"qty": 10, "mtrade": 0, "trade": 0, "active": False}}, "space": {}, "interstellar": {},
                      "portal": {}, "civic": {"free": 0, "farmer": {"job": "farmer", "name": "Farmer", "display": False,
                                                                    "workers": 0, "max": 0, "impact": 1.35,
                                                                    "assigned": 0, "stress": 5},
                                              "lumberjack": {"job": "lumberjack", "name": "Lumberjack",
                                                             "display": False, "workers": 0, "max": 0, "impact": 1,
                                                             "assigned": 0, "stress": 5},
                                              "quarry_worker": {"job": "quarry_worker", "name": "Quarry Worker",
                                                                "display": False, "workers": 0, "max": 0, "impact": 1,
                                                                "assigned": 0, "stress": 5},
                                              "miner": {"job": "miner", "name": "Miner", "display": False, "workers": 0,
                                                        "max": 0, "impact": 1, "assigned": 0, "stress": 4},
                                              "coal_miner": {"job": "coal_miner", "name": "Coal Miner",
                                                             "display": False, "workers": 0, "max": 0, "impact": 0.2,
                                                             "assigned": 0, "stress": 4},
                                              "craftsman": {"job": "craftsman", "name": "Craftsman", "display": False,
                                                            "workers": 0, "max": 0, "impact": 1, "assigned": 0,
                                                            "stress": 5},
                                              "cement_worker": {"job": "cement_worker", "name": "Cement Plant Worker",
                                                                "display": False, "workers": 0, "max": 0, "impact": 0.4,
                                                                "assigned": 0, "stress": 5},
                                              "entertainer": {"job": "entertainer", "name": "Entertainer",
                                                              "display": False, "workers": 0, "max": 0, "impact": 1,
                                                              "assigned": 0, "stress": 10},
                                              "professor": {"job": "professor", "name": "Professor", "display": False,
                                                            "workers": 0, "max": 0, "impact": 0.5, "assigned": 0,
                                                            "stress": 6},
                                              "scientist": {"job": "scientist", "name": "Scientist", "display": False,
                                                            "workers": 0, "max": 0, "impact": 1, "assigned": 0,
                                                            "stress": 5},
                                              "banker": {"job": "banker", "name": "Banker", "display": False,
                                                         "workers": 0, "max": 0, "impact": 0.1, "assigned": 0,
                                                         "stress": 6},
                                              "colonist": {"job": "colonist", "name": "Colonist", "display": False,
                                                           "workers": 0, "max": 0, "impact": 1, "assigned": 0,
                                                           "stress": 5},
                                              "space_miner": {"job": "space_miner", "name": "Space Miner",
                                                              "display": False, "workers": 0, "max": 0, "impact": 1,
                                                              "assigned": 0, "stress": 5},
                                              "hell_surveyor": {"job": "hell_surveyor", "name": "Surveyor",
                                                                "display": False, "workers": 0, "max": 0, "impact": 1,
                                                                "assigned": 0, "stress": 1},
                                              "taxes": {"tax_rate": 20, "display": False}},
                      "race": {"species": "protoplasm", "gods": "none", "old_gods": "none", "seeded": False,
                               "Plasmid": {"count": 0}, "Phage": {"count": 0}, "Dark": {"count": 0}, "deterioration": 0,
                               "gene_fortify": 0, "minor": {}, "mutation": 0}, "genes": {"minor": {}},
                      "stats": {"start": 1566692510773, "days": 0, "tdays": 0, "reset": 0, "plasmid": 0, "universes": 0,
                                "phage": 0, "starved": 0, "tstarved": 0, "died": 0, "tdied": 0, "know": 0, "tknow": 0,
                                "portals": 0, "achieve": {}, "feat": {}}, "event": 200, "new": False,
                      "version": "0.5.6",
                      "settings": {"civTabs": 7, "showEvolve": True, "showCity": False, "showIndustry": False,
                                   "showResearch": False, "showCivic": False, "showResources": False,
                                   "showMarket": False, "showStorage": False, "showGenetics": False, "showSpace": False,
                                   "showAchieve": False, "animated": True, "disableReset": False, "theme": "dark",
                                   "locale": "en-US",
                                   "space": {"home": True, "moon": False, "red": False, "hell": False, "sun": False,
                                             "gas": False, "gas_moon": False, "belt": False, "dwarf": False,
                                             "blackhole": False, "alpha": False, "proxima": False, "nebula": False,
                                             "neutron": False}, "showDeep": False, "showPortal": False,
                                   "portal": {"fortress": False, "badlands": False, "pit": False}, "showEjector": False,
                                   "resTabs": 0, "marketTabs": 0, "spaceTabs": 0, "statsTabs": 0, "mKeys": True,
                                   "arpa": {"arpaTabs": 0, "physics": True, "genetics": False, "crispr": False}},
                      "queue": {"display": False, "queue": []}, "r_queue": {"display": False, "queue": []},
                      "starDock": {}, "lastMsg": {"m": "You are protoplasm in the primordial ooze", "c": "warning"},
                      "arpa": {}}
        expected_file = os.path.join(test_data_dir, "startgame_original.txt")
        actual_file = os.path.join(tmpdir, "start_file.txt")
        evolve_save_editor.save_data = test_input
        evolve_save_editor.save_data_to_file(actual_file)
        assert filecmp.cmp(actual_file, expected_file)


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

    def test_adjust_save_data_adjusts_buildings(self, evolve_save_editor):
        test_input = {"city": {"basic_housing": {"count": 6}}, "space": {"swarm_control": {"count": 2}},
                      "interstellar": {"processing": {"count": 4}}, "portal": {"carport": {"count": 20}}}
        expected = copy.deepcopy(test_input)
        expected["city"]["basic_housing"]["count"] = evolve_save_editor.BuildingAmountsParam().housing
        expected["space"]["swarm_control"]["count"] = evolve_save_editor.BuildingAmountsParam().support
        expected["interstellar"]["processing"]["count"] = evolve_save_editor.BuildingAmountsParam().boost
        expected["portal"]["carport"]["count"] = evolve_save_editor.BuildingAmountsParam().job
        evolve_save_editor.save_data = test_input
        evolve_save_editor.adjust_save_data()
        assert evolve_save_editor.save_data == expected

    def test_adjust_save_data_fills_population(self, evolve_save_editor):
        test_input = {"resource": {"test_species": {"name": "Test_Species", "amount": 42, "max": 50}},
                      "city": {"basic_housing": {"count": 1}}, "space": {}, "interstellar": {}, "portal": {},
                      "race": {"species": "test_species"}}
        expected = copy.deepcopy(test_input)
        expected["city"]["basic_housing"]["count"] = 1000
        expected["resource"]["test_species"]["amount"] = 1000
        expected["resource"]["test_species"]["max"] = 1000
        evolve_save_editor.save_data = test_input
        evolve_save_editor.adjust_save_data()
        assert evolve_save_editor.save_data == expected

    def test_adjust_save_data_fills_soldiers(self, evolve_save_editor):
        test_input = {"city": {"garrison": {"count": 1}}, "space": {}, "interstellar": {}, "portal": {},
                      "civic": {"garrison": {"workers": 200, "wounded": 80, "raid": 200, "max": 600}}}
        expected = copy.deepcopy(test_input)
        expected["city"]["garrison"]["count"] = 1000
        expected["civic"]["garrison"]["workers"] = 3000
        expected["civic"]["garrison"]["max"] = 3000
        expected["civic"]["garrison"]["wounded"] = 0
        evolve_save_editor.save_data = test_input
        evolve_save_editor.adjust_save_data()
        assert evolve_save_editor.save_data == expected

    def test_adjust_save_data_adjusts_prestige_currency(self, evolve_save_editor):
        test_input = {
            "race": {"species": "test", "Plasmid": {"count": 100}, "Phage": {"count": 10}, "Dark": {"count": 1}},
            "stats": {"plasmid": 10000, "phage": 2000}}
        expected = {
            "race": {"species": "test", "Plasmid": {"count": 30000}, "Phage": {"count": 20000},
                     "Dark": {"count": 4000}},
            "stats": {"plasmid": 39900, "phage": 21990}}

        evolve_save_editor.save_data = test_input
        evolve_save_editor.adjust_save_data()
        assert evolve_save_editor.save_data == expected

    def test_adjust_save_data_adjusts_arpa_research(self, evolve_save_editor):
        test_input = {
            "arpa": {"launch_facility": {"complete": 15, "rank": 0}, "sequence": {"max": 50005, "progress": 2700},
                     "lhc": {"complete": 13, "rank": 45}}}
        expected = {
            "arpa": {"launch_facility": {"complete": 99, "rank": 0}, "sequence": {"max": 50005, "progress": 50000},
                     "lhc": {"complete": 99, "rank": 45}}}
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
            "RNA": {"name": "RNA", "display": True, "amount": 0, "crates": 0, "max": 100, "containers": 0},
            "DNA": {"name": "DNA", "display": False, "amount": 0, "crates": 0, "max": 100, "containers": 0}}}
        expected = {"resource": {
            "RNA": {"name": "RNA", "display": True, "amount": 100, "crates": 0, "max": 100, "containers": 0},
            "DNA": {"name": "DNA", "display": False, "amount": 100, "crates": 0, "max": 100, "containers": 0}}}
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
        expected = copy.deepcopy(test_input)
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
        expected = copy.deepcopy(test_input)
        actual = Ese.stack_resources(test_input, 240)
        assert actual == expected

    def test_stack_resources_does_not_update_unstackable_resources(self, unlocked_container_and_crate_json):
        test_input = unlocked_container_and_crate_json
        test_input["resource"] = {"RNA": {"name": "RNA", "amount": 44, "crates": 0, "containers": 0},
                                  "Oil": {"name": "Oil", "amount": 25, "crates": 0, "stackable": False,
                                          "containers": 0}}
        expected = copy.deepcopy(test_input)
        actual = Ese.stack_resources(test_input, 76)
        assert actual == expected

    def test_stack_resources_does_not_remove_extra_stackables(self, unlocked_container_and_crate_json):
        test_input = unlocked_container_and_crate_json
        test_input["resource"] = {
            "Furs": {"name": "Furs", "amount": 100, "crates": 30, "stackable": True, "containers": 30}}
        expected = copy.deepcopy(test_input)
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
        expected = copy.deepcopy(test_input)
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
        expected = copy.deepcopy(test_input)
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


class TestEvolveSaveEditorFillPopulation:
    def test_fill_population_can_handle_no_buildings(self):
        test_input = {"resource": {}, "city": {}, "space": {}, "interstellar": {}, "race": {}}
        expected = copy.deepcopy(test_input)
        actual = Ese.fill_population(test_input)
        assert actual == expected

    def test_fill_population_can_handle_missing_buildings(self):
        test_input = {"resource": {"test_species": {"name": "Test_Species", "amount": 42, "max": 50}},
                      "city": {"basic_housing": {"count": 100}}, "space": {}, "interstellar": {},
                      "race": {"species": "test_species"}}
        expected = copy.deepcopy(test_input)
        expected["resource"]["test_species"]["amount"] = 100
        expected["resource"]["test_species"]["max"] = 100
        actual = Ese.fill_population(test_input)
        assert actual == expected

    def test_fill_population_can_handle_missing_population_amount(self):
        test_input = {"resource": {"test_species": {"name": "Test_Species", "max": 100}},
                      "city": {"basic_housing": {"count": 100}}, "space": {}, "interstellar": {},
                      "race": {"species": "test_species"}}
        expected = copy.deepcopy(test_input)
        actual = Ese.fill_population(test_input)
        assert actual == expected

    def test_fill_population_can_work_with_all_housing_buildings(self):
        test_input = {"resource": {"test_species": {"name": "Test_Species", "amount": 18, "max": 100}},
                      "city": {"basic_housing": {"count": 3}, "farm": {"count": 40}, "cottage": {"count": 250},
                               "apartment": {"count": 1200}}, "space": {"living_quarters": {"count": 70000}},
                      "interstellar": {"habitat": {"count": 800000}}, "race": {"species": "test_species"}}
        expected = copy.deepcopy(test_input)
        expected["resource"]["test_species"]["amount"] = 876543
        expected["resource"]["test_species"]["max"] = 876543
        actual = Ese.fill_population(test_input)
        assert actual == expected


class TestEvolveSaveEditorFillSoldiers:
    def test_fill_soldiers_can_handle_no_buildings(self):
        test_input = {"city": {}, "space": {}, "interstellar": {}, "civic": {}}
        expected = copy.deepcopy(test_input)
        actual = Ese.fill_soldiers(test_input)
        assert actual == expected

    def test_fill_soldiers_can_handle_missing_civic(self):
        test_input = {"city": {"garrison": {"count": 100}}, "space": {"space_barracks": {"count": 20}},
                      "interstellar": {"cruiser": {"count": 3}}, "civic": {}}
        expected = copy.deepcopy(test_input)
        actual = Ese.fill_soldiers(test_input)
        assert actual == expected

    def test_fill_soldiers_can_handle_missing_buildings(self):
        test_input = {"city": {"garrison": {"count": 10}}, "space": {"space_barracks": {"count": 3}},
                      "interstellar": {}, "civic": {"garrison": {"workers": 15, "wounded": 10, "raid": 10, "max": 1}}}
        expected = copy.deepcopy(test_input)
        expected["civic"]["garrison"]["workers"] = 36
        expected["civic"]["garrison"]["max"] = 36
        expected["civic"]["garrison"]["wounded"] = 0
        actual = Ese.fill_soldiers(test_input)
        assert actual == expected

    def test_fill_soldiers_can_work_with_all_buildings(self):
        test_input = {"city": {"garrison": {"count": 100}}, "space": {"space_barracks": {"count": 10}},
                      "interstellar": {"cruiser": {"count": 1}},
                      "civic": {"garrison": {"workers": 15, "wounded": 100, "raid": 15, "max": 100}}}
        expected = copy.deepcopy(test_input)
        expected["civic"]["garrison"]["workers"] = 323
        expected["civic"]["garrison"]["max"] = 323
        expected["civic"]["garrison"]["wounded"] = 0
        actual = Ese.fill_soldiers(test_input)
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
        expected = copy.deepcopy(test_input)
        # noinspection PyProtectedMember
        actual_data, actual_added = Ese._update_prestige_currency_value(test_input, "fake", 1000)
        assert actual_data == expected
        assert actual_added == 0


class TestEvolveSaveEditorAdjustArpaResearch:
    def test_adjust_arpa_research_can_handle_no_research(self):
        test_input = {"arpa": {}}
        expected = copy.deepcopy(test_input)
        actual = Ese.adjust_arpa_research(test_input)
        assert actual == expected

    def test_adjust_arpa_research_skips_broken_nodes(self):
        test_input = {"arpa": {"sequence": {"progress": 0}, "launch_facility": {"rank": 0}, "lhc": {"rank": 10}}}
        expected = copy.deepcopy(test_input)
        actual = Ese.adjust_arpa_research(test_input)
        assert actual == expected

    def test_adjust_arpa_research_does_not_update_launch_facility_past_rank_1(self):
        test_input = {"arpa": {"launch_facility": {"complete": 0, "rank": 1}}}
        expected = copy.deepcopy(test_input)
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
        expected = copy.deepcopy(test_input)
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
