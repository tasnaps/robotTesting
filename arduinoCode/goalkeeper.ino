int trigPin = 12;      // Trig Pin Of HC-SR04
int echoPin = 11;     // Echo Pin Of HC-SR04
int echoPin_2 = 10;
int trigPin_2 = 9;
int r_m1 = 4; // Motor Pins
int r_m2 = 5;
int l_m1 = 8;
int l_m2 = 7;
float duration;
float front_dist;
float duration_2;
float back_dist;

void setup() {
  pinMode(trigPin, OUTPUT);         // set trig pin as output
  pinMode(echoPin, INPUT);          //set echo pin as input to capture reflected waves
  pinMode(trigPin_2, OUTPUT);      
  pinMode(echoPin_2, INPUT);        
  digitalWrite(trigPin, LOW);
  digitalWrite(trigPin_2, LOW);

Serial.begin(9600);
  pinMode(r_m1, OUTPUT);    　　　 // set Motor pins as output
  pinMode(r_m2, OUTPUT);
  pinMode(l_m1, OUTPUT);
  pinMode(l_m2, OUTPUT);
  digitalWrite(r_m1, LOW);
  digitalWrite(r_m2, LOW);
  digitalWrite(l_m1, LOW);
  digitalWrite(l_m2, LOW);

}

void loop() {
  cal_forward_dist();
  Serial.print("front_distance");
  cal_backward_dist();
  Serial.print("back_distance");

  if ((front_dist > 9) && (front_dist < 15)){
    Serial.print("forward");
    forward();
  }

  if ((front_dist < 9) && (front_dist > 15)){
    stop_m();
  }
// if object go far alway
  if ((front_dist > 15) && (back_dist < 15)){
    Serial.print("backward");
    backward();
  }
  if ((front_dist < 15) && (back_dist > 15)){
    forward();
  }
// if no object close by
  if (back_dist < 9) {
    stop_m();
    Serial.print("Stop");
  }
  if (front_dist < 9){
    stop_m();
  }

  delay(500);

}

void cal_forward_dist(){
  digitalWrite(trigPin, HIGH);      // send waves for 10 us
  delayMicroseconds(10);               
  digitalWrite(trigPin,LOW );
  duration =pulseIn(echoPin, HIGH);   // receive reflected waves
  front_dist = duration*0.0343/2;     // // convert to distance
}

void cal_backward_dist(){
  digitalWrite(trigPin_2, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin_2, LOW);
  duration_2 = pulseIn(echoPin_2, HIGH);
  back_dist = duration_2*0.0343/2;

}

void stop_m(){
  digitalWrite(r_m1, LOW);
  digitalWrite(r_m2, LOW);
  digitalWrite(l_m1, LOW);
  digitalWrite(l_m2, LOW);

}

void backward(){
  Serial.print("backward");
  Serial.println();
  digitalWrite(r_m1, LOW);
  digitalWrite(r_m2, HIGH);
  digitalWrite(l_m1, LOW);
  digitalWrite(l_m2, HIGH);

}

void forward(){
  Serial.print("forward");
  digitalWrite(r_m1, HIGH);
  digitalWrite(r_m2, LOW);
  digitalWrite(l_m1, HIGH);
  digitalWrite(l_m2, LOW);
}