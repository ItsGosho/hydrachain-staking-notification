import argparse

parser = argparse.ArgumentParser(description='Process some integers',
                                 formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument('--foo', type=int, default=42,
                    help='an integer (default: 42)\n'
                         'this is a multi-line help message\n'
                         'you can add as many lines as you want')

args = parser.parse_args()