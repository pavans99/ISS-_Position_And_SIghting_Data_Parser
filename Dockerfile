FROM python:3.9
RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app/requirements.txt
COPY test_midterm.py /app/test_midterm.py
RUN chmod +rx /app/test_midterm.py
RUN pip install -r /app/requirements.txt


ADD https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_OEM/ISS.OEM_J2K_EPH.xml .
ADD https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_sightings/XMLsightingData_citiesUSA09.xml .
COPY . /app

ENTRYPOINT ["python"]
CMD ["midterm.py"]
