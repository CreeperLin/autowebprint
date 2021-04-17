from autowebprint import webprint

if __name__ == '__main__':
    urls = ['https://example.com', 'https://example.org']
    webprint(urls=urls, outfiles='./out', prefs='ff-a4-L')
