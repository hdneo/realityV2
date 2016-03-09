//"c:\WINDOWS\Microsoft.NET\Framework\v2.0.50727\csc.exe /out:c:\01mainframe.exe /target:exe c:\01mainframe.cs"

// @author Bayamos
// This is some base code for automatically querying a remote server to see if a URL exists.
// You can easily mod this for separate purposes - i.e. add a for loop cycling through ints
// and chars, and search for 01mainframe KYEO map .gifs. Or autovote in online polls. The
// concept is the same.

using System;
using System.Collections.Generic;
using System.Text;
using System.IO;
using System.Net;

namespace URLBot
{
    class BotApp
    {
        private const string URL = "http://01mainframe.com/z11/sk397m/phasmata_";
	private const string EXT = ".html";

        static void Main(string[] args)
        {
            Console.WriteLine("Enter any key to start:");
            string key = Console.ReadLine();	
	    StreamReader sr = new StreamReader(@"C:\Wordlist.txt"); // put your wordlist here
	    String strLine;
	    Console.WriteLine("Quering 01mainframe. Silent mode to maximize speed.");
	    
	    while( (strLine = sr.ReadLine()) != null)
	    {
		// Console.WriteLine(URL + strLine + EXT);
		HTTPGet(URL + strLine + EXT);
	    }
	    Console.WriteLine("All done!");
	    sr.Close();
	    Console.ReadLine(); // keep program window open

        }

        private static void HTTPGet(string url)
        {
	    StreamWriter sw = new StreamWriter(@"C:\output.txt", true);
	    try
	    {
		HttpWebRequest HttpWReq = (HttpWebRequest)WebRequest.Create(url);
		HttpWebResponse HttpWResp = (HttpWebResponse)HttpWReq.GetResponse();
	        // Console.WriteLine(HttpWResp.StatusCode);
		sw.Write(url + "\r\n");
		sw.Write(HttpWResp.StatusCode + "\r\n");
	    }
	    catch(Exception e)
	    {
		sw.Write(url + "\r\n");
		sw.Write(e + "\r\n");
	    }
	    sw.Close();
        }
    }
} 
