import sys
import json
import csv
from datetime import datetime
import jsonschema
from jsonschema import validate
from jsonvalidator.logger import get_logger

logger = get_logger(__name__)


def load_schema(schema_file: str) -> json:
    """
    Loads the schema from given file in json format
    :param schema_file: location of schema file
    :return: json object
    """
    try:
        with open(schema_file, 'r') as file:
            schema = json.load(file)
        return schema
    except Exception as e:
        logger.exception(f"Failed to load schema file: {e}", exc_info=False)
        sys.exit(1)


def validate_schema(json_doc: json, schema: json) -> bool:
    """
    REF: https://json-schema.org/
    Validate the schema of input record against the provided schema.
    Throws validation exceptions for failures
    :param json_doc: input record
    :param schema: predefined schema
    :return is_valid: Validation result
    :return message: Error/Success message
    """
    try:
        validate(instance=json_doc, schema=schema)
    except jsonschema.exceptions.ValidationError as err:
        # Get validation failure message
        error_message = err.message
        logger.exception(f"Skipping document with invalid schema. Validation Error: [{error_message}]", exc_info=False)
        return False, error_message

    success_message = f"Input JSON document is valid, document_id:{json_doc['id']}"
    logger.info(success_message)
    return True, success_message


def merge_events(event_dict: dict , row: json) -> dict:
    """
    Merge individual records based on combinations of timestamp and event name

    :param event_dict: dictionary before merging
    :param row: json record from input file
    :return: merged dictionary
    """
    try:
        event_date = str(datetime.strptime(row['timestamp'], '%Y-%m-%d %H:%M:%S.%f').date())
    except Exception as e:
        logger.exception(f"Skipping document with invalid timestamp format: {row['timestamp']}", exc_info=False)
        return event_dict
    event = row['event']
    logger.info(f"Event name: {event}  Event date: {event_date}")
    if event_date not in event_dict.keys():
        event_dict[event_date] = {}
    if event not in event_dict[event_date].keys():
        event_dict[event_date][event] = 1
    else:
        event_dict[event_date][event] += 1
    return event_dict


def write_to_csv(events_merged: dict) -> None:
    """
    Parse the merged dictionary and write to a csv file

    :param events_merged: final merged dictionary
    """
    file_name = f"report_{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}.csv"
    with open(f'/jsonvalidator/output_reports/{file_name}', 'w') as file:
        writer = csv.writer(file)
        # Write header
        writer.writerow(['event_name', 'date', 'count'])
        for date in events_merged.keys():
            event_list = events_merged[date].keys()
            for event_name in event_list:
                count = events_merged[date][event_name]
                # Write each row
                writer.writerow([event_name, date, count])
    logger.info(f"CSV report generated: {file_name}")