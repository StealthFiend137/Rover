import asyncio
import json
import websockets
import paho.mqtt.client as mqtt
import math


def get_square_magnitude(theta):
    adjacent_length = 1
    if (abs(theta) < (math.pi / 4)) or (abs(theta) > (math.pi -(math.pi /4))):
        return abs(adjacent_length / math.cos(theta))
    return abs(adjacent_length / math.sin(theta))


def map_number(lowest, highest, point):
    return (1 - point) * lowest + point * highest


def get_normalised_joystick_position(theta, magnitude):
    square_magnitude = get_square_magnitude(theta)           
    normalised_magnitude = map_number(0, square_magnitude, magnitude)
    
    x = math.cos(theta) * normalised_magnitude
    y = math.sin(theta) * normalised_magnitude
    
    y /= 2
    
    return x, y


def calculate_wheel_speeds(data):
    
    angle = data['r']
    magnitude = data['m']
    x, y = get_normalised_joystick_position(angle, magnitude)
    
    max_speed = 255
    left_speed = (y * max_speed + x * max_speed)
    right_speed = -(y * max_speed - x * max_speed)

    left_speed = max(min(left_speed, max_speed), -max_speed)
    right_speed = max(min(right_speed, max_speed), -max_speed)
    
    print(left_speed, right_speed)
        
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
