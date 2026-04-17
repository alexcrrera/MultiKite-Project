unsigned long timeTELEMETRY = 0;


int dataIndexTelem = 0;
String incomingDataTelemString = "";

void handleTelemetry(){
  
  readTelem(); // read incoming bytes
   // in Hz
  if((micros()-timeTELEMETRY)*1.0>=1000.0*1000/TELEMETRYFREQUENCY){
    timeTELEMETRY = micros();
    sendTelem(); // send periodically telem
  }
}


#define NUM_FIELDS 28
void sendTelem(){
  
  if(!START_SYSTEM){
    return;
  }

  String fields[NUM_FIELDS];

  // Index 0: header
  fields[0] = "$LNDAS";

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
  fields[10] = String(percentageMotor);

  // Index 11
  fields[11] = MOTORON ? "ON" : "OFF";

  // Index 12
  fields[12] = MOTORARMED ? "ARMED" : "DISARMED";

  // Index 13
  // fields[13] = (sdWrite==1 || sdWrite==2) ? "NO SD REC" : "NO SD";

  // // Indexes 14-16
  // fields[14] = String(desiredPositionX,2);
  // fields[15] = String(desiredPositionY,2);
  // fields[16] = String(desiredPositionZ,3);

  // Index 17: flight mode
  if(takeOff){
    fields[17] = "TAKING OFF";
  } else if(flightMode){
    fields[17] = "FLIGHT MODE";
  } else if(landingNow){
    fields[17] = "LANDING NOW";
  } else if(spoolMotor){
    fields[17] = "SPOOLING UP";
  } else {
    fields[17] = "STANDBY";
  }

  // // Index 18
  // fields[18] = String(round(numSV),0);

  // // Index 19
  // fields[19] = String(fixTypeText);

  // // Index 20
  // fields[20] = String(headingDeg,2);

  // // Index 21
  // fields[21] = String(gSpeed,2);

  // // Index 22
  // fields[22] = gnssTimestamp;

  // // Index 23
  // fields[23] = gnssTimestamp;

  // // Index 24
  // fields[24] = String(averageRTK_accuracy,2);

  // Index 25
  fields[25] = errorMessage;

  // Index 26
  fields[26] = returnMessage;

  // Index 27
  fields[27] = "12";

  // Serialize once
  TELEM.print("\n");
  for(int i = 0; i < NUM_FIELDS; i++){
    if(i == 0){
      TELEM.print(fields[i]);
    } else {
      TELEM.print(",");
      TELEM.print(fields[i]);
    }
  }
  TELEM.print("*");
}












void readTelem() { // returns read output int.
  if (TELEM.available() > 0) {
    char incomingChar = TELEM.read(); 
   //Serial.print(incomingChar);
    if (incomingChar == '\n') {
      incomingDataTelem[dataIndexTelem] = '\0';
      processTelem();
      dataIndexTelem = 0;
    }
    else {
      incomingDataTelem[dataIndexTelem] = incomingChar;
      incomingDataTelemString=+incomingDataTelem;
      dataIndexTelem++;
      checkOverflowTelem();      
    }  
  }
  else{
      if (Serial.available() > 0) {
        char incomingChar = Serial.read(); 
        //Serial.print(incomingChar);
      if (incomingChar == '\n') {
        incomingDataTelem[dataIndexTelem] = '\0';
        processTelem();
        dataIndexTelem = 0;
      }
      else {
        incomingDataTelem[dataIndexTelem] = incomingChar;
        incomingDataTelemString=+incomingDataTelem;
        dataIndexTelem++;
        checkOverflowTelem();      
      }  
    } 
  }
}


void checkOverflowTelem(){
  if (dataIndexTelem >= bufferSize - 1) {
    Serial.println(F("RADIO OVERFLOW"));
    dataIndexTelem = 0;
    incomingDataTelemString = "";
  }
}



void sendMessage(String message){
  // Send individual message via telem (no Serial Studio Formatting)
  TELEM.print("\n");
  TELEM.print(message);
  TELEM.print("*");
}



