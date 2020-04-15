from bs4 import BeautifulSoup
import requests
import notify2

# Fetch the exchange rates from XE
def fetch_exchange_rates():

    # URL to fetch the latest rates
    url = "https://www.xe.com/currencytables/"

    # Fetch and parse the data from the request
    soup = BeautifulSoup(requests.get(url).text, "html.parser")

    # Find the table with the live currency data
    table = soup.find("table", attrs={'id': 'crLive'})

    rows = []
    # Find all trs in the table
    for row in table.findAll('tr'):
        # Find all tds in the table
        cells = row.findAll('td')
        row = []
        # Loop through cells and append the text to the row list
        for cell in cells:
            row.append(cell.text)
        # Append each row to the rows list
        rows.append(row)
    # Return GBP to EUR value
    return rows[2]

def notify():
    
    # Icon for the notification
    icon = "/home/nickdavies07/Python/Currency-Rates/currency-icon.png"
    
    # Fetch the current GBP to EUR rate
    currentRate = list(fetch_exchange_rates())
   
    # Initialise the DBus connection
    notify2.init("GBP to EUR rates notifier")
 
    # Create a notification object and assign the icon
    n = notify2.Notification("Currency Notifier", icon = icon)
        
    # Set the urgency level to normal
    n.set_urgency(notify2.URGENCY_NORMAL)
        
    # Set the timeout for the notification
    n.set_timeout(5000)

    # Store the text strings returned from the API
    message = str(currentRate[0]) + " - " + str(currentRate[1]) + " - " + str(currentRate[2]) + "\n"

    # Set the message for the notification
    n.update("Current Rates", message)

    # Request the server to show the notification
    n.show()

if __name__ == "__main__":
    notify()
