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


# noinspection SpellCheckingInspection
@pytest.fixture
def start_game_json():
    return {"seed": 2953, "resource": {
        "RNA": {"name": "RNA", "display": True, "amount": 0, "crates": 0, "diff": 0, "delta": 0, "max": 100, "rate": 1,
                "containers": 0},
        "DNA": {"name": "DNA", "display": False, "amount": 0, "crates": 0, "diff": 0, "delta": 0, "max": 100, "rate": 1,
                "containers": 0}}, "evolution": {}, "tech": {}, "city": {
        "morale": {"current": 0, "unemployed": 0, "stress": 0, "entertain": 0, "leadership": 0, "season": 0,
                   "weather": 0, "warmonger": 0, "tax": 0},
        "calendar": {"day": 0, "year": 0, "season": 0, "weather": 2, "temp": 1, "moon": 0, "wind": 0, "orbit": 365},
        "powered": False, "power": 0, "biome": "grassland", "geology": {},
        "market": {"qty": 10, "mtrade": 0, "trade": 0, "active": False}}, "space": {}, "interstellar": {}, "portal": {},
            "civic": {"free": 0, "farmer": {"job": "farmer", "name": "Farmer", "display": False, "workers": 0, "max": 0,
                                            "impact": 1.35, "assigned": 0, "stress": 5},
                      "lumberjack": {"job": "lumberjack", "name": "Lumberjack", "display": False, "workers": 0,
                                     "max": 0, "impact": 1, "assigned": 0, "stress": 5},
                      "quarry_worker": {"job": "quarry_worker", "name": "Quarry Worker", "display": False, "workers": 0,
                                        "max": 0, "impact": 1, "assigned": 0, "stress": 5},
                      "miner": {"job": "miner", "name": "Miner", "display": False, "workers": 0, "max": 0, "impact": 1,
                                "assigned": 0, "stress": 4},
                      "coal_miner": {"job": "coal_miner", "name": "Coal Miner", "display": False, "workers": 0,
                                     "max": 0, "impact": 0.2, "assigned": 0, "stress": 4},
                      "craftsman": {"job": "craftsman", "name": "Craftsman", "display": False, "workers": 0, "max": 0,
                                    "impact": 1, "assigned": 0, "stress": 5},
                      "cement_worker": {"job": "cement_worker", "name": "Cement Plant Worker", "display": False,
                                        "workers": 0, "max": 0, "impact": 0.4, "assigned": 0, "stress": 5},
                      "entertainer": {"job": "entertainer", "name": "Entertainer", "display": False, "workers": 0,
                                      "max": 0, "impact": 1, "assigned": 0, "stress": 10},
                      "professor": {"job": "professor", "name": "Professor", "display": False, "workers": 0, "max": 0,
                                    "impact": 0.5, "assigned": 0, "stress": 6},
                      "scientist": {"job": "scientist", "name": "Scientist", "display": False, "workers": 0, "max": 0,
                                    "impact": 1, "assigned": 0, "stress": 5},
                      "banker": {"job": "banker", "name": "Banker", "display": False, "workers": 0, "max": 0,
                                 "impact": 0.1, "assigned": 0, "stress": 6},
                      "colonist": {"job": "colonist", "name": "Colonist", "display": False, "workers": 0, "max": 0,
                                   "impact": 1, "assigned": 0, "stress": 5},
                      "space_miner": {"job": "space_miner", "name": "Space Miner", "display": False, "workers": 0,
                                      "max": 0, "impact": 1, "assigned": 0, "stress": 5},
                      "hell_surveyor": {"job": "hell_surveyor", "name": "Surveyor", "display": False, "workers": 0,
                                        "max": 0, "impact": 1, "assigned": 0, "stress": 1},
                      "taxes": {"tax_rate": 20, "display": False}},
            "race": {"species": "protoplasm", "gods": "none", "old_gods": "none", "seeded": False,
                     "Plasmid": {"count": 0}, "Phage": {"count": 0}, "Dark": {"count": 0}, "deterioration": 0,
                     "gene_fortify": 0, "minor": {}, "mutation": 0}, "genes": {"minor": {}},
            "stats": {"start": 1566692510773, "days": 0, "tdays": 0, "reset": 0, "plasmid": 0, "universes": 0,
                      "phage": 0, "starved": 0, "tstarved": 0, "died": 0, "tdied": 0, "know": 0, "tknow": 0,
                      "portals": 0, "achieve": {}, "feat": {}}, "event": 200, "new": False, "version": "0.5.6",
            "settings": {"civTabs": 7, "showEvolve": True, "showCity": False, "showIndustry": False,
                         "showResearch": False, "showCivic": False, "showResources": False, "showMarket": False,
                         "showStorage": False, "showGenetics": False, "showSpace": False, "showAchieve": False,
                         "animated": True, "disableReset": False, "theme": "dark", "locale": "en-US",
                         "space": {"home": True, "moon": False, "red": False, "hell": False, "sun": False, "gas": False,
                                   "gas_moon": False, "belt": False, "dwarf": False, "blackhole": False, "alpha": False,
                                   "proxima": False, "nebula": False, "neutron": False}, "showDeep": False,
                         "showPortal": False, "portal": {"fortress": False, "badlands": False, "pit": False},
                         "showEjector": False, "resTabs": 0, "marketTabs": 0, "spaceTabs": 0, "statsTabs": 0,
                         "mKeys": True, "arpa": {"arpaTabs": 0, "physics": True, "genetics": False, "crispr": False}},
            "queue": {"display": False, "queue": []}, "r_queue": {"display": False, "queue": []}, "starDock": {},
            "lastMsg": {"m": "You are protoplasm in the primordial ooze", "c": "warning"}, "arpa": {}}


