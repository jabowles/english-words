inDict = "/usr/share/dict/web2"
def load_words(filename=None):
    if filename is None:
       filename = inDict
    with open(filename) as word_file:
        valid_words = set(word_file.read().split())

    return valid_words


if __name__ == '__main__':
    english_words = load_words()
    # demo print
    print('fate' in english_words)
