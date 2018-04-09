import pandas as pd
import xml.etree.ElementTree as ET
import json
import gzip as G
import os,re,sys
import multiprocessing as mp

def extract_match_moreover(files,basePath,momentum_map,output):
    matches = []
    for zip_file in files:
        with G.open(basePath+'/'+zip_file) as file_ref:
            articles = ET.fromstring(file_ref.read()).find('articles')
            # for each article check match
            for article in articles:
                a_id = int(article.find('id').text.strip())
                if a_id in momentum_map:
                    m = momentum_map[a_id]
                    row = [article.find('title').text,article.find('content').text,
                            article.find('author')[0].text, article.find('source')[0].text,m]
                    matches.append(row)
    output.put(matches)

def get_files_in(dir):
    files = os.listdir(dir)
    regex = re.compile(r'.*.gz')
    return filter(regex.search,files)

def get_momentum_data(fn = './data/data_drop_w_momentum.csv'):
    data = pd.read_csv(fn)
    return data

def get_moreover_articles(base = './data/moreover', threadCount = 8):
    # title, content, author_name, source_name, momentum
    # article -> id
    momentum_map = moreover_momentum_map()
    files = get_files_in(base)[:500]
    processes = []
    load = len(files)/threadCount
    print "Load size: ",load
    output = mp.Queue()
    for i in range(threadCount):
        p = mp.Process(target = extract_match_moreover,
                     args = (files[i*load : (i+1)*load], base,momentum_map,output,))
        processes.append(p)
        p.start()
        
        
    processes.append(mp.Process(target = extract_match_moreover,
                    args = (files[threadCount*load : ], base,momentum_map,output,)))
    processes[-1].start()
    # wait for all to finish:
    for p in processes:
        p.join()
    
    # compile final data
    matched_articles = []
    for p in processes:
            matched_articles += output.get()
    
    df = pd.DataFrame(matched_articles,
        columns=['title', 'content', 'author_name', 'source_name', 'momentum'])
    print df.describe()
    df.to_csv('./data/moreover.csv', index = False, encoding='utf-8')
    return df

def moreover_momentum_map():
    df = get_momentum_data()
    final = {}
    for key,val,source in zip(df['feed_article_id'],df['momentum'], df['feed_source']):
        if 'moreover' in source:
            key = int(key.strip().strip("_"))
            final[key] = val
    return final

def opoint_momentum_map():
    df = get_momentum_data()
    final = {}
    for key,val in zip(df['feed_article_id'],df['momentum']):
        final[key] = val
    return final

def get_opoint_articles(base = './data/opoint'):
    # header_text, summary_text, body_text, firstSource_name, momentum
    # article -> id_article + "_" + id_site
    momentum_map = opoint_momentum_map()
    files = get_files_in(base)
    matched_articles = []
    for zip_file in files:
        with G.open(base+'/'+zip_file) as file_ref:
            try:
                articles = json.loads(file_ref.read())['searchresult']['document']
                # for each article check match
                for article in articles:
                    a_id = "%d_%d" % (article['id_site'],article['id_article'])
                    if (a_id in momentum_map):
                        m = momentum_map[a_id]
                        row = [article['header']['text'], article['summary']['text'],
                                article['body']['text'], article['first_source']['name'],m]
                        matched_articles.append(row)
            except:
                pass

    df = pd.DataFrame(matched_articles,
        columns=['header_text', 'summary_text', 'body_text', 'firstSource_name', 'momentum'])
    print df.describe()
    df.to_csv('./data/opoint.csv', index = False, encoding='utf-8')
    return df

if __name__ == '__main__':
    get_moreover_articles(threadCount = int(sys.argv[1]))
