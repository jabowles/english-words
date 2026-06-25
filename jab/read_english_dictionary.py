inDict = "/usr/share/dict/web2"

def load_words( fname = None):

    fn = fname
    if fname is None: fn = inDict
    
    with open(fn, "r") as word_file:
        lword = [ w.lower() for w in word_file.read().split()]
        valid_words = set(lword)

    return valid_words

def distance(s = None, t = None):
    if s is None: return(None)
    if t is None: return(None)
    if len(s) != len(t): return(None)
    return sum(c1 != c2 for c1, c2 in zip(s, t))

if __name__ == '__main__':
    english_words = load_words()
    # demo print
    print('pin' in english_words)
