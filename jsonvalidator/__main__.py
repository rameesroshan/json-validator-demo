import time
from jsonvalidator.validate import validate
from jsonvalidator.reports import generate_report
from jsonvalidator.logger import get_logger

logger = get_logger(__name__)


def main():
    """
    Run the workflow
    """
    start = time.time()
    logger.info("Started JSON validator..!!")
    config_file = '/jsonvalidator/config/demo.cfg'

    # Validate and merge json records
    ouput_dict = validate(config_file)

    # Generate report from merged dictionary in csv format
    generate_report(ouput_dict)

    end = time.time()
    logger.info(f"Finished JSON validator. Total time taken: {(end - start) * 1000.0} ms")


if __name__ == '__main__':
    main()