# noinspection SpellCheckingInspection
@pytest.fixture()
def end_game_json():
    return {"seed": 90001, "resource": {
        "RNA": {"name": "RNA", "display": False, "amount": 44, "crates": 0, "diff": 0, "delta": 0, "max": 300,
                "rate": 1, "containers": 0},
        "DNA": {"name": "DNA", "display": False, "amount": 44, "crates": 0, "diff": 0, "delta": 0, "max": 300,
                "rate": 1, "containers": 0},
        "Money": {"name": "$", "display": True, "amount": 2034884982240, "crates": 0, "diff": 184816132262.68,
                  "delta": 0, "max": 2034884982240, "rate": 1, "stackable": False, "containers": 0},
        "sharkin": {"name": "Sharkin", "display": True, "amount": 5547, "crates": 0, "diff": 0, "delta": 0, "max": 5752,
                    "rate": 0, "stackable": False, "containers": 0},
        "Knowledge": {"name": "Knowledge", "display": True, "amount": 247213594, "crates": 0, "diff": 32710410757.46,
                      "delta": 0, "max": 247213594, "rate": 1, "stackable": False, "containers": 0},
        "Crates": {"name": "Crate", "display": True, "amount": 0, "crates": 0, "diff": 0, "delta": 0, "max": 0,
                   "rate": 0, "stackable": False, "containers": 0},
        "Containers": {"name": "Container", "display": True, "amount": 0, "crates": 0, "diff": 0, "delta": 0, "max": 0,
                       "rate": 0, "stackable": False, "containers": 0},
        "Food": {"name": "Food", "display": True, "value": 13.87, "amount": 233752315, "crates": 0,
                 "diff": 2380440673.88, "delta": 0, "max": 233752315, "rate": 1, "stackable": True, "containers": 0,
                 "trade": 0},
        "Lumber": {"name": "Lumber", "display": True, "value": 5.259999999999999, "amount": 4281615685630.105,
                   "crates": 816, "diff": 4584076415.95, "delta": 0, "max": 9308117012481, "rate": 1, "stackable": True,
                   "containers": 2873, "trade": 0},
        "Stone": {"name": "Stone", "display": True, "value": 4.719999999999999, "amount": 936434740642.5002,
                  "crates": 824, "diff": 840769074.04, "delta": 0, "max": 9308255393262, "rate": 1, "stackable": True,
                  "containers": 2883, "trade": 0},
        "Furs": {"name": "Furs", "display": True, "value": 10.55, "amount": 9857266217.993454, "crates": 824,
                 "diff": 11969668.58, "delta": 0, "max": 4900302054057, "rate": 1, "stackable": True,
                 "containers": 2883, "trade": 0},
        "Copper": {"name": "Copper", "display": True, "value": 37.160000000000046, "amount": 1422613165727.07,
                   "crates": 824, "diff": 1464215113.32, "delta": 0, "max": 4225424668057, "rate": 1, "stackable": True,
                   "containers": 2883, "trade": 0},
        "Iron": {"name": "Iron", "display": True, "value": 31.460000000000026, "amount": 184329007184.4036,
                 "crates": 824, "diff": 128228770.55, "delta": 0, "max": 4264828707957, "rate": 1, "stackable": True,
                 "containers": 2883, "trade": 0},
        "Aluminium": {"name": "Aluminium", "display": True, "value": 54.82000000000006, "amount": 330335333929.29706,
                      "crates": 824, "diff": 470821219.46, "delta": 0, "max": 3666088209107, "rate": 1,
                      "stackable": True, "containers": 2883, "trade": -2198},
        "Cement": {"name": "Cement", "display": True, "value": 23.970000000000006, "amount": 4879598634.946998,
                   "crates": 824, "diff": 6209795.64, "delta": 0, "max": 3429663969157, "rate": 1, "stackable": True,
                   "containers": 2883, "trade": 0},
        "Coal": {"name": "Coal", "display": True, "value": 29.979999999999958, "amount": 4254222724.72751,
                 "crates": 824, "diff": 2947923.95, "delta": 0, "max": 1770688375907, "rate": 1, "stackable": True,
                 "containers": 2883, "trade": 0},
        "Oil": {"name": "Oil", "display": True, "value": 64.79999999999997, "amount": 14777535030, "crates": 0,
                "diff": 222861337.7, "delta": 0, "max": 14777535030, "rate": 1, "stackable": False, "containers": 0,
                "trade": 0},
        "Uranium": {"name": "Uranium", "display": True, "value": 545.0800000000002, "amount": 396259937.4133488,
                    "crates": 0, "diff": 297940.13, "delta": 0, "max": 3450613810, "rate": 1, "stackable": False,
                    "containers": 0, "trade": 2},
        "Steel": {"name": "Steel", "display": True, "value": 110.86000000000001, "amount": 494075786.4418533,
                  "crates": 1648, "diff": 1932177.91, "delta": 0, "max": 1005813586781, "rate": 1, "stackable": True,
                  "containers": 5765, "trade": 0},
        "Titanium": {"name": "Titanium", "display": True, "value": 147.3400000000001, "amount": 156345959502.29935,
                     "crates": 824, "diff": 117181345.53, "delta": 0, "max": 596916187607, "rate": 1, "stackable": True,
                     "containers": 2883, "trade": 50},
        "Alloy": {"name": "Alloy", "display": True, "value": 338.6499999999998, "amount": 1033008257.8256149,
                  "crates": 824, "diff": 3322715.23, "delta": 0, "max": 63292371007, "rate": 1, "stackable": True,
                  "containers": 2883, "trade": 50},
        "Polymer": {"name": "Polymer", "display": True, "value": 240.13999999999993, "amount": 59455495.94143558,
                    "crates": 824, "diff": 1564811.37, "delta": 0, "max": 51604806307, "rate": 1, "stackable": True,
                    "containers": 2883, "trade": 50},
        "Iridium": {"name": "Iridium", "display": True, "value": 423.11999999999995, "amount": 8459414646.298389,
                    "crates": 824, "diff": 6580124.39, "delta": 0, "max": 51827426557, "rate": 1, "stackable": True,
                    "containers": 2883, "trade": 50},
        "Helium_3": {"name": "Helium-3", "display": True, "value": 609.3600000000002, "amount": 8308188548, "crates": 0,
                     "diff": 168382587.88, "delta": 0, "max": 8308188548, "rate": 1, "stackable": False,
                     "containers": 0, "trade": 0},
        "Deuterium": {"name": "Deuterium", "display": True, "value": 955.7999999999998, "amount": 199934551.2414764,
                      "crates": 0, "diff": 337442.02, "delta": 0, "max": 1678556903, "rate": 1, "stackable": False,
                      "containers": 0},
        "Neutronium": {"name": "Neutronium", "display": True, "value": 1497.000000000001, "amount": 38406752738.5783,
                       "crates": 0, "diff": 44564837.75, "delta": 0, "max": 71516052526, "rate": 1, "stackable": False,
                       "containers": 0},
        "Adamantite": {"name": "Adamantite", "display": True, "value": 2253.4199999999996, "amount": 3596897184.5857363,
                       "crates": 824, "diff": 6580119.39, "delta": 0, "max": 210289443457, "rate": 1, "stackable": True,
                       "containers": 2883},
        "Infernite": {"name": "Infernite", "display": True, "value": 2750.429999999999, "amount": 46639750.22398848,
                      "crates": 0, "diff": 67919.64, "delta": 0, "max": 44500931306, "rate": 1, "stackable": False,
                      "containers": 0},
        "Elerium": {"name": "Elerium", "display": True, "value": 1991.4599999999998, "amount": 458041651, "crates": 0,
                    "diff": 3221396.48, "delta": 0, "max": 458041651, "rate": 1, "stackable": False, "containers": 0},
        "Nano_Tube": {"name": "Nano Tube", "display": True, "value": 742.7100000000002, "amount": 3709576544.756839,
                      "crates": 0, "diff": 5031510.66, "delta": 0, "max": 381350042300, "rate": 1, "stackable": False,
                      "containers": 0},
        "Graphene": {"name": "Graphene", "display": True, "value": 2996.2, "amount": 41748264561.10182, "crates": 824,
                     "diff": 51291187.01, "delta": 0, "max": 51604806257, "rate": 1, "stackable": True,
                     "containers": 2883},
        "Stanene": {"name": "Stanene", "display": True, "value": 3603.7900000000004, "amount": 2964812985.5700603,
                    "crates": 824, "diff": 26574906.67, "delta": 0, "max": 51604806257, "rate": 1, "stackable": True,
                    "containers": 2883},
        "Genes": {"name": "Genes", "display": True, "value": 0, "amount": 2000000626.5, "crates": 0, "diff": 0,
                  "delta": 0, "max": -2, "rate": 0, "stackable": False, "containers": 0},
        "Soul_Gem": {"name": "Soul_Gem", "display": True, "value": 0, "amount": 1999897279, "crates": 0, "diff": 0,
                     "delta": 0, "max": -2, "rate": 0, "stackable": False, "containers": 0},
        "Plywood": {"name": "Plywood", "display": True, "amount": 19999846003336.375, "crates": 0, "diff": 0,
                    "delta": -140000, "max": -1, "rate": 0, "stackable": False, "containers": 0},
        "Brick": {"name": "Brick", "display": True, "amount": 19999981820223.28, "crates": 0, "diff": 0, "delta": 0,
                  "max": -1, "rate": 0, "stackable": False, "containers": 0},
        "Wrought_Iron": {"name": "Wrought Iron", "display": True, "amount": 19999990899541.406, "crates": 0, "diff": 0,
                         "delta": 0, "max": -1, "rate": 0, "stackable": False, "containers": 0},
        "Sheet_Metal": {"name": "Sheet Metal", "display": True, "amount": 19997888305435, "crates": 0, "diff": 0,
                        "delta": 0, "max": -1, "rate": 0, "stackable": False, "containers": 0},
        "Mythril": {"name": "Mythril", "display": True, "amount": 19999917055284, "crates": 0, "diff": 0, "delta": 0,
                    "max": -1, "rate": 0, "stackable": False, "containers": 0},
        "Aerogel": {"name": "Aerogel", "display": True, "amount": 19999766805044, "crates": 0, "diff": 0, "delta": 0,
                    "max": -1, "rate": 0, "stackable": False, "containers": 0}},
            "evolution": {"dna": 1, "membrane": {"count": 10}, "organelles": {"count": 15}, "nucleus": {"count": 5},
                          "eukaryotic_cell": {"count": 5}, "mitochondria": {"count": 3},
                          "sexual_reproduction": {"count": 1}, "phagocytosis": {"count": 1}, "final": 100,
                          "multicellular": {"count": 1}, "bilateral_symmetry": {"count": 1}, "aquatic": {"count": 1},
                          "sentience": {"count": 1}, "sharkin": {"count": 0}, "octigoran": {"count": 0},
                          "bunker": {"count": 1}, "plasmid": {"count": 0}, "trade": {"count": 0}, "craft": {"count": 0},
                          "crispr": {"count": 0}, "junker": {"count": 0}, "joyless": {"count": 0}},
            "tech": {"theology": 5, "primitive": 3, "religion": 1, "queue": 3, "r_queue": 1, "wsc": 1, "agriculture": 7,
                     "housing": 3, "currency": 6, "storage": 7, "science": 15, "mining": 4, "axe": 6, "banking": 12,
                     "military": 9, "farm": 1, "cement": 6, "theatre": 3, "foundry": 8, "reproduction": 1,
                     "smelting": 7, "alumina": 2, "container": 7, "high_tech": 14, "trade": 3, "broadcast": 3,
                     "medic": 2, "explosives": 3, "fanaticism": 4, "hoe": 5, "anthropology": 4, "saw": 2, "hammer": 4,
                     "pickaxe": 6, "mercs": 2, "boot_camp": 2, "housing_reduction": 3, "steel_container": 6,
                     "home_safe": 3, "v_train": 1, "copper": 1, "mine_conveyor": 1, "oil": 7, "wharf": 1, "titanium": 3,
                     "factory": 3, "gambling": 3, "genetics": 7, "alloy": 1, "uranium": 4, "monument": 2, "polymer": 2,
                     "mad": 1, "launch_facility": 1, "space": 6, "monuments": 74, "stock_exchange": 69,
                     "space_explore": 4, "satellite": 1, "supercollider": 80, "particles": 4, "moon": 1, "luna": 3,
                     "vault": 4, "mass": 1, "hell": 1, "solar": 5, "gas_moon": 2, "mars": 5, "asteroid": 7,
                     "gas_giant": 1, "unify": 2, "marines": 1, "ancient_study": 1, "elerium": 2, "swarm": 3,
                     "genesis": 6, "dwarf": 1, "helium": 1, "nano": 1, "drone": 1, "space_housing": 1,
                     "world_control": 1, "ftl": 2, "portal": 5, "alpha": 3, "proxima": 3, "nebula": 3,
                     "portal_guard": 0, "turret": 2, "droids": 1, "q_factory": 1, "infernite": 4, "stanene": 1,
                     "graphene": 1, "superstar": 1, "aerogel": 1, "cruiser": 1, "neutron": 1, "blackhole": 5,
                     "ram_scoop": 1, "fusion": 1, "gravity": 2, "whitehole": 3}, "city": {
            "calendar": {"day": 391, "year": 2, "weather": 1, "temp": 0, "moon": 24, "wind": 1, "orbit": 461,
                         "season": 3}, "biome": "oceanic",
            "morale": {"current": 2024, "unemployed": 0, "stress": -1403, "entertain": 3350, "leadership": 0,
                       "season": -5, "weather": 0, "warmonger": 0, "tax": -30, "frenzy": 12}, "powered": True,
            "power": 60862.5550427156, "geology": {"Iridium": 0.1, "Uranium": 0.1},
            "market": {"qty": "1000", "mtrade": 2400, "trade": 2400, "active": True}, "lumber": 1,
            "power_total": 78999.5550427156, "farm": {"count": 100}, "basic_housing": {"count": 1000},
            "shed": {"count": 100}, "university": {"count": 100}, "rock_quarry": {"count": 100, "on": 100},
            "lumber_yard": {"count": 100}, "bank": {"count": 100}, "garrison": {"count": 100}, "silo": {"count": 100},
            "mine": {"count": 100, "on": 100}, "cement_plant": {"count": 100, "on": 100}, "library": {"count": 1000},
            "temple": {"count": 1000}, "amphitheatre": {"count": 500},
            "foundry": {"count": 100, "crafting": 0, "Plywood": 0, "Brick": 0, "Bronze": 0, "Wrought_Iron": 0,
                        "Sheet_Metal": 0, "Mythril": 0, "Aerogel": 0}, "cottage": {"count": 1000},
            "mill": {"count": 100, "on": 100},
            "smelter": {"count": 100, "Wood": 36, "Coal": 10, "Oil": 54, "Iron": 2, "Steel": 98},
            "coal_mine": {"count": 100, "on": 100}, "metal_refinery": {"count": 100, "on": 0},
            "storage_yard": {"count": 100}, "wardenclyffe": {"count": 100, "on": 100}, "trade": {"count": 300},
            "coal_power": {"count": 1000, "on": 1000}, "apartment": {"count": 500, "on": 500},
            "hospital": {"count": 1000}, "sawmill": {"count": 100, "on": 100}, "boot_camp": {"count": 1000},
            "warehouse": {"count": 500},
            "factory": {"count": 100, "on": 100, "Lux": 0, "Alloy": 40, "Polymer": 20, "Nano": 40, "Stanene": 100},
            "oil_well": {"count": 1000}, "wharf": {"count": 100}, "oil_depot": {"count": 1000},
            "oil_power": {"count": 2000, "on": 2000}, "casino": {"count": 500, "on": 500},
            "biolab": {"count": 200, "on": 200}, "fission_power": {"count": 2000, "on": 2000},
            "tourist_center": {"count": 500, "on": 500}, "mass_driver": {"count": 500, "on": 500}},
            "space": {"satellite": {"count": 100}, "propellant_depot": {"count": 100}, "gps": {"count": 100},
                      "moon_base": {"count": 100, "on": 100, "support": 150, "s_max": 300},
                      "iridium_mine": {"count": 50, "on": 50}, "helium_mine": {"count": 50, "on": 50},
                      "observatory": {"count": 50, "on": 50}, "nav_beacon": {"count": 100, "on": 100},
                      "spaceport": {"count": 50, "on": 50, "support": 302, "s_max": 350},
                      "swarm_control": {"count": 50, "support": 300, "s_max": 300},
                      "living_quarters": {"count": 52, "on": 52}, "garage": {"count": 100},
                      "red_mine": {"count": 50, "on": 50}, "fabrication": {"count": 50, "on": 50},
                      "geothermal": {"count": 50, "on": 50},
                      "space_station": {"count": 100, "on": 100, "support": 220, "s_max": 300},
                      "outpost": {"count": 100, "on": 100}, "iridium_ship": {"count": 10, "on": 10},
                      "iron_ship": {"count": 10, "on": 10}, "biodome": {"count": 10, "on": 10},
                      "ziggurat": {"count": 1000}, "red_tower": {"count": 100, "on": 100},
                      "red_factory": {"count": 100, "on": 100}, "swarm_satellite": {"count": 1200},
                      "swarm_plant": {"count": 100}, "gas_mining": {"count": 100, "on": 100},
                      "gas_storage": {"count": 100}, "space_barracks": {"count": 100, "on": 100},
                      "oil_extractor": {"count": 100, "on": 100}, "elerium_ship": {"count": 100, "on": 100},
                      "exotic_lab": {"count": 100, "on": 90},
                      "star_dock": {"count": 1, "ship": 0, "probe": 0, "template": "sharkin"},
                      "elerium_contain": {"count": 1000, "on": 1000}, "drone": {"count": 100},
                      "e_reactor": {"count": 1000, "on": 1000}, "world_collider": {"count": 1859},
                      "world_controller": {"count": 1, "on": 1}, "vr_center": {"count": 50, "on": 50}},
            "interstellar": {"starport": {"count": 100, "on": 100, "support": 380, "s_max": 700},
                             "nexus": {"count": 59, "on": 59, "support": 39, "s_max": 118}, "warehouse": {"count": 100},
                             "mining_droid": {"count": 100, "on": 100, "adam": 3, "uran": 1, "coal": 0, "alum": 0},
                             "xfer_station": {"count": 100, "on": 100}, "cargo_yard": {"count": 100},
                             "laboratory": {"count": 100, "on": 100}, "processing": {"count": 100, "on": 100},
                             "habitat": {"count": 100, "on": 100}, "dyson": {"count": 100},
                             "g_factory": {"count": 38, "on": 38, "Lumber": 38, "Coal": 0, "Oil": 0},
                             "exchange": {"count": 42, "on": 42}, "cruiser": {"count": 59, "on": 59},
                             "neutron_miner": {"count": 42, "on": 42}, "far_reach": {"count": 33, "on": 33},
                             "stellar_engine": {"count": 100, "mass": 7.98322864834621, "exotic": 0.035418192317915896},
                             "harvester": {"count": 40, "on": 1}, "fusion": {"count": 0, "on": 0},
                             "elerium_prospector": {"count": 38, "on": 38},
                             "mass_ejector": {"count": 38, "on": 38, "total": 0, "mass": 0, "Food": 0, "Lumber": 0,
                                              "Stone": 0, "Furs": 0, "Copper": 0, "Iron": 0, "Aluminium": 0,
                                              "Cement": 0, "Coal": 0, "Oil": 0, "Uranium": 0, "Steel": 0, "Titanium": 0,
                                              "Alloy": 0, "Polymer": 0, "Iridium": 0, "Helium_3": 0, "Deuterium": 0,
                                              "Neutronium": 0, "Adamantite": 0, "Infernite": 0, "Elerium": 0,
                                              "Nano_Tube": 0, "Graphene": 0, "Stanene": 0, "Plywood": 0, "Brick": 0,
                                              "Wrought_Iron": 0, "Sheet_Metal": 0, "Mythril": 0, "Aerogel": 0}},
            "portal": {
                "fortress": {"threat": 2841, "garrison": 0, "walls": 100, "repair": 0, "patrols": 0, "patrol_size": 1,
                             "siege": 690, "notify": "Yes"}, "turret": {"count": 100, "on": 100},
                "carport": {"count": 100, "damaged": 37, "repair": 50}, "war_drone": {"count": 43, "on": 43},
                "sensor_drone": {"count": 45, "on": 45}, "attractor": {"count": 54, "on": 54},
                "war_droid": {"count": 45, "on": 45}}, "civic": {"free": 0,
                                                                 "farmer": {"job": "farmer", "name": "Farmer",
                                                                            "display": True, "workers": 0, "max": -1,
                                                                            "impact": 1.35, "assigned": 0, "stress": 5},
                                                                 "lumberjack": {"job": "lumberjack",
                                                                                "name": "Lumberjack", "display": True,
                                                                                "workers": 1718, "max": -1, "impact": 9,
                                                                                "assigned": 1718, "stress": 5},
                                                                 "quarry_worker": {"job": "quarry_worker",
                                                                                   "name": "Quarry Worker",
                                                                                   "display": True, "workers": 1714,
                                                                                   "max": -1, "impact": 1,
                                                                                   "assigned": 1714, "stress": 5},
                                                                 "miner": {"job": "miner", "name": "Miner",
                                                                           "display": True, "workers": 100, "max": 100,
                                                                           "impact": 1, "assigned": 100, "stress": 4},
                                                                 "coal_miner": {"job": "coal_miner",
                                                                                "name": "Coal Miner", "display": True,
                                                                                "workers": 100, "max": 100,
                                                                                "impact": 0.2, "assigned": 100,
                                                                                "stress": 4},
                                                                 "craftsman": {"job": "craftsman", "name": "Craftsman",
                                                                               "display": True, "workers": 0,
                                                                               "max": 150, "impact": 1, "assigned": 0,
                                                                               "stress": 5},
                                                                 "cement_worker": {"job": "cement_worker",
                                                                                   "name": "Cement Plant Worker",
                                                                                   "display": True, "workers": 200,
                                                                                   "max": 200, "impact": 0.4,
                                                                                   "assigned": 200, "stress": 5},
                                                                 "entertainer": {"job": "entertainer",
                                                                                 "name": "Entertainer", "display": True,
                                                                                 "workers": 1000, "max": 1000,
                                                                                 "impact": 1, "assigned": 1000,
                                                                                 "stress": 10},
                                                                 "professor": {"job": "professor", "name": "Professor",
                                                                               "display": True, "workers": 100,
                                                                               "max": 100, "impact": 10.5,
                                                                               "assigned": 100, "stress": 6},
                                                                 "scientist": {"job": "scientist", "name": "Scientist",
                                                                               "display": True, "workers": 100,
                                                                               "max": 100, "impact": 1, "assigned": 100,
                                                                               "stress": 5},
                                                                 "banker": {"job": "banker", "name": "Banker",
                                                                            "display": True, "workers": 100, "max": 100,
                                                                            "impact": 0.1, "assigned": 100,
                                                                            "stress": 6},
                                                                 "colonist": {"job": "colonist", "name": "Colonist",
                                                                              "display": True, "workers": 52, "max": 52,
                                                                              "impact": 1, "assigned": 52, "stress": 5},
                                                                 "space_miner": {"job": "space_miner",
                                                                                 "name": "Space Miner", "display": True,
                                                                                 "workers": 300, "max": 300,
                                                                                 "impact": 1, "assigned": 300,
                                                                                 "stress": 5},
                                                                 "hell_surveyor": {"job": "hell_surveyor",
                                                                                   "name": "Surveyor", "display": True,
                                                                                   "workers": 63, "max": 63,
                                                                                   "impact": 1, "assigned": 63,
                                                                                   "stress": 1},
                                                                 "taxes": {"tax_rate": 50, "display": True},
                                                                 "garrison": {"display": True, "disabled": False,
                                                                              "progress": 0, "tactic": 4,
                                                                              "workers": 677, "wounded": 0, "raid": 500,
                                                                              "max": 677, "mercs": True, "fatigue": 0,
                                                                              "protest": 0, "m_use": 75},
                                                                 "mad": {"display": True, "armed": True}},
            "race": {"species": "sharkin", "Plasmid": {"count": 3450102}, "Phage": {"count": 2114155},
                     "Dark": {"count": 69.784}, "seeded": True, "probes": 28, "seed": 6830, "gods": "troll",
                     "old_gods": "scorpid", "deterioration": 2, "gene_fortify": 0,
                     "minor": {"cunning": 5, "gambler": 5, "metallurgist": 5, "analytical": 5, "ambidextrous": 5,
                               "resilient": 5}, "mutation": 5, "chose": "Oceanic9813", "submerged": 1, "frenzy": 2217,
                     "apex_predator": 1, "ambidextrous": 21, "regenerative": 1, "analytical": 21, "suction_grip": 1,
                     "modified": 2, "metallurgist": 21, "cunning": 21, "gambler": 21, "resilient": 21}, "genes": {
            "minor": {"ambidextrous": 15, "analytical": 15, "metallurgist": 15, "cunning": 15, "gambler": 15,
                      "resilient": 15}, "store": 4, "queue": 2, "evolve": 2, "birth": 1, "creep": 5, "crafty": 3,
            "challenge": 2, "synthesis": 3, "mutation": 3, "old_gods": 1, "ancients": 1, "transcendence": 1},
            "stats": {"start": 1566450454251, "days": 1312, "tdays": 14122, "reset": 3, "plasmid": 4351502,
                      "universes": 1, "phage": 2170000, "starved": 1, "tstarved": 4, "died": 617, "tdied": 1068,
                      "know": 1076848306, "tknow": 91126266, "portals": 0,
                      "achieve": {"red_tactics": 1, "apocalypse": 1, "extinct_entish": 1, "world_domination": 1,
                                  "colonist": 1, "extinct_scorpid": 1, "syndicate": 1, "pandemonium": 1, "blackhole": 1,
                                  "whitehole": 1, "warmonger": 1, "laser_shark": 1, "illuminati": 1}, "feat": {}},
            "event": 493, "new": False, "version": "0.5.6",
            "settings": {"civTabs": 7, "showEvolve": False, "showCity": True, "showIndustry": False,
                         "showResearch": True, "showCivic": True, "showResources": True, "showMarket": True,
                         "showStorage": True, "showGenetics": True, "showSpace": True, "showAchieve": True,
                         "animated": True, "disableReset": False, "theme": "dark", "locale": "en-US",
                         "space": {"home": True, "moon": True, "red": True, "hell": True, "sun": True, "gas": True,
                                   "gas_moon": True, "belt": True, "dwarf": True, "blackhole": True, "alpha": True,
                                   "proxima": True, "nebula": True, "neutron": True}, "showDeep": True,
                         "showPortal": True, "portal": {"fortress": True, "badlands": True, "pit": False},
                         "showEjector": True, "resTabs": 0, "marketTabs": 0, "spaceTabs": 1, "statsTabs": 1,
                         "mKeys": True, "arpa": {"arpaTabs": 1, "physics": True, "genetics": True, "crispr": True}},
            "queue": {"display": True, "queue": []}, "starDock": {"probes": {"count": 41}, "seeder": {"count": 100}},
            "lastMsg": {"m": "A surveyor was killed by demonic creatures.", "c": "warning"},
            "arpa": {"lhc": {"complete": 0, "rank": 80}, "stock_exchange": {"complete": 0, "rank": 69},
                     "m_type": "Sculpture", "monument": {"complete": 0, "rank": 74},
                     "sequence": {"max": 850000, "progress": 374800, "time": 475200, "on": True, "boost": True,
                                  "auto": True}, "launch_facility": {"complete": 0, "rank": 1}},
            "r_queue": {"display": True, "queue": []}}


class TestEvolveSaveEditorSaveLoadFile:
    def test_save_data_to_file_handles_start_file(self, evolve_save_editor, tmpdir, start_game_json):
        test_input = start_game_json
        expected_file = os.path.join(test_data_dir, "startgame_original.txt")
        actual_file = os.path.join(tmpdir, "start_file.txt")
        evolve_save_editor.save_data = test_input
        evolve_save_editor.save_data_to_file(actual_file)
        assert filecmp.cmp(actual_file, expected_file)

    def test_save_data_to_file_handles_end_file(self, evolve_save_editor, tmpdir, end_game_json):
        test_input = end_game_json
        expected_file = os.path.join(test_data_dir, "endgame_original.txt")
        actual_file = os.path.join(tmpdir, "end_file.txt")
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
