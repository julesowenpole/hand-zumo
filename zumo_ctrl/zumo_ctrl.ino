#include <ZumoMotors.h>

ZumoMotors motors;

void setup() {
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    if (cmd.startsWith("S")) {
      // Stop
      motors.setSpeeds(0, 0);

    } else if (cmd.startsWith("F")) {
      // Forward with left,right speeds
      // Format: "F,leftSpeed,rightSpeed"
      int firstComma  = cmd.indexOf(',');
      int secondComma = cmd.indexOf(',', firstComma + 1);

      int leftSpeed  = cmd.substring(firstComma + 1, secondComma).toInt();
      int rightSpeed = cmd.substring(secondComma + 1).toInt();

      motors.setSpeeds(leftSpeed, rightSpeed);
    }
  }
}