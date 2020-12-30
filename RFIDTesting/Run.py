from Presenters import LCD
from Reader import Reader
from UserLoginManager import LoginManager
from time import sleep


reader = Reader()
lcd = LCD()
login_manager = LoginManager(reader, lcd)


# Main loop
while True:
    # Fetch any data available from the RFID reader
    data = reader.get_tag_data()

    # Handle the data received
    login_manager.handle_received_data(data)

    # Wait two seconds
    sleep(2)
