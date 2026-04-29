
void checkStateSystem(){

  if(motor_test_mode){

      motor_output_percentage = motor_test_percentage;
    if(!motor_armed){
      returnMessage ="TST OFF - MTR UNARMED";
      motor_test_mode = false;
      motor_on = false;
      motor_test_percentage = MOTOR_MIN_PERCENTAGE;
      motor_armed = false;
    }
    if(!motor_armed || !motor_on){
      returnMessage = "TST OFF - MTR OFF";
      motor_test_mode = false;
      motor_on = false;
      motor_test_percentage = MOTOR_MIN_PERCENTAGE;
      motor_armed = false;

    }
    

    
    }
}


void toggleTest() {
  if (!motor_on && motor_armed && !motor_test_mode) {  // if motor off and armed, then we can proceed with the test, otherwise return error

    motor_test_mode = true;
    motor_on = true;
    motor_test_percentage = MOTOR_MIN_PERCENTAGE;  // start at min cmdable value
    
    returnMessage = "MOTOR TEST STARTED";
  }
  else if(motor_test_mode){
    motor_test_mode = false;
    motor_on = false;
    motor_armed = false;
    returnMessage = "MOTOR TEST DONE";
    motor_test_percentage = MOTOR_MIN_PERCENTAGE;
  }

  else {
    motor_test_mode = false;
    motor_on = false;
    motor_armed = false;
    returnMessage = "MOTOR TEST ERROR";
    motor_test_percentage = MOTOR_MIN_PERCENTAGE;
  }
}



void checkState(){
}



float EWA(float average, float newSample, float alpha){ // alpha parameter for EWA filter , alpha -> 0 means we lower the weight of the new sample
  return(average * (1-alpha) + alpha*newSample);
}



int signeValeur(float val){
  return(val<0 ? -1 : 1);
}


float wrapper(float val, float max){
  float inter = (fabs(val) > max) ? signeValeur(val) * max : val;
  return(inter);
}


void calculateOffsets(int offsetTool){
  switch(offsetTool){
    default:
      return;
  }
}


void updateData(){
}


