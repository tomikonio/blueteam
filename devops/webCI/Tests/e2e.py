#!/bin/python
import os
import telebot
import datetime

# czdvf


def testresult(providers, weight):
    if providers == 0 and weight == 0:
        telebot.parse_files('providers.txt', 'weight.txt')
        return "True"
    else:
        telebot.parse_files('providers.txt', 'weight.txt')
        return "False"


providers = os.system(
    'export URI=http://blue.develeap.com:8081/ && pytest ../../providers > providers.txt')
weight = os.system(
    'export URI=http://blue.develeap.com:8082 && pytest ../../weight > weight.txt')
os.system('cat providers.txt >> prolog.txt')
os.system('cat weight.txt >> wlog.txt')
print(testresult(providers, weight))
