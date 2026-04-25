

void initSystem() { 
  
  initTelem();
  initServos();
  sendMessage("STARTUP COMPLETE"); // sends message directly via Telem
}



void initServos() {

  BASE_TILT.attach(BASE_PIN,BASE_TILT_LOW_PULSE,BASE_TILT_HIGH_PULSE); // attach base servo and define min-max PWM range - see documentation and datasheet - values may vary per motor
  REEL.attach(REEL_PIN,REEL_LOW_PULSE,REEL_HIGH_PULSE);

  ESC.attach(ESC_PIN,ESC_LOW_PULSE,ESC_HIGH_PULSE);// ESC is treated like a servo  - we command via pulses @50Hz - see https://howtomechatronics.com/tutorials/arduino/arduino-brushless-motor-control-tutorial-esc-bldc/

  BASE_TILT.writeMicroseconds(round(BASE_TILT_STOP_PULSE)); // define 1500 us for the pulse - center of the command so we will not be moving
  REEL.writeMicroseconds(round(REEL_STOP_PULSE));

  ESC.writeMicroseconds(round(ESC_LOW_PULSE*1.0)); // define low point to perform arming of the ESC
  delay(1000);

}

void initTelem(){
  TELEM.begin(TELEM_BAUDRATE); //  must match Serial Studio's value
}





