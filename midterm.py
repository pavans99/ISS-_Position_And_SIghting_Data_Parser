from flask import Flask, request
import requests
import xmltodict
import logging


app = Flask(__name__)
logging.basicConfig()
iss_epoch_data = {}
iss_sighting_data = {}
@app.route('/read_data', methods=['GET','POST'])
def read_data_from_file_into_dict() -> str:
    """
    Downloads position and sight data and stores in xml files using url path /read_data
    Args:
        None
    Returns:
        result(string): string confirming that data has been read

    """
    logging.warning('Data is being read')
    url1 = 'https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_OEM/ISS.OEM_J2K_EPH.xml'
    url2 = 'https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_sightings/XMLsightingData_citiesUSA09.xml'
    r1 = requests.get(url1, allow_redirects=True)
    r2 = requests.get(url2, allow_redirects=True)
    data1=open('ISS.OEM_J2K_EPH.xml', 'wb').write(r1.content)
    data2=open('XMLsightingData_citiesUSA09.xml', 'wb').write(r2.content)

    global iss_epoch_data
    global iss_sighting_data

    with open('ISS.OEM_J2K_EPH.xml', 'r') as f:
        iss_epoch_data = xmltodict.parse(f.read()) 

    with open( 'XMLsightingData_citiesUSA09.xml' , 'r') as f:
        iss_sighting_data = xmltodict.parse(f.read());

    return f'Data has been read from file\n'

@app.route('/epochs', methods=['GET'])
def positional_epochs() -> str:
    """
    Prints all epochs present in positional data using url path /epochs
    Args:
        None
    Returns:
        result(string): string containing all epochs

    """
    logging.warning('List of epochs is being accessed')
    read_data_from_file_into_dict()
    x=[]
    for i in range(len(iss_epoch_data['ndm']['oem']['body']['segment']['data']['stateVector'])):
        x.append(str(iss_epoch_data['ndm']['oem']['body']['segment']['data']['stateVector'][i]['EPOCH']))
    return  'All epochs:'+'\n'.join(x)

@app.route('/epochs/', methods=['GET'])
def epoch_data() -> str:
    """
    Returns data for epoch specified by url path /epochs/?epoch=user_input
    Args:
        None
    Returns:
        result(string): string containing all data for specified epoch

    """
    logging.warning('Specified epoch data is being accessed')
    epoch = request.args.get('epoch')
    read_data_from_file_into_dict()
    x=[]
    y=0
    for i in range(len(iss_epoch_data['ndm']['oem']['body']['segment']['data']['stateVector'])):
        if(str(iss_epoch_data['ndm']['oem']['body']['segment']['data']['stateVector'][i]['EPOCH'])==epoch):
            y=i
            break
    x.append('Epoch: '+str(iss_epoch_data['ndm']['oem']['body']['segment']['data']['stateVector'][y]['EPOCH'])) 
    x.append('X:'+str(iss_epoch_data['ndm']['oem']['body']['segment']['data']['stateVector'][y]['X']['#text'])+' '+str(iss_epoch_data['ndm']['oem']['body']['segment']['data']['stateVector'][y]['X']['@units']))
    x.append('Y:'+str(iss_epoch_data['ndm']['oem']['body']['segment']['data']['stateVector'][y]['Y']['#text'])+' '+str(iss_epoch_data['ndm']['oem']['body']['segment']['data']['stateVector'][y]['Y']['@units']))
    x.append('Z:'+str(iss_epoch_data['ndm']['oem']['body']['segment']['data']['stateVector'][y]['Z']['#text'])+' '+str(iss_epoch_data['ndm']['oem']['body']['segment']['data']['stateVector'][y]['Z']['@units']))
    x.append('Xdot:'+str(iss_epoch_data['ndm']['oem']['body']['segment']['data']['stateVector'][y]['X_DOT']['#text'])+' '+str(iss_epoch_data['ndm']['oem']['body']['segment']['data']['stateVector'][y]['X_DOT']['@units']))
    x.append('Ydot:'+str(iss_epoch_data['ndm']['oem']['body']['segment']['data']['stateVector'][y]['Y_DOT']['#text'])+' '+str(iss_epoch_data['ndm']['oem']['body']['segment']['data']['stateVector'][y]['Y_DOT']['@units']))
    x.append('Zdot:'+str(iss_epoch_data['ndm']['oem']['body']['segment']['data']['stateVector'][y]['Z_DOT']['#text'])+' '+str(iss_epoch_data['ndm']['oem']['body']['segment']['data']['stateVector'][y]['Z_DOT']['@units']))
 
    return  'Epoch data:\n'+'\n'.join(x) +'\n' 

@app.route('/countries',methods=['GET'])
def print_countries() -> str:
    """
    Prints all countries present in sighting data and is accessed by url path/countries
    Args:
        None
    Returns:
        result(string): string of countries in sighting data

    """
    logging.warning('List of countries is being accessed')
    x=[]
    read_data_from_file_into_dict()
    for i in range(len(iss_sighting_data['visible_passes']['visible_pass'])):
        x.append(str(iss_sighting_data['visible_passes']['visible_pass'][i].get('country')))
    x = list(set(x))
    return  'All countries:\n' +'\n'.join(x) +'\n'

