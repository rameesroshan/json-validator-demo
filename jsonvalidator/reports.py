from jsonvalidator.utils import write_to_csv
from jsonvalidator.logger import get_logger

logger = get_logger(__name__)


def generate_report(merged_doc: dict):
    """
    Write merged events to a csv file
    :param merged_doc: python dictionary containing merged records
    """
    logger.info(f"Wrting report to CSV file")
    write_to_csv(merged_doc)