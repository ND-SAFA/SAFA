import nltk


def main() -> None:
    """
    Downloads nltk static files.
    :return: None
    """
    nltk.download('stopwords', quiet=True)
    nltk.download('wordnet', quiet=True)
    nltk.download('omw-1.4', quiet=True)
    nltk.download('punkt', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)


if __name__ == '__main__':
    main()
