#!/usr/bin/env python3

import sys
import csv
from pprint import pprint
from operator import add

MILLION = 1000000

g_std1 = g_std2 = 0

def load_csv(filename):
	datas = []
	with open(filename, 'r') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=';')
		next(csv_reader)
		for row in csv_reader:
			datas.append(row)
	return datas

def show_countries(countries):
	i = 0
	res = "country:  "
	print("country:  ", end="")
	for country in countries:
		if i + 1 == len(countries):
			print(country[0])
			res += country[0]
		else:
			print("{}, ".format(country[0]), end="")
			res += "{}, ".format(country[0])
		i += 1
	return res


def linear_adjustment_a(years, population):
    n = len(population)
    xy = xSum = ySum = xSquare = 0
    for i in range(n):
        xy += years[i] * population[i]
        xSum += years[i]
        ySum += population[i]
        xSquare += years[i] ** 2
    return (n * xy - xSum * ySum) / (n * xSquare - xSum ** 2)


def linear_adjustment_b(years, population):
    n = len(population) if len(population) > len(years) else len(years)
    xy = xSum = ySum = xSquare = 0
    for i in range(n):
        xy += years[i] * population[i]
        xSum += years[i]
        ySum += population[i]
        xSquare += years[i] ** 2
    return (ySum * xSquare - xSum * xy) / (n * xSquare - xSum ** 2)


def merge_list(lists):
	new_list = [sum(x) for x in zip(*lists)]
	return new_list

def stddev_fit1(a, b, pop, years):
	global g_std1
	std = 0.0
	a = round(a, 2)
	b = round(b, 2)
	for i in range(51):
		std += pow(pop[i] - (a * years[i] + b), 2)
	g_std1 = (std / 51) ** 0.5
	return g_std1


def fit1(countries):
	"""
	fit1
	"""
	years = [1961 + x for x in range(51)]
	populations = []
	for country in countries:
		populations.append([float(x.replace(",", ".")) for x in country[2:]])
	populations = merge_list(populations)
	a = linear_adjustment_a(years, populations)
	b = linear_adjustment_b(years, populations)
	if b > 0:
		print("fit 1\n\tY = {:.2f} X + {:.2f}".format(abs(a) / MILLION, abs(b) / MILLION))
	else:
		print("fit 1\n\tY = {:.2f} X - {:.2f}".format(abs(a) / MILLION, abs(b) / MILLION))
	std = stddev_fit1(a, b, populations, years)
	print("\tstandard deviation:  {:.2f}".format(std / MILLION))
	pop_predict = a / MILLION * 2050 + b / MILLION
	print("\tpopulation in 2050:  {:.2f}".format(pop_predict))
	return a, b

def stddev_fit2(a, b, pop, years):
	global g_std2
	std = 0.0
	for i in range(51):
		std += pow(pop[i] - ((-(b) + years[i]) / a), 2)
	g_std2 = (std / 51) ** 0.5
	return g_std2


def fit2(countries):
	years = [1961 + x for x in range(51)]
	populations = []
	for country in countries:
		populations.append([float(x.replace(",", ".")) for x in country[2:]])
	populations = merge_list(populations)
	a = linear_adjustment_a(populations, years)
	b = linear_adjustment_b(populations, years)
	if (b > 0):
		print("fit 2\n\tX = {:.2f} Y + {:.2f}".format(abs(a) * MILLION, abs(b)))
	else:
		print("fit 2\n\tX = {:.2f} Y - {:.2f}".format(abs(a) * MILLION, abs(b)))
	std = stddev_fit2(a, b, populations, years)
	print("\tstandard deviation:  {:.2f}".format(std / MILLION))
	pop_predict = ((-b + 2050) / a) / MILLION
	print("\tpopulation in 2050:  {:.2f}".format(pop_predict))
	return a, b


def correlation(countries, a, b, c, d):
	"""
	Correlation
	"""
	var = 0
	years = [1961 + x for x in range(51)]
	populations = []
	for country in countries:
		populations.append([float(x.replace(",", ".")) for x in country[2:]])
	pop = merge_list(populations)
	for i in range(51):
		var += (pop[i] - (a * years[i] + b)) * (pop[i] - ((-(b) + years[i]) / a))
	corr = var / (g_std1 * g_std2)
	print("correlation:  {}".format(round(corr / 51, 4)))

def demography(datas, av):
    countries = []
    for country in av:
        for row in datas:
            if len(row) > 2 and row[1] == country:
                countries.append(row)
#	if len(countries) == 0:
#        print("Country not found.")
#        return 84
    print(countries)
    show_countries(countries)
    a, b = fit1(countries)
    c, d = fit2(countries)
    correlation(countries,a,b,c,d)
    return 0


def main(sys_argv):
	"""
	Main function
	"""
	av = sys_argv
	av.pop(0)
	if (len(av) < 1):
		return usage(84)
	elif av[0] in ['-h', '--help']:
		return usage()
	try:
		datas = load_csv("demography_data.csv")
	except Exception as err:
		print(err)
		return 84
	return demography(datas, av)


if __name__ == '__main__':
	sys.exit(main(sys.argv))
