/*        

*/
#include <nRF24L01.h>
#include <RF24.h>
#include <VarSpeedServo.h>

// Define 6 servo home position arduino angle 
#define SERVO_0_HOME  90  
#define SERVO_1_HOME  90
#define SERVO_2_HOME  180
#define SERVO_3_HOME  30
#define SERVO_4_HOME  90
#define SERVO_5_HOME  180

#define BAS_SERVO   0 // base
#define SHL_SERVO   1 // shoulder
#define ELB_SERVO   2 // elbow
#define WRI_SERVO   3 // wrist up/down
#define WRO_SERVO   4 // wrist turn 
#define GRI_SERVO   5 // gripper

// Command from PC 
#define CMD_RUN_ROBOT           0x01
#define CMD_SAVE_POS            0x02
#define CMD_RESET_ROBOT         0x03
#define CMD_MOVE_ROBOT_JOY      0x04
#define CMD_CLEAR_POS           0x05
#define CMD_MOVE_ROBOT_SERIAL   0x06
#define CMD_MOVE_ROBOT_6LINK    0x07
#define CMD_STOP_ROBOT          0x08

#define SERVO_SPEED 50 // 0 full speed, 1~255 slower-to-faster

// nRF24L01 define CE and CSN 
RF24 radio(7, 8); 
// nRF24L01 address. same tx device and rx device
const byte address = '1'; 
// RF rx buffer
char rf_rx_buffer[13] = "";

// save position array - 20 storage 
int saved_pos_buff[20][6] = {0,};
int save_index = 0;
int current_index = 0;

// Servo instance 
VarSpeedServo bas_servo;
VarSpeedServo shl_servo;
VarSpeedServo elb_servo;
VarSpeedServo wri_servo;
VarSpeedServo wro_servo;
VarSpeedServo gri_servo;


// servo current position
int servo0Pos = SERVO_0_HOME, servo1Pos = SERVO_1_HOME, servo2Pos = SERVO_2_HOME, servo3Pos = SERVO_3_HOME, servo4Pos = SERVO_4_HOME, servo5Pos = SERVO_5_HOME; 
// servo destination position 
int servo00SP, servo01SP, servo02SP, servo03SP, servo04SP, servo05SP; 
// servo speed delay
int speedDelay = 10;

// joystick value 
unsigned int joy_1_h = 500; // base servo 
unsigned int joy_1_v = 500; // shoulder servo 
unsigned int joy_2_h = 500; // elbow servo 
unsigned int joy_2_v = 500; // wrist up/down servo 
unsigned int joy_3_h = 500; // wrist turn servo 
unsigned int joy_3_v = 500; // gripper servo 

// flag for representing robot is running now
bool run_robot_flag = false;

/*
  Description: Function for set robot arm home position
*/
void reset_arm_position(){

  servo0Pos = SERVO_0_HOME;
  servo1Pos = SERVO_1_HOME;
  servo2Pos = SERVO_2_HOME;
  servo3Pos = SERVO_3_HOME;
  servo4Pos = SERVO_4_HOME;
  servo5Pos = SERVO_5_HOME;

  /*--------------------- servo 0 ---------------------*/ 
  bas_servo.write(SERVO_0_HOME, SERVO_SPEED, false);
  /*--------------------- servo 1 ---------------------*/ 
  shl_servo.write(SERVO_1_HOME, SERVO_SPEED, false);
  /*--------------------- servo 2 ---------------------*/ 
  elb_servo.write(SERVO_2_HOME, SERVO_SPEED, false);
  /*--------------------- servo 3 ---------------------*/ 
  wri_servo.write(SERVO_3_HOME, SERVO_SPEED, false);
  /*--------------------- servo 4 ---------------------*/ 
  wro_servo.write(SERVO_4_HOME, SERVO_SPEED, false);
  /*--------------------- servo 5 ---------------------*/ 
  gri_servo.write(SERVO_5_HOME, SERVO_SPEED, false);

  Serial.print('a');
  Serial.print(0);
  Serial.print('b');
  Serial.print(0);
  Serial.print('c');
  Serial.print(-90);
  Serial.print('d');
  Serial.print(-60);
  Serial.print('e');
  Serial.print(0);
  Serial.print('f');
  Serial.print(90);
  Serial.println('g');
  
}

/*
  Description: converting 2 byte into int
*/
unsigned int BitShiftCombine( unsigned char x_high, unsigned char x_low)
{
  unsigned int combined; 
  combined = x_high;              //send x_high to rightmost 8 bits
  combined = combined<<8;         //shift x_high over to leftmost 8 bits
  combined |= x_low;                 //logical OR keeps x_high intact in combined and fills in                                                             //rightmost 8 bits
  return combined;
}

