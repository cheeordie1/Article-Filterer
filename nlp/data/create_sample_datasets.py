import newspaper
import pickle as pkl

"""Store corpora as lists of {'title': title, 'text': text, 'url': url} dicts"""

SAMPLES_DIR = 'sample_datasets'

# Define new corpora here
sample_corpora = {
        'gsw':
        [
            'http://www.slcdunk.com/2017/5/2/15513254/nba-playoffs-2017-utah-jazz-vs-golden-state-warriors-schedule-and-primer',
            'http://www.nba.com/article/2017/05/01/playoffs-numbers-preview-golden-state-warriors-utah-jazz',
            'http://www.knbr.com/2017/04/30/schedule-announced-for-warriors-second-round-series-vs-jazz',
            'http://www.espn.com/espn/feature/story/_/page/presents19256296/golden-state-warriors-steph-curry-stopped-only-kevin-durant',
            'http://www.espn.com/nba/story/_/id/19287923/golden-state-warriors-preferred-play-los-angeles-clippers-next-part-enjoy-la-nightlife',
            'http://www.mercurynews.com/2017/05/02/monta-ellis-among-we-believe-warriors-returning-to-oracle-arena/'
        ]
}

def build_corpus(name, urls):

    print('Building %s corpus with %d urls' % (name, len(urls)))
    corpus = []
    
    for url in urls:
        a = newspaper.Article(url)
        a.download()
        a.parse()
        corpus.append({'title': a.title, 'text': a.text, 'url': url})

    with open(SAMPLES_DIR + '/' + name + '.pkl', 'wb') as f:
        pkl.dump(corpus, f)

if __name__ == '__main__':
    for name, urls in sample_corpora.items():
        build_corpus(name, urls)




