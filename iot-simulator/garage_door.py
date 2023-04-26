import random
import threading
import tkinter as tk
import device_address_generator
import smart_contract
import encrypt
import paho.mqtt.client as mqtt
import json
from json.decoder import JSONDecodeError
from eth_account import Account
from eth_account.messages import encode_defunct
import time

broker_address = "broker.emqx.io"
port = 1883
client = mqtt.Client()
textSize = 16

# Call the function and store the returned values in variables
result = device_address_generator.generate_device_address()

# Store the private key, public key, and Ethereum address in different variables
private_key = result['private_key']
public_key = result['public_key']
ethereum_address = result['ethereum_address']

# Initialize variables
global garage_door 
garage_door = bool(random.randint(0, 1))
global device_owner_address
device_owner_address = ""

# Connect to MQTT broker
client.connect(broker_address, port)

# Define a set to store random numbers
nonce_pool = set()

# Define a timer to clear the nonce pool every 10 minutes
def clear_nonce_pool():
    global nonce_pool
    current_timestamp = int(time.time())
    expired_timestamp = current_timestamp - 3600  # Expiration time is 1 hour ago
    expired_nonce_set = {nonce for nonce in nonce_pool if nonce[1] < expired_timestamp}
    nonce_pool -= expired_nonce_set
    threading.Timer(600, clear_nonce_pool).start()  # Execute the function again after 10 minutes

clear_nonce_pool()  # Start the timer

# Verify the signature of the received message
def verify_signature(message, nonce, timestamp, signature, address):
    # Convert the message to a hex-encoded string
    msg = message.encode('utf-8').hex()
    # Extract the nonce from the received message and convert it to a hex-encoded string
    nonce_hex = nonce[2:]
    # Convert the timestamp to a hex-encoded string
    timestamp_hex = hex(timestamp)[2:]

    # Concatenate the message, nonce, and timestamp to create a string to sign
    data_to_sign = f"{msg}{nonce_hex}{timestamp_hex}"
    # Encode the string to sign as a defunct message
    encoded_message = encode_defunct(hexstr=f"0x{data_to_sign}")

    # Recover the Ethereum account associated with the signature
    account = Account.recover_message(encoded_message, signature=signature)

    # Print information for debugging purposes
    print("ecRecoverAddr: ",account)
    print("device_owner_address: ",device_owner_address)
    print("Received message: ", message)
    print("Received nonce: ", nonce)
    print("Received timestamp: ", timestamp)
    print("Received sign: ", signature)

    # Verify that the recovered account matches the expected address
    if account.lower() == address.lower():
        # Add the nonce to the set of used nonces
        nonce_pool.add(nonce)
        print("Nonce added to pool.")
        # Return True if the signature is valid
        return True
    else:
        # Return False if the signature is invalid
        return False


def on_message(client, userdata, message):
    global garage_door
    global device_owner_address

    try:
        # Load the received message payload as a JSON object
        payload = json.loads(message.payload.decode("utf-8"))
        # Extract the message, nonce, timestamp, and signature from the JSON object
        msg = payload["message"]
        nonce = payload["nonce"]
        timestamp = payload["timestamp"]
        sign = payload["sign"]

        # Check if the nonce has already been used to prevent replay attacks
        if nonce in nonce_pool:
            print("Signature Replay Attack:Nonce has been used before.")
            return
        
        # Verify the signature of the received message
        if verify_signature(msg, nonce, timestamp, sign, device_owner_address):
            print("Signature is valid!")
            # Update the garage door status based on the received message
            if msg.lower() == "on":
                garage_door = 1
            elif msg.lower() == "off":
                garage_door = 0
        else:
            print("Signature is not valid.")
        
        # Print the current garage door status for debugging purposes
        print("Current garage door status: ", garage_door)

    # Handle any JSON decoding errors
    except JSONDecodeError as e:
        # print("Error decoding JSON message: ", str(e))
        a=0


# Set the callback function for the MQTT client
client.on_message = on_message

# Subscribe to the topic
client.subscribe(ethereum_address)
client.loop_start()

