"""
This script is intended to be a save editor for the game evolve
The game can be found at https://pmotschmann.github.io/Evolve/
"""

import argparse
import collections
import copy
import json
import logging
import os
import sys

import lzstring


def main():
    """
    Call parse_args, then pass to edit_evolve_save() to do all the work
    :return: nothing
    """
    args = parse_args(sys.argv[1:])
    edit_evolve_save(args)


def parse_args(args):
    """
        Parses and validates command line arguments
        :param list args: arguments passed into the script (usually sys.argv[1:])
        :return: arguments parsed into a neat object
        """
    parser = argparse.ArgumentParser(
        description="Save editor for game evolve")
    parser.add_argument("filepath", help="path to save file", type=argparse.FileType("r+"))
    parsed_args = parser.parse_args(args)
    filename = parsed_args.filepath.name
    parsed_args.filepath.close()
    parsed_args.filepath = filename
    return parsed_args


def edit_evolve_save(args):
    ese = EvolveSaveEditor()
    ese.load_data_from_file(args.filepath)
    ese.adjust_save_data()
    ese.save_data_to_file(args.filepath)


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
    """
    The save editor itself.
    Expected usage flow:
        1. Call a load method to input data from an external source into the instance
        2. Call adjust_save_data() to actually edit the data
        3. Call a save method to output save data from the instance to an external source
    """
    save_data = {}

    BuildingAmountsParam = collections.namedtuple("BuildingAmountsParam",
                                                  ["boost", "housing", "job", "morale_job", "power_generator",
                                                   "production", "storage", "support"],
                                                  defaults=[1000, 1000, 100, 1000, 1000, 100, 1000, 1000])

    # noinspection PyArgumentList
    DEFAULT_BUILDING_AMOUNTS = BuildingAmountsParam()  # use all default values

    BUILDING_TYPES = {
        # buildings that provide a production or efficiency bonus but don't make things themselves
        "boost": ["attractor", "biodome", "biolab", "boot_camp", "citadel", "drone", "far_reach", "gps", "hospital",
                  "library", "lumber_yard", "mass_driver", "mass_ejector", "metal_refinery", "processing",
                  "red_mine", "rock_quarry", "satellite", "sawmill", "shrine", "swarm_plant", "temple",
                  "tourist_center", "turret", "vr_center", "war_droid", "war_drone", "ziggurat"],
        # buildings that increase the citizen cap
        "housing": ["apartment", "basic_housing", "cottage", "farm", "habitat", "lodge"],
        # buildings that provide job slots for citizens
        "job": ["bank", "carport", "cement_plant", "coal_mine", "fabrication", "foundry", "living_quarters",
                "mine", "university", "wardenclyffe"],
        # buildings that offer jobs which improve morale
        "morale_job": ["amphitheatre", "casino"],

        # buildings that can produce power when upgraded and turned on
        "power_generator": ["coal_power", "geothermal", "e_reactor", "fusion", "fission_power", "mill",
                            "oil_power", "windmill"],
        # buildings that generate resources
        "production": ["elerium_prospector", "elerium_ship", "factory", "g_factory", "gas_mining", "harvester",
                       "helium_mine", "iron_ship", "iridium_mine", "iridium_ship", "mining_droid", "neutron_miner",
                       "oil_extractor", "oil_well", "outpost", "red_factory", "smelter"],
        # buildings with special limits
        "special": ["dyson", "world_collider", "stellar_engine", "swarm_satellite"],
        # buildings that increase maximum capacity of resources
        "storage": ["cargo_yard", "cruiser", "elerium_contain", "exchange", "exotic_lab", "garage", "garrison",
                    "gas_storage", "laboratory", "observatory", "oil_depot", "propellant_depot", "sensor_drone", "shed",
                    "silo", "slave_pen", "soul_well", "smokehouse", "space_barracks", "storage_yard", "trade",
                    "warehouse", "wharf"],
        # buildings that increase the support limit in space zones
        "support": ["moon_base", "nav_beacon", "nexus", "red_tower", "spaceport", "space_station", "starport",
                    "swarm_control", "xfer_station"]
    }
    DEFAULT_UNBOUNDED_RESOURCE_AMOUNT = 2000000000000
    DEFAULT_STACK_AMOUNT = 1000
    DEFAULT_PRESTIGE_CURRENCY_AMOUNTS = {"Plasmid": 30000, "Phage": 20000, "Dark": 4000}

    def load_data_from_file(self, filepath):
        """
        Reads data from the file at the passed in filepath and stores it for later use
        :param filepath: path to the file where data should be read
        :return: nothing
        """
        adjusted_path = os.path.normpath(filepath)
        try:
            with open(adjusted_path, "r") as file:
                lz_string = file.read()
        except OSError:
            logger = get_logger()
            logger.warning(f"load_data_from_file() unable to read from file {adjusted_path}")
            return

        json_str = self.decompress_lz_string(lz_string)
        try:
            self.save_data = json.loads(json_str)
        except json.JSONDecodeError as err:
            logger = get_logger()
            logger.warning(
                f"load_data_from_file() could not load from file {adjusted_path} because of a json parse error {err}")
            logger.debug(f"failed json: {json_str}")
            return
        except TypeError:
            logger = get_logger()
            logger.warning(
                f"load_data_from_file() could not load from file {adjusted_path} because"
                f" the data was not encoded properly")
            return

    def save_data_to_file(self, filepath):
        """
        Outputs stored data to a file at the passed in filepath
        :param filepath: path to the file where save data should be outputted
        :return: nothing
        """
        adjusted_path = os.path.normpath(filepath)
        json_str = json.dumps(self.save_data, separators=(',', ':'))
        lz_string = self.compress_lz_string(json_str)
        try:
            with open(adjusted_path, "w") as file:
                file.write(lz_string)
        except OSError:
            logger = get_logger()
            logger.warning(f"save_data_to_file() unable to write to file {adjusted_path}")
            return

    @staticmethod
    def compress_lz_string(raw):
        return lzstring.LZString.compressToBase64(raw)

    @staticmethod
    def decompress_lz_string(compressed):
        try:
            decompressed = lzstring.LZString.decompressFromBase64(compressed)
        except IndexError:
            logger = get_logger()
            logger.warning(f"unable to decompress invalid value in decompress_lz_string()")
            logger.debug(f"failed decompress: {compressed}")
            return None
        return decompressed

    def adjust_save_data(self):
        # adjust_data method that calls all individual helper methods before saving the data to member
        data = copy.deepcopy(self.save_data)

        # TODO: make this pull settings from somewhere to determine whether to run each one or not
        # TODO: make this pull settings from somewhere to determine parameters for each call
        data = self.fill_resources(data, self.DEFAULT_UNBOUNDED_RESOURCE_AMOUNT)
        data = self.stack_resources(data, self.DEFAULT_STACK_AMOUNT)
        data = self.adjust_buildings(data, self.DEFAULT_BUILDING_AMOUNTS)
        data = self.fill_population(data)
        data = self.fill_soldiers(data)
        data = self.adjust_prestige_currency(data, self.DEFAULT_PRESTIGE_CURRENCY_AMOUNTS)
        data = self.adjust_arpa_research(data)

        self.save_data = data

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
        try:
            resources = copy.deepcopy(save_data["resource"])
        except KeyError:
            logger = get_logger()
            logger.warning("could not load resource node in data passed to fill_resources()")
            return save_data

        for name in resources:
            resource = resources[name]
            try:
                if resource["max"] < 0 and resource["amount"] < amount_for_unbounded:
                    resource["amount"] = amount_for_unbounded
                if 0 < resource["max"] != resource["amount"]:
                    resource["amount"] = resource["max"]
            except KeyError:
                continue

        updated_data = save_data
        updated_data["resource"] = resources
        return updated_data

    @staticmethod
    def stack_resources(save_data, amount):
        """
        Add containers and crates to all relevant resources.

        This method will add containers and crates to any resources that match these criteria:
            At least 1 of the resource exists, meaning the resource is unlocked
            The resource can use crates and containers for expanded storage
            At least 1 Freight Yard building exists (so crates are unlocked)
                OR
            At least 1 Container Port building exists (so containers are unlocked)
            (If only the Freight Yard is available, this method will only set crates)
            (If only the Container Port is available, this method will only set containers)

        :param save_data: the entire evolve savefile json data that needs to be adjusted
        :type save_data: dict
        :param amount: amount of crates and containers to set each resource to
        :type amount: int
        :return: save_data with resources at max amounts and unbounded resources at amount_for_unbounded amount
        :rtype: dict
        """
        try:
            resources = copy.deepcopy(save_data["resource"])
            city = save_data["city"]
        except KeyError:
            logger = get_logger()
            logger.warning("could not load resource or city node in data passed to stack_resources()")
            return save_data

        crates_unlocked, containers_unlocked = EvolveSaveEditor._are_stackables_unlocked(city)

        if not crates_unlocked and not containers_unlocked:
            # nothing to add here
            return save_data

        for name in resources:
            resource = resources[name]
            try:
                EvolveSaveEditor._stack_one_resource(resource, amount, crates_unlocked, containers_unlocked)
            except KeyError:
                continue

        updated_data = save_data
        updated_data["resource"] = resources
        return updated_data

    @staticmethod
    def _are_stackables_unlocked(city):
        crates_unlocked = False
        containers_unlocked = False
        try:
            if city["storage_yard"]["count"] > 0:
                crates_unlocked = True
        except KeyError:
            logger = get_logger()
            logger.info("crates are not unlocked")

        try:
            if city["warehouse"]["count"] > 0:
                containers_unlocked = True
        except KeyError:
            logger = get_logger()
            logger.info("containers are not unlocked")
        return crates_unlocked, containers_unlocked

    @staticmethod
    def _stack_one_resource(resource, amount, crates_unlocked, containers_unlocked):
        if not resource["stackable"]:
            # this resource doesn't use containers and crates
            return
        if resource["amount"] == 0:
            # don't add containers for resources that aren't unlocked yet
            return
        if crates_unlocked and resource["crates"] < amount:
            resource["crates"] = amount
        if containers_unlocked and resource["containers"] < amount:
            resource["containers"] = amount
        return

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
        try:
            city = copy.deepcopy(save_data["city"])
            space = copy.deepcopy(save_data["space"])
            interstellar = copy.deepcopy(save_data["interstellar"])
            portal = copy.deepcopy(save_data["portal"])
        except KeyError:
            logger = get_logger()
            logger.warning(
                "could not load city or space or interstellar or portal node in data passed to adjust_buildings()")
            return save_data

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
        for building_name in data:
            building = data[building_name]
            try:
                if building["count"] == 0:
                    continue
                if building_name in EvolveSaveEditor.BUILDING_TYPES["special"]:
                    building["count"] = EvolveSaveEditor._get_special_building_count(data, building_name,
                                                                                     building["count"])
                    continue
                for type_name in EvolveSaveEditor.BUILDING_TYPES:
                    if building_name in EvolveSaveEditor.BUILDING_TYPES[type_name]:
                        amount = getattr(amounts, type_name)
                        if building["count"] < amount:
                            building["count"] = amount
                        break
            except (KeyError, TypeError):
                continue
        return data

    @staticmethod
    def _get_special_building_count(other_building_data, name, curr_count):
        # world collider has total 1859 segments, last one has to be done manually
        if name == "world_collider" and curr_count < 1858:
            return 1858
        # swarm satellite scales based on swarm_control
        if name == "swarm_satellite":
            max_swarms = 18 * other_building_data["swarm_control"]["count"]
            if curr_count < max_swarms:
                return max_swarms
        # other special buildings have total 100 segments, last one has to be done manually
        elif curr_count < 99:
            return 99
        return curr_count

    @staticmethod
    def fill_population(save_data):
        """
        Fills citizen count up to maximum based on recalculated population cap

        This method goes through all the relevant buildings to figure out how many citizens
        the new save data should be able to accommodate, then updates population cap and current population to that num.
        It ignores the fact that some housing buildings need to be turned on to work, so errs on more citizens.

        :param save_data: the entire evolve savefile json data that needs to be adjusted
        :type save_data: dict
        :return: save_data with population's max and amounts set to the newly calculated value
        :rtype: dict
        """
        try:
            resources = copy.deepcopy(save_data["resource"])
            city = save_data["city"]
            space = save_data["space"]
            interstellar = save_data["interstellar"]
            race = save_data["race"]
        except KeyError:
            logger = get_logger()
            logger.warning("could not load resource or city or space or interstellar or race node in data passed to "
                           "fill_population()")
            return save_data
        try:
            # we need to know what species this is to figure out where the citizen count is stored
            species = race["species"]
            citizen_node = resources[species]
        except KeyError:
            logger = get_logger()
            logger.warning("could not determine species in fill_population()")
            return save_data

        new_citizen_cap = 0
        # use a wrapper function here to avoid a lot of try/except blocks
        new_citizen_cap += EvolveSaveEditor._get_building_count(city, "basic_housing")
        new_citizen_cap += EvolveSaveEditor._get_building_count(city, "farm")
        new_citizen_cap += EvolveSaveEditor._get_building_count(space, "living_quarters")
        new_citizen_cap += EvolveSaveEditor._get_building_count(interstellar, "habitat")
        new_citizen_cap += EvolveSaveEditor._get_building_count(city, "cottage") * 2  # each one holds 2
        new_citizen_cap += EvolveSaveEditor._get_building_count(city, "apartment") * 5  # each one holds 5

        try:
            if new_citizen_cap > citizen_node["amount"]:
                citizen_node["max"] = new_citizen_cap
                citizen_node["amount"] = new_citizen_cap
        except KeyError:
            logger = get_logger()
            logger.warning("could not update population count in fill_population()")
            return save_data

        updated_data = save_data
        updated_data["resource"] = resources
        return updated_data

    @staticmethod
    def _get_building_count(save_data, building_name):
        try:
            return save_data[building_name]["count"]
        except KeyError:
            pass
        return 0

    @staticmethod
    def fill_soldiers(save_data):
        """
        Fills soldier count up to maximum based on recalculated soldier cap

        This method goes through all the relevant buildings to figure out how many soldiers
        the new save data should be able to accommodate, then updates soldier cap and current soldiers to that number.
        It ignores the fact that some barracks buildings need to be turned on to work, so errs on more soldiers.
        It also heals any wounded soldiers.

        :param save_data: the entire evolve savefile json data that needs to be adjusted
        :type save_data: dict
        :return: save_data with soldier's max and amounts set to the newly calculated value
        :rtype: dict
        """
        try:
            civic = copy.deepcopy(save_data["civic"])
            city = save_data["city"]
            space = save_data["space"]
            interstellar = save_data["interstellar"]
        except KeyError:
            logger = get_logger()
            logger.warning(
                "could not load civic or city or space or interstellar node in data passed to fill_soldiers()")
            return save_data

        new_soldier_cap = 0
        # use a wrapper function here to avoid a lot of try/except blocks
        new_soldier_cap += EvolveSaveEditor._get_building_count(city, "garrison") * 3  # each one holds 3
        new_soldier_cap += EvolveSaveEditor._get_building_count(space, "space_barracks") * 2  # each one holds 2
        new_soldier_cap += EvolveSaveEditor._get_building_count(interstellar, "cruiser") * 3  # each one holds 3

        try:
            if new_soldier_cap > civic["garrison"]["workers"]:
                civic["garrison"]["workers"] = new_soldier_cap
                civic["garrison"]["max"] = new_soldier_cap
                civic["garrison"]["wounded"] = 0
        except KeyError:
            logger = get_logger()
            logger.warning("could not update garrison details in fill_soldiers()")
            return save_data

        updated_data = save_data
        updated_data["civic"] = civic
        return updated_data

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
        try:
            race = copy.deepcopy(save_data["race"])
            stats = copy.deepcopy(save_data["stats"])
        except KeyError:
            logger = get_logger()
            logger.warning("could not load race or stats node in data passed to adjust_prestige_currency()")
            return save_data

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
        try:
            if amount and data[currency]["count"]:
                added = amount - data[currency]["count"]
                if added > 0:
                    data[currency]["count"] = amount
                else:
                    added = 0
        except KeyError:
            pass
        return data, added

    @staticmethod
    def _update_prestige_currency_stats(data, currency, amount_added):
        try:
            if amount_added and data[currency]:
                data[currency] = data[currency] + amount_added
        except KeyError:
            pass
        return data

    @staticmethod
    def adjust_arpa_research(save_data):
        """
        Adjust arpa research projects to 99% and genetic sequencing to 5 seconds from completion

        This method will update arpa research projects to 99% complete at the current rank.
        Since the launch facility is a one time project, it won't touch it if its been completed.
        It will update the genetic sequencing to 5 seconds away from completion.
        of course if the genetic sequencing had less than 5 seconds left, it will leave it as is.

        :param save_data: the entire evolve savefile json data that needs to be adjusted
        :type save_data: dict
        :return: save_data with adjusted arpa research project completions
        :rtype: dict
        """
        try:
            arpa = copy.deepcopy(save_data["arpa"])
        except KeyError:
            logger = get_logger()
            logger.warning("could not load arpa node in data passed to adjust_arpa_research()")
            return save_data

        for research_name in arpa:
            research = arpa[research_name]
            try:
                # genetic sequencing is handled differently than others
                if research_name == "sequence":
                    if research["progress"] < research["max"] - 5:
                        research["progress"] = research["max"] - 5
                # launch facility only has 1 rank, ignore it if that rank is done
                elif research_name == "launch_facility":
                    if research["rank"] >= 1:
                        continue
                    EvolveSaveEditor._update_arpa_project(research)
                # we're in one of the uncapped rank researches
                else:
                    EvolveSaveEditor._update_arpa_project(research)
            except (KeyError, TypeError):
                continue

        updated_data = save_data
        updated_data["arpa"] = arpa
        return updated_data

    @staticmethod
    def _update_arpa_project(research):
        if research["complete"] < 99:
            research["complete"] = 99


if __name__ == "__main__":  # pragma: no cover
    main()
