

void handleServos(){ // gets LiDAR data at appropriate rate , raises flag if NACK
  const int SERVOFREQUENCY = 50; // in Hz
  
  static unsigned long time = 0;
  if((micros()-time)*1.0>=1000.0*1000/SERVOFREQUENCY){
    
    time = micros();
    servoWrite();
  }
}    



void handleEDF(){ // gets LiDAR data at appropriate rate , raises flag if NACK
  const int EDFFREQUENCY = 25; // in Hz
  static unsigned long timeEdf = 0;

  if((micros()-timeEdf)*1.0>=1000.0*1000/EDFFREQUENCY){
    timeEdf = micros();
    handleThrustEDF();
  }
}


void handleThrustEDF(){

 if(!MOTORON){
    percentageMotor = 0.0;
  }

   if(MOTORTEST ){
    percentageMotor = 21.0;
  }

  if(MOTORTEST && spoolMotor){
    percentageMotor = 21.0;
  }
  const int outFinal = round(map(percentageMotor,0.0,100.0,ESCLOWPOINT,ESCHIGHPOINT));
  ESC.writeMicroseconds(outFinal);
}

void servoWrite() {
  if(!SERVOTEST){
 
  }
  else{ // TEST 
  
    
  }
}