# Define the GarageDoor class
class GarageDoor:
    
    # Initialize the class
    def __init__(self, master):
        
        # Set the master window's title
        self.master = master
        master.title("Smart Electricity Meter")

        # Generate and set the device address
        self.device_address = ethereum_address

        # Create labels and temperature value labels
        # for displaying device information
        device_address_label = tk.Label(
            master, text="Device Address:", font=("Helvetica", textSize))
        device_address_label.pack()
        
        # Entry field to display the device address
        self.device_address_entry = tk.Entry(
            master, width=0, font=("Helvetica", textSize))
        self.device_address_entry.insert(0, self.device_address)
        self.device_address_entry.pack()

        # Label to display the status of the garage door
        self.status_label = tk.Label(
            master, text="Grage Door:", font=("Helvetica", textSize))
        self.status_label.pack()

        # Label to display the status value
        self.status_value = tk.Label(
            master, text="", font=("Helvetica", int(textSize*5))) # increased font size
        self.status_value.pack()

        # Label to display the device owner's address
        self.device_owner_label = tk.Label(
            master, text="Owner:", font=("Helvetica", textSize))
        self.device_owner_label.pack()

        # Label to display the device owner's address value
        self.device_owner_address = tk.Label(
            master, text="", font=("Helvetica", textSize))
        self.device_owner_address.pack()

        # Label to display the device's public key
        self.device_public_key_label = tk.Label(
            master, text="PublicKey:", font=("Helvetica", textSize))
        self.device_public_key_label.pack()

        # Label to display the device's public key value
        self.device_public_key = tk.Label(
            master, text="", font=("Helvetica", textSize))
        self.device_public_key.pack()

        # Label to display the encryption status of the device
        self.device_Encryption_Status_label = tk.Label(
            master, text="Encryption Status:", font=("Helvetica", textSize))
        self.device_Encryption_Status_label.pack()

        # Label to display the encryption status value
        self.device_Encryption_Status = tk.Label(
            master, text="N/A", font=("Helvetica", textSize))
        self.device_Encryption_Status.pack()

        # Label to display the registration status of the device
        self.device_Register_Status_label = tk.Label(
            master, text="Register Status:", font=("Helvetica", textSize))
        self.device_Register_Status_label.pack()

        # Label to display the registration status value
        self.device_Register_Status = tk.Label(
            master, text="N/A", font=("Helvetica", textSize))
        self.device_Register_Status.pack()
        
        # Start a timer to update the temperature value every second
        self.master.after(0, self.update_meter_reading)

        # Set a function to handle window closing
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    # Function to blink the component text
    def blink(self, component, color):
        if component.cget("foreground") == color:
            component.config(foreground="black")
        else:
            component.config(foreground=color)

    # Define the callback function for handling incoming messages
    def on_closing(self):
        client.disconnect()
        client.loop_stop()
        self.master.destroy()
    

    # The following code defines a function called "update_meter_reading" which is a method of a class.
    # The purpose of this function is to update the status of a device's garage door and publish it to a message broker (MQTT)
    # if the device is registered with a blockchain.

    def update_meter_reading(self):
        # Declare a global variable
        global device_owner_address

        # Initialize a variable to store the status of the garage door
        door_status = ""

        # Check if the device owner exists in the blockchain
        if smart_contract.check_device_owner_exist(self.device_address):
            # If the device is registered, check if the garage door is open or closed
            if garage_door:
                door_status = "ON"
            else:
                door_status = "OFF"
            
            # Update the status of the device's garage door
            self.status_value.config(text=door_status)
            
            # Get the device owner's address and public key from the blockchain
            device_owner_address = smart_contract.get_device_owner_address(self.device_address)
            device_public_key = smart_contract.get_device_owner_public_key(device_owner_address)
            
            # Display the device owner's address
            self.device_owner_address.config(text=device_owner_address)
            
            # Display the device registration status
            self.device_Register_Status.config(text="DEVICE REGISTERED WITH BLOCKCHAIN")
            
            # Blink the device registration status to indicate success
            self.blink(self.device_Register_Status, "green")
            
            # Check if the device owner's public key exists in the blockchain
            if device_public_key == "":
                # If the public key is not set up, display a message and publish the door status to the message broker
                self.device_public_key.config(text="Not Set Up")
                client.publish(self.device_address, door_status)
                
                # Display the encryption status and blink it to indicate an insecure status
                self.device_Encryption_Status.config(text="INSECURE STATUS: MQTT IS NOT ENCRYPTED")
                self.blink(self.device_Encryption_Status, "red")
            else:
                # If the public key is set up, encrypt the door status and publish it to the message broker
                self.device_public_key.config(text=device_public_key)
                client.publish(self.device_address, encrypt.encrypt_message(device_public_key, door_status))
                
                # Display the encryption status and blink it to indicate a secure status
                self.device_Encryption_Status.config(text="SECURE STATUS: MQTT IS ENCRYPTED")
                self.blink(self.device_Encryption_Status, "green")
        else:
            # If the device is not registered, display messages indicating its unregistered status
            self.status_value.config(text="N/A")
            self.device_owner_address.config(text="UNREGISTERED")
            self.device_public_key.config(text="NOT EXIST")
            self.device_Register_Status.config(text="DEVICE NOT REGISTERED WITH BLOCKCHAIN")
            
            # Blink the device registration status and encryption status to indicate an unregistered status
            self.blink(self.device_Register_Status, "blue")
            self.blink(self.device_Encryption_Status, "blue")

        # Schedule the function to run again after a 1-second delay
        self.master.after(1000, self.update_meter_reading)



# The following code block is used to instantiate a `GarageDoor` object and display it using a `Tkinter` GUI.

if __name__ == '__main__':
    # Create a `Tk` object and assign it to the `root` variable
    root = tk.Tk()
    
    # Instantiate a `GarageDoor` object and pass the `root` object as its parent
    sensor = GarageDoor(root)
    
    # Enter the main event loop of the `Tk` object to display the GUI
    root.mainloop()
