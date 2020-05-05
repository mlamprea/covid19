# -*- coding: utf-8 -*-
#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import matplotlib.pyplot as plt
from dateutil.parser import parse
import numpy as np
from scipy.optimize import curve_fit


def get_pos_first_day(n):
    for i,v in enumerate(n):
        if(v!=0):
           return i


def date_to_nDays(date):
    return (parse(date) - parse("2020-01-01")).days


def logistic_model(t,a,b,c):
    return c/(1 + np.exp(-(t-b)/a))


def getData(url,country):
    df = pd.read_csv(url)
    dates = df.columns[4:].values
    values = list(df[df['Country/Region']==country].values[0][4:])
    pos_first_day = get_pos_first_day(values) #TODO
    nDays = list(map(date_to_nDays,dates))

    print('last date => ',dates[len(dates)-1])




    # from first day with cases confirmed
    nDays = nDays[pos_first_day:]
    # model is overwritten cause it seems to fit better from 0 to N
    nDays = [x for x in range(len(nDays))]
    values = values[pos_first_day:]
    return (nDays,values)


def applyModel(nDays,values):
    fit = curve_fit(logistic_model,nDays,values,p0=[5,100,1000])
    a,b,c = fit[0]
    errors = [np.sqrt(fit[1][i][i]) for i in range(3)]
    return (a,b,c,errors)


def printModel(a,b,c,errors):

    # Total Confirmed Cases
    ce = errors[2]
    print("Total Confirmed Cases ")
    print('Min:',c-ce)
    print('Max:',c+ce)


    # Infection Rate
    ae = errors[0]
    print("Infection Rate")
    print('Min:',a-ae)
    print('Max:',a+ae)


    # Last Day with Confirmed Cases
    be = errors[1]
    print("Last Day with Confirmed Cases")
    print('Min:',b-be)
    print('Max:',b+be)

    data = {'Rate':[a],'Last Day':[b],'Total':[c]}
    dfSummary = pd.DataFrame(data,columns = ['Rate','Last Day','Total'])
    print(dfSummary)


def plotModel(nDays,values,a,b,c):

    plt.tit
    le("Cases confirmed - 2020")
    plt.xlabel("Number of day")
    plt.ylabel("Cases confirmed")
    plt.scatter(nDays,values,label='data')
    plt.plot(nDays,logistic_model(nDays,a,b,c),label='model')
    plt.legend()
    plt.show()


    n = 60
    nProjDays = [x for x in range(n)]
    plt.title("Cases confirmed - 2020")
    plt.xlabel("Number of day")
    plt.ylabel("Cases confirmed")
    plt.scatter(nDays,values,label='data')
    plt.plot(nProjDays,logistic_model(nProjDays,a,b,c),label='model')
    plt.legend()

    #fig = plt.gcf()
    #from datetime import date
    #file_name = 'Covid19_Prediction'+str(date.today())+'.png'
    #fig.savefig(file_name, dpi=100)
    plt.show()




def getDelta(v,n):
    deltas = []
    def getDeltaAux(v,n,deltas):
        if(n==0):
            return deltas
        delta = v[n] - v[n-1]
        deltas.append(delta)
        getDeltaAux(v, n-1,deltas)
        return deltas

    deltas = getDeltaAux(v,n,deltas)
    deltas.append(v[0])
    return list(reversed(deltas))





def plotBar(nDays,values,title):

    deltas = getDelta(values,len(values)-1)

    plt.title(title)
    plt.xlabel("#days")
    plt.ylabel("Cases")
    plt.bar(nDays,deltas,label='growth')
    plt.legend()
    plt.show()
    print(pd.DataFrame({'total':[np.sum(deltas)]},columns=['total']))
    print(pd.DataFrame({'last_value':[deltas[len(deltas)-1]]},columns=['last_value']))


    """
    fig = plt.gcf()
    from datetime import date
    file_name = 'Covid19_Deltas'+str(date.today())+'.png'
    fig.savefig(file_name, dpi=100)
    plt.show()
    """



def plotLine(nDays,values,title):

    plt.title(title)
    plt.xlabel("#days")
    plt.ylabel("Cases")
    plt.plot(nDays,values,label='data')
    plt.legend()
    plt.show()



    """
    fig = plt.gcf()
    from datetime import date
    file_name = 'Covid19_Prediction'+str(date.today())+'.png'
    fig.savefig(file_name, dpi=100)
    plt.show()
    """


def main():
    import sys
    from optparse import OptionParser

    parser = OptionParser(usage="usage: python covid19pyworld.py [options] country",
                          version="%prog 1.0")
    parser.add_option("-c", "--confirmed",action="store_true",dest="confirmed",default=False,help="Build report from Covid 19 confirmed cases")
    parser.add_option("-r", "--recovered",action="store_true",dest="recovered",default=False,help="Build report from Covid 19 recovered cases")
    parser.add_option("-d", "--deaths",action="store_true",dest="deaths",default=False,help="Build report from Covid 19 reported deaths")

    (options, args) = parser.parse_args()


    try:
        if len(args) != 1:
            parser.print_help()
            sys.exit(1)

        country = args[0]
        report = ''

        if options.confirmed:
            report = 'confirmed'
        if options.recovered:
            report = 'recovered'
        if options.deaths:
            report = 'deaths'

        url = "data/time_series_covid19_"+report+"_global.csv"

        print("Processing file "+url)

        nDays, values = getData(url,country)
        title = " variation " + report +" - "+country
        plotBar(nDays,values,title)
        title =  report +" - "+country
        plotLine(nDays, values,title)

    except Exception as e:
        print('error: '+str(e))


if __name__ == '__main__':
    main()