/*============================= robot control functions ===========================*/ 

/*
  Description: Function for programming robot using joystick through nRF24L01
*/
void move_robot(){

  int temp_servo0, temp_servo1, temp_servo2, temp_servo3, temp_servo4, temp_servo5;
  //Serial.println("program robot");
  joy_1_h = BitShiftCombine(rf_rx_buffer[2], rf_rx_buffer[1]);
  joy_1_v = BitShiftCombine(rf_rx_buffer[4], rf_rx_buffer[3]);

  joy_2_h = BitShiftCombine(rf_rx_buffer[6], rf_rx_buffer[5]);
  joy_2_v = BitShiftCombine(rf_rx_buffer[8], rf_rx_buffer[7]);

  joy_3_h = BitShiftCombine(rf_rx_buffer[10], rf_rx_buffer[9]);
  joy_3_v = BitShiftCombine(rf_rx_buffer[12], rf_rx_buffer[11]);

  /*--------------------- servo 0 ---------------------*/ 
  if(joy_1_h > 800){
    servo0Pos++;
    if(servo0Pos > 180){
      servo0Pos = 180;
    }
    bas_servo.write(servo0Pos, 0, true);
  }else if(joy_1_h < 200){
    servo0Pos--;
    if(servo0Pos < 0){
      servo0Pos = 0;
    }
    bas_servo.write(servo0Pos, 0, true);
  }
  delay(speedDelay);
  /*--------------------- servo 1 ---------------------*/ 
  if(joy_1_v > 800){
    servo1Pos++;
    if(servo1Pos > 180){
      servo1Pos = 180;
    }
    shl_servo.write(servo1Pos, 0, true);
  }else if(joy_1_v < 200){
    servo1Pos--;
    if(servo1Pos < 0){
      servo1Pos = 0;
    }
    shl_servo.write(servo1Pos, 0, true);
  }
  delay(speedDelay);
  /*--------------------- servo 2 ---------------------*/ 
  if(joy_2_v < 200){
    servo2Pos++;
    if(servo2Pos > 180){
      servo2Pos = 180;
    }
    elb_servo.write(servo2Pos, 0, true);
  }else if(joy_2_v > 800){
    servo2Pos--;
    if(servo2Pos < 0){
      servo2Pos = 0;
    }
    elb_servo.write(servo2Pos, 0, true);

  }
  delay(speedDelay);
  /*--------------------- servo 3 ---------------------*/ 
  if(joy_2_h > 800){
    servo3Pos++;
    if(servo3Pos > 180){
      servo3Pos = 180;
    }
    wri_servo.write(servo3Pos, 0, true);
  }else if(joy_2_h < 200){
    servo3Pos--;
    if(servo3Pos < 0){
      servo3Pos = 0;
    }
    wri_servo.write(servo3Pos, 0, true);
  }
  /*--------------------- servo 4 ---------------------*/ 
  if(joy_3_h > 800){
    servo4Pos++;
    if(servo4Pos > 180){
      servo4Pos = 180;
    }
    wro_servo.write(servo4Pos, 0, true);
  }else if(joy_3_h < 200){
    servo4Pos--;
    if(servo4Pos < 0){
      servo4Pos = 0;
    }
    wro_servo.write(servo4Pos, 0, true);
  }
  /*--------------------- servo 5 ---------------------*/ 
  if(joy_3_v > 800){
    servo5Pos++;
    if(servo5Pos > 180){
      servo5Pos = 180;
    }
    gri_servo.write(servo5Pos, 0, true);
  }else if(joy_3_v < 200){
    servo5Pos--;
    if(servo5Pos < 0){
      servo5Pos = 0;
    }
    gri_servo.write(servo5Pos, 0, true);
  }
  delay(speedDelay);
  
  temp_servo0 = servo0Pos;
  temp_servo1 = servo1Pos;
  temp_servo2 = servo2Pos;
  temp_servo3 = servo3Pos;
  temp_servo4 = servo4Pos;
  temp_servo5 = servo5Pos;

  temp_servo0 -= 90;
  temp_servo1 -= 90;
  temp_servo2 = (180-temp_servo2)-90;
  temp_servo3 -= 90;
  temp_servo4 -= 90;
  temp_servo5 -= 90;

  Serial.print('a');
  Serial.print(temp_servo0);
  Serial.print('b');
  Serial.print(temp_servo1);
  Serial.print('c');
  Serial.print(temp_servo2);
  Serial.print('d');
  Serial.print(temp_servo3);
  Serial.print('e');
  Serial.print(temp_servo4);
  Serial.print('f');
  Serial.print(temp_servo5);
  Serial.println('g');
  
}

