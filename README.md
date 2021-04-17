# AutoWebPrint

Automatically printing web pages (to PDFs) using browsers and selenium in Python.

## Requirements

- Firefox & Geckodriver
- Xvfb (if no GUI available)
- Python3
- Selenium on Python

on Ubuntu:

```bash
apt install -y firefox-geckodriver xvfb
python3 setup.py install
```

## Usage

Print a single page:

```python
from autowebprint import webprint
webprint('https://example.org')
```

Print multiple pages:

```python
from autowebprint import webprint
webprint(urls=['http://csrankings.org', 'https://amazon.com', 'https://stackoverflow.com'], output_dir='./out')
```

With preferences (A4, Landscape):

```python
from autowebprint import webprint
prefs = {
    'print.printer_Mozilla_Save_to_PDF.print_orientation': 1,
    'print.printer_Mozilla_Save_to_PDF.print_paper_id': 'iso_a4'
}
webprint(urls='https://steampowered.com', prefs=prefs)
```

A predefined set of preferences can be used by passing ``ff-a4-L`` as prefs argument, which sets the page to A4 in landscape mode with no margin. You can also pass the path to a YAML file for preferences.

## Command-line Usage

AutoWebPrint can also be used as a command-line tool.

```bash
# single page
python3 -m autowebprint https://example.org -f example.pdf -o prefs=ff-a4-L
# multiple pages (2 threads, verbose output)
python3 -m autowebprint https://example.com https://example.org -f ./out -o prefs=ff-a4-L -o n_threads=2 -v
```
