
//================================MULTIKITE 17/04/2026================================================



/////////////////////////////////////////////LIBRARIES/////////////////////////////////////////
#include <Wire.h>
#include <textparser.h> 
#include <string.h>
#include <String.h>
#include <Servo.h>
#include <SPI.h>       // Include SPI library (needed for SD card)
#include <elapsedMillis.h>




TextParser commaParser(",");  // Delimiter is a comma followed by a space.

#define TELEM Serial


bool START_SYSTEM = true;

int TELEMETRYFREQUENCY = 10;

const float FREQUENCYCHECK = 0.1;
unsigned int CLKCOUNTER = 0;
unsigned long timeClck = 0;

bool flightMode = false;
bool landingNow = false;
bool takeOff = false;
bool takeOffCommand = false;
bool timeFlag = false;
bool spoolMotor = false;
bool landingFlag  = false;

bool FLAGMOTOR = false; bool MOTORARMED = false; bool MOTORON = false;

bool MOTORTEST = false;
bool SERVOTEST = false; // false = normal activity, true means 0º

elapsedMillis  rampLandingTime = 0;
elapsedMillis timerFlight;
elapsedMillis timerSpoolMotor;

String errorMessage = "NO ERRORS";
String returnMessage = "SUCCESS";

////////////////////////////////////// PIN DEFINITION ///////////////////////////////////////////////////////
const int internal_LED_BUZZER = 13;   // =35;
const int LEDLR = 26; const int LEDLG = 25;  const int LEDLB = 24;
const int servoX1 = 2; const int servoX2 = 3; const int servoY1 = 4; const int servoY2 = 5;
const int motorCtrlPin = 16;

float percentageMotor = 0;


int ki = 0; // blender stuff

/////////////////////////////////// FLIGHT STUFF ////////////////////////////////////////
float TAKEOFFALTITUDE = 0.75;
float LANDINGSPEED = 0.21;



const int bufferSize = 80;  // Define the maximum length of the input string
//char incomingDataJavad[bufferSize];
char incomingDataTelem[bufferSize];


bool PLOTMODE = false;

/////////////////////////////////////////////TVC MOUNT/////////////////////////////////////////

float EWMA_PID_ORIENTATION_SERVO = 0.33;


////////////////////////////////////////////====================SETUP BEGIN====================/////////////////////////////////////////
float MOTORMAX =80; //%
float MOTORMIN =50;
float MOTORSTARTUP = 50;


int motorTestLaunch = 0;
unsigned long timeServo = 0;
float verticalTol= 0.05;


int PLTRATE = 25;
Servo ESC;
const int ESCPIN = 3;
const int MIN_ANGLE = 0;
const int MAX_ANGLE = 180;
const int MIN_PULSE = 1000; // in microseconds
const int MAX_PULSE = 2000; // in microseconds
/////////////////////////////////////////////DEFINITIONS/////////////////////////////////////////

const int ESCLOWPOINT = 1100;
const int ESCHIGHPOINT = 1940; // as per the hobbywing datasheet

const int SERVOFREQUENCY = 50;



const int BUFFERMESSAGESIZE = 128;
const int SYNCHMESSAGELENGHT = 2; // 2 CHARS for header is standard
const int SIZEOFLENGTH = 3; // 3 chars for hex
byte messageData[BUFFERMESSAGESIZE]; // stores bytes of the body
