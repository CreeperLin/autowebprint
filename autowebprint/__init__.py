import os
import logging
import logging.config
from . import drivers, displays


DEFAULT_LOGGING_CONF = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s - %(levelname)s - %(message)s',
        }
    },
    'handlers': {
        'stream': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
    },
    'loggers': {
        'autowebprint': {
            'handlers': ['stream'],
            'level': 'WARNING',
            'propagate': False,
        },
    }
}

logging.config.dictConfig(DEFAULT_LOGGING_CONF)


_drivers = {k[7:].lower(): v for k, v in drivers.__dict__.items() if k.startswith('driver_')}
_displays = {k[:-7].lower(): v for k, v in displays.__dict__.items() if k.endswith('Display')}


def proc_url(url):
    if os.path.exists(url):
        url = open(url, 'r').read()
    return [ln.strip() for ln in url.split() if len(ln) > 1]


def get_specs(urls, outfiles):
    out_dir = ''
    if isinstance(outfiles, str):
        if len(urls) > 1 or not os.path.basename(outfiles):
            out_dir = outfiles
            os.makedirs(out_dir, exist_ok=True)
            outfiles = {}
        else:
            outfiles = [outfiles]
    if isinstance(outfiles, list):
        outfiles = {url: file for url, file in zip(urls, outfiles)}
    specs = [(url, outfiles.get(url, [p for p in url.split('/') if len(p)][-1])) for url in urls]
    specs = [(k, v + ('' if v.endswith('.pdf') else '.pdf')) for k, v in specs]
    specs = [(k, os.path.abspath(os.path.join(out_dir, v))) for k, v in specs]
    return specs


def webprint(urls, outfiles='./', driver='firefox', display='xvfb', verbose=0, *args, **kwargs):
    if verbose:
        logging.getLogger('autowebprint').setLevel(max(logging.WARNING - 10 * int(verbose), 1))
    drv = _drivers.get(driver)
    disp = _displays.get(display)
    if drv is None:
        raise ValueError('Unknown driver: {}'.format(driver))
    if disp is None:
        raise ValueError('Unknown display: {}'.format(display))
    if isinstance(urls, str):
        urls = [urls]
    urls_all = []
    for url in urls:
        urls_all.extend(proc_url(url))
    specs = get_specs(urls_all, outfiles)
    with disp():
        return drv(specs, *args, **kwargs)
