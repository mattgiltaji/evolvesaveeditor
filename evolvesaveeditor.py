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
    logger = logging.getLogger("validatebackups.py")
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
    #   fill_resources (set constrained resources to max, update infinite resources to large number)
    #   expand_resource_storage (add containers & crates)
    #   add_owned_buildings (split into city/space/interstellar?)

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
        race, plasmid_added = EvolveSaveEditor.update_prestige_currency_value(race, "Plasmid", amounts["Plasmid"])
        race, phage_added = EvolveSaveEditor.update_prestige_currency_value(race, "Phage", amounts["Phage"])
        race, dark_added = EvolveSaveEditor.update_prestige_currency_value(race, "Dark", amounts["Dark"])

        # update the stats
        stats = EvolveSaveEditor.update_prestige_currency_stats(stats, "plasmid", plasmid_added)
        stats = EvolveSaveEditor.update_prestige_currency_stats(stats, "phage", phage_added)
        # dark isn't currently tracked in stats but maybe one day it will be
        stats = EvolveSaveEditor.update_prestige_currency_stats(stats, "dark", dark_added)

        # update the save data and return it
        updated_data = save_data
        updated_data["race"] = race
        updated_data["stats"] = stats
        return updated_data

    @staticmethod
    def update_prestige_currency_value(data, currency, amount):
        added = 0
        if amount and currency in data and data[currency]["count"]:
            added = amount - data[currency]["count"]
            if added > 0:
                data[currency]["count"] = amount
            else:
                added = 0
        return data, added

    @staticmethod
    def update_prestige_currency_stats(data, currency, amount_added):
        if amount_added and currency in data and data[currency]:
            data[currency] = data[currency] + amount_added
        return data
