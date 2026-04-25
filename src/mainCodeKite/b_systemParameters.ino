
//=========================================MULTIKITE 17/04/2026================================================



// ======================================================================================================================================================================
// ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//==================================== SYSTEM PARAMETERS - DO NOT MODIFY ================================================================================================
// ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
// ======================================================================================================================================================================




// DO NOT MODIFY THIS FILE UNLESS YOU KNOW WHAT YOU ARE DOING



/////////////////////////////////////////////LIBRARIES/////////////////////////////////////////
#include <textparser.h>  // basic library for parsing the incoming telemm - download @ https://arduinotextparser.readthedocs.io/en/latest/
#include <string.h>
#include <String.h>
#include <Servo.h>
#include <elapsedMillis.h>  // timer, interrupt-based and non blocking, autowrapping

TextParser commaParser(",");  // Delimiter is a comma followed by a space.


////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////// PIN DEFINITION - CHECK DATASHEET AND WIRING ///////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

const int BASE_PIN = 9; // check that pin can handle PWM 
const int ESC_PIN = 10;// check that pin can handle PWM 
const int REEL_PIN = 11;// check that pin can handle PWM 




////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////// MOTOR DEFINITION  ///////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// init conditions
bool motor_armed = false;
bool motor_on = false;  // DO NOT MODIFY

bool motor_test_mode = false;  // flag for when in motor test mode
float motor_test_percentage = MOTOR_MIN_PERCENTAGE; // test percentage should start at the minimum controllable value and then increase from there via cmds

float motor_output_percentage = 0.0;  // value between 0-100% for motor control - software limits defined in userParameters.ino

Servo ESC;  // object to control esc

const int ESC_LOW_PULSE = 850;    // min pulse as per the Hobbywing datasheet
const int ESC_HIGH_PULSE = 1940;  // as per the hobbywing datasheet


const int MOTOR_FREQUENCY = 50;
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////// BASE TILT SERVO DEFINITION ///////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

const int BASE_TILT_SERVO_FREQUENCY = 50; // 50 Hz is the most standard value

Servo BASE_TILT; // object to control servo

constexpr int BASE_TILT_LOW_PULSE = 1000;                                          // in microseconds
constexpr int BASE_TILT_HIGH_PULSE = 2000;                                         // in microsecond
constexpr int BASE_TILT_STOP_PULSE = round((BASE_TILT_LOW_PULSE + BASE_TILT_HIGH_PULSE) / 2.0);  // in microseconds - midpoint of the PWM range

bool base_tilt_down = false;
bool base_tilt_up = false;
unsigned long base_tilt_burst_start_time = 0; // for timing the burst when the user sets a burst time for the base tilt movement


float base_tilt_servo_output_pulse = BASE_TILT_STOP_PULSE; // pulse for the servo control - initial value is "stopped" - in float for intermediate calculations but rounded afterwards


constexpr float BASE_TILT_SPEED_DELTA_CLAMPING = 0.3; // max allowed value that will clamp the user's set value
constexpr int BASE_BURST_TIME_MILLIS_CLAMPING = 500; // 0.5s steps max



////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////// REELING SERVO DEFINITION ///////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

const int REEL_SERVO_FREQUENCY = 50; // 50 Hz is the most standard value

Servo REEL; // object to control servo

constexpr int REEL_LOW_PULSE = 1000;                                          // in microseconds
constexpr int REEL_HIGH_PULSE = 2000;                                         // in microsecond
constexpr int REEL_STOP_PULSE = round((REEL_LOW_PULSE + REEL_HIGH_PULSE) / 2.0);  // in microseconds - midpoint of the PWM range

bool reel_in = false;
bool reel_out = false;
unsigned long reel_burst_start_time = 0; // for timing the burst when the user sets a burst time for the reeling movement


constexpr float REEL_SPEED_DELTA_CLAMPING = 0.2; // max allowed value that will clamp the user's set value
constexpr int REEL_BURST_TIME_MILLIS_CLAMPING = 500; // 0.5s steps max


////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////// TELEM DEFINITION ///////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#define TELEM Serial // define which serial is used for telemetry - if via usb, use Serial (or Serial1 if multiple Serial ports are available ie on a Mega)

String errorMessage = "NO ERRORS"; // initial error message
String returnMessage = "SUCCESS"; // initial return message

const int bufferSize = 50;  // Define the maximum length of the incoming telem packet - we expect 10 char commands
char incomingDataTelem[bufferSize]; // init char array for storing the incoming chars

