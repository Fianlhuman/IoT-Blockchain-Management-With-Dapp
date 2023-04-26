# Import necessary modules
import random
import tkinter as tk
import device_address_generator
import smart_contract
import encrypt
import paho.mqtt.client as mqtt

# Set up MQTT broker address and port
broker_address = "broker.emqx.io"
port = 1883

# Connect to MQTT broker
client = mqtt.Client()
client.connect(broker_address, port)

# Set the font size for the labels
textSize = 16

# Call the function to generate a device address and store the returned values in variables
result = device_address_generator.generate_device_address()
private_key = result['private_key']
public_key = result['public_key']
ethereum_address = result['ethereum_address']

# Define a class for the TemperatureSensor object
class TemperatureSensor:
    def __init__(self, master):
        # Set the parent window for the object and configure the window title
        self.master = master
        master.title("Temperature Sensor")

        # Set the device address for the sensor to the Ethereum address generated earlier
        self.device_address = ethereum_address

        # Create labels for the device address, temperature value, device owner, public key, and encryption and registration status
        device_address_label = tk.Label(master, text="Device Address:",font=("Helvetica", textSize))
        device_address_label.pack()
        self.device_address_entry = tk.Entry(master, width=0,font=("Helvetica", textSize))
        self.device_address_entry.insert(0, self.device_address)
        self.device_address_entry.pack()
        self.temperature_label = tk.Label(master, text="Temperature:",font=("Helvetica", textSize))
        self.temperature_label.pack()
        self.temperature_value = tk.Label(master, text="", font=("Helvetica", int(textSize*2)))
        self.temperature_value.pack()
        self.device_owner_label = tk.Label(master, text="Owner:",font=("Helvetica", textSize))
        self.device_owner_label.pack()
        self.device_owner_address = tk.Label(master, text="", font=("Helvetica", textSize))
        self.device_owner_address.pack()
        self.device_public_key_label = tk.Label(master, text="PublicKey:",font=("Helvetica", textSize))
        self.device_public_key_label.pack()
        self.device_public_key = tk.Label(master, text="", font=("Helvetica", textSize))
        self.device_public_key.pack()
        self.device_Encryption_Status_label = tk.Label(master, text="Encryption Status:",font=("Helvetica", textSize))
        self.device_Encryption_Status_label.pack()
        self.device_Encryption_Status = tk.Label(master, text="N/A", font=("Helvetica", textSize))
        self.device_Encryption_Status.pack()
        self.device_Register_Status_label = tk.Label(master, text="Register Status:",font=("Helvetica", textSize))
        self.device_Register_Status_label.pack()
        self.device_Register_Status = tk.Label(master, text="N/A", font=("Helvetica", textSize))
        self.device_Register_Status.pack()

        # Start the timer to update the temperature value every second
        self.master.after(0, self.update_temperature)

    # Define a method to blink the color of a component's text
    def blink(self,component,color):
        if component.cget("foreground") == color:
            component.config(foreground="black")
        else:
            component.config(foreground=color)    
     

    def update_temperature(self):
        # Generate a random temperature value between -20 and 40 degrees Celsius
        temperature = random.uniform(-20, 40)
        
        # Format the temperature value to display with the unit of measurement
        temperature_str = "{:.2f} ℃".format(temperature)
        
        # Print the temperature value to the console for debugging purposes
        print(temperature_str);
        
        # Update the temperature value label on the GUI with the current temperature value
        self.temperature_value.config(text=temperature_str)
        
        # Check if the device owner is registered on the blockchain
        if smart_contract.check_device_owner_exist(self.device_address):
            # Retrieve the Ethereum address of the device owner and their associated public key
            device_owner_address = smart_contract.get_device_owner_address(self.device_address)
            device_public_key = smart_contract.get_device_owner_public_key(device_owner_address)            
            
            # Update the device owner address label on the GUI with the retrieved value
            self.device_owner_address.config(text=device_owner_address)
            
            # Update the device registration status label on the GUI
            self.device_Register_Status.config(text="DEVICE REGISTERED WITH BLOCKCHAIN") 
            
            # Blink the device registration status label in green to indicate success
            self.blink(self.device_Register_Status,"green")
            
            # Check if the device owner has a public key associated with their Ethereum address
            if device_public_key == "":
                # If the device owner does not have a public key, publish the unencrypted temperature value to the MQTT broker
                self.device_public_key.config(text="Not Set Up")           
                client.publish(self.device_address, temperature_str)  
                print(device_owner_address)
                
                # Update the device encryption status label on the GUI to indicate that MQTT is not encrypted
                self.device_Encryption_Status.config(text="INSECURE STATUS: MQTT IS NOT ENCRYPTED") 
                
                # Blink the device encryption status label in red to indicate failure
                self.blink(self.device_Encryption_Status,"red")
                
            else:
                # If the device owner has a public key, encrypt the temperature value with the public key and publish it to the MQTT broker
                self.device_public_key.config(text=device_public_key) 
                print(smart_contract.get_device_owner_public_key(device_owner_address))
                client.publish(self.device_address, encrypt.encrypt_message(device_public_key,temperature_str))
                
                # Update the device encryption status label on the GUI to indicate that MQTT is encrypted
                self.device_Encryption_Status.config(text="SECURE STATUS: MQTT IS ENCRYPTED") 
                
                # Blink the device encryption status label in green to indicate success
                self.blink(self.device_Encryption_Status,"green")      
        else:
            # If the device owner is not registered on the blockchain, update the device status labels on the GUI accordingly
            self.device_owner_address.config(text="UNREGISTERED")
            self.device_public_key.config(text="NOT EXIST")
            self.device_Register_Status.config(text="DEVICE NOT REGISTERED WITH BLOCKCHAIN") 
            self.blink(self.device_Register_Status,"blue")
            self.blink(self.device_Encryption_Status,"blue")
        
        # Schedule the update_temperature method to run again after a delay of 1000 milliseconds (1 second)
        self.master.after(1000, self.update_temperature)

        

if __name__ == '__main__':
    # Create a new instance of the Tkinter root window
    root = tk.Tk()
    
    # Create a new instance of the TemperatureSensor class, passing in the root window as an argument
    sensor = TemperatureSensor(root)
    
    # Start the Tkinter event loop, which will keep the GUI running until the user closes the window
    root.mainloop()
