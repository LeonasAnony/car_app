#include <WiFi.h>
#include "MD5.h"               // Zur Berechnung des unsigned long MD5 Hashes
#include "Secret.h"

#define SERVER_PORT 4711      // Portnummer 
#define MAX_BUFFER_SIZE 1024  // Maximale Anzahl der Socket Input Chars
#define MAX_VALUE_SIZE 14     // Maximale Anzahl des Namens
#define TICK_TIME 1000        // Time between ticks
#define LED_PIN 4             // GPIO 4 for LED Output
#define SWITCH_PIN 16         // GPIO 16 for Switch Input
#define OFF LOW               
#define ON HIGH

#define HASH_INFO         2090370257  // hash of info
#define HASH_HELP         2090324718  // hash of help
#define HASH_EXIT         2090237503  // hash of exit
#define HASH_SET          193505681   // hash of set
#define HASH_GET          193492613   // hash of get
#define HASH_VALUE        277698370   // hash of value
#define HASH_LED          193498042   // hash of led
#define HASH_ON           5863682     // hash of on
#define HASH_OFF          193501344   // hash of off
#define HASH_SWITCH       482686839   // hash switch
#define HASH_TICK         2090760016  // hash tick

const char* WLAN_SSID                     = __SSID__;
const char* WPA2_PASSWORD                 = __WPA2_PHRASE__;
const char* INFO_TITLE                    = "TCP DATA DAEMON";
const char* INFO_VALUE                    = "value: ";
const char* INFO_IP                       = "ip:   ";
const char* INFO_GW                       = "gw:   ";
const char* INFO_NM                       = "mask: ";
const char* INFO_DHCP                     = " (DHCP)";
const char* INFO_MAC                      = "mac:  ";
const char* INFO_FUNCT_OK                 = "ok";
const char* INFO_PROMPT                   = "-> ";
const char* INFO_CONNECTING               = "Connecting to WiFi SSID: ";
const char* UNDEFINED_NAME                = "undefined";
const char* EXCEPTION_BUFFER_TO_SMALL     = "exception: buffer tp small";
const char* EXCEPTION_UNKNOWN_COMMAND     = "exception: unknown command";
const char* EXCEPTION_UNKNOWN_KEY         = "exception: unknown key";
const char* EXCEPTION_MISSING_KEY         = "exception: missing key";
const char* EXCEPTION_NO_VALUE_SPECIFIED  = "exception: no value specified";
const char* EXCEPTION_VALUE_TO_LONG       = "exception: value to long";

WiFiServer server(SERVER_PORT);
WiFiClient client;

unsigned long lastTick;
unsigned long tickCounter;

char value[MAX_VALUE_SIZE];
char buffer[MAX_BUFFER_SIZE];
char charBuffer[MAX_BUFFER_SIZE];

bool externalSwitch = 0;
bool useTick = false;

bool connected = false;
int loop_counter = 0;

void clearRecvBuffer(WiFiClient __client) {
  while (__client.connected() && __client.available()) {
    byte recv_byte = __client.read();
  }
}

const unsigned long hash(const char *str) {
  unsigned long hash = 5381;
  int c;
  while ((c = *str++))
    hash = ((hash << 5) + hash) + c;
  return hash;
}

void setup() {
  pinMode(SWITCH_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);

  externalSwitch = digitalRead(SWITCH_PIN);
  digitalWrite(LED_PIN,OFF);
  
  lastTick = millis();

  Serial.begin(115200);
  WiFi.begin(WLAN_SSID, WPA2_PASSWORD);

  Serial.println();
  Serial.println(INFO_TITLE);
  
  server.begin();

  Serial.print(INFO_CONNECTING);
  Serial.println(WLAN_SSID);

  byte counter = 0;
  while (WiFi.status() != WL_CONNECTED) {
    delay(75);

    char selectedChar = '-';
    if (counter % 4 == 0) selectedChar = '\\';
    if (counter % 4 == 1) selectedChar = '|';
    if (counter % 4 == 2) selectedChar = '/';
    Serial.print(selectedChar);
    Serial.print("\r");
    counter++;
  }

  Serial.println("Connected:");
  Serial.print(INFO_MAC);
  Serial.println(WiFi.macAddress());
  Serial.print(INFO_IP);
  Serial.print(WiFi.localIP().toString().c_str());
  Serial.print(" ");
  Serial.print(SERVER_PORT);
  Serial.println(INFO_DHCP);

  Serial.print(INFO_NM);
  Serial.print(WiFi.subnetMask());
  Serial.println(INFO_DHCP);

  Serial.print(INFO_GW);
  Serial.print(WiFi.gatewayIP());
  Serial.println(INFO_DHCP);
}

