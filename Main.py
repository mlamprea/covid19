import covid19builderdf

builder = covid19builderdf.Covid19Builder()
covidSD = builder.buildDailyDF()
covidMD = builder.buildTotalDF()
covidSD2 = builder.buildByDate('2020-05-02')

#Plotting
covidMD.plotByCity([covidMD.bogota])
covidMD.plotByDeptTopN(5)
covidMD.plotAll()
covidMD.plotGrowthRate()
covidMD.plotGrowthRateByDept('Boyacá')
len(covidMD.df)

len(covidSD2.df)

covidSD2.plotDepts()


covidSD2.plotCities(20)
