/*********************************************\
*    MEDIDOR DE TEMPERATURA E UMIDADE         *
*    Plataforma: ESP8266 NODEMCU ESP12E       *
*    Linguagem: C++/Arduino/HTML/JS           *
*    Autor: BMN                               *
*    06/03/23                                 *
\*********************************************/

#include <SPI.h> //for the SD card module
#include <SD.h> // for the SD card
#include <DHTesp.h> // for the DHT sensor
#include <NTPClient.h> //NTP client to get time
#include <ESP8266WiFi.h> //ESP8266 nodemcu ESP12E
#include <WiFiUdp.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>
#include <LCDIC2.h> // LCD
#include <WebSocketsServer.h>
#include <Ticker.h>

// LCD initialization..........................................................................
LCDIC2 lcd(0x27, 16, 2);

// DHT  sensor initialization..................................................................
DHTesp dht;
float t, h;

// SD card initialization......................................................................
const int chipSelect = D8; // Pin para CS
File myFile; // Create a file to store the data

// Wifi connection.............................................................................
const char *ssid     = "**********";
const char *password = "**********";

ESP8266WebServer server(80);
WebSocketsServer webSocket = WebSocketsServer(81);

// Define NTP Client to get time...............................................................
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org");

unsigned long last_time;
Ticker timer;
Ticker timer_log;

//HTML page....................................................................................
#include "pagina.h"

// Setup.......................................................................................
void setup() 
{
  //initializing Serial monitor
  Serial.begin(115200);

  //initializing WIFI
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.println("");

  while ( WiFi.status() != WL_CONNECTED ) {
    delay ( 500 );
    Serial.print ( "." );
  }
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  delay ( 10000 );

  //initializing the DHT sensor
  dht.setup(D0, DHTesp::DHT22);// which pin it's connected to; DHT 21 (AM2301)
   
  // setup for the SD card
  Serial.println(F("Initializing SD card..."));

  if(!SD.begin(chipSelect)) {
    Serial.println(F("initialization failed!"));
    return;
  }
  Serial.println(F("initialization done."));
  
  last_time = micros()/1000000; // init saving o SD every 30s
  
  // Start the web server
  server.begin();
  Serial.println("Web server started");
  
  server.on("/", handleRoot);
  server.onNotFound(handleNotFound);
  webSocket.begin();
  webSocket.onEvent(webSocketEvent);

  //initializing time client
  timeClient.begin();
  timeClient.setTimeOffset(-10800);
  
  timer.attach(10, getData); // get data every 10s
  timer_log.attach(30, logging);

  //initializing the LCD
  lcd.begin(); 
  lcd.setCursor(0,0);
  lcd.print(F("T:     C"));
  lcd.setCursor(0,1);
  lcd.print(F("U:     %"));
  
}


// Log Temp and Time...........................................................................
void logging() 
{
  // Reading temperature or humidity takes about 250 milliseconds!
  // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
  // Read temperature as Celsius
  t = dht.getTemperature();
  h = dht.getHumidity();
  
  // Check if any reads failed and exit early (to try again).
  if  (isnan(h) || isnan(t)) {
    lcd.setCursor(2,0);
    lcd.print(F("ERR "));
    Serial.println(F("sensor error"));
    delay(1000);
    return;
  }

  timeClient.update();
  timeClient.setTimeOffset(-10800);
  time_t epochTime = timeClient.getEpochTime();
  struct tm *ptm = gmtime ((time_t *)&epochTime); 
  int monthDay = ptm->tm_mday;
  int currentMonth = ptm->tm_mon+1;
  int currentYear = ptm->tm_year+1900;
  String currentDate = String(currentYear) + "-" + String(currentMonth)+ "-" + String(monthDay) ;
  
  String formattedTime = timeClient.getFormattedTime();

  // update filename
  String savefile = currentDate + ".txt"; // add date with .txt

  // save on SD every 30s
  
  if  ( epochTime - last_time > 30 ) {
    
    myFile = SD.open(savefile, FILE_WRITE);
    if (!myFile) {
      lcd.setCursor(9,0);
      lcd.print(F("ERROR"));
      Serial.println(F("Error opening file"));
    }
    if (myFile) {
      Serial.println(F("open with success"));
      myFile.print(currentDate);
      myFile.print(F(","));
      myFile.print(formattedTime);
      myFile.print(F(","));
      myFile.print(t);
      myFile.print(F(","));
      myFile.println(h);
    
      myFile.close();

      lcd.setCursor(9,0);
      lcd.print(F("SAVED"));
      Serial.println(F("data saved"));
    }

    last_time = epochTime;
  }

  
  Serial.print(currentDate);
  Serial.print(F(","));
  Serial.print(formattedTime);
  Serial.print(F(","));
  Serial.print(t);
  Serial.print(F("°C,"));
  Serial.print(h);
  Serial.println(F("%"));
  

  lcd.setCursor(9,1);
  lcd.print(formattedTime);
  lcd.setCursor(2,0);
  lcd.print(String(t));
  lcd.setCursor(2,1);
  lcd.print(String(h));
}


// HTML Page...................................................................................
void handleRoot() 
{
  timeClient.update();
  timeClient.setTimeOffset(-10800);
  time_t epochTime = timeClient.getEpochTime();
  struct tm *ptm = gmtime ((time_t *)&epochTime); 
  int monthDay = ptm->tm_mday;
  int currentMonth = ptm->tm_mon+1;
  int currentYear = ptm->tm_year+1900;
  String currentDate = String(currentYear) + "-" + String(currentMonth)+ "-" + String(monthDay) ;
  String formattedTime = timeClient.getFormattedTime();

  String page;
  page += pagina;
  page += dia;
  page += currentDate;
  page += hora;
  page += formattedTime;
  page += tempera;
  page += t;
  page += umida;
  page += h;
  page += grafi;
  page += rodape;
  
  server.send(200, "text/html", page);
}

void handleNotFound() {
  String message = "File Not Found\n\n";
  message += "URI: ";
  message += server.uri();
  message += "\nMethod: ";
  message += (server.method() == HTTP_GET) ? "GET" : "POST";
  message += "\nArguments: ";
  message += server.args();
  message += "\n";
  for (uint8_t i = 0; i < server.args(); i++) { message += " " + server.argName(i) + ": " + server.arg(i) + "\n"; }
  server.send(404, "text/plain", message);
}

void getData(){
  String json = "{\"value\":";
  json += dht.getTemperature();
  json += "}";
  webSocket.broadcastTXT(json.c_str(), json.length());
}



// Loop measurements..........................................................................
void loop() {

  logging();
  webSocket.loop();
  server.handleClient();
  
}

void webSocketEvent(uint8_t num, WStype_t type, uint8_t * payload, size_t length){
  
}
