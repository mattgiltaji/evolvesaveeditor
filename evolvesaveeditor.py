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
    def adjust_prestige_currency(save_data, amounts):
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
            data[currency] =  data[currency] + amount_added
        return data