import argparse
import yaml
from autowebprint import webprint


if __name__ == '__main__':
    parser = argparse.ArgumentParser('AutoWebPrint')
    parser.add_argument('urls', nargs='+', type=str, action='append', help='input url')
    parser.add_argument('-f', '--output_dir', type=str, default='./', help='output dir')
    parser.add_argument('-o', '--option', type=str, default=[], nargs='*', action='append', help='options')
    parser.add_argument('-d', '--driver', type=str, default='firefox', help='driver')
    parser.add_argument('-p', '--display', type=str, default='xvfb', help='display')
    args = vars(parser.parse_args())
    opts = {k: yaml.load(v, Loader=yaml.SafeLoader) for k, v in [s[0].split('=') for s in args.pop('option')]}
    args['urls'] = args['urls'][0]
    webprint(**args, **opts)
