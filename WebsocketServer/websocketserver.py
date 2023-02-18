import asyncio
import json
import websockets
import paho.mqtt.client as mqtt
import math


def get_square_magnitude(theta):
    adjacent_length = 1
    if (abs(theta) < (math.pi / 4)) or (abs(theta) > (math.pi -(math.pi /4))):
        return adjacent_length / math.cos(theta)
    return adjacent_length / math.sin(theta)

def x_and_y_from_theta_and_magnitude(theta, magnitude):

    x = math.cos(theta) 
    y = math.sin(theta) 
        
    square_magnitude = get_square_magnitude(theta)       
    
    
    print(magnitude, square_magnitude)
    
    return x, y

def calculate_wheel_speeds(data):
    
    angle = data['r']
    magnitude = data['m']
    x, y = x_and_y_from_theta_and_magnitude(angle, magnitude)
    
    

    left_speed = 0
    right_speed = 0

    return {
        "l" : int(left_speed ),
        "r" : int(right_speed )
    }

def generate_buggycall(data):
    anciliary = {
        "h" : data['h']
    }
    movement = calculate_wheel_speeds(data)
    return {**anciliary, **movement}

async def handle(websocket, path):
    while True:
        try:
            message = await websocket.recv()
            data = json.loads(message)
            
            sendData = generate_buggycall(data)
            
            # print(json.dumps(sendData))
            client.publish("buggy", json.dumps(sendData))

        except websockets.exceptions.ConnectionClosed:
            print("Client disconnected")
            break
        
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # client.subscribe("topic")

def on_disconnect(client, userdata, rc):
    print("disconnected")

listen_address = "0.0.0.0"
listen_port = 8765
start_server = websockets.serve(handle, listen_address, listen_port)
print("\nMovement support version\n")
print(f"Listening for websocket traffic on: {listen_address}:{listen_port}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
#client.on_message = on_message
client.connect("192.168.0.2", 1883, 60)
client.loop_start()

# client.loop_forever()

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

