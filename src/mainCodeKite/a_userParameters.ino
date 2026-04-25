// ================================================ THERE IS A PARAMETER SANITY CHECK BUT USERS SHOULD TRIPLECHECK THESE VALUES ===================================

// ======================================================================================================================================================================
// ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//==================================== USER PARAMETERS ================================================================================================
// ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
// ======================================================================================================================================================================

constexpr int TELEMETRY_FREQUENCY = 10; // in Hz, 10 is enough - can be increased but baudrate should be scaled accordingly (to packet size as well - n chars * Hz)
constexpr unsigned long TELEM_BAUDRATE = 57600; // possible values for ex: 9600,14400,19200,28800,38400,57600,115200,230400 - MUST MATCH SERIAL STUDIO

////////////////////////////////////////////======== MOTOR LIMITS =============/////////////////////////////////////////
constexpr float MOTOR_MAX_PERCENTAGE = 50.0; //%
constexpr float MOTOR_MIN_PERCENTAGE = 8.0; // % value

///////////////////////////////======== SPEED LIMITS  FOR REEL IN =============/////////////////////////////////////////
constexpr float REEL_SPEED_DELTA_PERCENTAGE_REEL_IN = 0.05;
constexpr float REEL_SPEED_DELTA_PERCENTAGE_REEL_OUT = 0.05; // this must be a positive value
constexpr int REEL_BURST_TIME_MILLIS = 300; //SEC

///////////////////////////////======== SPEED LIMITS  FOR REEL IN =============/////////////////////////////////////////
constexpr float BASE_TILT_SPEED_DELTA_PERCENTAGE_POSITIVE_TILT = 0.1;
constexpr float BASE_TILT_SPEED_DELTA_PERCENTAGE_NEGATIVE_TILT = 0.1; // this must be a positive value
constexpr int BASE_TILT_BURST_TIME_MILLIS = 200;

