import os
import time
import traceback
import yaml
import threading
import logging
import selenium
from selenium import webdriver


logger = logging.getLogger('autowebprint.driver_firefox')


_default_preferences = {
    'browser.aboutConfig.showWarning': False,
    'print.always_print_silent': True,
    'print_printer': 'Mozilla_Save_to_PDF',
    'print.printer_Mozilla_Save_to_PDF.print_to_file': True,
    'print.printer_Mozilla_Save_to_PDF.print_bgimages': True,
}


def set_bool_pref(driver, name, value):
    value = 'true' if value else 'false'
    set_string_pref(driver, name, value)


def set_string_pref(driver, name, value):
    driver.get("about:config")
    driver.execute_script("""
    var prefs = Components.classes["@mozilla.org/preferences-service;1"]
        .getService(Components.interfaces.nsIPrefBranch);
    prefs.setCharPref(arguments[0], arguments[1]);
    """, name, value)
    time.sleep(1)


def print_page(driver, url, outfile, prefs=None, get_fn=None, to_load=1, to_print=200, js_wait=False, close=False):
    logger.info('Printing {} to {}'.format(url, outfile))
    pref_key_outfile = 'print.printer_Mozilla_Save_to_PDF.print_to_filename'
    if driver:
        set_string_pref(driver, pref_key_outfile, outfile)
    else:
        prefs[pref_key_outfile] = outfile
    driver = driver or get_new_driver(prefs)
    try:
        if os.path.exists(outfile):
            os.remove(outfile)
        tic = time.time()

        def watch_file_exist(path, interval=1, max_try=10):
            for _ in range(max_try):
                if os.path.exists(path):
                    logger.info('Finished: {} in {:.2f}s'.format(url, time.time() - tic))
                    return
                time.sleep(interval)
            logger.error('Timeout: {}'.format(url))
        if get_fn:
            get_fn(driver, url)
        else:
            driver.get(url)
        time.sleep(to_load)
        if js_wait:
            driver.execute_script("window.print();")
        else:
            driver.execute_script("setTimeout(()=>{window.print();}, 1);")
        watch_file_exist(outfile, max_try=to_print)
    except selenium.common.exceptions.WebDriverException:
        logger.error('Failed: {}\n{}'.format(url, traceback.format_exc()))
    if close:
        driver.close()
        driver.quit()


def get_new_driver(prefs=None):
    preferences = _default_preferences.copy()
    preferences.update(prefs or {})
    fp = webdriver.FirefoxProfile()
    preferences = {k: str(v) if isinstance(v, float) else v for k, v in preferences.items()}
    for k, v in preferences.items():
        fp.set_preference(k, v)
    fp.DEFAULT_PREFERENCES['mutable'].update(preferences)
    return webdriver.Firefox(firefox_profile=fp, service_log_path=os.path.devnull)


def driver_firefox(specs, prefs=None, windowed=True, n_threads=4, **kwargs):
    prefs = prefs or {}
    if isinstance(prefs, str):
        prefs_path = os.path.join(os.path.dirname(__file__), prefs + '.yml')
        if not os.path.exists(prefs_path):
            prefs_path = prefs
        prefs = yaml.load(open(prefs_path, 'r'), Loader=yaml.SafeLoader)
    kwargs['close'] = True if windowed else False
    driver = None if windowed else get_new_driver(prefs)
    threads = [None] * n_threads
    for url, outfile in specs:
        page_prefs = prefs.copy()
        if n_threads:
            while True:
                idle = False
                for th_idx, th in enumerate(threads):
                    if th is None or not th.is_alive():
                        idle = True
                        break
                if idle:
                    break
                logger.debug('Waiting for idle threads')
                time.sleep(1)
            logger.debug('New thread: {}'.format(th_idx))
            th = threading.Thread(target=print_page, args=(driver, url, outfile, page_prefs), kwargs=kwargs)
            th.start()
            threads[th_idx] = th
        else:
            print_page(driver, url, outfile, page_prefs, **kwargs)
    for th in threads:
        if th is not None and th.is_alive():
            logger.debug('Waiting for thread: {}'.format(th))
            th.join()
    if not windowed:
        driver.close()
        driver.quit()
