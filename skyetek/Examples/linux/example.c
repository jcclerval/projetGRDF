#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "SkyeTekAPI.h"
#include "SkyeTekProtocol.h"

int main(int argc, char* argv[])
{
	LPSKYETEK_DEVICE *devices = NULL;
	LPSKYETEK_READER *readers = NULL;
	LPSKYETEK_TAG *tags = NULL;
	SKYETEK_STATUS status;
	unsigned short count = 0;
	int numDevices = 0;
	int numReaders = 0;
	int nombreIterations = 100;
	if( argc == 2 ) {
        nombreIterations = atoi(argv[1]);
    }

	int failures = 0;
	int total = 0;

    numDevices = SkyeTek_DiscoverDevices(&devices);
    SkyeTek_DiscoverReaders(devices,numDevices,&readers);

    if((numDevices = SkyeTek_DiscoverDevices(&devices)) > 0)
    {
        for(int i = 0; i < nombreIterations; i++)
        {
            status = SkyeTek_GetTags(readers[0], AUTO_DETECT, &tags, &count);

            if(status == SKYETEK_SUCCESS)
            {
                if(count != 0)
                {
                    for(int j = 0; j < count; j++)
                    {
                        printf("%s\n", tags[j]->friendly);
                    }
                }
            }
            else            //{
                //    printf("NTR\n");
                //}
                //else
            {
                printf("ERROR: GetTags failed");
            }
        }
    }
    printf("end\n");
    SkyeTek_FreeTags(readers[0],tags,count);

    //free(etiquettes);
}
