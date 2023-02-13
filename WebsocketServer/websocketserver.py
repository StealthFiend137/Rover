import asyncio
import json
import websockets
import paho.mqtt.client as mqtt

def calculate_wheel_speeds(data):
    return {
        "left" : 0,
        "right" : 0
    }

def generate_buggycall(data):
    deps = {
                "h" : data['h'],
                "r" : data['r'],
                "m" : data['m']
            }
    
    # we're now decoupling the heading and radians from the actual speed and direction of the buggy.
    # the new format for the buggy messages are 'l' and 'r'
    # with 'l' being the forward velocity of the left hand wheel
    # and 'r' being the forward velocity of the right hand wheel
    # so that we're further decoupling, the range is from -1 for full reverse, through 0 for stationary to 1 for full forwards.
    
    
    
    new = calculate_wheel_speeds(data)
    
    
    return {**deps, **new}

async def handle(websocket, path):
    while True:
        try:
            message = await websocket.recv()
            data = json.loads(message)
            # print(f"received: r={data['r']}, m={data['m']}, h={data['h']}")
            
            #sendData = {
            #    "h" : data['h'],
            #    "r" : data['r'],
            #    "m" : data['m']
            #}
            
            sendData = generate_buggycall(data)
            
            print(json.dumps(sendData))
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

