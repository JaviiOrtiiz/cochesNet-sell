import requests
import json
from datetime import datetime

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

def fromPagesListGetDict(pages):
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
    timestamp = []
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
        timestamp.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
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
    
    # Create a json with the lists
    data = {
      'timestamp': timestamp,
      'title': title,
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
      'transmissionTypeId':transmissionTypeId}
    return data


def main():
    # We make a request to see how many pages there are.
    testForNumOfPages = doRequest(0, minPrice, maxPrice, minKm, maxKm, minHp, maxHp, minYear, maxYear)
    NPages = int(testForNumOfPages['meta']['totalPages'])

    # We do the requests and store them in a list.
    pages = []
    for pageNumber in range(NPages+1):
        pages.append(doRequest(pageNumber, minPrice, maxPrice, minKm, maxKm, minHp, maxHp, minYear, maxYear))

    # We generate a CSV with the information of the ads.
    csv = fromPagesListGetDict(pages)

    # csv to file withouth pandas
    #csv name is timestamp
    with open('csv/cochesnet-{}.csv'.format(datetime.now().strftime("%Y-%m-%d-%H-%M-%S")), 'w') as f:
        f.write('date;title;url;price;km;year;cubicCapacity;mainProvince;fuelType;bodyTypeId;warranty_id;warranty_months;isProfessional;publishedDate;hasUrge;phone;environmentalLabel;drivenWheelsId;transmissionTypeId\n')
        for i in range(len(csv['title'])):
            f.write('{}'.format(';'.join([str(csv[key][i]) for key in csv.keys()])))
            f.write('\n')
        f.close()

main()