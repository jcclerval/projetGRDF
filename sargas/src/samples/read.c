/**
 * Sample program that reads tags for a fixed period of time (500ms)
 * and prints the tags found.
 * @file read.c
 */

#include <tm_reader.h>
#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#include <string.h>
#include <inttypes.h>

#ifndef BARE_METAL
#if WIN32
#define snprintf sprintf_s
#endif 

/* Enable this to use transportListener */
#ifndef USE_TRANSPORT_LISTENER
#define USE_TRANSPORT_LISTENER 0
#endif

#define usage() {errx(1, "Please provide reader URL, such as:\n"\
                         "tmr:///com4 or tmr:///com4 --ant 1,2\n"\
                         "tmr://my-reader.example.com or tmr://my-reader.example.com --ant 1,2\n");}

void errx(int exitval, const char *fmt, ...)
{
  va_list ap;

  va_start(ap, fmt);
  vfprintf(stderr, fmt, ap);

  exit(exitval);
}

void checkerr(TMR_Reader* rp, TMR_Status ret, int exitval, const char *msg)
{
  if (TMR_SUCCESS != ret)
  {
    errx(exitval, "Error %s: %s\n", msg, TMR_strerr(rp, ret));
  }
}

void serialPrinter(bool tx, uint32_t dataLen, const uint8_t data[],
                   uint32_t timeout, void *cookie)
{
  FILE *out = cookie;
  uint32_t i;

  fprintf(out, "%s", tx ? "Sending: " : "Received:");
  for (i = 0; i < dataLen; i++)
  {
    if (i > 0 && (i & 15) == 0)
    {
      fprintf(out, "\n         ");
    }
    fprintf(out, " %02x", data[i]);
  }
  fprintf(out, "\n");
}

void stringPrinter(bool tx,uint32_t dataLen, const uint8_t data[],uint32_t timeout, void *cookie)
{
  FILE *out = cookie;

  fprintf(out, "%s", tx ? "Sending: " : "Received:");
  fprintf(out, "%s\n", data);
}

void parseAntennaList(uint8_t *antenna, uint8_t *antennaCount, char *args)
{
  char *token = NULL;
  char *str = ",";
  uint8_t i = 0x00;
  int scans;

  /* get the first token */
  if (NULL == args)
  {
    fprintf(stdout, "Missing argument\n");
    usage();
  }

  token = strtok(args, str);
  if (NULL == token)
  {
    fprintf(stdout, "Missing argument after %s\n", args);
    usage();
  }

  while(NULL != token)
  {
    scans = sscanf(token, "%"SCNu8, &antenna[i]);
    if (1 != scans)
    {
      fprintf(stdout, "Can't parse '%s' as an 8-bit unsigned integer value\n", token);
      usage();
    }
    i++;
    token = strtok(NULL, str);
  }
  *antennaCount = i;
}
#endif

