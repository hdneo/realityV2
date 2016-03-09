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

//include a unit test at the very top if you want to run it

#ifndef UNITTEST
#include "Common.h"
#include "Master.h"
#include "Util.h"
#include "Crypto.h"
#include <iostream>
#endif

int main()
{
#ifndef UNITTEST
	Master::getSingleton().Run();
#else
	runTest();
	for(;;){Sleep(10000);}
#endif

	return 0;
}
