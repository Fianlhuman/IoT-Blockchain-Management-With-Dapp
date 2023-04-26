# The following code block is used to establish a connection to an MQTT broker and publish messages to a specified topic.

# Import the `paho.mqtt.client` module to enable communication with the MQTT broker
import paho.mqtt.client as mqtt

# Import the `time` module to enable delay between message publications
import time

# Set the address of the MQTT broker to connect to
broker_address = "broker.emqx.io"

# Define a callback function to handle successful connection to the broker
def on_connect(client, userdata, flags, rc):
    # If the connection is successful, print a message indicating success
    if rc == 0:
        print("Connected to broker")
    # If the connection is not successful, print a message indicating failure
    else:
        print("Connection failed")

# Define a callback function to handle disconnection from the broker
def on_disconnect(client, userdata, rc):
    # Print a message indicating disconnection from the broker
    print("Disconnected from broker. Trying to reconnect...")
    
    # Attempt to reconnect to the broker indefinitely until reconnection is successful
    while True:
        try:
            client.reconnect()
            break
        # If reconnection fails, print a message indicating failure and retry after a delay of 5 seconds
        except:
            print("Failed to reconnect. Retrying in 5 seconds...")
            time.sleep(5)

# Instantiate an `mqtt.Client()` object to represent the MQTT client
client = mqtt.Client()

# Set the callback functions for connection and disconnection events
client.on_connect = on_connect
client.on_disconnect = on_disconnect

# Connect to the MQTT broker at the specified address and port
client.connect(broker_address, port)

# Set the topic and message to publish
topic = "0x37fd669195cfe32ff55e6ff7ca6084eae66abcd7"
message = "hello"

# Publish the message to the specified topic repeatedly with a delay of 1 second between publications
while True:
    try:
        client.publish(topic, message)
        print("Message published:", message)
        time.sleep(1)
    # If publishing the message fails, print a message indicating failure and retry after a delay of 5 seconds
    except:
        print("Failed to publish message. Retrying in 5 seconds...")
        time.sleep(5)