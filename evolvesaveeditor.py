# This script is intended to be a save editor for the game evolve
# The game can be found at https://pmotschmann.github.io/Evolve/

import argparse
import logging
import sys
import lzstring


def main():
    """
    Call parse_args, then pass to edit_evolve_save() to do all the work
    :return: nothing
    """
    parse_args(sys.argv[1:])
    edit_evolve_save()


def parse_args(args):
    """
        Parses and validates command line arguments
        :param list args: arguments passed into the script (usually sys.argv[1:])
        :return: arguments parsed into a neat object
        """
    parser = argparse.ArgumentParser(
        description="Save editor for game evolve")
    return parser.parse_args(args)


def edit_evolve_save():
    pass


def get_logger():
    logger = logging.getLogger("evolvesaveeditor.py")
    configure_logging(logger)
    return logger


def configure_logging(logger):
    logger.setLevel(logging.INFO)
    if not logger.hasHandlers():
        add_console_logging(logger)


def add_console_logging(logger):
    console_handler = logging.StreamHandler(sys.stdout)
    log_format = get_logging_format()
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)


def get_logging_format():
    return logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")


class EvolveSaveEditor:
    # save_data attribute
    # load_data_from_file method
    # save_data_to_file method
    # adjust_data method that calls all individual helper methods before saving the data to member
    # individual data methods that accept a json object and return the modified object
    #   expand_resource_storage (add containers & crates)

    BUILDING_TYPES = {
        # buildings that provide a production or efficiency bonus bu don't make things themselves
        "boost": ["attractor", "biodome", "biolab", "boot_camp", "drone", "far_reach", "gps", "hospital",
                  "library", "lumber_yard", "mass_driver", "mass_ejector", "metal_refinery", "processing",
                  "red_mine", "rock_quarry", "satellite", "sawmill", "swarm_plant", "temple", "tourist_center",
                  "turret", "vr_center", "war_droid", "war_drone", "ziggurat"],
        # buildings that increase the citizen cap
        "housing": ["apartment", "basic_housing", "cottage", "farm", "habitat"],
        # buildings that provide job slots for citizens
        "job": ["bank", "carport", "cement_plant", "coal_mine", "fabrication", "foundry", "living_quarters",
                "mine", "university", "wardenclyffe"],
        # buildings that offer jobs which improve morale
        "morale_job": ["amphitheatre", "casino"],

        # buildings that can produce power when upgraded and turned on
        "power_generator": ["coal_power", "geothermal", "e_reactor", "fusion", "fission_power", "mill",
                            "oil_power"],
        # buildings that generate resources
        "production": ["elerium_prospector", "elerium_ship", "factory", "g_factory", "gas_mining", "harvester",
                       "helium_mine", "iron_ship", "iridium_mine", "iridium_ship", "mining_droid", "neutron_miner",
                       "oil_extractor", "oil_well", "outpost", "red_factory", "smelter"],
        # buildings with special limits
        "special": ["dyson", "world_collider", "stellar_engine", "swarm_satellite"],
        # buildings that increase maximum capacity of resources
        "storage": ["cargo_yard", "cruiser", "elerium_contain", "exchange", "exotic_lab", "garage", "garrison",
                    "gas_storage", "laboratory", "observatory", "oil_depot", "propellant_depot", "sensor_drone", "shed",
                    "silo", "space_barracks", "storage_yard", "trade", "warehouse", "wharf"],
        # buildings that increase the support limit in space zones
        "support": ["moon_base", "nav_beacon", "nexus", "red_tower", "spaceport", "space_station", "starport",
                    "swarm_control", "xfer_station"]
    }

    @staticmethod
    def compress_lz_string(raw):
        return lzstring.LZString.compressToBase64(raw)

    @staticmethod
    def decompress_lz_string(compressed):
        return lzstring.LZString.decompressFromBase64(compressed)

    @staticmethod
    def fill_resources(save_data, amount_for_unbounded):
        """
        Adjust resources to maximum amounts.

        This method will update all resources to their specified maximums.
        If the resource doesn't have a maximum, it will update to amount_for_unbounded,
            provided that amount_for_unbounded is more than the current amount of the resource.

        :param save_data: the entire evolve savefile json data that needs to be adjusted
        :type save_data: dict
        :param amount_for_unbounded: amount to set unbounded resources (resources that don't have a max value) to
        :type amount_for_unbounded: int or float
        :return: save_data with resources at max amounts and unbounded resources at amount_for_unbounded amount
        :rtype: dict
        """
        # resource node has the data we are interested in
        resources = save_data["resource"]

        for name in resources:
            resource = resources[name]
            if "max" not in resource or "amount" not in resource:
                continue
            if resource["max"] < 0 and resource["amount"] < amount_for_unbounded:
                resource["amount"] = amount_for_unbounded
            if 0 < resource["max"] != resource["amount"]:
                resource["amount"] = resource["max"]

        updated_data = save_data
        updated_data["resource"] = resources
        return updated_data

    @staticmethod
    def adjust_buildings(save_data, amounts):
        """
        Adjust building counts to passed in amounts.

        This method will set, not add, the building counts.
        it won't update a building count if the building count is currently zero, as that will break things.
        It won't reduce a building count if the amount is less than the building count's current value.

        :param save_data: the entire evolve savefile json data that needs to be adjusted
        :type save_data: dict
        :param amounts: object with properties BuildingAmountsParam indicating the desired number of each building type
        :type amounts: BuildingAmountsParam
        :return: save_data with building counts adjusted appropriately
        :rtype: dict
        """
        city = save_data["city"]
        space = save_data["space"]
        interstellar = save_data["interstellar"]
        portal = save_data["portal"]

        city = EvolveSaveEditor._update_building_counts(city, amounts)
        space = EvolveSaveEditor._update_building_counts(space, amounts)
        interstellar = EvolveSaveEditor._update_building_counts(interstellar, amounts)
        portal = EvolveSaveEditor._update_building_counts(portal, amounts)

        # update the save data and return it
        updated_data = save_data
        updated_data["city"] = city
        updated_data["space"] = space
        updated_data["interstellar"] = interstellar
        updated_data["portal"] = portal
        return updated_data

    @staticmethod
    def _update_building_counts(data, amounts):
        for Building_name in data:
            building = data[Building_name]
            if "count" not in building:
                continue
            if building["count"] == 0:
                continue
            if Building_name in EvolveSaveEditor.BUILDING_TYPES["special"]:
                # world collider has total 1859 segments, last one has to be done manually
                if Building_name == "world_collider" and building["count"] < 1858:
                    building["count"] = 1858
                # swarm satellite scales based on swarm_control
                elif Building_name == "swarm_satellite":
                    max_swarms = 6 * data["swarm_control"]["count"]
                    if building["count"] < max_swarms:
                        building["count"] = max_swarms
                # other special buildings have total 100 segments, last one has to be done manually
                else:
                    if building["count"] < 99:
                        building["count"] = 99
                continue
            for type_name in EvolveSaveEditor.BUILDING_TYPES:
                if Building_name in EvolveSaveEditor.BUILDING_TYPES[type_name]:
                    amount = getattr(amounts, type_name)
                    if building["count"] < amount:
                        building["count"] = amount
                    break
        return data

    @staticmethod
    def adjust_prestige_currency(save_data, amounts):
        """
        Adjust prestige currency values to passed in amounts.

        This method will set, not add, the currencies.
        it won't update a currency if the currency is currently zero, as that can break things.
        It won't reduce a currency if the amount is less than the currency's current value.
        Example: call this function and pass in 1000 plasmids.
            If save_data has 0 plasmids, the function will return adjusted data with 0 plasmids.
            If save_data has between 1 and 999 plasmids, the function will return adjusted data with 1000 plasmids.
            If save_data has more than 1000 plasmids, the function will return adjusted data with the same plasmids.

        :param save_data: the entire evolve savefile json data that needs to be adjusted
        :type save_data: dict
        :param amounts: dict of prestige currencies and how much we should update each one to (int or float)
        :type amounts: dict
        :return: save_data with adjusted prestige currencies and relevant statistics
        :rtype: dict
        """
        # race node has the data for the current run, stats node has the overall totals
        race = save_data["race"]
        stats = save_data["stats"]

        # update the live amounts
        race, plasmid_added = EvolveSaveEditor._update_prestige_currency_value(race, "Plasmid", amounts["Plasmid"])
        race, phage_added = EvolveSaveEditor._update_prestige_currency_value(race, "Phage", amounts["Phage"])
        race, dark_added = EvolveSaveEditor._update_prestige_currency_value(race, "Dark", amounts["Dark"])

        # update the stats
        stats = EvolveSaveEditor._update_prestige_currency_stats(stats, "plasmid", plasmid_added)
        stats = EvolveSaveEditor._update_prestige_currency_stats(stats, "phage", phage_added)
        # dark isn't currently tracked in stats but maybe one day it will be
        stats = EvolveSaveEditor._update_prestige_currency_stats(stats, "dark", dark_added)

        # update the save data and return it
        updated_data = save_data
        updated_data["race"] = race
        updated_data["stats"] = stats
        return updated_data

    @staticmethod
    def _update_prestige_currency_value(data, currency, amount):
        added = 0
        if amount and currency in data and data[currency]["count"]:
            added = amount - data[currency]["count"]
            if added > 0:
                data[currency]["count"] = amount
            else:
                added = 0
        return data, added

    @staticmethod
    def _update_prestige_currency_stats(data, currency, amount_added):
        if amount_added and currency in data and data[currency]:
            data[currency] = data[currency] + amount_added
        return data

    @staticmethod
    def adjust_arpa_research(save_data):
        arpa = save_data["arpa"]

        for research_name in arpa:
            research = arpa[research_name]
            # genetic sequencing is handled differently than others
            if research_name == "sequence":
                if "progress" not in research or "max" not in research:
                    continue
                if research["progress"] < research["max"] - 5:
                    research["progress"] = research["max"] - 5
            # launch facility only has 1 rank, ignore it if that rank is done
            elif research_name == "launch_facility":
                if "rank" not in research or research["rank"] >= 1:
                    continue
                if "complete" in research and research["complete"] < 99:
                    research["complete"] = 99
            # we're in one of the uncapped rank researches
            else:
                if "complete" in research and research["complete"] < 99:
                    research["complete"] = 99
        updated_data = save_data
        updated_data["arpa"] = arpa
        return updated_data

    class BuildingAmountsParam:
        # used in adjust_buildings() call
        # default amounts of each building type are below, adjust after instantiating
        boost = 1000
        housing = 1000
        job = 100
        morale_job = 500
        power_generator = 1000
        production = 100
        storage = 1000
        support = 1000
