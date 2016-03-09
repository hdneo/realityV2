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

#include "Common.h"
#include "Log.h"
#include "ConsoleThread.h"
#include "Util.h"
#include "Master.h"
#include "Crypto.h"
#include "GameServer.h"
#include "AuthServer.h"

bool ConsoleThread::run()
{
	SetThreadName("Console Thread");

	for (;;) 
	{
		string command;
		cin >> command;

		if (strcmp(command.c_str(), "exit") == 0)
		{
			Master::m_stopEvent = true;
			INFO_LOG("Got exit command. Shutting down...");
			break;
		}
		else if (strcmp(command.c_str(),"register") == 0)
		{
			string theLine;
			getline(cin,theLine);
			stringstream lineParser;
			lineParser.str(theLine);
			string username,password;
			lineParser >> username;
			lineParser >> password;

			bool accountCreated = sAuth.CreateAccount(username,password);
			if (accountCreated)
				INFO_LOG("Created account with username %s password %s",username.c_str(),password.c_str());
		}
		else if (strcmp(command.c_str(), "send") == 0)
		{
			stringstream hexStream;
			for (;;)
			{
				string word;
				cin >> word;

				string::size_type semicolonPos = word.find_first_of(";");
				if (semicolonPos != string::npos)
				{
					word = word.substr(0,semicolonPos);
					if (word.length() > 0)
					{
						hexStream << word;
					}
					break;
				}
				else
				{
					hexStream << word;
				}
			}

			string binaryOutput;
			try
			{
				CryptoPP::HexDecoder hexDecoder(new CryptoPP::StringSink(binaryOutput));
				hexDecoder.Put((const byte*)hexStream.str().data(),hexStream.str().size(),true);
				hexDecoder.MessageEnd();
			}
			catch (...)
			{
				cout << "Invalid hex string" << endl;		
				continue;
			}
			sGame.Broadcast(ByteBuffer(binaryOutput));
			cout << "OK" << endl;
		}
	}

	return true;
}