/*
 *  Created on: 12/10/2009
 *  Author: Morpheus
 *
 *  Description:
 *
 *  Stores most packet code to operate with mood & emote commands.
 *	Mostly just comparison and reply with the right answer ;)
 */
#ifndef EMOTES_H_
#define EMOTES_H_

#include <string>
using namespace std;


int isEmoteAnimation(string packet);
int isEmotePacket(string packet, char *response, int *responseLength ,float*x,float*y,float*z);

void copyData(char *source, char *end, int quantity);



#endif /* EMOTES_H_ */
