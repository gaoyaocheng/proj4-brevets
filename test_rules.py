import sys, getopt

from rules import Rules

def test_load():
    r = Rules("data/rules.txt")
    assert r.rules

    r = Rules("")
    assert not r.rules

def test_overflow():
    r = Rules("data/rules.txt")
    assert  r.calc_time(0,0) == (0,60)
    assert  r.calc_time(100,0) == (0,0)
    assert  r.calc_time(221,200) == (0,0)
    assert  r.calc_time(331,300) == (0,0)
    assert  r.calc_time(441,400) == (0,0)
    assert  r.calc_time(661,600) == (0,0)
    assert  r.calc_time(1101,1000) == (0,0)

def test_calctime200():
    r = Rules("data/rules.txt")

    assert  r.calc_time(0,200) == (0,60)
    assert  r.calc_time(100,200) == (176,400)
    assert  r.calc_time(150,200) == (265,600)
    assert  r.calc_time(200,200) == (353,810)
    assert  r.calc_time(220,200) == (353,810)

def test_calctime300():
    r = Rules("data/rules.txt")
    assert  r.calc_time(0,300) == (0,60)
    assert  r.calc_time(200,300) == (353,800)
    assert  r.calc_time(220,300) == (390,880)
    assert  r.calc_time(250,300) == (447,1000)
    assert  r.calc_time(300,300) == (540,1200)
    assert  r.calc_time(330,300) == (540,1200)

def test_calctime400():
    r = Rules("data/rules.txt")
    assert  r.calc_time(0,400) == (0,60)
    assert  r.calc_time(300,400) == (540,1200)
    assert  r.calc_time(330,400) == (597,1320)
    assert  r.calc_time(400,400) == (728,1620)
    assert  r.calc_time(440,400) == (728,1620)

def test_calctime600():
    r = Rules("data/rules.txt")
    assert  r.calc_time(0,600) == (0,60)
    assert  r.calc_time(300,400) == (540,1200)
    assert  r.calc_time(400,600) == (728,1600)
    assert  r.calc_time(440,600) == (808,1760)
    assert  r.calc_time(500,600) == (928,2000)
    assert  r.calc_time(550,600) == (1028,2200)
    assert  r.calc_time(600,600) == (1128,2400)
    assert  r.calc_time(660,600) == (1128,2400)

def test_calctime1000():
    r = Rules("data/rules.txt")
    assert  r.calc_time(0,1000) == (0,60)
    assert  r.calc_time(600,1000) == (1128,2400)
    assert  r.calc_time(660,1000) == (1257,2715)
    assert  r.calc_time(700,1000) == (1342,2925)
    assert  r.calc_time(800,1000) == (1557,3450)
    assert  r.calc_time(900,1000) == (1771,3975)
    assert  r.calc_time(1000,1000) == (1985,4500)
    assert  r.calc_time(1100,1000) == (1985,4500)
