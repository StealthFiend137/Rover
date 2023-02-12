#ifndef MESSAGEHANDLERBASE_CPP
#define MESSAGEHANDLERBASE_CPP

#include <ArduinoJson.h>

namespace MessageHandlers
{
    class MessageHandlerBase
    {
    public:
        virtual void handle(const StaticJsonDocument<200> doc) = 0;
    };
}

#endif