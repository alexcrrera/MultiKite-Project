void handleTelemetry() {

  readTelem();  // read incoming bytes

  static unsigned long timeTelemetry = 0;
  const unsigned long intervalUs = 1000000UL / TELEMETRY_FREQUENCY;
  unsigned long now = micros();

  if (now - timeTelemetry >= intervalUs) {
    timeTelemetry = now;
    sendTelem();  // send periodically telem
  }
}


#define NUM_FIELDS 28
void sendTelem() {
  // CHECK WITH SERIAL STUDIO FOR INDEX VALUES

  String fields[NUM_FIELDS];

  // Index 0: header
  fields[0] = "$MKTE";

  // Indexes 1-3
  // fields[1] = String(AngleX,1);
  // fields[2] = String(AngleY,1);
  // fields[3] = String(AngleZ,1);

  // // Indexes 4-6
  // fields[4] = String(positionX,2);
  // fields[5] = String(positionY,2);
  // fields[6] = String(positionZ,2);

  // Indexes 7-9
  // fields[7] = String(latitudeDeg,8);
  // fields[8] = String(longitudeDeg,8);
  // fields[9] = String(altitudeM,2);

  // Index 10
  fields[10] = String(motor_output_percentage);

  // Index 11
  fields[11] = motor_on ? "ON" : "OFF";

  // Index 12
  fields[12] = motor_armed ? "ARMED" : "DISARMED";

  // Index 13
  // fields[13] = (sdWrite==1 || sdWrite==2) ? "NO SD REC" : "NO SD";

  // // Indexes 14-16
  // fields[14] = String(desiredPositionX,2);
  // fields[15] = String(desiredPositionY,2);
  // fields[16] = String(desiredPositionZ,3);

  // Index 17: flight mode
  if (motor_test_mode) {
    fields[17] = "TEST MODE";
  }

  else {
    fields[17] = "STANDBY";
  }

  // // Index 18
  // fields[18] = String(round(numSV),0);

  // // Index 19

  // fields[19] = digitalRead(BRAKEINPUT) ? "ENGAGED" : "DISENGAGED";

  // // Index 20
  // fields[20] = String(headingDeg,2);

  // // Index 21
  // fields[21] = String(gSpeed,2);

  // // Index 22
  // fields[22] = gnssTimestamp;

  // // Index 23
  // fields[23] = gnssTimestamp;

  // // Index 24
  //fields[24] = String(analogRead);

  // Index 25
  fields[25] = errorMessage;

  // Index 26
  fields[26] = returnMessage;

  // Index 27
  fields[27] = "12";

  // Serialize once
  TELEM.print("\n");
  for (int i = 0; i < NUM_FIELDS; i++) {
    if (i == 0) {
      TELEM.print(fields[i]);
    } else {
      TELEM.print(",");
      TELEM.print(fields[i]);
    }
  }
  TELEM.print("*");
}



int dataIndexTelem = 0;
String incomingDataTelemString = "";

void readTelem() {  // returns read output int.
  // checks TELEM port and reads one char at a time, only parses String once sentence is complete and handles overflow case
  if (TELEM.available() > 0) {         // if char available
    char incomingChar = TELEM.read();  // read incoming char

    if (incomingChar == '\n') {  // handle endline - complete packet received (allegedly)
      incomingDataTelem[dataIndexTelem] = '\0';
      incomingDataTelemString = incomingDataTelem;  // we convert the char array incomingDataTelem into a String for easier handling
      processTelem();                               // we process the packet
      dataIndexTelem = 0;                           // reset index for next String
    }

    else {
      checkOverflowTelem();  // make sure we dont overflow to avoid segmentation faults
      incomingDataTelem[dataIndexTelem] = incomingChar;

      dataIndexTelem++;  // increase index
    }
  }
}

void checkOverflowTelem() {
  // handle String buffer overflow
  if (dataIndexTelem >= bufferSize - 1) {
    dataIndexTelem = 0;
    incomingDataTelemString = "";
  }
}



void sendMessage(String message) {
  // Send individual message via telem (no Serial Studio Formatting)
  TELEM.print("\n");
  TELEM.print(message);
  TELEM.print("*");
}



int checkHeaderTelem() {

  int TelemIdentity = -1;

  if (incomingDataTelemString.indexOf("IMTR") != -1) {  // Action to increase Motor Thrust value - value is algeb. so can be a negative increase (thurst decrease) - parameters passed handled elsewhere
    TelemIdentity = 14;
    returnMessage = "CHANGED THRUST VALUE";
  }



  if (incomingDataTelemString.indexOf("SBASE") != -1) {  // Action to control the Servo attached to the BASE
    TelemIdentity = 15;
  }

    if (incomingDataTelemString.indexOf("SREEL") != -1) {  // Action to control the Servo attached to the BASE
    TelemIdentity = 16;
  }



  if (incomingDataTelemString.indexOf("TAO") != -1) {  // Action to perform a take off - placeholder for now
    returnMessage = "TAKE OFF PLACEHOLDER";
  }


  if (incomingDataTelemString.indexOf("LND") != -1) {  // Action to perform a landing - placeholder for now
    returnMessage = "LND PLACEHOLDER";
  }

  if (incomingDataTelemString.indexOf("MARM") != -1) {  // Action to virtually arm the motor
    motor_armed = true;
    returnMessage = "MOTOR ARMED";
  }

  if (incomingDataTelemString.indexOf("DSRM") != -1) {
    motor_armed = false;
    returnMessage = "MOTOR DSRM";
  }


  if (incomingDataTelemString.indexOf("MOFF") != -1) {
    motor_on = false;
    returnMessage = "MOTOR OFF";
  }


  if (incomingDataTelemString.indexOf("MTEST") != -1) {
    returnMessage = "MOTOR TEST INIT";
    toggleTest();
  
  }

  return (TelemIdentity);  // none
}


void processTelem() {
  int TelemIdentity = checkHeaderTelem();

  char headerTelem[10];
  int offsetTool = -1;
  float inter = 0.0;


  switch (TelemIdentity) {

    case -1:

      break;

    case 14:
      commaParser.parseLine(incomingDataTelem, headerTelem, inter);
      returnMessage = "INC: " + String(inter) + "%";
      motor_test_percentage = constrain(motor_test_percentage + inter, MOTOR_MIN_PERCENTAGE, MOTOR_MAX_PERCENTAGE);
      break;



    case 15:  // SBASE - TILTING OF BASE
      commaParser.parseLine(incomingDataTelem, headerTelem, inter);

      if (inter == -1) {  // tilt negative
        base_tilt_down = true;
        base_tilt_up = false;
        base_tilt_burst_start_time = millis(); 

        returnMessage = "TILTING BASE-";
      }

      else if (inter == 1) {  // tilt positive
        base_tilt_down = false;
        base_tilt_up = true;
        base_tilt_burst_start_time = millis(); 
        returnMessage = "TILTING BASE+";
      }

      
      break;



       case 16:  // SREEL - REELING
      commaParser.parseLine(incomingDataTelem, headerTelem, inter);

      if (inter == -1) {  // reel in
        reel_in = true;
        reel_out = false;
        reel_burst_start_time = millis(); 

        returnMessage = "REELING IN";
      }

      else if (inter == 1) {  // reel out
        reel_in = false;
        reel_out = true;
        reel_burst_start_time = millis(); 
        returnMessage = "REELING OUT";
      }

      
      break;

    default:
      break;

}
}
