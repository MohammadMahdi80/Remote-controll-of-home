#include <ESP8266WiFi.h>
#include "ThingSpeak.h"


const char* ssid = "norozi";   // your network SSID (name) 
const char* password = "qwedsazxc";   // your network password

WiFiClient  client;

unsigned long myChannelNumber = 1;
const char * myWriteAPIKey = "6D2G6KX0C85J75O9";

// Timer variables
unsigned long lastTime = 0;
unsigned long timerDelay = 3000;

int data = 0;
int statusCode;
int pinNumber = 2;

void setup() {
  Serial.begin(500000);  //Initialize serial
  
  WiFi.mode(WIFI_STA);   
  
  ThingSpeak.begin(client);  // Initialize ThingSpeak

  pinMode(pinNumber, OUTPUT);
  digitalWrite(pinNumber, LOW);
}

void loop() {
  // if ((millis() - lastTime) > timerDelay) {
    
    // Connect or reconnect to WiFi
    if(WiFi.status() != WL_CONNECTED){
      Serial.print("Attempting to connect");
      while(WiFi.status() != WL_CONNECTED){
        WiFi.begin(ssid, password); 
        delay(5000);     
      } 
      Serial.println("\nConnected.");
    }
    
    // Write to ThingSpeak. There are up to 8 fields in a channel, allowing you to store up to 8 different
    // pieces of information in a channel.  Here, we write to field 1.
    // ThingSpeak.writeField(myChannelNumber, 1, 0x7fffffff, myWriteAPIKey); 

  ////////////////// for connection to telegram bot/////////////////////////////////////
  //   long data = ThingSpeak.readLongField(1825423, 1, "S4UIM4O8ZWOXQ2A8");
  //   statusCode = ThingSpeak.getLastReadStatus();
  // if (statusCode == 200)
  // {
  //   if(data == 1) {digitalWrite(pinNumber, HIGH);Serial.println(data);}
  //   else if(data == 0) {digitalWrite(pinNumber, LOW);Serial.println(data);}
  // }
  /////////////////////////////////// END ////////////////////////////////////////

  
  

  // delay(15000);

    
    // if(x == 200){
    //   Serial.println("Channel update successful.");
    // }
    // else{
    //   Serial.println("Problem updating channel. HTTP error code " + String(x));
    // }
    // lastTime = millis();
  // }
}