int main(int argc, char *argv[])
{
  TMR_Reader r, *rp;
  TMR_Status ret;
  TMR_ReadPlan plan;
  TMR_Region region;
  uint8_t *antennaList = NULL;
  uint8_t buffer[20];
  uint8_t i;
  uint8_t antennaCount = 0x0;
  TMR_String model;
  char str[64];

#ifndef BARE_METAL
#if USE_TRANSPORT_LISTENER
  TMR_TransportListenerBlock tb;
#endif
 
  if (argc < 2)
  {
    usage(); 
  }
// gestion des arguments
  for (i = 2; i < argc; i+=2)
  {
    if(0x00 == strcmp("--ant", argv[i]))
    {
      if (NULL != antennaList)
      {
        fprintf(stdout, "Duplicate argument: --ant specified more than once\n");
        usage();
      }
      parseAntennaList(buffer, &antennaCount, argv[i+1]);
      antennaList = buffer;
    }
    else
    {
      fprintf(stdout, "Argument %s is not recognized\n", argv[i]);
      usage();
    }
  }
#endif
  
  rp = &r;
#ifndef BARE_METAL
  ret = TMR_create(rp, argv[1]);
#else
  ret = TMR_create(rp, "tmr:///com1");
  buffer[0] = 1;
  antennaList = buffer;
  antennaCount = 0x01;
#endif
/*
 * Creation du l'Antenne
 * 
 * 
 */	
#ifndef BARE_METAL
  checkerr(rp, ret, 1, "creating reader");

#if USE_TRANSPORT_LISTENER

  if (TMR_READER_TYPE_SERIAL == rp->readerType)
  {
    tb.listener = serialPrinter;
  }
  else
  {
    tb.listener = stringPrinter;
  }
  tb.cookie = stdout;

  TMR_addTransportListener(rp, &tb);
#endif
#endif

  ret = TMR_connect(rp);

#ifndef BARE_METAL
  checkerr(rp, ret, 1, "connecting reader");
#endif
  region = TMR_REGION_NONE;
  ret = TMR_paramGet(rp, TMR_PARAM_REGION_ID, &region);
#ifndef BARE_METAL
  checkerr(rp, ret, 1, "getting region");
#endif

/* Gestion des régions
 * 
 * 
 * 
 * 
 */
 
  if (TMR_REGION_NONE == region)
  {
    TMR_RegionList regions;
    TMR_Region _regionStore[32];
    regions.list = _regionStore;
    regions.max = sizeof(_regionStore)/sizeof(_regionStore[0]);
    regions.len = 0;

    ret = TMR_paramGet(rp, TMR_PARAM_REGION_SUPPORTEDREGIONS, &regions);
#ifndef BARE_METAL
    checkerr(rp, ret, __LINE__, "getting supported regions");

    if (regions.len < 1)
    {
      checkerr(rp, TMR_ERROR_INVALID_REGION, __LINE__, "Reader doesn't supportany regions");
    }
#endif  
    region = regions.list[0];
    ret = TMR_paramSet(rp, TMR_PARAM_REGION_ID, &region);
#ifndef BARE_METAL    
	checkerr(rp, ret, 1, "setting region");  
#endif 
  }
/** Gestion des antennes
 * 
 * 
 * 
 **/
 
  model.value = str;
  model.max = 64;
  TMR_paramGet(rp, TMR_PARAM_VERSION_MODEL, &model);
  if (((0 == strcmp("Sargas", model.value)) || (0 == strcmp("M6e Micro", model.value)) ||(0 == strcmp("M6e Nano", model.value)))
    && (NULL == antennaList))
  {
#ifndef BARE_METAL	  
    fprintf(stdout, "Module doesn't has antenna detection support please provide antenna list\n");
    usage();
#endif	
  }

  /**
  * for antenna configuration we need two parameters
  * 1. antennaCount : specifies the no of antennas should
  *    be included in the read plan, out of the provided antenna list.
  * 2. antennaList  : specifies  a list of antennas for the read plan.
  **/ 

  // initialize the read plan 
  ret = TMR_RP_init_simple(&plan, antennaCount, antennaList, TMR_TAG_PROTOCOL_GEN2, 1000);
#ifndef BARE_METAL
  checkerr(rp, ret, 1, "initializing the  read plan");
#endif
  
  /* Commit read plan */
  ret = TMR_paramSet(rp, TMR_PARAM_READ_PLAN, &plan);
#ifndef BARE_METAL
  checkerr(rp, ret, 1, "setting read plan");
#endif
  ret = TMR_read(rp, 5000, NULL); 
  /**
   * C'est ici (au dessus que ca se passe, ici on scan pendant 500ms et on regarde combien de tags on a
   * 
   * 
   * --> mettre le temps souhaité ici, dépendra de la facilité à trouver les tags
   * 
   **/
  
#ifndef BARE_METAL
if (TMR_ERROR_TAG_ID_BUFFER_FULL == ret)
  {
    /* In case of TAG ID Buffer Full, extract the tags present
    * in buffer.
    */
    fprintf(stdout, "reading tags:%s\n", TMR_strerr(rp, ret));
  }
  else
  {
    checkerr(rp, ret, 1, "reading tags");
  }
#endif
  while (TMR_SUCCESS == TMR_hasMoreTags(rp))
  {
    TMR_TagReadData trd;
    char epcStr[128];
    char timeStr[128];

    ret = TMR_getNextTag(rp, &trd);
#ifndef BARE_METAL  
  checkerr(rp, ret, 1, "fetching tag");
#endif
    TMR_bytesToHex(trd.tag.epc, trd.tag.epcByteCount, epcStr);

/**
 * Traitement à proprement parler
 * 
 * 
 **/
 
 
#ifndef BARE_METAL
#ifdef WIN32
	{
		FILETIME ft, utc;
		SYSTEMTIME st;
		char* timeEnd;
		char* end;
		
		utc.dwHighDateTime = trd.timestampHigh;
		utc.dwLowDateTime = trd.timestampLow;

		FileTimeToLocalFileTime( &utc, &ft );
		FileTimeToSystemTime( &ft, &st );
		timeEnd = timeStr + sizeof(timeStr)/sizeof(timeStr[0]);
		end = timeStr;
		end += sprintf(end, "%d-%d-%d", st.wYear,st.wMonth,st.wDay);
		end += sprintf(end, "T%d:%d:%d %d", st.wHour,st.wMinute,st.wSecond, st.wMilliseconds);
		end += sprintf(end, ".%06d", trd.dspMicros);
  }
#else
    {
      uint8_t shift;
      uint64_t timestamp;
      time_t seconds;
      int micros;
      char* timeEnd;
      char* end;

      shift = 32;
      timestamp = ((uint64_t)trd.timestampHigh<<shift) | trd.timestampLow;
      seconds = timestamp / 1000;
      micros = (timestamp % 1000) * 1000;

      /*
       * Timestamp already includes millisecond part of dspMicros,
       * so subtract this out before adding in dspMicros again
       */
      micros -= trd.dspMicros / 1000;
      micros += trd.dspMicros;

      timeEnd = timeStr + sizeof(timeStr)/sizeof(timeStr[0]);
      end = timeStr;
      end += strftime(end, timeEnd-end, "%FT%H:%M:%S", localtime(&seconds));
      end += snprintf(end, timeEnd-end, ".%06d", micros);
      end += strftime(end, timeEnd-end, "%z", localtime(&seconds));
    }
#endif
    
    //printf("EPC:%s ant:%d count:%d Time:%s\n", epcStr, trd.antenna, trd.readCount, timeStr);
    printf("%s\n", epcStr);
#endif
  }

  TMR_destroy(rp);
  return 0;
}
