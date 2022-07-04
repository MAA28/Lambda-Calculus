import re
import logging
import os

class Code:
    def __init__(self, title: str, text: str):
        self.title = title
        self.lines = text.split('\n')
        self.strip()
        self.analyse()
        
    def strip(self):
        logging.debug('stripping the code')
        for n, line in enumerate(self.lines):
            if re.fullmatch('\s*', line):
                self.lines.pop(n)
                logging.debug(f'poped {n} since it was empty')
            else:
                if (index := line.find('#')) != -1:
                    if index == 0:
                        self.lines.pop(n)
                        logging.debug(f'poped {n} since it was a comment')
                    else:
                        self.lines[n] = line[:index]
                        logging.debug(f'deleted the comment {n}:{index}')
    
    def analyse(self):
        logging.debug('analysing code')
        for n, line in enumerate(self.lines):
            if ':=' in line:
                logging.debug(f'{n} is an asignment')
                self.lines[n] = Asignment(line)
            else:
                logging.debug(f'{n} is a expression')
                self.lines[n] = Expression(line)


    def __str__(self):
        k = len(str(len(self.lines)))
        return f'[{self.title}]\n' + '\n'.join([f'[{format(n, f">{k}")} / {len(self.lines)}]: {line}' for n, line in enumerate(self.lines)])

class Expression:
    def __init__(self, line: str):
        k = line.find('(', 1)
        self.parameters = [parameters[1:-1] for parameters in re.findall(r'λ[A-Za-z]+.', line[:k])]

        self.operator = line[line.find('.', end=k) + 1:]
        
    def __str__(self):
        return '(' + ''.join([f'λ{parameter}.' for parameter in self.parameters]) + ' '.join(self.operator) + ')'



class Asignment:
    def __init__(self, line: str):
        self.name = line.split(':=')[0]
        self.expression = Expression(line.split(':='))
    
    def __str__(self):
        return f'{self.name}:={self.expression}'


def load_file(filename: str) -> str:
    logging.debug(f'loading {filename}')
    if not re.fullmatch('[A-Za-z]+.lambda', os.path.basename(filename)):
        print(filename, re.match('[A-Za-z]+.lambda', filename))
        raise NameError(f'{filename} is a invalid name')
    
    code = None
    with open(filename, 'r') as file:
        code = Code(os.path.basename(filename[:-7]), file.read())
    logging.debug(f'loaded {code}') 
    return code




def run(filename: str):
    logging.debug(f'running {filename}')
    code = load_file(filename)
    
    
