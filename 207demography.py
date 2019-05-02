#!/usr/bin/env python3

import sys, os, math, csv
from sys import stdin
from math import factorial, sqrt, exp, pi

filename = "./demography_data.csv"

def countries_loarder(data):
    countries =[]
    i = 0
    while i < len(data):
        countries.append(data[i][1])
        i+=1
    return countries

def csv_loader():
    print("Enter in")
    data = []
    with open(filename, 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter=';')
        next(reader)
        for row in reader:
            data.append(row)
        return data

def compare_country(data, arg):
    i = 0
    j = 0
    count = 0
    res = 0
    print("Country: ", sep ="", end="")
    while i < len(data):
        try:
            arg[j]
        except:
            break
        if arg[j] == data[i] and j == len(arg[j])-1 :
            print(data[i])
            j += 1
            i = 0
        elif arg[j] == data[i]:
            print(data[i], " ", sep=',' , end ="")
            j += 1
            i = 0
        i += 1
    if j != len(arg):
        print("COUNTRY NOT FOUND", arg[j])
        exit(84)

def main():
    arg = []
    i = 1
    while (i < len(sys.argv)):
        arg.append(sys.argv[i])
        i += 1
    data = csv_loader()
    countries = countries_loarder(data)
    compare_country(countries, arg)

main()
