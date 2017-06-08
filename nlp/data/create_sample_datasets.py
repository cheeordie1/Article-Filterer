import newspaper
import pickle as pkl

SAMPLES_DIR = 'sample_datasets'

# Define new corpora here
sample_corpora = {
        'gsw':
        [
            'http://www.espn.com/espn/feature/story/_/page/presents19256296/golden-state-warriors-steph-curry-stopped-only-kevin-durant',
            'http://www.espn.com/nba/story/_/id/19287923/golden-state-warriors-preferred-play-los-angeles-clippers-next-part-enjoy-la-nightlife',
            'http://www.mercurynews.com/2017/05/02/monta-ellis-among-we-believe-warriors-returning-to-oracle-arena/',
            'http://www.cbssports.com/nba/news/nba-playoffs-warriors-jazz-is-david-vs-goliath-yes-but-david-is-a-lot-bigger/',
            'http://www.sfchronicle.com/warriors/article/Now-the-real-playoffs-begin-for-Warriors-11113274.php'
        ],
        'tuval':
        [
            'https://en.wikipedia.org/wiki/Hypatia_transracialism_controversy',
            'http://www.chronicle.com/article/Why-Tuvel-s-Article-So/240029',
            'http://thephilosophicalsalon.com/if-this-is-feminism-its-been-hijacked-by-the-thought-police/',
            'http://www.nationalreview.com/article/447419/rebecca-tuvel-controversy-campus-radicals-free-speech-social-justice',
            'http://nymag.com/daily/intelligencer/2017/05/transracialism-article-controversy.html?mid=twitter-share-di'
        ]
}

"""Stores corpora as lists of {'title': title, 'text': text, 'url': url} dicts"""
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


