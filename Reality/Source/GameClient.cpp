// *************************************************************************************************
// --------------------------------------
// Copyright (C) 2006-2010 Rajko Stojadinovic
// Modified 2009 John Kussack
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

#include "Common.h"
#include "Log.h"
#include "GameClient.h"
#include "Timer.h"
#include "GameResponses.h"
#include "Util.h"
#include "MersenneTwister.h"
#include "EncryptedPacket.h"
#include "SequencedPacket.h"
#include "RsiData.h"
#include "Manager/Manager.h"

using namespace std;

#pragma pack(1)

uint8 twofishkeyz[16] = { 0x6C, 0xAB, 0x8E, 0xCC, 0xE7, 0x3C, 0x22, 0x47, 0xDB,
		0xEB, 0xDE, 0x1A, 0xA8, 0xE7, 0x5F, 0xB8 };

GameClient::GameClient(struct sockaddr_in address, SOCKET *sock, uint32 id) {

	_sock = sock;
	_address = address;
	server_sequence = 0;
	client_sequence = 0;
	numPackets = 0;
	PlayerSetupState = 0;
	_id = id;

	uint8 hax[CryptoPP::Twofish::BLOCKSIZE];
	memset(hax, 0, CryptoPP::Twofish::BLOCKSIZE);
	TFDecrypt = new CryptoPP::CBC_Mode<CryptoPP::Twofish>::Decryption(
			twofishkeyz, CryptoPP::Twofish::DEFAULT_KEYLENGTH, hax);
	TFEncrypt = new CryptoPP::CBC_Mode<CryptoPP::Twofish>::Encryption(
			twofishkeyz, CryptoPP::Twofish::DEFAULT_KEYLENGTH, hax);
	Valid_Client = true;
	Handled_Session = false;

	uint32 random = sRand.randInt(999999);
	stringstream lol;
	lol << "lolcharacter";
	MyData.name = lol.str();

	cout << "Initialized name" << endl;
}

GameClient::~GameClient() {
	delete TFDecrypt;
	delete TFEncrypt;

}

uint32 GameClient::getID() {

	return _id;
}

