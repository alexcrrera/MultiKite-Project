

void initSystem() {
 // delay(1000);
  
  pinMode(motorCtrlPin, INPUT);
    pinMode(LEDLR, OUTPUT);
  pinMode(LEDLG, OUTPUT);
  pinMode(LEDLB, OUTPUT);
  pinMode(internal_LED_BUZZER, OUTPUT);
  initTelem();
  sendMessage("[OK] TELEM INIT");
 // delay(1000);
  sendMessage("TESTING SERVOS");

  initServos();
  sendMessage("[OK] SERVOS");


 // delay(500);



  sendMessage("STARTUP COMPLETE");
  sendMessage("WAITING FOR SIGNAL");
 // delay(1000);
}



void initServos() {
  ESC.attach(ESCPIN,ESCLOWPOINT,ESCHIGHPOINT);//,,ESCHIGHPOINT);
  //.attach(servoX1);


  ESC.writeMicroseconds(round(ESCLOWPOINT*1.1));
  delay(1000);

}

void initTelem(){
  TELEM.begin(57600); // 57600
}





