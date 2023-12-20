#include <SimpleDHT.h>
#include <ArduinoJson.h>
StaticJsonDocument<200> json_doc;
char json_output[100];
DeserializationError json_error;
const char* payload_room;
const char* payload_msg;
const int buttonPin = A3;     // the number of the pushbutton pin
int buttonState = 0;
int killed_key = 0;
int pinDHT11 = 2;
SimpleDHT11 dht11;

int dustPin = 0;

float dustVal = 0;

int ledPower = 5;
int delayTime = 280;
int delayTime2 = 40;
float offTime = 9680;
void setup() {
  pinMode(buttonPin, INPUT);
  Serial.begin(115200);
  pinMode(ledPower, OUTPUT);
  pinMode(dustPin, INPUT);
}

void loop() {
  buttonState = digitalRead(buttonPin);
  byte temperature = 0;
  byte humidity = 0;
  int err = SimpleDHTErrSuccess;
  // start working...
  if ((err = dht11.read(pinDHT11, &temperature, &humidity, NULL)) != SimpleDHTErrSuccess) {
    Serial.print("Read DHT11 failed, err="); Serial.println(err); delay(1000);
    return;
  }
  digitalWrite(ledPower, LOW);
  delayMicroseconds(delayTime);
  dustVal = analogRead(dustPin);
  delayMicroseconds(delayTime2);
  digitalWrite(ledPower, HIGH);
  delayMicroseconds(offTime);
  float aqi = 0;
  if (dustVal > 36.455)
    aqi = (float(dustVal / 1024) - 0.0356) * 120000 * 0.035;
  if (buttonState == HIGH) {
    killed_key = 1;
  }
  json_doc["temp"] = temperature;
  json_doc["humidy"] = humidity;
  json_doc["killed_key"] = killed_key;
  json_doc["aqi"] = aqi;
  serializeJson(json_doc, json_output);
  Serial.println( json_output );
  //Serial.println( "string to json:" );
  delay(1000);
}
