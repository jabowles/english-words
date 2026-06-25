import networkx as nx
from functools import wraps

import cProfile
import pstats
import io
from functools import wraps

def profile_function(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()  # Start profiling
        
        try:
            result = func(*args, **kwargs)
        finally:
            pr.disable()  # Stop profiling
            
            # Aggregate and format stats
            s = io.StringIO()
            ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
            ps.print_stats()
            
            # print(f"--- Profiling stats for: {func.__name__} ---")
            # print(s.getvalue())
            
        return result
    return wrapper


class storedWord:
  def load_words(self, dictFile = '../words_alpha.txt' ):
    print(f"Loading words from {dictFile}...")
    with open(dictFile) as word_file:
      valid_words = set([ w for w in word_file.read().split()] )

        # valid_words = set([ w for w in word_file.read().split() if len(w) == 3] )
    return valid_words

  def addNewEntry(self, w=None, g=None):
    '''  What does this self.distances stuff do?
    Use create a mapping from the current entry to all its 'neighbors'
    using this mechanism:
       "pin" (your start word)
            '*in'  remember this 'equivalence class of neighbors'
            'p*n'  remember this 'equivalence class of neighbors'
         -->'pi*'  remember this 'equivalence class of neighbors'
                   (remember this third entry.)
    Note that when the entry for "pie" is processed, that will look like:
       "pie" (your start word)
            '*ie'  remember this 'equivalence class of neighbors'
            'p*e'  remember this 'equivalence class of neighbors'
         -->'pi*'  remember this 'equivalence class of neighbors'
                   (remember this third entry.)
    We will remember for the 'pi*' entry, that [ pin, pie ] both are in that 'class'.

    WE MAKE A GRAPH "EDGE" BETWEEN THE TWO. (Rinse and repeat.)

    Once we have the edges of the graph for [all] entries that are neighbors,
    we're done.  The rest is a basic find-the-path algorithm, between two nodes.
    Since the names of the nodes ARE the words themselves, there's no lookup
    involved.'''

    if w is None:
        raise RuntimeError("addNewEntry(None) was invoked. Oops.")
    for idx in range(len(w)):
        '''notice all equivalence classes and add the new word to each one. '''

        prod = list(w)
        prod[idx] = "*"
        neighbor = ''.join(prod)
        if self.distances.get(neighbor) is None:
            self.distances[neighbor] = []
        self.distances[neighbor].append(w)

        # prod.pop(idx)
        # shorty = ''.join(prod)
        # if shorty in self.wordList:
        #     # print(f"{w} and {shorty} connected.")
        #     g.add_edge(w, shorty)

  @profile_function
  def __init__(self, wordList=None, ng=None, distances=None):
    if wordList:
      self.wordList = wordList
    else:
      self.wordList = self.load_words()

    if distances:
      self.distances = distances
    else:
      self.distances = {}

    if ng:
      self.NG = ng
    else:
      self.NG=nx.Graph()
      for w in self.wordList:
         self.addNewEntry(w, self.NG)
      ##
      #  After all words are entered and all immediate neighbors are known,
      #  do the connecting of those neighbors.  We've kept an arr for each
      #  equivalence class, so it's just a matter of combining ({set} X {set})
      #  and connecting.
      ##
      for (d,arr) in self.distances.items():
         import itertools
         if len(arr) < 2: continue
         for (x1,x2) in list(itertools.combinations(arr, 2)):
            self.NG.add_edge(x1, x2)

  def makePath(self, src,targ):
    '''Make someone else do the graph shortest-path work.

    "Do the smart thing. Let somebody else try first." — Doctor Who

    '''
    import traceback
 
    try:
      if src is None: raise(nx.exception.NetworkXPointlessConcept("'src' is None"))
      if targ is None: raise(nx.exception.NetworkXPointlessConcept("'targ' is None"))

      return( nx.shortest_path(self.NG, source=src, target=targ))
    except (nx.exception.NetworkXPointlessConcept, nx.exception.NetworkXNoPath, nx.exception.NodeNotFound) as e:
      print(f"{type(e)}: {e}")
      return(None)
    except Exception as e:
      traceback.print_exc()
      print(e)
      return(None)

if __name__ == "__main__":
    n = storedWord()

    print(n.makePath("book", "blue"))
    m = storedWord(ng = n.NG, distances=n.distances, wordList=n.wordList)
    print(m.makePath("spiders", "monster"))
