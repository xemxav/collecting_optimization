# optimisation_collecte

## Overview
The aim of this project is to calculate distance and duration statistics for collections tours by a truck.
It uses the [openroute service API](https://openrouteservice.org/) in order to get information on routes.

First, our script collects you data gathered in a excel sheet. It will then use the [openroute service API](https://openrouteservice.org/) to find each distance between the starting point of the tour and the other places using the Matrix endpoint.
Then it uses optimization endpoint to computes duration and distance :
* between the starting point and it's closest collect place
* the route for each collect places
* between the end point and the starting point (truck go back to their bases) 

This project is a tool for [medmed107](https://github.com/Medmed107) master's thesis.

---

## Usage

##### Get the project and instal the requirements:
We strongly advise to use a virtual environnement for all your python projects, with [virtualenv](https://pypi.org/project/virtualenv/) for example.
More info on virtual environnement [here](https://openclassrooms.com/fr/courses/4425111-perfectionnez-vous-en-python/4463278-travaillez-dans-un-environnement-virtuel) (in French).

```bash
git clone [link to this repop] [directory_name]
cd optimisation_collecte | [directory_name]
pip install requirement.txt
```
##### Prepare your data:

Prepare your data in a excel file, by default the script will look for a file called ```retraitement.xlsx``` in your working directory.
It must contains the following columns :
* a unique  ID for each collections (ID)
* the name of the starting point (Inlet)
* Longitude coordinate of starting point (Inlet_Longitude)
* Latitude coordinate of starting point (Inlet_Latitude)
* Date of execution (Execution_date)
* Truck's plate number (Immatriculation)
* Truck Driver's name (Driver)
* Client's name (Client_name)
* Client's adress (Client_adress)
* Client's Longitude coordinate (Client_Longitude)
* Client's Latitude coordinate (Client_Latitude)
* Type of marchandise collected (Transport_type)
* The name of the end point (Outlet)
* End point's Longitude coordinate (Outlet_Longitude)
* End point's Longitude coordinate (Outlet_Latitude)

| ID | Inlet | Inlet_Longitude | Inlet_Latitude | Execution_date | Immatriculation | Driver | Client_name | Client_adress | Client_Longitude | Client_Latitude | Transport_type | Outlet | Outlet_Longitude | Outlet_Latitude |
| -- | ----- | --------------- | -------------- | -------------- | --------------- | ------ | ----------- | ------------- | ---------------- | --------------- | -------------- | ------ | ---------------- | --------------- |
| int | string | float | float | date | string | string | string | string | float | float | string | string | float | float |

Example of excel file, all headers can be changed in the file reference.py

##### Insert your openroute service API key in reference.py
[Sign up](https://openrouteservice.org/dev/#/signup) on Openroute Service and copy your API key in the file reference.py
```python
# reference.py
APIKEY = "" # insert your API key between the quotes
```

##### Use the script:
```bash
python import.py [your_file.xlsx]
```
Then open ```output.xlsx``` with excel.