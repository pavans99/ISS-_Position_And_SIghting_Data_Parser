<h1>Application for Reading and Parsing ISS Positional and Sighting Data</h1>
The repository comprises two scripts, a Dockerfile, a Makefile, and a text file requirements.txt. The script midterm.py contains all of the functions for the application, and test_midterm.py contains tests for the application. The Dockerfile contains protocols to containzerize the application and datasets. The Makefile contains protocols to build a container, start the Flask application, and push the image to DockerHub. requirements.txt contains Python packages necessary to the application. As a whole, the application serves to download, containerize, and parse ISS data. The user can access different pieces of data using queries and commands described in this document. 
<h2>Functions</h2>
<h3>read_data_from_file_into_dict</h3>
This function downloads the ISS position and sighting data and writes them into xml files. The function route can be accessed using the command

	curl localhost:5030/read_data

<h3>positional_epochs</h3>
This function returns all epochs present in the positional data. The function route can be accessed using the command

	curl localhost:5030/epochs

<h3>epoch_data</h3>
This function returns all data associated with a specified epoch in the positional data. An example command to access this function route is

	curl localhost:5030/epochs/?epoch=2022-042T12:12:00.000Z

<h3>print_countries</h3>
This function returns all countries in the sighting data. To access the function route use the command

        curl localhost:5030/countries

<h3>country_data</h3>
This function returns all data associoated with a specified country in the sighting data. An example command to access the function route is

        curl localhost:5030/countries/?country=United_States

<h3>get_regions</h3>
This function returns all regions associated with a specified country in the sighting data. An example command to access the function route is

        curl localhost:5030/regions/?country=United_States

<h3>region_data</h3>
This function returns all data associated with a specified region in the sighting data. An example command to access this function route is

        curl localhost:5030/regions/data/?region=Texas

<h3>get_cities</h3>
This function returns all cities associated with a specified country and region in the sighting data. An example command to access this function route is

        curl -i "localhost:5030/cities/?country=United_States&region=Texas"

Its format is slightly different from other commands since this url accepts two routes from the user specifiying country and region.
 
<h3>city_data</h3>
This function returns all data associated with a specified city in the sighting data. An example command to access this function route is

        curl localhost:5030/cities/data/?city=Austin

<h3>userguide</h3>
This function returns some example commands to help the user get started. The functions route is accessed using the command

	curl localhost:5030/

<h3>Example Outputs</h3>
Output is printed to the terminal. Each piece of data is printed to a new line. A portion of the output for the command given for city_data is

	country:United_States
	region:Texas
	city:Austin
	spacecraft:ISS
	sighting_date:Tue Feb 22/05:28 AM
	duration_minutes:1
	max_elevation:13
	enters:13 above N
	exits:10 above NNE
	utc_offset:-6.0
	utc_time:11:28
	utc_date:Feb 22, 2022

All data is printed sequentially as it appears in the xml file. Text before the colon indicates a value key and text after the colon indicates the key value. 

Example output for the command given for print_countries is

	All countries:
	United_States

At the very top of each output is a label indicating what type of data is returned. In this example the list of countries in the sighting data is returned so "All countries:" is printed. On each subsequent line data conforming to the query parameter is printed. Repeated values such as the same country or region when returning a list of all countries or regions are not printed. For example, even though "United_States" appears many times in the sighting data, it is only printed once. However, as in the example for city_data, country or region data may be repeated when it is referenced in the context of each specific sighting case. 

<h2>Instructions for Running</h2>
<h4>Pulling and Running the Image</h4>
The image is pulled using one command:

	docker pull pavanshukla99/midterm:latest 

The image can be run using the command

	docker run --name "midterm_container" -d -p 5030:5000 pavanshukla99/midterm:latest

Then queries can be made to the server using commands of the format specified in the functions section.  

<h4>Building and Running the Image</h4>
First the git repository containing the necessary build files must be pulled using the command

	git clone https://github.com/pavans99/ISS_position_and_sighting_data_application.git

Move into the repositroy directory and run the command

	make

Then the image will be built, and the Flask application will start automatically. Queries can be made to the application using commands of the format specified in the functions section.
Alternatively, one can build and run the image manually. Inside the same directory, instead run the commands

	docker build -t pavanshukla99/midterm:latest .
	docker run --name "midterm_container" -d -p 5030:5000 pavanshukla99/midterm:latest

<h4>Running the Unit Tests</h4>
To run the unit tests the image must be pulled down or built first. Then run the command 

	docker run --rm -v $PWD:/app pavanshukla99/midterm:latest test_midterm.py

to execute the unit tests.

<h2>Some notes about the Dockerfile and downloading the data</h2>
There are two Dockerfiles present in the repository, Dockerfile and Dockerfile2. Dockerfile is the only one being used in the current configuration. Dockerfile runs ADD commands for both files, then downloads and containerizes them automatically. This Dockerfile conforms to the criteria that the Dockerfile should containerize the datasets. However, the function read_data_from_file_into_dict contains routines to download the data and write the data to files. Therefore the ADD commands and subsequent containerization are not actually necessary and only included to satisfy assignment requirements. Dockerfile2 does not contain commands to download and containerize the data, but it will function properly and return identical outputs to the application built using Dockerfile. In both cases the user does not have to do anything to download the data. However if one wishes to download the position and sighting data themselves then they can run the commands

	wget https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_OEM/ISS.OEM_J2K_EPH.xml
	wget https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_sightings/XMLsightingData_citiesUSA09.xml

<h2>Citations</h2>
NASA website: https://data.nasa.gov/Space-Science/ISS_COORDS_2022-02-13/r6u8-bhhq

Position data: https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_OEM/ISS.OEM_J2K_EPH.xml

Sighting data: https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_sightings/XMLsightingData_citiesUSA09.xml
