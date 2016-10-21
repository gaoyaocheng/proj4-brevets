# Project 4:  Brevet time calculator with Ajax

Reimplement the RUSA ACP controle time calculator with flask and ajax

## Overview
That's "controle" with an 'e', because it's French, although "control" is also accepted. Controls are points where
a rider must obtain proof of passage, and control[e] times are the minimum and maximum times by which the rider must
arrive at the location

## Feature

the speed table 
control km minspeed maxspeed(km/hr)
0 - 200    15       34
200 - 400  15       32
400 - 600  15       30
600 - 1000 11.42828 28

start date and time:
    format YYYY-MM-DD HH-mm
    example: 2016-10-24 08:00

control point:
    shuold one of 200,300,400,600,1000

distance (km):
   last distance cannot set 1.1 longer than control point ,also cannot shorter than control point,
   example:
    control point:  200
         distance:  0~220
    last distance:  200~220 (cannot less than 200 or more than 220)

open time:
  use the maxspeed to reach each control distance,for examples:
  550km:
     200/34 + 200/32 + 150/30 = 17H08

close time:
  use the minspeed to reach each control distance,for examples:
  1000km:
     600/15 + 290/11.428 = 65H23


   *  extra minutes added to calc result when:
      distance control : 200km 10 minutes added to calc result
      distance control : 400km 20 minutes added to calc result

*  if distance is longer than control point, exactly only 10% longer than control point is allowed,
  longer distance close time equal to close time of control point distance
  example:
    200km  control point
checkpoint    opentime     closetime
      0 km 10/24 08:00   10/24 09:00
    200 km 10/24 13:53   10/24 21:30
    210 km 10/24 13:53   10/24 21:30
    220 km 10/24 13:53   10/24 21:30
    210 km and 220km open and close time is equal to 200km

## Authors 

version by  YaoCheng Gao

## Status
use ajax to send argument and get result from server when you set distance
after you set all argument corrently, click showlist ,will get text list of you choose
rules.py get the minutes calc from the BREVET rules 


## To run automated tests 
* `nosetests`

rules test for rules.py to nose tests
    make test
to test all test cases

## To Install and Run
    bash ./configure
    make test    # make all test, should pass 
    make service # service run background



