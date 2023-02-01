import asyncio
import json
import websockets
import paho.mqtt.client as mqtt

async def handle(websocket, path):
    while True:
        try:
            message = await websocket.recv()
            data = json.loads(message)
            print(f"received: x={data['r']}, y={data['m']}, h={data['h']}")
            
            sendData = {
                "h" : data['h']
            }
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

