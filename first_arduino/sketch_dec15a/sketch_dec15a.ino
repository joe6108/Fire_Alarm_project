#include "DHT.h"
#define DHTPIN 2
#define DHTTYPE DHT22
#include <ArduinoJson.h>
StaticJsonDocument<200> json_doc;
char json_output[100];
DeserializationError json_error;
const char* payload_room;
const char* payload_msg;
const int buttonPin = A3;     // the number of the pushbutton pin
int buttonState = 0;
int killed_key = 0;

DHT dht(DHTPIN, DHTTYPE);

int dustPin = 0;

float dustVal = 0;

int ledPower = 5;
int delayTime = 280;
int delayTime2 = 40;
float offTime = 9680;
void setup() {
  pinMode(buttonPin, INPUT);
  Serial.begin(115200);
  dht.begin();
  pinMode(ledPower, OUTPUT);
  pinMode(dustPin, INPUT);
}

void loop() {
  buttonState = digitalRead(buttonPin);
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  if (isnan(h) || isnan(t) ) {
    Serial.println(F("感測器讀取失敗"));
    return;
  }
  //  Serial.print(F("濕度: "));
  //  Serial.print(h);
  //  Serial.print(F("% 溫度: "));
  //  Serial.print(t);
  //  Serial.println("°C");
  // ledPower is any digital pin on the arduino connected to Pin 3 on the sensor
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
  json_doc["temp"] = t;
  json_doc["humidy"] = h;
  json_doc["killed_key"] = killed_key;
  json_doc["aqi"] = aqi;
  serializeJson(json_doc, json_output);
  Serial.println( json_output );
  //Serial.println( "string to json:" );
  delay(1000);
}
