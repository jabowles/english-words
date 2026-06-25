import pytest
import networkx as nx
import processlib
# from processlib import storedWord, profile_function
from test_processlib import sample_data


def test_basicAlink(sample_data):
    n =  sample_data
    
    ret = n.makePath("book", "blue")
    assert ret is not None
    assert type(ret) == type([])
    assert ret[0] == 'book'
    assert ret[-1] == 'blue'
    assert len(ret) > 2

def test_basicAlink2(sample_data):
    n =  sample_data
    
    ret = n.makePath("spiders", "monster")
    assert ret is not None
    assert type(ret) == type([])
    assert ret[0] == 'spiders'
    assert ret[-1] == 'monster'
    assert len(ret) > 2

# Data-driven testing using Parametrization
@pytest.mark.parametrize(
    "a, b, isGood",
    [
        ('book', 'blue',  True ),
        ('monster', 'spiders',  True ),
        ('monster', 'rs', False ),
        (None, 'rs', False ),
        ( 'be', None, False ),
        ( None, None, False ),
        ('arfarf', 'dog', False ),
        ('spiders', 'monster',  True),
    ]
)
@processlib.profile_function
def test_add_multiple_casesAA(a, b, isGood, sample_data):
    n =  sample_data
    
    try:
       ret = n.makePath(a, b)
    except (nx.exception.NetworkXNoPath, nx.NodeNotFound) as e:
       print(str(e))
       if isGood: raise(e)

    if isGood:
       assert ret is not None
       assert type(ret) == type([])
       assert ret[0] == a
       assert ret[-1] == b
       assert len(ret) > 2


if __name__ == "__main__":
    n = processlib.storedWord()

    print(n.makePath("book", "blue"))
    m = processlib.storedWord(ng = n.NG, distances=n.distances, wordList=n.wordList)
    print(m.makePath("spiders", "monster"))
