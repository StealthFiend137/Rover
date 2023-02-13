#include "MessageHandlerBase.cpp"

namespace MessageHandlers
{
    class MovementMessageHandler : MessageHandlerBase
    {
    private:
        int leftForwardPin;
        int leftReversePin;
        int leftSpeedPin;
        int rightForwardPin;
        int rightReversePin;
        int rightSpeedPin;

        int *leftSpeedPtr = new int(0);
        int *rightSpeedPtr = new int(0);

        void calculateSpeeds(const float radians, const float magnitude, int* leftSpeedPtr, int* rightspeedPtr)
        {
            //*leftSpeedPtr = map(magnitude * cos(radians), 0, 100, -255, 255);;
            //*rightSpeedPtr = map(magnitude * sin(radians), 0, 100, -255, 255);

            float x = magnitude * cos(radians);
            float y = magnitude * sin(radians);

            // Serial.println("Radians: " + String(radians) + " Magnitude:" + String(magnitude) + "x:" + String(x) + " y:" + String(y));

            const float MAX_SPEED = 255.0f;
            *leftSpeedPtr = (y * MAX_SPEED - x * MAX_SPEED / 2.0f);
            *rightSpeedPtr = -(y * MAX_SPEED + x * MAX_SPEED / 2.0f);
            
            Serial.println("Left Speed: " + String(*leftSpeedPtr) + " Right Speed: " + String(*rightspeedPtr));
        }

        void setLeftSpeed(int speed)
        {
            int isForwards = speed >= 0 ? HIGH : LOW;
            digitalWrite(leftForwardPin, isForwards);
            digitalWrite(leftReversePin, !isForwards);
            analogWrite(leftSpeedPin, abs(speed));
        };

        void setRightspeed(int speed)
        {
            int isForwards = speed >= 0 ? HIGH : LOW;
            digitalWrite(rightForwardPin, isForwards);
            digitalWrite(rightReversePin, !isForwards);
            analogWrite(rightSpeedPin, abs(speed));
        }

    public:
        MovementMessageHandler(int leftForwardPin, int leftReversePin, int leftSpeedPin, int rightForwardPin, int rightReversePin, int rightSpeedPin) :
            leftForwardPin(leftForwardPin), leftReversePin(leftReversePin), leftSpeedPin(leftSpeedPin),
            rightForwardPin(rightForwardPin), rightReversePin(rightReversePin), rightSpeedPin(rightSpeedPin) {

            pinMode(leftForwardPin, OUTPUT);
            pinMode(leftReversePin, OUTPUT);
            pinMode(leftSpeedPin, OUTPUT);

            pinMode(rightForwardPin, OUTPUT);
            pinMode(rightReversePin, OUTPUT);
            pinMode(rightSpeedPin, OUTPUT);
        };

        ~MovementMessageHandler() {
            delete leftSpeedPtr;
            leftSpeedPtr = nullptr;
            delete rightSpeedPtr;
            rightSpeedPtr = nullptr;
        }

        void handle(const StaticJsonDocument<200> doc) {          
            int leftSpeed = 0;
            int rightSpeed = 0;

            {
                float r = doc["r"];
                float m = doc["m"];

                calculateSpeeds(r, m, leftSpeedPtr, rightSpeedPtr);
                leftSpeed = *leftSpeedPtr;
                rightSpeed = *rightSpeedPtr;
            }
            
            setLeftSpeed(leftSpeed);
            setRightspeed(rightSpeed);
        };
    };
}
