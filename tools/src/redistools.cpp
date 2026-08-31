#include <stdlib.h>
#include <stdlib.h>
#include <iostream>
#include "hiredis.h"
#include <bson/bson.h>
#include "common_utils.h"


using namespace std;
using namespace bson;


int  main(int argc, char **argv)
{
	if(argc<4 || strcasecmp(argv[1],"HELP")==0)
	{
		cout << "Usage: " << argv[0] << " ip port key" << endl;
		exit(0);
	} 
    
	std::string ip = argv[1];
	int  port = atoi(argv[2]);
	std::string key = argv[3];
	if ( argc >= 5 )
	{
	    std::string field = argv[4];
	}

	redisContext *m_pRedisContext;
    m_pRedisContext = redisConnect(ip.c_str(), port );
    if ( m_pRedisContext == NULL )                          
	{
	    cout << "context null" << endl;
		return 0;
	}
	sleep(0.1);
	
	cout <<"getting key:"<<key<<" from :"<<ip<<","<<port<<endl;

	redisReply *reply = (redisReply*)redisCommand(m_pRedisContext,"HGETALL %s", key.c_str() );
	if ( reply != NULL )
	{

        string strRecordKey;
        string strValue;
		for ( int ii = 0; ii < reply->elements; ii++ )
		{
		    strRecordKey = reply->element[ii]->str;
			ii++;
			strValue = reply->element[ii]->str;
    		cout << "key:"<<strRecordKey << endl;
		    bson::bo boTmp(reply->element[ii]->str);
    		cout << "bson value:"<<boTmp.toString()<<endl;
		}
		freeReplyObject(reply);
		redisFree( m_pRedisContext );
		return 1;   
	}
#if 0
	redisReply *reply = (redisReply*)redisCommand(m_pRedisContext,"HGET %s %s", key.c_str(), field.c_str() );
	if ( reply != NULL )
	{
	    cout << "type:" << reply->type << endl;

        string strRecordKey;
        string strValue;
		for ( int ii = 0; ii < reply->elements; ii++ )
		{
		    strRecordKey = reply->element[ii]->str;
			ii++;
			strValue = reply->element[ii]->str;
    		cout << "key:"<<strRecordKey << endl;
		    bson::bo boTmp(reply->element[ii]->str);
    		cout << "bson value:"<<boTmp.toString()<<endl;
		}
		freeReplyObject(reply);
		redisFree( m_pRedisContext );
		return 1;   
	}
#endif

	cout <<"not found"<<endl;
	return 0;

	
}
