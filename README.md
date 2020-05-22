# Covid19PY

Covid19PY is a library to show statistics and charts of COVID-19 cases.
Covid19pycolombia is a module to plot data about reported cases and deaths in Colombia and Covid19pyworld is a module to plot data about reported cases and deaths by Country.

Source data  
World Cases: https://github.com/CSSEGISandData/COVID-19.git (Johns Hopkins Coronavirus Resource Center: Home)
Colombia Cases: https://www.datos.gov.co/resource/gt2j-8ykr.json (https://www.ins.gov.co/Paginas/Inicio.aspx)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

- The [Covid19Colombia.ipynb](Covid19Colombia.ipynb) notebook provides examples using the covid19pycolombia module.
- The [Covid19World.ipynb](Covid19World.ipynb) notebook provides examples using the covid19pyworld module

- The covid19pyworld module is a commad line tool. See usage:

Usage: python covid19pyworld.py [options] country  

Options:  
  --version        show program's version number and exit  
  -h, --help       show this help message and exit  
  -c, --confirmed  Build report from Covid 19 confirmed cases 
  -r, --recovered  Build report from Covid 19 recovered cases  
  -d, --deaths     Build report from Covid 19 reported deaths  


### Prerequisites

What things you need to install the software and how to install them

pip install -r requirements.txt


## Authors

* **Milton Lamprea Murcia** - *Initial work* - [mlamprea](https://github.com/mlamprea)


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
