# Import necessary libraries
import random
import tkinter as tk
import device_address_generator
import smart_contract
import encrypt
import paho.mqtt.client as mqtt

# Connect to the MQTT broker
broker_address = "broker.emqx.io"
port = 1883
client = mqtt.Client()
client.connect(broker_address, port)

# Set the font size for the labels
textSize = 16

# Generate a device address using the device_address_generator module
result = device_address_generator.generate_device_address()

# Store the private key, public key, and Ethereum address in separate variables
private_key = result['private_key']
public_key = result['public_key']
ethereum_address = result['ethereum_address']

# Define a class for the electricity meter GUI
class ElectricityMeter:
    def __init__(self, master):
        self.master = master
        master.title("Smart Electricity Meter")

        # Set the device address to the Ethereum address generated earlier
        self.device_address = ethereum_address

        # Create labels for the device address, meter reading, device owner, public key, encryption status, and registration status
        device_address_label = tk.Label(
            master, text="Device Address:", font=("Helvetica", textSize))
        device_address_label.pack()
        self.device_address_entry = tk.Entry(
            master, width=0, font=("Helvetica", textSize))
        self.device_address_entry.insert(0, self.device_address)
        self.device_address_entry.pack()
        self.meter_label = tk.Label(
            master, text="Electricity Meter:", font=("Helvetica", textSize))
        self.meter_label.pack()
        self.meter_value = tk.Label(master, text="", font=(
            "Helvetica", int(textSize*2)))  # Changed font size
        self.meter_value.pack()
        self.device_owner_label = tk.Label(
            master, text="Owner:", font=("Helvetica", textSize))
        self.device_owner_label.pack()
        self.device_owner_address = tk.Label(
            master, text="", font=("Helvetica", textSize))
        self.device_owner_address.pack()
        self.device_public_key_label = tk.Label(
            master, text="PublicKey:", font=("Helvetica", textSize))
        self.device_public_key_label.pack()
        self.device_public_key = tk.Label(
            master, text="", font=("Helvetica", textSize))
        self.device_public_key.pack()
        self.device_Encryption_Status_label = tk.Label(
            master, text="Encryption Status:", font=("Helvetica", textSize))
        self.device_Encryption_Status_label.pack()
        self.device_Encryption_Status = tk.Label(
            master, text="N/A", font=("Helvetica", textSize))
        self.device_Encryption_Status.pack()
        self.device_Register_Status_label = tk.Label(
            master, text="Register Status:", font=("Helvetica", textSize))
        self.device_Register_Status_label.pack()
        self.device_Register_Status = tk.Label(
            master, text="N/A", font=("Helvetica", textSize))
        self.device_Register_Status.pack()

        # Initialize the meter reading to a random value between 0 and 10000
        self.meter_reading = random.uniform(0, 10000)

        # Start a timer to update the meter reading every second
        self.master.after(0, self.update_meter_reading)

    # Define a function to blink a component by changing its foreground color
    def blink(self, component, color):
        if component.cget("foreground") == color:
            component.config(foreground="black")
        else:
            component.config(foreground=color)

    # Define a class method to update the meter reading for a device
    def update_meter_reading(self):
        # Generate a random increment value between 0 and 1 to add to the current meter reading
        increment = random.uniform(0, 1)
        self.meter_reading += increment
        
        # Format the meter reading value to two decimal places and add the unit of measurement
        meter_str = "{:.2f} kWh".format(self.meter_reading)
        print(meter_str)
        
        # Update the GUI display with the current meter reading
        self.meter_value.config(text=meter_str)
        
        # Check if the device owner is registered on the blockchain
        if smart_contract.check_device_owner_exist(self.device_address):
            # Get the device owner's address and public key from the blockchain
            device_owner_address = smart_contract.get_device_owner_address(self.device_address)
            device_public_key = smart_contract.get_device_owner_public_key(device_owner_address)
            
            # Update the GUI display with the device owner's address and registration status
            self.device_owner_address.config(text=device_owner_address)
            self.device_Register_Status.config(text="DEVICE REGISTERED WITH BLOCKCHAIN")
            self.blink(self.device_Register_Status, "green")
            
            # Check if the device owner has set up their public key for encryption
            if device_public_key == "":
                # If the public key is not set up, publish the meter reading in plain text over MQTT
                self.device_public_key.config(text="Not Set Up")
                client.publish(self.device_address, meter_str)
                print(device_owner_address)
                
                # Update the GUI display with the encryption status (insecure) and blink the status indicator
                self.device_Encryption_Status.config(text="INSECURE STATUS: MQTT IS NOT ENCRYPTED")
                self.blink(self.device_Encryption_Status, "red")

            else:
                # If the public key is set up, encrypt the meter reading before publishing it over MQTT
                self.device_public_key.config(text=device_public_key)
                print(smart_contract.get_device_owner_public_key(device_owner_address))
                client.publish(self.device_address, encrypt.encrypt_message(device_public_key, meter_str))
                
                # Update the GUI display with the encryption status (secure) and blink the status indicator
                self.device_Encryption_Status.config(text="SECURE STATUS: MQTT IS ENCRYPTED")
                self.blink(self.device_Encryption_Status, "green")
        else:
            # If the device owner is not registered on the blockchain, update the GUI display accordingly
            self.device_owner_address.config(text="UNREGISTERED")
            self.device_public_key.config(text="NOT EXIST")
            self.device_Register_Status.config(text="DEVICE NOT REGISTERED WITH BLOCKCHAIN")
            self.blink(self.device_Register_Status, "blue")
            self.blink(self.device_Encryption_Status, "blue")
            
        # Schedule the method to run again after 1000 milliseconds (1 second)
        self.master.after(1000, self.update_meter_reading)




# Define the entry point of the program as the main block
if __name__ == '__main__':
    # Create a new Tkinter root window
    root = tk.Tk()
    
    # Instantiate an ElectricityMeter object with the root window as its parent
    sensor = ElectricityMeter(root)
    
    # Start the Tkinter event loop to handle user interface events
    root.mainloop()
