import logging
import warnings

from collections import Counter
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)
warnings.filterwarnings("ignore")

class TermlistService:
    def apply_commands(self, input_file_name, command_file_name, output_file_name):
        '''
        Main entry point to apply the commands to the all the terms and save the result into output file.
        :param input_file_name:
        :param command_file_name:
        :param output_file_name:
        :return:
        '''
        term_list = self.get_all_terms(input_file_name)
        counter = Counter(term_list)

        command_list = self.get_commands(command_file_name)

        self.exec_commands(term_list, counter, command_list, output_file_name)

    def get_all_terms(self, input_file_name):
        '''
        Get all term from input file
        :param input_file_name:
        :return: a list of all terms in the file
        '''
        with open(input_file_name, 'r') as fp:
            soup = BeautifulSoup(fp)  # TODO: Use a new parser, instead of default "html.parser"
            soup = BeautifulSoup(soup.prettify())   # TODO: this is temporary fix to deal with <div>xxx</div><div>yyy</div> on 1 line.

        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()  # rip it out

        # get text
        text = soup.get_text()

        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)

        all_terms = []
        for line in text.splitlines():
            for term in line.split(' '):
                if len(term.strip())>0:
                    all_terms.append(term)

        fp.close()
        return all_terms

    def get_commands(self, command_file_name):
        '''
        Get a list of commands from the input command file.
        :param command_file_name:
        :return: a list of commands
        '''
        all_commands = []
        with open(command_file_name, 'r') as fp:
            for line in fp:
                command = line.strip().split()
                all_commands.append(command)
        fp.close()
        return all_commands

    def exec_commands(self, term_list, counter, command_list, output_file_name):
        '''
        Execute command one by one and write output to file.
        :param term_list:
        :param counter:
        :param command_list:
        :param output_file_name:
        :return:
        '''
        output_f = open(output_file_name, 'w')
        for cmd in command_list:
            if len(cmd) <= 1:
                output_f.write('format of command ' + str(cmd[0]) + " is not right\n")
                continue

            logger.info('Executing command ' + cmd[0])
            if cmd[0] == 'FREQUENCY':
                for i in range(1, len(cmd)):
                    if i != len(cmd)-1:
                        output_f.write(str(counter[cmd[i]]) + ' ')
                    else:
                        output_f.write(str(counter[cmd[i]]) + '\n')
            elif cmd[0] == 'TOP':
                result = self.get_sort_string(counter.most_common(int(cmd[1].strip())))
                output_f.write(result + '\n')
            elif cmd[0] == 'IN_ORDER':
                is_in_order = self.check_order(term_list, cmd)
                output_f.write(str(is_in_order).upper() + '\n')
            else:
                output_f.write('command ' + str(cmd[0]) + " is not recognized\n")
        output_f.close()

    def get_sort_string(self, top_words):
        '''
        get sorted string based on count descreasing, and word in increasing order.
        :param top_words:
        :return: a string seperated by space
        '''
        top_words.sort(key=lambda x: (x[1], x[0]), reverse=True)

        start_pos = 0
        result = ''
        for i in range(1, len(top_words)):
            if top_words[i][1] != top_words[i-1][1]:
                result += self.get_reverse_words_string(top_words[start_pos:i])
                start_pos = i
            if i == len(top_words) - 1:
                result += self.get_reverse_words_string(top_words[start_pos:i+1])
        return result

    def get_reverse_words_string(self, words):
        '''
        Reverse the term in list and return a concatenated string seperated by space
        :param words:
        :return: a string of term in increasing order
        '''
        result = ''
        for i in reversed(range(len(words))):
            result += words[i][0] + ' '

        return result

    def check_order(self, term_list, cmd):
        '''
        Check whether the terms appear found in term list in the order as it is.
        :param term_list:
        :param cmd:
        :return: True if appear in order.
        '''

        next_term_start_inx = 0
        for i in range(1, len(cmd)):
            if next_term_start_inx == len(term_list):
                break

            for j in range(next_term_start_inx, len(term_list)):
                if cmd[i] == term_list[j]:
                    next_term_start_inx = j+1
                    break
                if j == len(term_list) - 1:
                    next_term_start_inx += j+1

        return next_term_start_inx < len(term_list)