#!/usr/bin/python3
import csv
from math import sqrt
import os
import sys


class Country:
    def __init__(self, row):
        self.code = row['Country Code']
        self.name = row['Country Name']

        self.pop = {}
        for year in range(1961, 2012):
            pop = row['%d' % year].replace(',', '.')
            if pop == '':
                continue
            self.pop[year] = float(pop)

    def __repr__(self):
        return '<Country \'%s\'>' % self.name


def usage(progname):
    print('USAGE')
    print('\t%s code1 [...]' % progname)
    print()
    print('DESCRIPTION')
    print('\tcode1\tcountry code')


def main(args):
    if '-h' in args[1:]:
        usage(args[0])
        return 0

    if len(args) < 2:
        print('%s: missing arguments' % args[0], file=sys.stderr)
        usage(args[0])
        return 84

    db = {}

    try:
        with open(os.path.dirname(args[0]) + os.path.sep + 'demography_data.csv') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                cc = row['Country Code']
                if cc in db:
                    raise Exception('Duplicate country code')
                db[cc] = Country(row)
    except Exception as ex:
        print('%s: failed to read country data base: %s' % (args[0], ex), file=sys.stderr)
        #return 84

    countries = []
    for arg in args[1:]:
        if arg not in db:
            print('%s: invalid country \'%s\'' % (args[0], arg), file=sys.stderr)
            return 84
        countries.append(db[arg])

    years = {}
    for year in range(1961, 2012):
        years[year] = 0.0

    for country in countries:
        missing_years = []
        for year in years:
            if year not in country.pop:
                missing_years.append(year)
            else:
                years[year] += country.pop[year] / 10**6
        for year in missing_years:
            del years[year]

    if len(years) == 0:
        print('%s: not enough data for selected countries' % args[0], file=sys.stderr)
        return 84

    n = 0
    x = 0
    x2 = 0
    y = 0.0
    y2 = 0.0
    xy = 0.0

    for year in years:
        pop = years[year]
        n += 1
        x += year
        x2 += pow(year, 2)
        y += pop
        y2 += pow(pop, 2)
        xy += year * pop

    def linreg(n, x, x2, y, y2, xy, f):
        a = (n * xy - x * y) / (n * x2 - pow(x, 2))
        b = (y * x2 - x * xy) / (n * x2 - pow(x, 2))

        e = []
        for year in years:
            e.append(years[year] - f(year, a, b))

        return a, b, e

    print('country: %s' % ', '.join([country.name for country in countries]))

    print('fit 1')
    a, b, ey = linreg(n, x, x2, y, y2, xy, lambda x, a, b: a * x + b)
    sy = 0.0
    for e in ey:
        sy += pow(e, 2)
    sy = sqrt(sy / n)
    print('\tY = %.2f X %c %.2f' % (a, '+' if b >= 0.0 else '-', abs(b)))
    print('\tstandard deviation: %.2f' % sy)
    print('\tpopulation in 2050: %.2f' % (a * 2050 + b))

    print('fit 2')
    a, b, ex = linreg(n, y, y2, x, x2, xy, lambda x, a, b: (x - b) / a)
    sx = 0.0
    for e in ex:
        sx += pow(e, 2)
    sx = sqrt(sx / n)
    print('\tX = %.2f Y %c %.2f' % (a, '+' if b >= 0.0 else '-', abs(b)))
    print('\tstandard deviation: %.2f' % sx)
    print('\tpopulation in 2050: %.2f' % ((2050 - b) / a))

    sxy = 0
    for i in range(len(ey)):
        sxy += ex[i] * ey[i]
    sxy = sxy / n

    print('correlation: %.4f' % (sxy / (sx * sy)))

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