/*
  Description: Function for programming robot throgh PC 
*/
void move_robot_serial(String inString){
  
  int temp_servo0, temp_servo1, temp_servo2, temp_servo3, temp_servo4, temp_servo5;
  String temp = "";

  if(inString[1] == 'a'){
    temp = inString.substring(2);
    if(temp.toInt() != 0){
      servo0Pos = temp.toInt() + 90;
      bas_servo.write(servo0Pos, SERVO_SPEED, true);
    }
  }else if(inString[1] == 'b'){
    temp = inString.substring(2);
    if(temp.toInt() != 0){
      servo1Pos = temp.toInt() + 90;
      shl_servo.write(servo1Pos, SERVO_SPEED, true);
    }
  }else if(inString[1] == 'c'){
    temp = inString.substring(2);
    if(temp.toInt() != 0){
      servo2Pos = (180 - temp.toInt())-90;
      elb_servo.write(servo2Pos, SERVO_SPEED, true);
    }
  }else if(inString[1] == 'd'){
    temp = inString.substring(2);
    if(temp.toInt() != 0){
      servo3Pos = temp.toInt() + 90;
      wri_servo.write(servo3Pos, SERVO_SPEED, true);
    }
  }else if(inString[1] == 'e'){
    String temp = inString.substring(2);
    if(temp.toInt() != 0){
      servo4Pos = temp.toInt() + 90;
      wro_servo.write(servo4Pos, SERVO_SPEED, true);
    }
  }else if(inString[1] == 'f'){
    String temp = inString.substring(2);
    if(temp.toInt() != 0){
      servo5Pos = temp.toInt() + 90;
      gri_servo.write(servo5Pos, SERVO_SPEED, true);
    }
  }

  temp_servo0 = servo0Pos;
  temp_servo1 = servo1Pos;
  temp_servo2 = servo2Pos;
  temp_servo3 = servo3Pos;
  temp_servo4 = servo4Pos;
  temp_servo5 = servo5Pos;

  temp_servo0 -= 90;
  temp_servo1 -= 90;
  temp_servo2 = (180-temp_servo2)-90;
  temp_servo3 -= 90;
  temp_servo4 -= 90;
  temp_servo5 -= 90;

  Serial.print('a');
  Serial.print(temp_servo0);
  Serial.print('b');
  Serial.print(temp_servo1);
  Serial.print('c');
  Serial.print(temp_servo2);
  Serial.print('d');
  Serial.print(temp_servo3);
  Serial.print('e');
  Serial.print(temp_servo4);
  Serial.print('f');
  Serial.print(temp_servo5);
  Serial.println('g');
}

/*
  Description: Function for reset robot arm
*/
void reset_robot(){
  reset_arm_position(); 
}

/*
  Description: Function for stopping robot arm
*/
void stop_robot_btn(){
  Serial.println('8');
}

/*
  Description: Function for saving 
*/
void save_pos_btn(){
  Serial.println('2');
}

/*
  Description: Function for saving 
*/
void run_robot_btn(){
  Serial.println('1');
}

/*
  Description: Function for saving robot position PC 
*/
void save_pos_serial(String inString){
  int start, end, index;
  // Get index value
  start = inString.indexOf('z');
  end = inString.indexOf('a');
  if(start != -1 && end != -1){
    String tempStr = inString.substring(start+1, end);
    index = tempStr.toInt();
  }
  if(index >= 20){
    return;
  }
  // Get servo 0 value
  start = inString.indexOf('a');
  end = inString.indexOf('b');
  if(start != -1 && end != -1){
    String tempStr = inString.substring(start+1, end);
    int save_0 = tempStr.toInt();
    saved_pos_buff[index][0] = save_0;
  }
  // Get servo 1 value
  start = inString.indexOf('b');
  end = inString.indexOf('c');
  if(start != -1 && end != -1){
    String tempStr = inString.substring(start+1, end);
    int save_1 = tempStr.toInt();
    saved_pos_buff[index][1] = save_1;
  }
  // Get servo 2 value
  start = inString.indexOf('c');
  end = inString.indexOf('d');
  if(start != -1 && end != -1){
    String tempStr = inString.substring(start+1, end);
    int save_2 = tempStr.toInt();
    saved_pos_buff[index][2] = save_2;
  }
  // Get servo 3 value
  start = inString.indexOf('d');
  end = inString.indexOf('e');
  if(start != -1 && end != -1){
    String tempStr = inString.substring(start+1, end);
    int save_3 = tempStr.toInt();
    saved_pos_buff[index][3] = save_3;
  }
  // Get servo 4 value
  start = inString.indexOf('e');
  end = inString.indexOf('f');
  if(start != -1 && end != -1){
    String tempStr = inString.substring(start+1, end);
    int save_4 = tempStr.toInt();
    saved_pos_buff[index][4] = save_4;
  }
  // Get servo 5 value
  start = inString.indexOf('f');
  end = inString.indexOf('g');
  if(start != -1 && end != -1){
    String tempStr = inString.substring(start+1, end);
    int save_5 = tempStr.toInt();
    saved_pos_buff[index][5] = save_5;
  }

  save_index = index;
  Serial.print("save pos ");
  Serial.println(save_index);
}

