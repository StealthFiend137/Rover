#include <Arduino.h>
#include <PubSubClient.h>
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <secrets/wifi.h>
#include <secrets/mqtt.h>
#include <ArduinoJson.h>
#include "handlers/HornMessageHandler.cpp"
#include "handlers/MovementMessageHandler.cpp"

#define HORNPIN = D2;

WiFiClient espClient;
PubSubClient client(espClient);

MessageHandlers::HornMessageHandler hornHandler = MessageHandlers::HornMessageHandler(D2);
MessageHandlers::MovementMessageHandler movementHandler = MessageHandlers::MovementMessageHandler(D5, D6, D3, D7, D8, D4);

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(WIFI_SSID);

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* message, unsigned int length) {
  StaticJsonDocument<200> doc;
  DeserializationError error = deserializeJson(doc, message);

  if (error) {
    Serial.println("Deserialization failed");
    return;
  }

  // Get the appropriate handlers for this message, and action them.
  hornHandler.handle(doc);
  movementHandler.handle(doc);
}

void setup() {
  Serial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT);
  
  setup_wifi();
  client.setServer(MQTT_SERVER, MQTT_PORT);
  client.setCallback(callback);
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP8266Client", MQTT_USER, MQTT_PASSWORD)) {
      Serial.println("connected");
      client.subscribe(MQTT_TOPIC);
      
      tone(D2, 500, 200);
      delay(200);
      tone(D2, 1200, 200);
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void mqttHandler()
{
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
}

void loop() {
  mqttHandler();
}
