import logging
import warnings

from collections import Counter
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)
warnings.filterwarnings("ignore")

class TermlistService:
    def apply_commands(self, input_file_name, command_file_name, output_file_name):

        term_list = self.get_all_terms(input_file_name)
        counter = Counter(term_list)

        command_list = self.get_commands(command_file_name)

        self.exec_commands(term_list, counter, command_list, output_file_name)

    def get_all_terms(self, input_file_name):
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
        all_commands = []
        with open(command_file_name, 'r') as fp:
            for line in fp:
                command = line.strip().split()
                all_commands.append(command)
        fp.close()
        return all_commands

    def exec_commands(self, term_list, counter, command_list, output_file_name):

        output_f = open(output_file_name, 'w')
        for cmd in command_list:
            if len(cmd) <= 1:
                output_f.write('format of command ' + str(cmd[0]) + " is not right\n")
            elif cmd[0] == 'FREQUENCY':
                for i in range(1, len(cmd)):
                    if i != len(cmd)-1:
                        output_f.write(str(counter[cmd[i]]) + ' ')
                    else:
                        output_f.write(str(counter[cmd[i]]) + '\n')
            elif cmd[0] == 'TOP':
                result = self.get_sort_string(counter.most_common(int(cmd[1].strip())))
                output_f.write(result + '\n')
            elif cmd[0] == 'IN_ORDER':
                output_f.write(cmd[0] + '\n')
            else:
                output_f.write('command ' + str(cmd[0]) + " is not recognized\n")

    def get_sort_string(self, top_words):
        top_words.sort(key=lambda x: (x[1], x[0]), reverse=True)

        start_pos = 0
        result = ''
        for i in range(1, len(top_words)):
            if top_words[i][1] != top_words[i-1][1]:
                result += self.get_reverse_words_string(top_words[start_pos:i])
                start_pos = i
            if i == len(top_words) - 1:
                result += self.get_reverse_words_string(top_words[start_pos:i+1])


        print(result)
        return result

    def get_reverse_words_string(self, words):
        result = ''
        for i in reversed(range(len(words))):
            result += words[i][0] + ' '

        return result