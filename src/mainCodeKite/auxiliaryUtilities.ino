







unsigned long timePrint = 0;

void handlePrint(){ // gets LiDAR data at appropriate rate , raises flag if NACK
  const int PRINTFREQUENCY = PLTRATE; // in Hz
  if((micros()-timePrint)*1.0>=1000.0*1000/PRINTFREQUENCY){
    //Serial.println("LETS");
    timePrint = micros();
    getPrint(); 
  }
}

void printSingle(String header, float d1){

  String res = header + ": ";
 


  if(PLOTMODE){
    res = "";
  }
  Serial.print(res +String(d1)+",");
}


void printGroup(String header, float d1, float d2, float d3){

  String res = header + ": ";

  if(PLOTMODE){
    res = "";
  }
  Serial.print(res  + String(d1) + "," + String(d2) + ","+ String(d3)+",");


}

void printGroup4(String header, float d1, float d2, float d3,float d4){

  String res = header + ": ";

  if(PLOTMODE){
    res = "";
  }
  Serial.print(res  + String(d1) + "," + String(d2) + ","+ String(d3)+ ","+ String(d3)+",");
 
}

void getPrint() {
  bool printNow = false;

  if(printNow){
     //float timeNowSD = millis()/1000.0;
 Serial.print("\n");
 ///////////////////////////////////////////////printSingle("Time",timeNowSD);
  //printBlender();
  
  //printSingle("Desired Altitude",desiredPositionZ);
  //printSingle("Altitude",positionZ);
 
 // printGroup("Position",positionX,positionY,positionZ);
 
// //////////////////////////////////////////// printSingle("Motor", percentageMotor/100);
  /////////////////////// printSingle("Time S", timeTestTakeOff/1000.0);
 ////////////////////////////////////////////printGroup("x,y,z",posN,posE,posD);
 ////////////////////////////////// printSingle("RTK status",rtkStatus*1.0);
  
  //printSingle("Mi",Mi);


 //printGroup("LiDAR Readings", lidarReadings[0],lidarReadings[1],lidarReadings[2]);
  //printWarnings();
  //printSingle("AngleX",AngleX);
 
  //printSingle("Desired AngleX", desiredAngleX);
  //printSingle("Current AngleX", AngleX);


  }
   //printGroup("GAINS",pGainAngleX,iGainAngleX,dGainAngleX);
   // printGroup("INTEGRAL",integralAngleX,integralAngleY,integralAngleZ);
 
 //// printSingle("Motor Arm?",MOTORARMED);
    //printSingle("Take Off?",takeOff);
    
    //printSingle("Motor On",MOTORON);
    //printSingle("max TVCANGLEZ",maxAngleZTVC);
    //printSingle("max TVCANGLEZ",maxAngleZTVC);
  // printSingle("MAX ABORT ANGLE", abortAngle);
 // printGroup4("PID OUTPUT",finalOutputX1pid,finalOutputY1pid,finalOutputX2pid,finalOutputY2pid);
   // printSingle("Roll offsets",  rollOffset);
  
}













