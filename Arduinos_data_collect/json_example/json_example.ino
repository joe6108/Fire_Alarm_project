#include <ArduinoJson.h>
StaticJsonDocument<200> json_doc;
char json_output[100];
DeserializationError json_error;
const char* payload_room;
const char* payload_msg;
const int buttonPin = 13;     // the number of the pushbutton pin
int buttonState = 0;
int killed_key = 0;
void setup() {
  pinMode(buttonPin, INPUT);
  Serial.begin(115200);
}

void loop() {
  buttonState = digitalRead(buttonPin);
  if (buttonState == HIGH) {
    killed_key = 1;
  }
  json_doc["temp"] = 18;
  json_doc["humidy"] = 20;
  json_doc["outputV"] = 30;
  json_doc["ugm3"] = 30;
  json_doc["aqi"] = 30;
  json_doc["killed_key"] = killed_key;
  serializeJson(json_doc, json_output);
  //Serial.println( "string to json:" );
  Serial.println( json_output );
  delay(1000);
}