void GameClient::HandlePacket(char *pData, uint16 nLength) {
	_last_activity = getTime();
	numPackets++;

	if (Handled_Session == true && pData[0] != 0x01) // Ping...just reply with the same thing
	{
		int clientlen = sizeof(_address);
		sendto(*_sock, pData, nLength, 0, (struct sockaddr*) &_address,
				clientlen);
	} else {
		if (pData[0] == 0x01) { // encrypted packet
			SequencedPacket packetData = Decrypt(&pData[1], nLength - 1);
			client_sequence = packetData.getLocalSeq();

			cout << "CSeq: " << packetData.getLocalSeq() << " SSeq: "
					<< packetData.getRemoteSeq();
			cout << " " << Bin2Hex(packetData) << endl;

			string contents = string(packetData.contents(), packetData.size());

			string::size_type loc = contents.find("Spawnalot", 0);
			if (loc != std::string::npos) {
				if (PlayerSetupState == 0x7F)
					Send(ByteBuffer(rawData, sizeof(rawData)));
				else {
				} //WTF
				return;
			}

			if (manager_processPacket(contents, responseToClient,
					&responseLength, &MyData.coordXF, &MyData.coordYF,
					&MyData.coordZF)) {
				Send(ByteBuffer(responseToClient, responseLength));
				return;
			}

		}

		if (numPackets < 10)
			switch (numPackets) {
			case 1: {
				cout << "Initializing p1" << endl;
				DEBUG_LOG("First unecrypted Packet received |%s|",Bin2Hex(pData).c_str());
				for (unsigned int i = 0; i < 5; i++) {
					int clientlen = sizeof(_address);
					sendto(*_sock, (const char *) GAMEResponseTo1_1_2_3_4_5,
							sizeof(GAMEResponseTo1_1_2_3_4_5), 0,
							(struct sockaddr*) &_address, clientlen);
				}

				Send(ByteBuffer(GAMEResponseTo1_6, sizeof(GAMEResponseTo1_6)));
				Send(ByteBuffer(GAMEResponseTo1_7, sizeof(GAMEResponseTo1_7)));
				Send(ByteBuffer(GAMEResponseTo1_8, sizeof(GAMEResponseTo1_8)));
				Send(ByteBuffer(GAMEResponseTo1_9, sizeof(GAMEResponseTo1_9)));
				Send(ByteBuffer(GAMEResponseTo1_10, sizeof(GAMEResponseTo1_10)));
				Send(ByteBuffer(GAMEResponseTo1_11, sizeof(GAMEResponseTo1_11)));
				Send(ByteBuffer(GAMEResponseTo1_12, sizeof(GAMEResponseTo1_12)));
				Send(ByteBuffer(GAMEResponseTo1_13, sizeof(GAMEResponseTo1_13)));
				Send(ByteBuffer(GAMEResponseTo1_14, sizeof(GAMEResponseTo1_14)));
				Send(ByteBuffer(GAMEResponseTo1_15, sizeof(GAMEResponseTo1_15)));
				Send(ByteBuffer(GAMEResponseTo1_16, sizeof(GAMEResponseTo1_16)));
				Send(ByteBuffer(GAMEResponseTo1_17, sizeof(GAMEResponseTo1_17)));
				Send(ByteBuffer(GAMEResponseTo1_18, sizeof(GAMEResponseTo1_18)));
				Send(ByteBuffer(GAMEResponseTo1_19, sizeof(GAMEResponseTo1_19)));
				Send(ByteBuffer(GAMEResponseTo1_20, sizeof(GAMEResponseTo1_20)));
				break;
			}
			case 2: {
				cout << "Initializing p2" << endl;
				PlayerSetupState = 1;
				Send(ByteBuffer(GAMEResponseTo2, sizeof(GAMEResponseTo2)));
				break;
			}
			case 5: {
				cout << "Initializing p5" << endl;
				Send(ByteBuffer(GAMEResponseTo5, sizeof(GAMEResponseTo5)));
				break;
			}
			case 6: {
				cout << "Initializing p6" << endl;
				PlayerSetupState = 0x1F;

				byte GAMEResponseTo6_1Modified[200];
				memcpy(GAMEResponseTo6_1Modified, GAMEResponseTo6_1,
						sizeof(GAMEResponseTo6_1Modified));

				byte *nameInPacket = &GAMEResponseTo6_1Modified[0x55];
				memset(nameInPacket, 0, 32);
				memcpy(nameInPacket, MyData.name.c_str(), MyData.name.length()
						+ 1);

				/*double playerX,playerY,playerZ;
				 playerX = 27800;
				 playerY = -5;
				 playerZ = -11700;*/
				memcpy(&GAMEResponseTo6_1Modified[0x92], &MyData.coordX,
						sizeof(MyData.coordX));
				memcpy(&GAMEResponseTo6_1Modified[0x9A], &MyData.coordY,
						sizeof(MyData.coordY));
				memcpy(&GAMEResponseTo6_1Modified[0xA2], &MyData.coordZ,
						sizeof(MyData.coordZ));

				//change rsi data
				byte *rawPointer = &GAMEResponseTo6_1Modified[0x80];

				//load
				RsiDataMale playerRsi; //change this to RsiDataFemale if you want a girl
				playerRsi.FromBytes(rawPointer, 13);
				//read/modify
				//read RsiData.h for a list of all the parameters
				playerRsi["Sex"] = 0; //also change this to 1 if you want a girl
				playerRsi["Shirt"] = 2;
				playerRsi["ShirtColor"] = 14;
				playerRsi["Body"] = 2;
				playerRsi["Hat"] = 10;
				playerRsi["Pants"] = 2;
				playerRsi["PantsColor"] = 13;
				playerRsi["Hair"] = 5;
				playerRsi["Glasses"] = 7;
				playerRsi["Coat"] = 3;
				playerRsi["CoatColor"] = 10;
				//save
				playerRsi.ToBytes(rawPointer, 13);

				Send(ByteBuffer(GAMEResponseTo6_1Modified,
						sizeof(GAMEResponseTo6_1Modified)));
				Send(ByteBuffer(GAMEResponseTo6_2, sizeof(GAMEResponseTo6_2)));
				Send(ByteBuffer(GAMEResponseTo6_4, sizeof(GAMEResponseTo6_4)));
				Send(ByteBuffer(GAMEResponseTo6_6, sizeof(GAMEResponseTo6_6)));
				break;
			}
			case 9: {
				cout << "Initializing p9" << endl;
				PlayerSetupState = 0x7F;
				Send(std::string((const char *) GAMEResponseTo9_2,
						sizeof(GAMEResponseTo9_2)));
				Handled_Session = true;
				break;
			}
			}

		if (Handled_Session) {
			Send(std::string((const char *) GAMEResponseTo9_2,
					sizeof(GAMEResponseTo9_2)));
		}
	}
}

SequencedPacket GameClient::Decrypt(char *pData, uint16 nLength) {
	EncryptedPacket decryptedData(ByteBuffer(pData, nLength), TFDecrypt);
	return SequencedPacket(decryptedData);
}

void GameClient::Send(const ByteBuffer &contents) {
	if (!TFEncrypt)
		return;

	server_sequence++;

	if (server_sequence == 4096)
		server_sequence = 0;

	SequencedPacket withSequences(server_sequence, client_sequence,
			PlayerSetupState, contents);
	EncryptedPacket withEncryption(withSequences.getDataWithHeader());
	ByteBuffer sendMe;
	sendMe << uint8(1);
	sendMe.append(withEncryption.toCipherText(TFEncrypt));

	int clientlen = sizeof(_address);
	sendto(*_sock, sendMe.contents(), (int) sendMe.size(), 0,
			(struct sockaddr*) &_address, clientlen);
}