/*
  Description: Function for clear robot position
*/
void clear_pos_serial(){
  save_index = 0;
  current_index = 0;
  for(int i=0;i<20;i++){
    for(int j=0;j<6;j++){
      saved_pos_buff[i][j] = 0; 
    }
  }
}

/*
  Description: Function for running robot arm with pre-saved route
*/
void run_robot(){
  Serial.print("run robot  ");
  Serial.println(save_index); 
  /*--------------------- servo 0 ---------------------*/ 
  servo0Pos = saved_pos_buff[current_index][0]+90;
  bas_servo.write(servo0Pos, SERVO_SPEED, true);
  /*--------------------- servo 1 ---------------------*/ 
  servo1Pos = saved_pos_buff[current_index][1]+90;
  shl_servo.write(servo1Pos, SERVO_SPEED, true);
  /*--------------------- servo 2 ---------------------*/ 
  servo2Pos = (180-saved_pos_buff[current_index][2]-90);
  elb_servo.write(servo2Pos, SERVO_SPEED, true);
  /*--------------------- servo 3 ---------------------*/
  servo3Pos = saved_pos_buff[current_index][3]+90;
  wri_servo.write(servo3Pos, SERVO_SPEED, true);
  /*--------------------- servo 4 ---------------------*/ 
  servo4Pos = saved_pos_buff[current_index][4]+90;
  wro_servo.write(servo4Pos, SERVO_SPEED, true);
  /*--------------------- servo 5 ---------------------*/ 
  servo5Pos = saved_pos_buff[current_index][5]+90;
  gri_servo.write(servo5Pos, SERVO_SPEED, true);

  Serial.print('a');
  Serial.print(saved_pos_buff[current_index][0]);
  Serial.print('b');
  Serial.print(saved_pos_buff[current_index][1]);
  Serial.print('c');
  Serial.print(saved_pos_buff[current_index][2]);
  Serial.print('d');
  Serial.print(saved_pos_buff[current_index][3]);
  Serial.print('e');
  Serial.print(saved_pos_buff[current_index][4]);
  Serial.print('f');
  Serial.print(saved_pos_buff[current_index][5]);
  Serial.println('g');
}

/*
  Description: Function for stopping robot move 
*/
void stop_robot(){
  run_robot_flag = false;
  current_index = 0;
}
/*
  Description: Function for move robot arm with 6 servo at same time.
*/
void move_robot_6link(String inString){
  
  int base, shoulder, elbo, wrist_ud, wrist_turn, gripper;

  int start, end, index;
 
  // Get servo 0 value
  start = inString.indexOf('a');
  end = inString.indexOf('b');
  if(start != -1 && end != -1){
    String tempStr = inString.substring(start+1, end);
    base = tempStr.toInt();
  }
  // Get servo 1 value
  start = inString.indexOf('b');
  end = inString.indexOf('c');
  if(start != -1 && end != -1){
    String tempStr = inString.substring(start+1, end);
    shoulder = tempStr.toInt();
  }
  // Get servo 2 value
  start = inString.indexOf('c');
  end = inString.indexOf('d');
  if(start != -1 && end != -1){
    String tempStr = inString.substring(start+1, end);
    elbo = tempStr.toInt();
  }
  // Get servo 3 value
  start = inString.indexOf('d');
  end = inString.indexOf('e');
  if(start != -1 && end != -1){
    String tempStr = inString.substring(start+1, end);
    wrist_ud = tempStr.toInt();
  }
  // Get servo 4 value
  start = inString.indexOf('e');
  end = inString.indexOf('f');
  if(start != -1 && end != -1){
    String tempStr = inString.substring(start+1, end);
    wrist_turn = tempStr.toInt();
  }
  // Get servo 5 value
  start = inString.indexOf('f');
  end = inString.indexOf('g');
  if(start != -1 && end != -1){
    String tempStr = inString.substring(start+1, end);
    gripper = tempStr.toInt();
  }

  /*--------------------- servo 0 ---------------------*/ 
  servo0Pos = base+90;
  bas_servo.write(servo0Pos, SERVO_SPEED, true);
  /*--------------------- servo 1 ---------------------*/ 
  servo1Pos = shoulder+90;
  shl_servo.write(servo1Pos, SERVO_SPEED, true);
  /*--------------------- servo 2 ---------------------*/ 
  servo2Pos = (180-elbo-90);
  elb_servo.write(servo2Pos, SERVO_SPEED, true);
  /*--------------------- servo 3 ---------------------*/
  servo3Pos = wrist_ud+90;
  wri_servo.write(servo3Pos, SERVO_SPEED, true);
  /*--------------------- servo 4 ---------------------*/ 
  servo4Pos = wrist_turn+90;
  wro_servo.write(servo4Pos, SERVO_SPEED, true);
  /*--------------------- servo 5 ---------------------*/ 
  servo5Pos = gripper+90;
  gri_servo.write(servo5Pos, SERVO_SPEED, true);

  Serial.print('a');
  Serial.print(base);
  Serial.print('b');
  Serial.print(shoulder);
  Serial.print('c');
  Serial.print(elbo);
  Serial.print('d');
  Serial.print(wrist_ud);
  Serial.print('e');
  Serial.print(wrist_turn);
  Serial.print('f');
  Serial.print(gripper);
  Serial.println('g');

}

