#include "Streaming.h"
const uint8_t SensorPin = A6; 

void setup()
{
    Serial.begin(115200);
    pinMode(SensorPin,INPUT);
}

void loop()
{
    static int count = 0;
    uint16_t sensor_raw = analogRead(SensorPin);
    Serial << count << " " << sensor_raw << endl; 
    delay(10);
    count++;
}
