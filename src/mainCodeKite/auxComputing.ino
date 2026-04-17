


void forceLanding(){
  landingFlag = true;
   timeFlag = false;
      landingNow = true;
      rampLandingTime = 0;
          Serial.println("\n LANDING NOW - TIMEOUT");
}

elapsedMillis  timeTestTakeOff = 0;
float timeFlight = 21.0; // in sec


void testHelper(){

  if((timeTestTakeOff/1000.0 >= timeFlight) && timeFlag){
  forceLanding();
    
  }
}



void resetIntegralAngle(){
 

}

void resetIntegralMotor(){
  //integralMotor = 0.0;
}



float EWA(float average, float newSample, float alpha){ // alpha parameter for EWA filter , alpha -> 1 means we lower the weight of the new sample
  return(average * (1-alpha) + alpha*newSample);
}






int signeValeur(float val){
  return(val<0 ? -1 : 1);
}






float timeFlightCheck = 1.0;
void spoolMotorCheck(){
  if(spoolMotor){
    if(timerSpoolMotor/1000.0 >=timeFlightCheck){
       timeTestTakeOff = 0;
      spoolMotor = false;
      MOTORTEST =false;
      takeOffCommand = true;
       // resta
    }
    
  
      
  }
}





float wrapper(float val, float max){
  float inter = (fabs(val) > max) ? signeValeur(val) * max : val;
  return(inter);
}







void calculateOffsets(int offsetTool){
  switch(offsetTool){
    case 1: // vectornav angles

    break;

    case 2: // pressure reset
    
    break;

    case 3: // reset lidar 

      break;

    case 4:

  

    default:
      return;


  }

}





void updateData(){
}


