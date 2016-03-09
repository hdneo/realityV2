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

#ifndef MXOSIM_AUTHSERVER_H
#define MXOSIM_AUTHSERVER_H

#include "Singleton.h"
#include "AuthHandler.h"
#include "AuthSocket.h"
#include "Crypto.h"
#include "ByteBuffer.h"

#include <Sockets/ListenSocket.h>

class AuthServer : public Singleton <AuthServer>
{
public:
	AuthServer();;
	~AuthServer();;
	void Start();
	void Stop();
	void Loop();
	string Encrypt(string input);
	string Decrypt(string input);
	ByteBuffer SignWith1024Bit(byte *message,size_t messageLen);
	bool VerifyWith1024Bit(byte *message,size_t messageLen,byte *signature,size_t signatureLen);
	ByteBuffer GetPubKeyData();
	string HashPassword(const string& salt, const string& password);
	bool CreateAccount(const string& username,const string& password);
private:
	void GenerateRSAKeys(unsigned int keyLen,CryptoPP::RSA::PublicKey &publicOutput, CryptoPP::RSA::PrivateKey &privateOutput);
	void GenerateSignKeys(string &privKeyOut, string &pubKeyOut);
	void LoadSignKeys();
	ByteBuffer MessageFromPublicKey(CryptoPP::RSA::PublicKey &inputKey);
	void GenerateCryptoKeys(string &privKeyOut, string &pubKeyOut);
	void LoadCryptoKeys();

	string MakeSHA1HashHex(const string& input);
	string GenerateSalt(uint32 length);

	AuthHandler authSocketHandler;
	typedef ListenSocket<AuthSocket> AuthListenSocket;
	AuthListenSocket *listenSocketInst;

	CryptoPP::AutoSeededRandomPool randPool;

	auto_ptr<CryptoPP::RSAES_OAEP_SHA_Decryptor> rsaDecryptor;
	auto_ptr<CryptoPP::RSAES_OAEP_SHA_Encryptor> rsaEncryptor;
	auto_ptr<CryptoPP::Weak::RSASSA_PKCS1v15_MD5_Signer> signer1024bit;
	auto_ptr<CryptoPP::Weak::RSASSA_PKCS1v15_MD5_Verifier> verifier1024bit;
	auto_ptr<CryptoPP::Weak::RSASSA_PKCS1v15_MD5_Signer> signer2048bit;
	auto_ptr<CryptoPP::Weak::RSASSA_PKCS1v15_MD5_Verifier> verifier2048bit;

	CryptoPP::Integer pubKeyModulus;
	vector<byte> pubKeySignature;
};


#define sAuth AuthServer::getSingleton()

#endif

