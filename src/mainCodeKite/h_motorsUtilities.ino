

// ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
// ============== FUNCTIONS TO RUN PERIODICALLY MOTOR CONTROL LOGIC
// ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

void handleReelServo() {  // run servo control logic at REEL_SERVO_FREQUENCY Hz
  static unsigned long lastTime = 0;
  constexpr unsigned long intervalMs = 1000UL / REEL_SERVO_FREQUENCY; 
  if (millis() - lastTime >= intervalMs) {
    lastTime = millis();
    reelServoWrite();
  }
}

void handleBaseTiltServo() {  // run servo control logic at BASE_TILT_SERVO_FREQUENCY Hz
  static unsigned long lastTime = 0;
  constexpr unsigned long intervalMs = 1000UL / BASE_TILT_SERVO_FREQUENCY; 
  if (millis() - lastTime >= intervalMs) {
    lastTime = millis();
    baseTiltServoWrite();
  }
}

void handleMotor() {  // run servo control logic at MOTOR_FREQUENCY Hz
  static unsigned long lastTime = 0;
  constexpr unsigned long intervalMs = 1000UL / MOTOR_FREQUENCY; 
  if (millis() - lastTime >= intervalMs) {
    lastTime = millis();
    motorWrite();
  }
}


// ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
// ============== FUNCTIONS TO WRITE TO MOTORS
// ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

void motorWrite() {
  if(!motor_on || !motor_armed){
      motor_output_percentage = 0;
  }
  const int outFinal = round(map(motor_output_percentage, 0.0, 100.0, ESC_LOW_PULSE, ESC_HIGH_PULSE));
  ESC.writeMicroseconds(outFinal);
}

void baseTiltServoWrite() {
 // const int outFinal = round(map(percentageMotor, 0.0, 100.0, ESCLOWPOINT, ESCHIGHPOINT));
  
 if (base_tilt_down || base_tilt_up){
    if (millis() - base_tilt_burst_start_time >= BASE_TILT_BURST_TIME_MILLIS){
      base_tilt_burst_start_time = 0; // reset burst timer
      base_tilt_down = false; // stop the burst by resetting the input flags
      base_tilt_up = false;
     // returnMessage="Base tilt burst ended - both directions reset";
    }
  }
 float base_tilt_servo_output_pulse= BASE_TILT_STOP_PULSE; // default to stop pulse
 if (base_tilt_down && !base_tilt_up){
  
  base_tilt_servo_output_pulse = BASE_TILT_STOP_PULSE + (BASE_TILT_SPEED_DELTA_PERCENTAGE_POSITIVE_TILT * (BASE_TILT_HIGH_PULSE - BASE_TILT_STOP_PULSE));
 }
 else if (base_tilt_up && !base_tilt_down){
  base_tilt_servo_output_pulse = BASE_TILT_STOP_PULSE - (BASE_TILT_SPEED_DELTA_PERCENTAGE_NEGATIVE_TILT * (BASE_TILT_STOP_PULSE - BASE_TILT_LOW_PULSE));
 }
  //returnMessage = "BASE TILT SERVO OUT: " + String(base_tilt_servo_output_pulse) + "us";
 BASE_TILT.writeMicroseconds(round(base_tilt_servo_output_pulse));
}


void reelServoWrite() {
  float reel_servo_output_pulse= REEL_STOP_PULSE; // default to stop pulse

  if (reel_in || reel_out){
    if (millis() - reel_burst_start_time >= REEL_BURST_TIME_MILLIS){
      reel_burst_start_time = 0; // reset burst timer
      reel_in = false; // stop the burst by resetting the input flags
      reel_out = false;
      //returnMessage="Reel burst ended - both directions reset";
    }
  }
  if (reel_in && !reel_out){
    reel_servo_output_pulse = REEL_STOP_PULSE * (1-REEL_SPEED_DELTA_PERCENTAGE_REEL_IN);
  }
  else if (reel_out && !reel_in){
    reel_servo_output_pulse = REEL_STOP_PULSE * (1+REEL_SPEED_DELTA_PERCENTAGE_REEL_OUT);
  }
 // returnMessage = "REEL SERVO OUT: " + String(reel_servo_output_pulse) + "us";
  REEL.writeMicroseconds(round(reel_servo_output_pulse));
}



