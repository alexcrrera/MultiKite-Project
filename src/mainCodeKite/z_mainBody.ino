


void setup() {

  Serial.begin(57600);
  initSystem();

}

////////////////////////////////////////////====================SETUP END & MAIN LOOP START====================/////////////////////////////////////////

void loop() {
  checkStateSystem();
  handleTelemetry();

  handleReelServo();
  handleMotor();
  handleBaseTiltServo();
}

////////////////////////////////////////////====================MAIN LOOP END====================/////////////////////////////////////////
