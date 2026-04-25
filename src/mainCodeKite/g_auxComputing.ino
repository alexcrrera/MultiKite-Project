
void startTest() {
  if (!motor_on && motor_armed) {  // if motor off and armed, then we can proceed with the test, otherwise return error

    motor_test_mode = true;
    motor_on = true;
    motor_test_percentage = MOTOR_MIN_PERCENTAGE;  // start at min cmdable value
    returnMessage = "MOTOR TEST STARTED";
  }

  else {
    motor_test_mode = false;
    returnMessage = "MOTOR TEST ERROR";
  }
}



void checkState(){
}



float EWA(float average, float newSample, float alpha){ // alpha parameter for EWA filter , alpha -> 1 means we lower the weight of the new sample
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


