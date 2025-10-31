#include <ArduinoJson.h>

struct KeyValue {
  String sensor;
  int relay;
};

KeyValue pins[] = {
  {"A0", 13},
  {"A1", 9},
  {"A2", 10},
  {"A3", 11},
  {"A4", 12},
  {"A5", 8}
};

const int numOfPins = sizeof(pins)/sizeof(pins[0]);
bool pinsAvailability[numOfPins]; 

void setup() {
  // put your setup code here, to run once:
  for (int i = 0; i < numOfPins; i++) {
    pinMode(pins[i].relay, OUTPUT);
    pinsAvailability[i] = false;
  }

  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0) {

    String command = Serial.readStringUntil('\n');

    if (command.startsWith("FETCH_PINS")) {
      sendPins();

    } else if (command.startsWith("RESERVE_PIN:")) {
      String pin = command.substring(12);
      int pinNumber = convertPin(pin);
      reservePin(pinNumber);

    } else if (command.startsWith("RELEASE_PIN:")) {
      String pin = command.substring(12);
      int pinNumber = convertPin(pin);    
      releasePin(pinNumber);

    } else if (command.startsWith("GET_RESERVED_PINS")) {
      reservedPins();
    
    } else if (command.startsWith("READ:")) {
      String pins = command.substring(5);
      readPins(pins);
    
    } else if (command.startsWith("WATER:")) {
      String pins = command.substring(6);
      waterPins(pins);
    }

  }

}

void sendPins() {
  StaticJsonDocument<128> doc;
  JsonArray availablePins = doc.createNestedArray("available_pins");

  for (int i = 0; i < numOfPins; i++) {

    if (!pinsAvailability[i]) {
      availablePins.add(pins[i].sensor);
    }
  }

  serializeJson(doc, Serial);
  Serial.println();
}

void reservePin(int pin) {
  for (int i = 0; i < numOfPins; i++) {
    if (convertPin(pins[i].sensor) == pin) {
      pinsAvailability[i] = true;
    }
  }
}

void releasePin(int pin) {
  for (int i = 0; i < numOfPins; i++) {
    if (convertPin(pins[i].sensor) == pin) {
      pinsAvailability[i] = false;
      digitalWrite(pins[i].relay, LOW);
    }
  }
}

void reservedPins() {

  StaticJsonDocument<128> doc;
  JsonArray reservedPins = doc.createNestedArray("reserved_pins");

  for (int i = 0; i<numOfPins; i++) {
    if (pinsAvailability[i]) {
      reservedPins.add(pins[i].sensor);
    }
  }

  serializeJson(doc, Serial);
  Serial.println();
}

void readPins(String pins) {
  StaticJsonDocument<128> doc;
  StaticJsonDocument<128> result;
  deserializeJson(doc, pins);

  for (int i = 0; i < doc.size(); i++) {
    String pinName = doc[i].as<String>();
    int pin = convertPin(pinName);
    int moistureLevel = analogRead(pin);
    result[pinName] = moistureLevel;
  }

  serializeJson(result, Serial);
  Serial.println();

} 

void waterPins(String pinsToWater) {
  StaticJsonDocument<256> doc;
  deserializeJson(doc, pinsToWater);

  for (int i = 0; i < doc.size(); i++) {
    for (int j = 0; j < numOfPins; j++) {
      if (doc[i]["pins"] == pins[j].sensor) {
        digitalWrite(pins[j].relay, HIGH);
        delay(doc[i]["time"]);
        digitalWrite(pins[j].relay, LOW);
      } 
    }
  }
}

int convertPin(String pin) {
  pin.trim();
  if (pin == "A0") return A0;
  if (pin == "A1") return A1;
  if (pin == "A2") return A2;
  if (pin == "A3") return A3;
  if (pin == "A4") return A4;
  if (pin == "A5") return A5;
  return pin.toInt();
}