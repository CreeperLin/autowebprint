from . import drivers, displays


_drivers = {k[7:].lower(): v for k, v in drivers.__dict__.items() if k.startswith('driver_')}
_displays = {k[:-7].lower(): v for k, v in displays.__dict__.items() if k.endswith('Display')}


def webprint(driver='firefox', display='xvfb', *args, **kwargs):
    drv = _drivers.get(driver)
    disp = _displays.get(display)
    if drv is None:
        raise ValueError('Unknown driver: {}'.format(driver))
    if disp is None:
        raise ValueError('Unknown display: {}'.format(display))
    with disp():
        return drv(*args, **kwargs)
