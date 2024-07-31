#!/usr/bin/env python3
"""
This script processes the data downloaded from Meta i.e. Facebook/Instagram into useful or interesting statistics.

This script has a companion script "data_pres.py" which uses Plotly/Dash to provide an interactive display of the
data analysis performed

"""

__author__ = "Joseph Clancy"
__version__ = "0.1.0"
__license__ = "MIT"

import logging
import pathlib
import json
from datetime import datetime

proj_dir = pathlib.Path.cwd()
raw_data_dir = pathlib.Path(f"D:/Social_Media_Data")
logger = logging.getLogger(__name__)


def import_raw():
    """This function literally just iterates over the weird directory structure provided by Meta until you find the
    message_n.json and imports it """

    raw_data = {
        "Facebook": {},
        "Instagram": {}
    }

    # Import for Facebook data
    facebook_data_dir = raw_data_dir / "Facebook/your_activity_across_facebook/messages/inbox"
    instagram_data_dir = raw_data_dir / "Instagram/messages/inbox"
    data_dirs = {
        "Facebook": facebook_data_dir,
        "Instagram": instagram_data_dir
    }

    for platform, plat_data_dir in data_dirs.items():
        for chat in plat_data_dir.iterdir():
            chat_name = chat.stem.split("_")[0]
            chat_messages = {}

            data_dir = plat_data_dir / chat.name
            for file in data_dir.iterdir():
                if file.suffix == ".json":
                    message_path = data_dir / file.name
                    with message_path.open() as data_file:
                        chat_messages[file.stem] = json.load(data_file)

            raw_data[platform][chat_name] = chat_messages

    return raw_data


def process_raw(raw_data):
    """This function processes the raw_data"""
    processed_data = dict.fromkeys(list(raw_data.keys()), {})

    # Iterate over the social media platforms
    for platform, platform_data in raw_data.items():
        # Iterate over each chat for the given platform

        for chat, chat_data in platform_data.items():
            # Iterate over each message file in the chat
            # Time to combine the message files into one large fuck-off dictionary
            participants = []
            messages = []
            for message, message_data in chat_data.items():
                # Reminder of what the structure of a "message_n.json"
                # {
                #   "participants": [list of dicts]
                #   "messages": [list of dicts]
                #   "title": <person or group name>,
                #   "is_still_participant": bool,
                #   "thread_path": "<path_to_here>",
                #   "magic_words": [list]
                # }

                for participant in message_data["participants"]:
                    if participant["name"] not in participants:
                        participants.append(participant["name"])

                messages.extend(message_data["messages"])

            # Reminder of structure of message dict
            # {
            #   "sender_name": "<name>",
            #   "timestamp_ms": int,
            #   "content": "<text>",
            #   "reactions": [
            #   {
            #       "reaction": "\u00f0\u009f\u0098\u0082",
            #       "actor": "<name>"
            #   }
            #   "share": {
            #       "link": "<URL>",
            #       "share_text": "<text>",
            #       "original_content_owner": "<text>"
            #   },
            #   "is_geoblocked_for_viewer": bool
            #  },
            message_count = {}
            for message in messages:
                sender_name = message["sender_name"]
                if sender_name in message_count:
                    message_count[sender_name] += 1
                else:
                    message_count[sender_name] = 1

            processed_data[platform][chat] = {}
            processed_data[platform][chat]["Statistics"] = {
                "counts": message_count
            }

    return processed_data


def export_data(processed_data):
    """Horse it out t'fuck"""
    with open("../output/results.json", "w") as outfile:
        json.dump(processed_data, outfile)


def main():
    """ Main entry point of the script"""
    start = datetime.now()
    logger.info("Starting post-processing @ " + start.strftime('%Y/%m/%d %H:%M:%S') + "...")

    # Import raw data from the raw folder
    logger.info("Importing raw data...")
    raw_data = import_raw()

    # Process raw data
    logger.info("Processing raw data...")
    processed_data = process_raw(raw_data)

    # Export processed data to database_dir
    logger.info("Exporting processed data...")
    export_data(processed_data)

    # Finish and collect runtime
    finish = datetime.now()
    logger.info("Finished post-processing @ " + finish.strftime('%Y/%m/%d %H:%M:%S') + "...")
    exec_time = finish - start
    logger.info("Execution time: " + str(exec_time))


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
