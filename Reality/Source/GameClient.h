// *************************************************************************************************
// --------------------------------------
// Copyright (C) 2006-2010 Rajko Stojadinovic
//
//
// This program is free software; you can redistribute it and/or
// modify it under the terms of the GNU Lesser General Public
// License as published by the Free Software Foundation; either
// version 2.1 of the License, or (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
// Lesser General Public License for more details.
//
// You should have received a copy of the GNU Lesser General Public
// License along with this library; if not, write to the Free Software
// Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
//
// *************************************************************************************************

#ifndef MXOSIM_GAMECLIENT_H
#define MXOSIM_GAMECLIENT_H

#include "Crypto.h"
#include "SequencedPacket.h"
#include "Sockets.h"

class GameClient
{
	private:
		// Valid Client + Anti-Flood bool
		bool Valid_Client;
		bool Handled_Session;

		// Master Sock handle, client's address structure, last received packet
		SOCKET *_sock;
		struct sockaddr_in _address;
		uint32 _last_activity;

		//Number of packets received
		uint32 numPackets;

		// Sequences
		uint8 PlayerSetupState;
		uint16 server_sequence;
		uint16 client_sequence;

		// Client tick count
		uint32 tick;

		//Player name lol
		//string name;

		CryptoPP::CBC_Mode<CryptoPP::Twofish>::Decryption *TFDecrypt;
		CryptoPP::CBC_Mode<CryptoPP::Twofish>::Encryption *TFEncrypt;

		//Client "unique" ID based on +1 each connection
		uint32 _id;
		
		//Client last action has to be broadcasted?

		char coordX[5];
		char coordY[5];
		char coordZ[5];

		//Client data stored on struct
		struct Data {
		   string name;
		   uint16 minSpawnValue;
		   uint8 health;
		   uint8 inner;
		   uint8 level;
		   double coordX;
		   double coordY;
		   double coordZ;
		   float coordXF;
		   float coordYF;
		   float coordZF;
		   uint8 rotation;
		   Data(){

		   		rotation=0;
		   		coordX = 27800;
				coordY = -5;
				coordZ = -11700;
				coordXF = 27800;
				coordYF = -5;
				coordZF = -11700;
		   }
		} MyData;

		char responseToClient[4096];
		int responseLength;
		char broadcastResponse[4096];
		int broadcastLength;
		bool isBroadcast;


	public:
		
		GameClient(sockaddr_in address, SOCKET *sock,uint32 id);
		~GameClient();

		inline uint32 LastActive() { return _last_activity; }
		inline bool IsValid() { return Valid_Client; }
		char *Address() { return inet_ntoa(_address.sin_addr); }

		void HandlePacket(char *pData, uint16 Length);
		SequencedPacket Decrypt(char *pData, uint16 nLength);
		void Send(const ByteBuffer &contents);

		/* Multiplayer update */

		uint32 getID();



private:
		typedef enum 
		{
			SET_HATS,
			SET_FACES,
			SET_GLASSES,
			SET_HAIRS,
			SET_SHIRTS,
			SET_FACIALDETAILS,
			SET_LEGGINGS,
			SET_SHIRTCOLORS,
			SET_PANTSCOLORS,
			SET_COATS,
			SET_PANTS,
			SET_SHOES,
			SET_GLOVES,
			SET_COATCOLORS,
			SET_HAIRCOLORS,
			SET_SKINTONES,
			SET_TATTOOS,
			SET_FACIALDETAILCOLORS,
			SET_SHOECOLORS,
			SET_GLASSESCOLORS
		}WhatToSet;

		void SpawnTroop(int rows, int columns,WhatToSet typeToSet);
};

#endif
