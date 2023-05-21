import requests
import os
import pandas as pd
from io import StringIO
from datetime import datetime
os.environ["OPENAI_API_KEY"] = "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"
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
def get_user_input():
    destination = input("Please enter the destination: ")
    start_date = input("Please enter the start date (YYYY-MM-DD): ")
    end_date = input("Please enter the end date (YYYY-MM-DD): ")
    adults_num = int(input("Please enter the number of adults: "))
    
    # Check if the user is traveling with children
    has_children = input("Are you traveling with children? (yes/no): ").lower()

    if has_children == 'yes':
        # For children_num, if you expect multiple ages separated by comma.
        children_num = list(map(int, input("Please enter the ages of children separated by comma: ").split(',')))
    else:
        children_num = []
    
    attraction = input("Please enter attractions you are interested in(e.g: museums, theme parks, landmarks, nature trails, historical sites, etc): ")
    transportation = input("Please enter the mode of transportation(e.g: bus, rental car, taxi, bicycle, walking, etc): ")
    
    return destination, start_date, end_date, adults_num, children_num, attraction, transportation
def get_gui_input():
    destination =""# input("Please enter the destination: ")
    start_date =""# input("Please enter the start date (YYYY-MM-DD): ")
    end_date =""# input("Please enter the end date (YYYY-MM-DD): ")
    adults_num =""# int(input("Please enter the number of adults: "))
    
    # Check if the user is traveling with children
    has_children = ""#input("Are you traveling with children? (yes/no): ").lower()

    if has_children == 'yes':
        # For children_num, if you expect multiple ages separated by comma.
        children_num = "" #list(map(int, input("Please enter the ages of children separated by comma: ").split(',')))
    else:
        children_num = []
    
    attraction =  "" #input("Please enter attractions you are interested in(e.g: museums, theme parks, landmarks, nature trails, historical sites, etc): ")
    transportation = "" #input("Please enter the mode of transportation(e.g: bus, rental car, taxi, bicycle, walking, etc): ")
    
    return destination, start_date, end_date, adults_num, children_num, attraction, transportation
def open_chat(destination, start_date, end_date, adults_num, children_num, attraction, tranportaion):
    children_ages = " and ".join(str(age) for age in children_num)
    prompt = f'''
    Plan a trip to {destination}, from {start_date} to {end_date}. 
    {adults_num} adults and {children_ages} years old kids. 
    They are interested in {attraction}. They plan to get around by {tranportaion}. 
    Remember to break down the itinerary into days and include a variety of activities based on the user's interests. 
    Also, don't forget to consider travel times between activities and rest periods. You can even provide a few options for each day so the user can choose their preferred itinerary.
    At the end of the itinerary create a table with from_date, to_date, and location for each stay needed (to easy plan the accommodations).
    add a new location if the drive needed is approximately more than an hour.
    Don't print anything else after the table. create the table in a csv format. write "table:" before the table.'''
    chat = ChatOpenAI(temperature=0, request_timeout=240)
    res = chat([HumanMessage(content=prompt)])
    return res.content
def get_search_data(location):
    url = "https://hotels4.p.rapidapi.com/locations/v3/search"

    querystring = {"q":location,"locale":"en_US"}

    headers = {
	    "X-RapidAPI-Key": "57f5107708msh55b46a107095710p14508cjsn4fec6559325e",
	    "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    return response
def get_gaiaID(response):
    return response.json()['sr'][0]['gaiaId']
def get_hotels(gaiaID, check_in, check_out, adults_num, children_num):
    url = "https://hotels4.p.rapidapi.com/properties/v2/list"

    # Split the check_in date into day, month, year
    check_in_day, check_in_month, check_in_year = map(int, check_in.split('-'))
    check_out_day, check_out_month, check_out_year = map(int, check_out.split('-'))

    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "en_US",
        "destination": { "regionId": gaiaID },
        "checkInDate": {
            "day": check_in_day,
            "month": check_in_month,
            "year": check_in_year
        },
        "checkOutDate": {
            "day": check_out_day,
            "month": check_out_month,
            "year": check_out_year
        },
        "rooms": [
            {
                "adults": adults_num,
                "children": children_num
            }
        ],
        "resultsSize": 3,
        "sort": "REVIEW ",
        "filters": {
        "price": {
            "max": 300,
            "min": 50
        }
    }
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "57f5107708msh55b46a107095710p14508cjsn4fec6559325e",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers)
    data = response.json()

    # Check if the response contains the expected data
    if 'data' in data and 'propertySearch' in data['data'] and 'properties' in data['data']['propertySearch']:
        properties = data['data']['propertySearch']['properties']
        if properties:
            hotels = []
            for hotel in properties:
                hotel_info = {
                    'name': hotel['name'],
                    'price': hotel['price'],
                    'reviews': hotel['reviews']
                }
                hotels.append(hotel_info)
            
            return hotels
        else:
            print("No hotels found for the given criteria.")
    else:
        print("Invalid response from the hotel API.")
    
    return []  # Return an empty list if no hotels or invalid response
def create_table(itinerary):
    # itinerary is your string
    table_start = itinerary.find("table:") + len("table:")
    table_str = itinerary[table_start:].strip()

    try:
        # Convert the CSV string into a pandas DataFrame
        df = pd.read_csv(StringIO(table_str))

        # Print the DataFrame
        #print(df)
        return df
    except pd.errors.ParserError as e:
        print(f"Error occurred while parsing CSV: {e}")
        return None
