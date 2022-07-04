import Interpreter
import logging

logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    print('Running...')
    Interpreter.run('./examples/true.lambda')
