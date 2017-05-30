"""Base class all nlp models conform to """
class Model():
    """
    Args:
        corpus: a list of document strings
    """
    def load_corpus(self, corpus):
        raise NotImplementedError

    """
    Args:
        article: A string containing the text of the article to be highlighted 
    Returns:
        indices: A list of tuples containing start and end indices for highlighted sections
    """
    def highlight(self, article):
        raise NotImplementedError
    
