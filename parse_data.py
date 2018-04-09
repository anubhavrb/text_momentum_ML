import pandas as pd
import xml.etree.ElementTree as ET
import json
import gzip as G
import os,re,sys,time
import multiprocessing as mp

def extract_match_moreover(raw_xmls,momentum_map,output,index):
    matches = []
    for str_xml in raw_xmls:
        articles = ET.fromstring(str_xml).find('articles')
        for article in articles:
            a_id = int(article.find('id').text.strip())
            if a_id in momentum_map:
                m = momentum_map[a_id]
                row = [article.find('title').text,article.find('content').text,
                        article.find('author')[0].text, article.find('source')[0].text,m]
                matches.append(row)
    output.append(matches)
    print "Process #%2d is Done! Found %d matches" % (index,len(matches))
    return 
    

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
    files = get_files_in(base)
    print "Reading all zips..."
    start = time.time()
    raw_xmls = []
    for zip_file in files:
        with G.open(base+'/'+zip_file) as file_ref:
            raw_xmls.append(file_ref.read())
    print "Done. Total time taken: %.4f sec" % (time.time()-start)        
    processes = []
    load = len(raw_xmls)/threadCount
    print "Load size: ",load
    with mp.Manager() as manager:
        output = manager.list()
        for i in range(threadCount):
            p = mp.Process(target = extract_match_moreover,
                         args = (raw_xmls[i*load : (i+1)*load],momentum_map,output,i))
            processes.append(p)
            p.start()
            
            
        processes.append(mp.Process(target = extract_match_moreover,
                        args = (raw_xmls[threadCount*load : ],momentum_map,output,threadCount)))
        processes[-1].start()
        
        # Wait for all to finish
        for p in processes:
            p.join()
            
        # compile final data
        matched_articles = []
        for i in range(threadCount+1):
                matched_articles += output[i]
        
    df = pd.DataFrame(matched_articles,
        columns=['title', 'content', 'author_name', 'source_name', 'momentum'])
    print df.describe()
    df.to_csv('./data/moreover.csv', index = False, encoding='utf-8', sep=';')
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
    df.to_csv('./data/opoint.csv', index = False, encoding='utf-8', sep = ";")
    return df

if __name__ == '__main__':
    get_opoint_articles()
    #get_moreover_articles(threadCount = int(sys.argv[1]))
