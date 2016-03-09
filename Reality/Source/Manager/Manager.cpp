#include <iostream>
#include "Manager.h"
#include "Emotes.h"
#include "Movement.h"

using namespace std;

int manager_processPacket(string packetData, char responseToClient[],
		int *responseLength, float*x, float*y, float*z) {

	if(isMovementPacket(packetData,x,y,z))
		return 0;

	if (isEmotePacket(packetData, responseToClient, responseLength, x, y, z))
		return 1;
	return 0;
}
