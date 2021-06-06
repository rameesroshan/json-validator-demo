import json
import configparser
from jsonvalidator.utils import load_schema, validate_schema, merge_events, write_to_csv
from jsonvalidator.logger import get_logger

logger = get_logger(__name__)


def validate(config_path: str) -> dict:
    """
    Read input file, validate and merge the json records
    :param config_path: config file location
    :return events_combined: merged dictionary
    """
    # Load config file
    config = configparser.ConfigParser()
    config.read(config_path)

    data_path = config['project_info']['data_path']
    logger.info(f"Loading data from file: {data_path}")

    schema_file = config['project_info']['schema_file']
    logger.info(f"Loading schema from file: {schema_file}")

    # Load schema from file
    schema = load_schema(schema_file)

    # For storing merged events
    events_combined = {}

    # Read file line by line without loading full file
    with open(data_path) as infile:
        for row in infile:
            if row.strip():
                row = json.loads(row)
                # Check if input row has valid schema
                is_valid, err = validate_schema(row, schema)
                if is_valid:
                    # Merge rows into a single dictionary
                    events_combined = merge_events(events_combined, row)
    return events_combined



