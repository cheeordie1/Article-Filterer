"""Base class all nlp models conform to """
class Model():
    """
    Args:
        corpus: a list of {'title': title, 'text': text, 'url': url} dicts
    """
    def load_corpus(corpus):
        raise NotImplementedError

    """
    Args:
        article: A string containing the text of the article to be highlighted 
    Returns:
        indices: A list of tuples containing start and end indices for highlighted sections
    """
    def highlight(article):
        raise NotImplementedError
    
