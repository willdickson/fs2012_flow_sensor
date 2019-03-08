#include "Streaming.h"

const uint8_t NumSensor = 2;
const uint8_t SensorPins[NumSensor] = {A5, A6}; 

void setup()
{
    Serial.begin(115200);
    for (int i=0; i<NumSensor; i++) 
    {
        pinMode(SensorPins[i],INPUT);
    }
}

void loop()
{
    static unsigned long t_start = millis();
    unsigned long dt = millis() - t_start;
    Serial << dt; 
    for (int i=0; i<NumSensor; i++) 
    {
        uint16_t sensor_raw = analogRead(SensorPins[i]);
        Serial << " " << sensor_raw; 
    }
    Serial << endl;
    delay(10);
}
