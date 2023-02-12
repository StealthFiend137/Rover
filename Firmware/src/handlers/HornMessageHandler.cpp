#include "MessageHandlerBase.cpp"

namespace MessageHandlers
{
    class HornMessageHandler : MessageHandlerBase
    {
    private:
        int pinNumber;

    public:
        HornMessageHandler(int pinNumber) : pinNumber(pinNumber)
        {
        };

        void handle(const StaticJsonDocument<200> doc) 
        {
            if(doc["h"])
            {
                tone(D2, 300);
            }
            else
            {
                noTone(D2);
            }
        };
    };
}