void loop() {
 if (!connected) {
    client = server.available();
    if (client) {
      Serial.print("<INFO> New incoming socket request");
      if (client.connected()) {
        Serial.println(" managed succesfully: ACCEPTED");
        connected = true;
        client.println(INFO_TITLE);
        client.println(INFO_FUNCT_OK);
        client.print(INFO_PROMPT);
        clearRecvBuffer(client);
      } else {
        Serial.println(" managed errorsly: REJECTED");
        client.stop();
      }
    } 
  } else {

    WiFiClient checkClient = server.available();
    if ((checkClient.fd() != -1) && checkClient.fd() != client.fd()) {
      Serial.println("Exception: Only one socket connection is permitted.");
      checkClient.stop();
    } else {
      if (client.connected()) {
        if ((useTick) && (lastTick + TICK_TIME) < millis()) {
          lastTick = millis();
          sprintf(charBuffer,"<TICK>%u</TICK>",tickCounter);
          client.println(charBuffer);
          tickCounter++;
        }
        if (externalSwitch != digitalRead(SWITCH_PIN)) {
          if (digitalRead(SWITCH_PIN)) {
            client.println("<EVENT><KEY>switch</KEY><VALUE>on</VALUE></EVENT>");
          } else {
            client.println("<EVENT><KEY>switch</KEY><VALUE>off</VALUE></EVENT>");
          }
          externalSwitch = digitalRead(SWITCH_PIN);
        }
        if (client.available()) {
          char recv_char = client.read();
          int bufferUsedLength = strlen(buffer);
          if (bufferUsedLength < MAX_BUFFER_SIZE) {
            if (recv_char == '\n') {
              char *ptrCmd = NULL;
              char *ptrKey = NULL;
              char *ptrValue = NULL;
              int  index = 0;
              byte cntSpace = 0;
              ptrCmd = buffer;
              while (index < bufferUsedLength) {
                if ((buffer[index] == 32) && (cntSpace < 2)) {
                  buffer[index] = 0;
                  cntSpace++;
                  if (ptrKey == NULL) {
                    ptrKey = &buffer[index + 1];
                  } else if (ptrValue == NULL) {
                    ptrValue = &buffer[index + 1];
                  }
                }
                index++;
              }
              switch (hash(ptrCmd)) {
                case HASH_HELP:
                  Serial.println("<INFO> Execute command HELP");
                  client.println("exit - close connection");
                  client.println("help - show command list");
                  client.println("info - show systems vars");
                  client.println("set  - set value <value>    | note: memory");
                  client.println("set  - set led (on | off)   | note: gpio 4");
                  client.println("set  - set tick (on | off)");
                  client.println("get  - get value (memory)   | note: memory");
                  client.println("get  - get led              | note: gpio 4");
                  client.println("get  - get switch           | note: gpio 16");
                  client.println(INFO_FUNCT_OK);
                  break;
                case HASH_EXIT:
                  Serial.println("<INFO> Execute command EXIT");
                  client.println("bye bye");
                  client.stop();
                  break;
                case HASH_SET:
                  Serial.print("<INFO> Execute command SET ");
                  if (ptrKey != NULL) {
                    if (hash(ptrKey) == HASH_TICK) {
                      Serial.print("TICK ");
                      if (hash(ptrValue) == HASH_ON) {
                        Serial.println("ON");
                        useTick = true;
                        client.println(ptrValue);
                        client.println(INFO_FUNCT_OK);
                      } else if (hash(ptrValue) == HASH_OFF) {
                        Serial.println("OFF");
                        useTick = false;
                        client.println(ptrValue);
                        client.println(INFO_FUNCT_OK);
                      } else {
                        Serial.println(EXCEPTION_UNKNOWN_KEY);
                        client.println(EXCEPTION_UNKNOWN_KEY);
                      }
                    } else if (hash(ptrKey) == HASH_LED) {
                      Serial.print("LED ");
                      if (hash(ptrValue) == HASH_ON) {
                        Serial.println("ON");
                        digitalWrite(LED_PIN,ON);
                        client.println(ptrValue);
                        client.println(INFO_FUNCT_OK);
                        client.println("<EVENT><KEY>led</KEY><VALUE>on</VALUE></EVENT>");
                      } else if (hash(ptrValue) == HASH_OFF) {
                        Serial.println("OFF");
                        digitalWrite(LED_PIN,OFF);
                        client.println(ptrValue);
                        client.println(INFO_FUNCT_OK);
                        client.println("<EVENT><KEY>led</KEY><VALUE>off</VALUE></EVENT>");
                      } else {
                        Serial.println(EXCEPTION_UNKNOWN_KEY);
                        client.println(EXCEPTION_UNKNOWN_KEY);
                      }
                    } else if (hash(ptrKey) == HASH_VALUE) {
                      Serial.print("VALUE ");
                      if (strlen(ptrValue) < MAX_VALUE_SIZE) {
                        Serial.println(ptrValue);
                        memcpy(value, ptrValue, strlen(ptrValue));
                        value[strlen(ptrValue)] = '\0';
                        client.println(ptrValue);
                        client.println(INFO_FUNCT_OK);
                        client.print("<EVENT><KEY>Value</KEY><VALUE>");
                        client.print(value);
                        client.println("</VALUE></EVENT>");
                        Serial.print("<EVENT><KEY>Value</KEY><VALUE>");
                        Serial.print(value);
                        Serial.println("</VALUE></EVENT>");
                      } else {
                        Serial.println(EXCEPTION_VALUE_TO_LONG);
                        client.println(EXCEPTION_VALUE_TO_LONG);
                      }
                    } else { 
                      Serial.println(EXCEPTION_UNKNOWN_KEY);
                      client.println(EXCEPTION_UNKNOWN_KEY);
                    }
                  } else {
                    Serial.println(EXCEPTION_MISSING_KEY);
                    client.println(EXCEPTION_MISSING_KEY);
                  }
                  break;
                case HASH_GET:
                  Serial.print("<INFO> Execute command GET ");
                  if (ptrKey != NULL) {
                    if (hash(ptrKey) == HASH_LED) {
                      Serial.print("LED ");
                      if (digitalRead(LED_PIN)) {
                        Serial.println("ON");
                        client.println("on");
                      } else {
                        Serial.println("OFF");
                        client.println("off");
                      }
                      client.println(INFO_FUNCT_OK);
                    } else if (hash(ptrKey) == HASH_SWITCH) {
                      Serial.print("SWITCH ");
                      if (externalSwitch) {
                        Serial.println("ON");
                        client.println("on");
                      } else {
                        Serial.println("OFF");
                        client.println("off");
                      }
                      client.println(INFO_FUNCT_OK);
                    } else if (hash(ptrKey) == HASH_VALUE) {
                      Serial.print("VALUE ");
                      Serial.println(value);
                      client.println(value);
                      client.println(INFO_FUNCT_OK);
                    } else { 
                      Serial.println(EXCEPTION_UNKNOWN_KEY);
                      client.println(EXCEPTION_UNKNOWN_KEY);
                    }
                  } else {
                    Serial.println(EXCEPTION_UNKNOWN_KEY);
                    client.println(EXCEPTION_MISSING_KEY);
                  }
                  break;
                case HASH_INFO:
                  Serial.println("<INFO> Execute command INFO");
                  snprintf(buffer, MAX_BUFFER_SIZE, "local ip: %s:%i", client.localIP().toString().c_str(), client.localPort());
                  client.println(buffer);
                  snprintf(buffer, MAX_BUFFER_SIZE, "remote ip: %s:%i", client.remoteIP().toString().c_str(), client.remotePort());
                  client.println(buffer);
                  snprintf(buffer, MAX_BUFFER_SIZE, "%s %s", INFO_VALUE, value);
                  client.println(buffer);
                  if (digitalRead(LED_PIN)) {
                    snprintf(buffer, MAX_BUFFER_SIZE, "led: on");
                    client.println(buffer);
                  } else {
                    snprintf(buffer, MAX_BUFFER_SIZE, "led: off");
                    client.println(buffer);
                  }
                  if (digitalRead(SWITCH_PIN)) {
                    snprintf(buffer, MAX_BUFFER_SIZE, "switch: on");
                    client.println(buffer);
                  } else {
                    snprintf(buffer, MAX_BUFFER_SIZE, "switch: off");
                    client.println(buffer);
                  }
                  client.println(INFO_FUNCT_OK);
                  break;
                default:
                  client.println(EXCEPTION_UNKNOWN_COMMAND);
              }
              buffer[0] = 0;
              client.print(INFO_PROMPT);
            } else if ((((byte) recv_char) >= 32) && (((byte) recv_char) <= 126)) {
              buffer[bufferUsedLength] = recv_char;
              buffer[bufferUsedLength + 1] = 0;
            }
          } else {
            client.println(EXCEPTION_BUFFER_TO_SMALL);
            clearRecvBuffer(client);
            buffer[0] = 0;
            client.print(INFO_PROMPT);
          }
        }
      } else {
        Serial.println("<INFO> Connection interruption detected, CLOSE CONNECTION");
        client.stop();
        connected = false;
      }
    }
  }
}
