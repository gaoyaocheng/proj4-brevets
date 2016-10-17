

from loadrules import Rules

def test_load():
    r = Rules("data/rules.txt")
    print (r.rules)

if __name__=='__main__':
    test_load()
