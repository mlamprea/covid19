from covid19builderdf  import Covid19Builder

builder = Covid19Builder()
covid19 = builder.buildTotalDF()

covid19.getDataByStatus()
covid19.getDataByAttention()
covid19.getDataByGenre()
covid19.getDataByAge()

covid19.plotStatus()
covid19.plotAttention()
covid19.plotGenre()
covid19.plotAge()
