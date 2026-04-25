

// ======================================================================================================================================================================
// ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//==================================== USER PARAMETERS CHECK - **DO NOT** MODIFY ================================================================================================
// ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
// ======================================================================================================================================================================


// ---- Telemetry frequency ----
static_assert(TELEMETRY_FREQUENCY > 0, "TELEMETRY_FREQUENCY must be > 0");
static_assert(TELEMETRY_FREQUENCY <= 100, "TELEMETRY_FREQUENCY too high");

// ---- Baudrate whitelist ----
constexpr bool validBaud =
  TELEM_BAUDRATE == 9600 || TELEM_BAUDRATE == 14400 || TELEM_BAUDRATE == 19200 || TELEM_BAUDRATE == 28800 || TELEM_BAUDRATE == 38400 || TELEM_BAUDRATE == 57600 || TELEM_BAUDRATE == 115200 || TELEM_BAUDRATE == 230400 || TELEM_BAUDRATE == 250000 || TELEM_BAUDRATE == 460800 || TELEM_BAUDRATE == 921600;

static_assert(validBaud, "Invalid TELEM_BAUDRATE");

// ---- Motor limits ----
static_assert(MOTOR_MIN_PERCENTAGE >= 0.0f, "MOTOR_MIN_PERCENTAGE < 0");
static_assert(MOTOR_MAX_PERCENTAGE <= 100.0f, "MOTOR_MAX_PERCENTAGE > 100");
static_assert(MOTOR_MIN_PERCENTAGE < MOTOR_MAX_PERCENTAGE, "motor_min >= motor_max");

// ---- Reel deltas sign check ----
static_assert(REEL_SPEED_DELTA_PERCENTAGE_REEL_IN > 0.0f, "REEL_IN must be > 0");
static_assert(REEL_SPEED_DELTA_PERCENTAGE_REEL_OUT > 0.0f, "REEL_OUT must be > 0");

// ---- Tilt deltas sign check ----
static_assert(BASE_TILT_SPEED_DELTA_PERCENTAGE_POSITIVE_TILT > 0.0f, "POSITIVE_TILT must be > 0");
static_assert(BASE_TILT_SPEED_DELTA_PERCENTAGE_NEGATIVE_TILT > 0.0f, "NEGATIVE_TILT must be > 0");

// ---- SPEED limiter ----
static_assert(REEL_SPEED_DELTA_PERCENTAGE_REEL_IN <= REEL_SPEED_DELTA_CLAMPING, "REEL_IN too large");
static_assert(REEL_SPEED_DELTA_PERCENTAGE_REEL_OUT <= REEL_SPEED_DELTA_CLAMPING, "REEL_OUT too large");
static_assert(BASE_TILT_SPEED_DELTA_PERCENTAGE_POSITIVE_TILT <= BASE_TILT_SPEED_DELTA_CLAMPING, "POSITIVE_TILT too large");
static_assert(BASE_TILT_SPEED_DELTA_PERCENTAGE_NEGATIVE_TILT <= BASE_TILT_SPEED_DELTA_CLAMPING, "NEGATIVE_TILT too large");

// ---- BURST TIME limiter ---
static_assert(REEL_BURST_TIME_MILLIS > 0 && REEL_BURST_TIME_MILLIS < REEL_BURST_TIME_MILLIS_CLAMPING, "INVALID BURST TIME FOR REELING");
static_assert(BASE_TILT_BURST_TIME_MILLIS > 0 && BASE_TILT_BURST_TIME_MILLIS < BASE_BURST_TIME_MILLIS_CLAMPING, "INVALID BURST TIME FOR TILTING");