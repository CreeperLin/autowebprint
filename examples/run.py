from autowebprint import webprint

if __name__ == '__main__':
    urls = ['https://bing.com', 'http://csrankings.org', 'https://amazon.com', 'https://stackoverflow.com']
    webprint(urls=urls, output_dir='./out', prefs='ff-a4-L')
