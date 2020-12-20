from bs4 import BeautifulSoup as bs
from utils.list_all_files import *
import hashlib

def get_hash(text):
    return hashlib.md5(text.encode('utf8')).hexdigest()

poem_attributes = ['.o-article .c-feature-hd', '.c-txt_attribution a', '.o-poem']
for flie in list_all_files('www.poetryfoundation.org/'):
    with open(file) as f:
        soup = bs(html, 'html.parser')
        results = [soup.select(e) for e in poem_attributes]
        if all(results):
            title = results[0][0].text.strip().split('\n')[0]
            author = results[1][0].text.strip().split('\n')[0]
            poem = results[2][0].get_text('\n').strip().split('\n')
            poem = [e.strip() for e in poem if len(e.strip())]
            poem = '\n'.join(poem)
            output_fn = 'output/' + get_hash(title + author) + '.txt'
            
            if len(poem) < 100:
                print(f'Parsing error: {fn}')
                continue
                
            with open(output_fn, 'w') as ff:
                ff.write('\n'.join([fn, title, author, poem]))