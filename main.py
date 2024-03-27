import requests
import json
import pandas as pd
from datetime import datetime
import logging
from flask import Flask, send_file

# Request parameters
minPrice = 18000
maxPrice = 35000
minKm = None
maxKm = 100000
minHp = 199
maxHp = 201
minYear = 2018
maxYear = 2023

def doRequest(pageNum, minPrice, maxPrice, minKm, maxKm, minHp, maxHp, minYear, maxYear):
    """It makes the request to the coches.net server and returns the response in JSON format."""

    url = "https://ms-mt--api-web.spain.advgo.net/search/listing"

    payload = json.dumps({
      "pagination": {
        "page": pageNum,
        "size": 30
      },
      "sort": {
        "order": "desc",
        "term": "relevance"
      },
      "filters": {
        "isFinanced": False,
        "price": {
          "from": minPrice,
          "to": maxPrice
        },
        "bodyTypeIds": [],
        "categories": {
          "category1Ids": [
            2500
          ]
        },
        "contractId": 0,
        "drivenWheelsIds": [],
        "environmentalLabels": [],
        "equipments": [],
        "fuelTypeIds": [],
        "hasPhoto": True,
        "hasWarranty": None,
        "hp": {
          "from": minHp,
          "to": maxHp
        },
        "isCertified": False,
        "km": {
          "from":minKm,
          "to": maxKm
        },
        "luggageCapacity": {
          "from": None,
          "to": None
        },
        "onlyPeninsula": True,
        "offerTypeIds": [
          0,
          2,
          3,
          4,
          5
        ],
        "provinceIds": [],
        "sellerTypeId": 0,
        "transmissionTypeId": 0,
        "vehicles": [
          {
            "make": "VOLKSWAGEN",
            "makeId": 47,
            "model": "Polo",
            "modelId": 109
          }
        ],
        "year": {
          "from": minYear,
          "to": maxYear
        }
      }
    })
    headers = {
      'authority': 'ms-mt--api-web.spain.advgo.net',
      'accept': 'application/json, text/plain, */*',
      'accept-language': 'es-ES,es;q=0.9',
      'content-type': 'application/json',
      'origin': 'https://www.coches.net',
      'referer': 'https://www.coches.net/',
      'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'cross-site',
      'sec-gpc': '1',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
      'x-adevinta-channel': 'web-desktop',
      'x-schibsted-tenant': 'coches'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return json.loads(response.text)

def fromPagesListGetDataframe(pages):
    """Converts the list of pages into a pandas dataframe"""
    pages_dict = []

    # Pass each request from each page to a common dictionary.
    for page in pages:
      pages_dict.append(page)

    # Create a list of cars
    cars_list = []
    for page in pages_dict:
        for car in page['items']:
            cars_list.append(car)

    # Create a list for each column of the following dataframe
    title = []
    url = []
    price = []
    km = []
    year = []
    cubicCapacity = []
    mainProvince = [] 
    fuelType = []
    bodyTypeId = []
    warranty_id = []
    warranty_months = []
    isProfessional = []
    publishedDate = []
    hasUrge = []
    phone = []
    environmentalLabel = []
    drivenWheelsId = []
    transmissionTypeId = []

    # For each car, append the value of
    # each attribute to the corresponding list
    for car in cars_list:
        # Attributes that are always present
        title.append(str(car['title']))
        url.append(str(car['url']))
        price.append(int(car['price']['amount']))
        isProfessional.append(str(car['isProfessional']))
        publishedDate.append(str(car['publishedDate']))
        hasUrge.append(str(car['hasUrge']))
        phone.append(str(car['phone']))
        
        # Attributes that are not always present 
        try:
            km.append(int(car['km']))
        except KeyError:
            km.append("None")
        try:
            year.append(int(car['year']))
        except KeyError:
            year.append("None")
        try:
            cubicCapacity.append(int(car['cubicCapacity']))
        except KeyError:
            cubicCapacity.append("None")
        mainProvince.append(str(car['mainProvince']) )
        try:
            fuelType.append(str(car['fuelType']))
        except KeyError:
            fuelType.append("None")
        try:
            bodyTypeId.append(int(car['bodyTypeId']))
        except KeyError:
            bodyTypeId.append("None")
        try:
            warranty_id.append(int(car['warranty']['id']))
        except KeyError:
            warranty_id.append('None')
        try:        
            warranty_months.append(int(car['warranty']['months']))
        except KeyError:
            warranty_months.append('None')
        try:
          environmentalLabel.append(str(car['environmentalLabel']))
        except KeyError:
          environmentalLabel.append('None')
        try:
            drivenWheelsId.append(int(car['drivenWheelsId']))
        except KeyError:
            drivenWheelsId.append("None")
        transmissionTypeId.append(int(car['transmissionTypeId']))
    

    # Dataframe creation
    df = pd.DataFrame({'title': title,
                       'url':url,
                       'price':price,
                       'km':km,
                       'year':year,
                       'cubicCapacity':cubicCapacity,
                       'mainProvince':mainProvince,
                       'fuelType':fuelType,
                       'bodyTypeId':bodyTypeId,
                       'warranty_id':warranty_id,
                       'warranty_months':warranty_months,
                       'isProfessional':isProfessional,
                       'publishedDate':publishedDate,
                       'hasUrge':hasUrge,
                       'phone':phone,
                       'environmentalLabel':environmentalLabel,
                       'drivenWheelsId':drivenWheelsId,
                       'transmissionTypeId':transmissionTypeId})
    # Sort by price
    df = df.sort_values(by=['price'])
    return df

def fromDataframeGenerateLogs(df):
    """For each row in the dataframe, generates a log with the information of the ad."""
    # We define a dataframe to store the interesting cars
    interestingCars = []
    
    # We iterate over the dataframe
    for i in range(len(df)):
        interestingCars.append([df['title'][i], df['price'][i], df['km'][i], df['url'][i], df['year'][i], df['mainProvince'][i]])
        logging.info('Timestamp: {} - Car: {} - Price: {} - Km: {} - URL: {} - Year: {} - Province: {}'.format(datetime.now(), df['title'][i], df['price'][i], df['km'][i], df['url'][i], df['year'][i], df['mainProvince'][i]))
    
    # We generate a dataframe with the information of the interesting cars and save it to a csv file.
    interestingCars = pd.DataFrame(interestingCars, columns=['title', 'price', 'km', 'url','year','province'])
    # Add a column with the current date
    interestingCars['date'] = datetime.now()
    # Reorder columns
    interestingCars = interestingCars[['date', 'title', 'price', 'km', 'year', 'url', 'province']]
    interestingCars.to_csv('interestingCars.csv', index=False, sep=';')

def main():
    # We generate a log to see the number of pages to be processed.
    logging.basicConfig(filename='cochesnet.log', level=logging.INFO)

    # We make a request to see how many pages there are.
    testForNumOfPages = doRequest(0, minPrice, maxPrice, minKm, maxKm, minHp, maxHp, minYear, maxYear)
    NPages = int(testForNumOfPages['meta']['totalPages'])
    logging.info('Starting to scrape. Total pages: {}'.format(NPages))

    # We do the requests and store them in a list.
    pages = []
    for pageNumber in range(NPages+1):
        pages.append(doRequest(pageNumber, minPrice, maxPrice, minKm, maxKm, minHp, maxHp, minYear, maxYear))

    logging.info('Scraping finished (SUCCESS!). {} pages scraped.'.format(NPages))    
    # We generate a dataframe with the information of the ads.
    df = fromPagesListGetDataframe(pages)

    # Generate logs
    fromDataframeGenerateLogs(df)

    # When finished, we generate a log to indicate that the process has been completed.
    logging.info('Scraping finished (SUCCESS!). {} pages scraped.'.format(NPages))

app = Flask(__name__)

@app.route('/')
def index():
    main()  # Call the function to generate the CSV
    # Specify the path to the generated CSV file
    csv_path = 'interestingCars.csv'
    # Send the file as response with appropriate headers
    return send_file(csv_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)