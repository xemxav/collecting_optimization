# optimisation_collecte

The aim of this project is to calculate statistics on garbage collection.

It computes excel sheets containing data about different collections. It must contains the following columns :
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
* The kind of garbage (Transport_type)
* The name of the end point (Outlet)
* End point's Longitude coordinate (Outlet_Longitude)
* End point's Longitude coordinate (Outlet_Latitude)

Example of excel file, all headers can be change in the file reference.py

| ID | Inlet | Inlet_Longitude | Inlet_Latitude | Execution_date | Immatriculation | Driver | Client_name | Client_adress | Client_Longitude | Client_Latitude | Transport_type | Outlet | Outlet_Longitude | Outlet_Latitude |
| -- | ----- | --------------- | -------------- | -------------- | --------------- | ------ | ----------- | ------------- | ---------------- | --------------- | -------------- | ------ | ---------------- | --------------- |
| int | string | float | float | date | string | string | string | string | float | float | string | string | float | float |

## Usage

###### Get the project and instal the requirement:
```bash
git clone [link to this repop] [directory_name]
cd optimisation_collecte | [directory_name]
pip install requirement.txt
```
###### Use the script:
Prepare your data in a excel file, by default the script will look for a file called ```retraitement.xlsx``` in your working directory.
```bash
python import.py [your_file.xlsx]
```
Then open ```output.xlsx``` with excel.