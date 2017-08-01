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
	const int delay = 400000;  	//wait at least 400ms after closing the interface before re-opening (USB enumeration)
	const int tests = 3; 		//number of open/close tests to perform

	//int* etiquettes = NULL;
	int nombreEtiquettes = NULL;
	if( argc == 2 ) {
        //printf("%s\n", argv[1]);
        nombreEtiquettes = atoi(argv[1]);
    }
    else {
        //printf("Nothing\n");
        nombreEtiquettes = 100;
    }
    //etiquettes = (int*)malloc(nombreEtiquettes * sizeof(int));

	//const int iterations = 100; 	//number of select tag operations to perform for each test

	int failures = 0;
	int total = 0;

    numDevices = SkyeTek_DiscoverDevices(&devices);
    SkyeTek_DiscoverReaders(devices,numDevices,&readers);
    //printf("Reader Found: %s-%s-%s\n", readers[0]->manufacturer, readers[0]->model, readers[0]->firmware);

    status = SkyeTek_GetTags(readers[0], AUTO_DETECT, &tags, &count);

    //printf("Iterations à venir : %d\n", nombreEtiquettes);


    for(int i = 0; i < nombreEtiquettes; i++)
    {
        //printf("Iteration %d\n", i);
        if(status == SKYETEK_SUCCESS)
        {
            if(count != 0)
            //{
            //    printf("NTR\n");
            //}
            //else
            {
                for(int j = 0; j < count; j++)
                {
                    printf("%s\n", tags[j]->friendly);
                }
            }
        }
        else
        {
            printf("ERROR: GetTags failed");
        }
    }
    printf("end\n");
    SkyeTek_FreeTags(readers[0],tags,count);

    //free(etiquettes);
}
