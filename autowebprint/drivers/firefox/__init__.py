import os
import time
import traceback
import yaml
import selenium
from selenium import webdriver
import threading


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
                    print('Print finished: {:.2f}s'.format(time.time() - tic))
                    return
                time.sleep(interval)
            print('Print timeout: {}'.format(path))
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
        print('Print failed: {}'.format(traceback.format_exc()))
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
    return webdriver.Firefox(firefox_profile=fp)


def driver_firefox(urls, output_dir='./', filenames=None, prefs=None,
                   windowed=True, threaded=False, verbose=True, **kwargs):
    prefs = prefs or {}
    if isinstance(prefs, str):
        prefs_path = os.path.join(os.path.dirname(__file__), prefs + '.yml')
        if not os.path.exists(prefs_path):
            prefs_path = prefs
        prefs = yaml.load(open(prefs_path, 'r'), Loader=yaml.SafeLoader)
    filenames = filenames or {}
    urls = [urls] if isinstance(urls, str) else urls
    output_dir = os.path.abspath(output_dir)
    os.makedirs(output_dir, exist_ok=True)
    kwargs['close'] = True if windowed else False
    driver = None if windowed else get_new_driver(prefs)
    threads = []
    for url in urls:
        f_name = filenames.get(url, [p for p in url.split('/') if len(p)][-1])
        f_fullname = f_name + ('' if f_name.endswith('.pdf') else '.pdf')
        outfile = os.path.join(output_dir, f_fullname)
        if verbose:
            print('Printing {} to {}'.format(url, outfile))
        page_prefs = prefs.copy()
        if threaded:
            th = threading.Thread(target=print_page, args=(driver, url, outfile, page_prefs), kwargs=kwargs)
            th.start()
            threads.append(th)
        else:
            print_page(driver, url, outfile, page_prefs, **kwargs)
    for th in threads:
        th.join()
    if not windowed:
        driver.close()
        driver.quit()
