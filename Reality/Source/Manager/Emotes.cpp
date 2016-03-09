/*
 *  Created on: 12/10/2009
 *      Author: Morpheus
 */


#include <iostream>
#include <stdio.h>
#include <string.h>

#include "Emotes.h"
#include "EmoteList.h"

using namespace std;

char moodAnswer[10] = { 0x02, 0x03, 0x02, 0x00, 0x01, 0x01, 0x00, 0x01, 0x00,
		0x00 };
char emoteAnimationResponse[32]={0x02 ,0x03 ,0x02 ,0x00 ,0x01 ,0x28 ,0x03 ,0x40 ,0x00 ,0x25 ,0x01 ,0x00 ,0x00 ,0x10 ,0xae ,0x88 ,0x84 ,0xc7 ,0x00 ,0x00 ,0xbe ,0x42 ,0xa9 ,0xc0 ,0x7d ,0x46 ,0x2a ,0x9f ,0x1e ,0x20 ,0x00 ,0x00};

unsigned int lastEmote=0x00;

void copyData(char *source, char *end, int quantity) {
	int pos = 0;		
	for (pos = 0; pos < quantity; pos++) {
		end[pos] = source[pos];
	}
}


int isEmoteAnimationRequest(string packet,int pointer) {

	if(!initialized()){
		initializeEmoteList();
	}

	cout<<"getting key"<<endl;
	string key;
	char id [5]= {packet[pointer],packet[pointer+1],packet[pointer+2],packet[pointer+3],'\0'};
	key = id;

	int result = getEmoteCode(key);

	cout <<"result: "<<result<<endl;
	if (result >0 && result <240){
		emoteAnimationResponse[10]=result;
		return 1;
	}

	return 0;
}

int isEmotePacket(string packet, char *response, int * responseLength, float*x,float*y,float*z) {

	string::size_type loc = packet.find("\x02\x04\x01\x00", 0);

	/* check if it's protocol 04 */
	if (loc != std::string::npos) {

		/* point to the first byte with info for protocol 04*/
		int pointer = loc + 5;

		if (packet[pointer] == '\x01') {
			switch (packet[pointer + 1]) {

			case '\x02':

				//Animation or mood
				if (packet[pointer + 2] == '\x33') { //Stop animation
					moodAnswer[6] = '\00';
					copyData(moodAnswer, response, 10);
					*responseLength = 10;
					return 1;
				}

				if (packet[pointer + 2] == '\x34') { //ID animation
					moodAnswer[6] = packet[pointer + 3];
					copyData(moodAnswer, response, 10);
					*responseLength = 10;
					return 1;
				}

				if (packet[pointer + 2] == '\x35') { //ID mood
					moodAnswer[7] = packet[pointer + 3];
					copyData(moodAnswer, response, 10);
					*responseLength = 10;
					return 1;
				}

				break;

			case '\x09':
				/* Maybe it's an emote. Checking */
				if (packet[pointer + 2] == '\x30')
					if (isEmoteAnimationRequest(packet,pointer+3)) {
						lastEmote = lastEmote+0x01;
						if(lastEmote>=0xfe)
							lastEmote=0x00;
						emoteAnimationResponse[6]= lastEmote;
						memcpy(&emoteAnimationResponse[14], x,4);
						memcpy(&emoteAnimationResponse[18], y,4);
						memcpy(&emoteAnimationResponse[22], z,4);
						copyData(emoteAnimationResponse, response, 32);
						*responseLength = 32;
						return 1;
					}

				break;
			}
			return 0;
		}
		return 0;
	}

	return 0;
}
