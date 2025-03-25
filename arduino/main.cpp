#include <Servo.h>

#define TRIG_PIN 7   // Пин триггера
#define ECHO_PIN 8   // Пин эха
#define SERVO_PIN 6  // Пин сервомотора
#define LED_PIN 3    // Пин светодиода

Servo servo;

void setup() {
    pinMode(TRIG_PIN, OUTPUT);
    pinMode(ECHO_PIN, INPUT);
    pinMode(LED_PIN, OUTPUT);
    servo.attach(SERVO_PIN);
    Serial.begin(9600);
}

long getDistance() {
    digitalWrite(TRIG_PIN, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIG_PIN, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG_PIN, LOW);
    
    long duration = pulseIn(ECHO_PIN, HIGH);
    long distance = duration * 0.034 / 2; 
    return distance;
}

void loop() {
    long distance = getDistance();  
    Serial.print("Distance: ");
    Serial.print(distance);
    Serial.println(" cm");

    int angle = map(distance, 0, 300, 0, 180); 
    angle = constrain(angle, 0, 180);         
    servo.write(angle);                        

    if (distance < 10) {
        digitalWrite(LED_PIN, HIGH);
    } else {
        digitalWrite(LED_PIN, LOW);
    }

    delay(500);  
}
