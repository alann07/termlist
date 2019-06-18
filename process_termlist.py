import argparse
import logging
from termlist_service import TermlistService

logger = logging.getLogger(__name__)


def parse_args():
    input_f = '<input-file>'
    command_f = '<commands-file>'
    output_f = '<output-file>'
    parser = argparse.ArgumentParser()
    parser.add_argument(input_f, help="termlist input file")
    parser.add_argument(command_f, help="termlist commands file")
    parser.add_argument(output_f, help="termlist output-file")

    args = parser.parse_args()
    args_dict = vars(args)

    return args_dict[input_f], args_dict[command_f], args_dict[output_f]


def main():
    logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler()],
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger.info("Start processing")
    input_file_name, command_file_name, output_file_name = parse_args()
    termlist_service = TermlistService()
    termlist_service.apply_commands(input_file_name, command_file_name, output_file_name)
    logger.info("processing complete. check result in " + output_file_name)


if __name__ == '__main__':
    main()