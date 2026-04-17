





void handleFlightMode(){
  if(takeOffCommand){
    if(MOTORARMED){
      //calculateOffsets(1);
      //calculateOffsets(3);
      //calculateOffsets(4);
      resetIntegralMotor();
      resetIntegralAngle();
      Serial.println("\n\nTAKE OFF;");
  
  
      MOTORON = true;
      takeOff = true; 
      timerFlight = 0;
      takeOffCommand = false; // resets flag
      timeFlag = true;
      rampLandingTime = 0;
        
      return;
    }
    else{
      takeOffCommand = false;
      return;
      }
  }

  if(takeOff){ // Requires restart to take off
     
      rampLandOrTakeOff();
  }



  if(flightMode){
    flightMode = true;
    takeOff = false;
  }



  if(landingNow){ // Requires restart to take off

    if(landingFlag){
      landingFlag = false;
      rampLandingTime = 0;
      flightMode = false;
      
    takeOff = false;
    }
    rampLandOrTakeOff();
    
  }
}




float rampTime = LANDINGSPEED/TAKEOFFALTITUDE; // in sec

void rampLandOrTakeOff(){
  if(landingNow){
  
  
  return;
  }
  if(takeOff){
   
     
  return;
  }


}