int checkHeaderTelem(){
  
    int TelemIdentity = -1;
    if(incomingDataTelemString.indexOf("GO") != -1) {  // parameters
      Serial.println("GO");   
      
      START_SYSTEM = true;
      resetIntegralAngle();
      }

    if(incomingDataTelemString.indexOf("RANGLES") != -1) {  // parameters
      Serial.println("CONFIGU");   
      returnMessage = "ANGLES RESET";

      resetIntegralAngle();
      TelemIdentity = 1;      
    }
      
    if(incomingDataTelemString.indexOf("RPOS") != -1) { // reset position
      TelemIdentity = 2;
      Serial.println("RESET POSITION");
      returnMessage = "POSITION RESET";
    }
    
    if(incomingDataTelemString.indexOf("PID") != -1) {
      TelemIdentity = 3; 
    }
    
    if(incomingDataTelemString.indexOf("ABORTANGLE") != -1) {
      TelemIdentity = 4;
    }
    
    if(incomingDataTelemString.indexOf("MAXANGLETVC") != -1) {
      TelemIdentity = 5;  
    }

    if(incomingDataTelemString.indexOf("RLIDAR") != -1) {
      returnMessage = "LiDAR RESET";
      TelemIdentity = 6;
    }

    if(incomingDataTelemString.indexOf("TLM") != -1) {
      TelemIdentity = 13;
    }

    if(incomingDataTelemString.indexOf("$VN300") != -1) {
      
    }

    if(incomingDataTelemString.indexOf("TAO") != -1) {
      returnMessage = "TAKE OFF CMD SENT";
      MOTORTEST = true;
      spoolMotor = true;  // flag
      timerSpoolMotor = 0; // reset time
      Serial.println("\nTAKE OFF COMMAND SENT");
    }

    if(incomingDataTelemString.indexOf("PLT") != -1) {
      PLOTMODE = !PLOTMODE;
      TelemIdentity = 69;
      }
      if (incomingDataTelemString.indexOf("LND") != -1) {
        returnMessage = "LND CMD SENT";
     
       
        forceLanding();
     
        // LAND NOW!
      }
      if (incomingDataTelemString.indexOf("MARM") != -1) {
        
        // Arm motor
        takeOff = false;
        MOTORARMED = true;
        returnMessage = "MOTOR ARMED";
        Serial.println("MOTOR ARMED!");
          
      }

      if (incomingDataTelemString.indexOf("SETHOME") != -1) {
 //calculateOffsets(1);
//calculateOffsets(3);
        calculateOffsets(4);
        Serial.println("SET HOME!");
        returnMessage = "HOME SET";
     
            }
      
      if (incomingDataTelemString.indexOf("MOFF") != -1) {
        takeOff = false;
        MOTORARMED = false;
        MOTORON = false;
        Serial.println("MOTOR OFF!");
        returnMessage = "MOTOR OFF";
   
      }



      if (incomingDataTelemString.indexOf("DSRM") != -1) {
        // Disarm motor
        MOTORARMED = false;
        Serial.println("MOTOR UNARMED!");
        returnMessage = "MOTOR UNARMED";
      }

       if (incomingDataTelemString.indexOf("MTEST") != -1) {
        // Test motor
        MOTORTEST = !MOTORTEST;
        Serial.println("MOTOR test!");
        returnMessage = "MOTOR TESTED";
      }


       if (incomingDataTelemString.indexOf("STEST") != -1) {
        
        SERVOTEST = !SERVOTEST;
        resetIntegralAngle();

        if(SERVOTEST){
            returnMessage = "SERVO TESTING";
        }
        else{
           returnMessage = "SERVO TESTING OFF";
        }
        
        
        Serial.println("SERVO test!");
        // LAND NOW!
          
      }



  return(TelemIdentity); // none
}


void processTelem(){
  int TelemIdentity = checkHeaderTelem();

  char headerTelem[10];
  int offsetTool = -1;
float inter = 0.0;
  switch (TelemIdentity) {
    
    case -1:
   
      return;
      break; // useless but meh
      
    case 1:
     offsetTool = 1;
      break;

    case 2:
      //ommaParser.parseLine(incomingDataTelem,headerTelem,Xangle,Yangle,Zangle);
      offsetTool = 4;


    case 4:
      //
      
      //offsetTool = 4;

      break;
           case 5:
      //
      
      //offsetTool = 4;

      break;

      case 6:
      offsetTool = 3;

      break;


        case 10:
      
         break;
     case 11:
    
         break;
             case 12:

         break;
          case 13:
             commaParser.parseLine(incomingDataTelem,headerTelem,TELEMETRYFREQUENCY);
         break;

            case 14:
             
         break;

            case 15:
           
          
             commaParser.parseLine(incomingDataTelem,headerTelem,inter);

             
         break;
            case 16:

            
             commaParser.parseLine(incomingDataTelem,headerTelem,inter);

            

 
         break;            
        

      case 69:
         commaParser.parseLine(incomingDataTelem,headerTelem,PLTRATE);
      if(PLTRATE==0){
        TELEM.println("TELEM OFF");
      }
  }



  calculateOffsets(offsetTool);
}






