#include <Arduino.h>
#include <PubSubClient.h>
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <secrets/wifi.h>
#include <secrets/mqtt.h>
#include <ArduinoJson.h>

const char* ssid = WIFI_SSID;
const char* password = WIFI_PASSWORD;

const char* mqttServer = MQTT_SERVER;
const int mqttPort = MQTT_PORT;
const char* mqttUser = MQTT_USER;
const char* mqttPassword = MQTT_PASSWORD;
const char* topic = MQTT_TOPIC;

WiFiClient espClient;
PubSubClient client(espClient);

int ledPin = LED_BUILTIN;

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

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
  //int state = message[0] - '0';
  //digitalWrite(ledPin, state);
  
  Serial.println("Message Received:");
  Serial.write(message, length);
  Serial.println();
  
  StaticJsonDocument<200> doc;
  DeserializationError error = deserializeJson(doc, message);

  if (error) {
    Serial.println("Deserialization failed");
    return;
  }

  if(doc["h"])
  {
    //tone(D2, 300, 500);
    tone(D2, 300);
  }
  else
  {
    noTone(D2);
  }
  
}

void setup() {
  Serial.begin(115200);
  pinMode(ledPin, OUTPUT);
  setup_wifi();
  client.setServer(mqttServer, mqttPort);
  client.setCallback(callback);
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP8266Client", mqttUser, mqttPassword)) {
      Serial.println("connected");
      client.subscribe(topic);
      
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

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
}
