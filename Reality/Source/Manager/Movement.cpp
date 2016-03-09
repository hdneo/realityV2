/*
 * Movement.cpp
 *
 *  Created on: 18/10/2009
 *      Author: Pahefu
 */

#include "Movement.h"

#include <sstream>
#include <iostream>
#include <stdio.h>
#include <string.h>

using namespace std;

int isMovementPacket(string packet, float*x, float*y, float*z) {

	string::size_type loc = packet.find("\x02\x03\x02\x00\x01", 0);

	/* check if it's protocol 03 for movement */
	if (loc != std::string::npos) {

		/* point to the first byte with info for movement */
		int pointer = loc + 5;
		switch(packet[pointer]){
			case '\x08':
				pointer++;

				memcpy(x, &packet[pointer], 4);
				memcpy(y, &packet[pointer + 4], 4);
				memcpy(z, &packet[pointer + 8], 4);
				return 1;
			break;
			
			case '\x0a':
				pointer = pointer + 2;
				memcpy(x, &packet[pointer], 4);
				memcpy(y, &packet[pointer + 4], 4);
				memcpy(z, &packet[pointer + 8], 4);
				return 1;
			break;

			default:
				return 0;
			break;
		}

		
		return 0;
	}

	return 0;
}
