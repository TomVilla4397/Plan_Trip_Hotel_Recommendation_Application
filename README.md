# Trip Planner & Hotel Finder 🌍

This Python application helps users plan their trips and provides hotel recommendations based on their preferences. It uses PyQt5 for the graphical user interface and leverages APIs to fetch trip itineraries and hotel data.

## Features 🚀

- User-friendly GUI for entering trip details and preferences.
- Retrieves trip itineraries and hotel recommendations from external APIs.
- Displays the trip itinerary and hotel recommendations in separate windows.
- Supports input validation and error handling.
- Utilizes pandas and NumPy libraries for data processing.

## Dependencies 📦

- Python 3.7 or newer
- [pandas](https://pandas.pydata.org/)
- [requests](https://docs.python-requests.org/en/latest/)
- [PyQt5](https://pypi.org/project/PyQt5/)
- [langchain](https://pypi.org/project/langchain/)
- [NumPy](https://numpy.org/)

## Installation 🛠

1. Clone this repository to your local machine.
2. Install the necessary dependencies using pip:

```sh
pip install -r requirements.txt

## Usage 💡
1.Replace "insert your key here" in the api_keys.py file with your actual API keys.
2.Open a terminal or command prompt and navigate to the project directory.
3.Run the following command to execute the application: python plan_trip_Gui.py.
4.The GUI window will appear, prompting you to enter trip details.
5.Click "Submit" to generate the trip itinerary and hotel recommendations.

Note: In the line of code from api_keys import keys, the API keys for OpenAI and RapidAPI are being imported. headers = keys() then sets the API key for the RapidAPI.


##Contribution 🤝
Feel free to explore the code and modify it according to your needs. Contributions are welcome! If you encounter any issues or have suggestions for improvement, please open an issue in the repository.

License ⚖️
This project is open-source and available under the MIT License.

Happy trip planning!