@app.route('/countries/',methods=['GET'])
def country_data() -> str:
    """
    Prints data for country specified by url path /countries/?country=user_input
    Args:
        None
    Returns:
        result(string): string of sighting data for specified country

    """
    logging.warning('Data for specified country is being accessed')
    read_data_from_file_into_dict()
    country = request.args.get('country')
    x=[]
    k=list(iss_sighting_data['visible_passes']['visible_pass'][1].keys())
    for i in range(len(iss_sighting_data['visible_passes']['visible_pass'])):
        for j in range(len(list(iss_sighting_data['visible_passes']['visible_pass'][1].keys()))):
            y=list(iss_sighting_data['visible_passes']['visible_pass'][i].values())
            x.append(str(k[j]+':'+y[j]))
    #x= list(iss_sighting_data['visible_passes']['visible_pass'][1].keys())
        x.append(' ')
    #for i in range(len(x)):
    #    x[i]=str(x[i])
    return 'Country data:\n' +'\n'.join(x) +'\n'

@app.route('/regions/',methods=['GET'])
def get_regions() -> str:
    """
    Prints all regions in country specified by url path /regions/?country=user_input
    Args:
        None
    Returns:
        result(string): string of regions for specified country

    """
    logging.warning('List of regions for specified country is being accessed')
    read_data_from_file_into_dict()
    country = request.args.get('country')
    x=[]
    for i in range(len(iss_sighting_data['visible_passes']['visible_pass'])):
        if(str(iss_sighting_data['visible_passes']['visible_pass'][i].get('country'))==country):
            x.append(str(iss_sighting_data['visible_passes']['visible_pass'][i].get('region')))
    x=list(set(x))
    return 'Regions:\n' +'\n'.join(x) +'\n'

@app.route('/regions/data/',methods=['GET'])
def region_data() -> str:
    """
    Prints region data for region specified by url path /regions/data/?region=user_input
    Args:
        None
    Returns:
        result(string): string of region data for specified region

    """
    logging.warning('Data for specifed region is being accessed')
    read_data_from_file_into_dict()
    region = request.args.get('region')
    x=[]
    k=list(iss_sighting_data['visible_passes']['visible_pass'][1].keys())
    for i in range(len(iss_sighting_data['visible_passes']['visible_pass'])):
        if(str(iss_sighting_data['visible_passes']['visible_pass'][i].get('region'))==region):
            for j in range(len(list(iss_sighting_data['visible_passes']['visible_pass'][1].keys()))):           
                y=list(iss_sighting_data['visible_passes']['visible_pass'][i].values()) 
                x.append(str(k[j]+':'+y[j]))
            x.append(' ')
    return 'Region data:\n' +'\n'.join(x) +'\n'

@app.route('/cities/',methods=['GET'])
def get_cities() -> str:
    """
    Prints all cities in country and region specified by url path /cities/?country=input1&region=input2
    Args:
        None
    Returns:
        result(string): string of cities in specified country and region

    """
    logging.warning('Cities for specified region and country are being accessed')
    read_data_from_file_into_dict()
    country = request.args.get('country',None)
    region = request.args.get('region',None)
    x=[]
    for i in range(len(iss_sighting_data['visible_passes']['visible_pass'])):
        if(str(iss_sighting_data['visible_passes']['visible_pass'][i].get('region'))==region and str(iss_sighting_data['visible_passes']['visible_pass'][i].get('country'))==country):
            x.append(str(iss_sighting_data['visible_passes']['visible_pass'][i].get('city')))
    x=list(set(x))
    return 'Cities:\n' +'\n'.join(x) +'\n'

@app.route('/cities/data/',methods=['GET'])
def city_data() -> str:
    """
    Prints data for city specified by url path /cities/data/?city=user_input
    Args:
        None
    Returns:
        result(string): string of city data for specified city

    """
    logging.warning('Data for specified city is being accessed')
    read_data_from_file_into_dict()
    city = request.args.get('city')
    x=[]
    k=list(iss_sighting_data['visible_passes']['visible_pass'][1].keys())
    for i in range(len(iss_sighting_data['visible_passes']['visible_pass'])):
        if(str(iss_sighting_data['visible_passes']['visible_pass'][i].get('city'))==city):
            for j in range(len(list(iss_sighting_data['visible_passes']['visible_pass'][1].keys()))):
                y=list(iss_sighting_data['visible_passes']['visible_pass'][i].values())
                x.append(str(k[j]+':'+y[j]))
            x.append(' ')
    return 'City data:\n' +'\n'.join(x) +'\n'
@app.route('/',methods=['GET'])
def userguide() -> str:
    return 'Once the image is running, type the command: localhost:5030/(input here).\n Some simple inputs are: countries, epochs, Austin.\n These are just a few examples. Refer to the README or the writeup for more detailed information.'






if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