def process_data(df):
    # Ensure dates are datetime objects
    df['from_date'] = pd.to_datetime(df['from_date'])
    df['to_date'] = pd.to_datetime(df['to_date'])
    hotel_data = {}
    for _, row in df.iterrows():
        check_in = row['from_date'].strftime('%d-%m-%Y')
        check_out = row['to_date'].strftime('%d-%m-%Y')
        location = row['location']

        # Get the search data for this location
        search_data = get_search_data(location)

        try:
            gaiaID = get_gaiaID(search_data)
        except (KeyError, IndexError):
            print(f"No gaiaId found for location: {location}")
            continue  # Skip this iteration and move to the next one

        
        # Now you can use gaiaID    
    hotel_info = get_hotels(gaiaID, check_in, check_out, adults_num, children_num)

        # Save hotel details
    if hotel_info:
        hotel_data[location] = hotel_info
    else:
        hotel_data[location] = "No hotels found in {location}."

    return hotel_data
def plan_trip_and_find_hotels(destination, start_date, end_date, adults_num, children_num, attraction, tranportaion):
    # Get the chat response
    chat_response = open_chat(destination, start_date, end_date, adults_num, children_num, attraction, tranportaion)

    if "table:" not in chat_response:
        print("Error: 'table:' delimiter not found in chat response.")
        return

    itinerary, table_str = chat_response.split("table:", 1)
    
    if not itinerary:
        print("Error: Itinerary not found in chat response.")
        return
    # Print the trip itinerary
    print("Trip Itinerary:")
    days = itinerary.split("Day")
    for day in days:
        if day:
            print(f"Day{day}")

    df = pd.read_csv(StringIO(table_str.strip()))
    df['from_date'] = pd.to_datetime(df['from_date'])
    df['to_date'] = pd.to_datetime(df['to_date'])

    hotel_data = {}
    for _, row in df.iterrows():
        location = row['location']
        check_in = row['from_date'].strftime('%d-%m-%Y')
        check_out = row['to_date'].strftime('%d-%m-%Y')

        search_data = get_search_data(location)
        gaiaID = get_gaiaID(search_data)
        hotel_info = get_hotels(gaiaID, check_in, check_out, adults_num, children_num)

        hotel_data[location] = (check_in, check_out, hotel_info if hotel_info else f"No hotels found in {location}")

    # Print the hotel recommendations
    print("\nHotel Recommendations:")
    for location, info in hotel_data.items():
        check_in, check_out, hotels = info
        print(f"\nHotels in {location} from {check_in} to {check_out}:")
        if isinstance(hotels, str):
            print(hotels)
        else:
            print(f'{"Name:":<90} {"Price:":<30} {"Review:"}')
            for hotel in hotels:
                name = hotel['name']
                price = hotel['price']['lead']['formatted']
                review = hotel['reviews']['score']
                print(f'{name:<90} {price:<30} {review}')

# You can then use this function to get user input and pass it to open_chat function
# destination, start_date, end_date, adults_num, children_num, attraction, transportation = get_user_input()
# plan_trip_and_find_hotels(destination, start_date, end_date, adults_num, children_num, attraction, transportation)
from PyQt5.QtWidgets import QMessageBox

def plan_trip_and_find_hotels_gui(destination, start_date, end_date, adults_num, children_num, attraction, tranportaion):
    # Get the chat response
    chat_response = open_chat(destination, start_date, end_date, adults_num, children_num, attraction, tranportaion)

    if "table:" not in chat_response:
        error_message = "Error: 'table:' delimiter not found in chat response."
        print(chat_response)
        QMessageBox.critical(None, "Error", error_message)
        return

    itinerary, table_str = chat_response.split("table:", 1)
    
    if not itinerary:
        error_message = "Error: Itinerary not found in chat response."
        QMessageBox.critical(None, "Error", error_message)
        return
    # Create a message box to display the trip itinerary and hotel recommendations
    message_box = QMessageBox()
    message_box.setWindowTitle("Trip Information")
    
    # Create a message box to display the trip itinerary
    itinerary_message = "Trip Itinerary:\n"
    days = itinerary.split("Day")
    for day in days:
        if day:
            itinerary_message += f"Day{day}\n"
    df = pd.read_csv(StringIO(table_str.strip()))
    df['from_date'] = pd.to_datetime(df['from_date'])
    df['to_date'] = pd.to_datetime(df['to_date'])
    # Create a message box to display the hotel recommendations
    hotel_message = "\nHotel Recommendations:\n"
    hotel_data = {}
    for _, row in df.iterrows():
        location = row['location']
        check_in = row['from_date'].strftime('%d-%m-%Y')
        check_out = row['to_date'].strftime('%d-%m-%Y')

        search_data = get_search_data(location)
        gaiaID = get_gaiaID(search_data)
        hotel_info = get_hotels(gaiaID, check_in, check_out, adults_num, children_num)

        hotel_data[location] = (check_in, check_out, hotel_info if hotel_info else f"No hotels found in {location}")

    for location, info in hotel_data.items():
        check_in, check_out, hotels = info
        hotel_message += f"\nHotels in {location} from {check_in} to {check_out}:\n"
        if isinstance(hotels, str):
            hotel_message += hotels + "\n"
        else:
            hotel_message += f'{"Name:":<90} {"Price:":<30} {"Review:"}\n'
            for hotel in hotels:
                name = hotel['name']
                price = hotel['price']['lead']['formatted']
                review = hotel['reviews']['score']
                hotel_message += f'{name:<90} {price:<30} {review}\n'

    # Set the combined message
    combined_message = itinerary_message + hotel_message
    message_box.setText(combined_message)

    # Display the message box
    message_box.exec_()