/*============================= arduino functions ===========================*/ 

void setup() {

  // radio setup
  radio.begin();
  radio.openWritingPipe(address);
  radio.setPALevel(RF24_PA_MIN);
  radio.stopListening();  
 
  // serial setup
  Serial.begin(9600);
  Serial.println("cobit robot arm controller v1.0");

  // start radio 
  radio.begin();
  radio.openReadingPipe(0, address);
  radio.setPALevel(RF24_PA_MAX);
  radio.startListening(); 

  // Servo setup 
  bas_servo.attach(2);
  shl_servo.attach(3);
  elb_servo.attach(4);
  wri_servo.attach(5);
  wro_servo.attach(6);
  gri_servo.attach(9);

  // robot home position 
  reset_arm_position();
  
  delay(2000);
}

void loop() {

  char inCommand;
  int intCommand;

  // radio input 
  if (radio.available()) {
    radio.read(&rf_rx_buffer, sizeof(rf_rx_buffer));

    // reset robot 
    if(rf_rx_buffer[0] == CMD_RESET_ROBOT){
      run_robot_flag = false;
      reset_robot();

    // move robot 
    }else if(rf_rx_buffer[0] == CMD_MOVE_ROBOT_JOY){
      if(run_robot_flag == false){
        move_robot();
      }
    
    }else if(rf_rx_buffer[0] == CMD_STOP_ROBOT){
      run_robot_flag = false;
      stop_robot_btn();

    }else if(rf_rx_buffer[0] == CMD_SAVE_POS){
      run_robot_flag = false;
      save_pos_btn();
     
    }else if(rf_rx_buffer[0] == CMD_RUN_ROBOT){
      run_robot_btn();
    }
  }
 
  // serial input 
  String inString = "";
  if(Serial.available()>0){
    
    inString = Serial.readStringUntil('\n');
    inCommand = inString[0];
    intCommand = inCommand - 0x30;
    //Serial.println(intCommand);

    // run robot  
    if(intCommand == CMD_RUN_ROBOT){ 
      if(run_robot_flag == false){
        run_robot_flag = true;
        current_index = 0;
      }    
    // reset robot 
    }else if(intCommand == CMD_RESET_ROBOT){   
      run_robot_flag = false;
      current_index = 0;
      reset_robot();
    // move robot 
    }else if(intCommand == CMD_MOVE_ROBOT_SERIAL){
      if(run_robot_flag == false){
        move_robot_serial(inString);
      }
    // Save position
    }else if(intCommand == CMD_SAVE_POS){
      if(run_robot_flag == false){
        save_pos_serial(inString);
      }
    // Clear position
    }else if(intCommand == CMD_CLEAR_POS){
      if(run_robot_flag == false){
        clear_pos_serial();
      }
    // move robot with 6 servo at the same time 
    }else if(intCommand == CMD_MOVE_ROBOT_6LINK){
      if(run_robot_flag == false){
        move_robot_6link(inString);
      }
    // Clear position
    }else if(intCommand == CMD_STOP_ROBOT){
      stop_robot();
  }

  if(run_robot_flag == true){
    run_robot();
    current_index++;
    if(current_index > save_index){
      current_index = 0;
    }
  }
}
