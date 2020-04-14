/**
**	功能：更改配置文件的标签号，让序号一次递增
**	日期：20200414 
*/
#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>
#include<string.h>
#include<stdlib.h>
#include<stdbool.h>

int findNum(char *src)
{
	int num = 0;
	int len = strlen(src);
	int dst[1024];
	int i,res=0;
	
	for(i=0; i< len; i++)
	{
		if(src[i]>= '0' && src[i] <= '9')
		{
			dst[num] = (int)(src[i]-'0');
			printf("dst: %d\n",  dst[num]);
			if(++num>1024)
			{
				printf("数组越界");
				return -1;
			}
		}
	}

	for(i=0;i<num;i++)
	{
		printf("dst: %d\n", dst[i]);
		res=10*res+dst[i];
	}
	printf("index in findNum: %d", res);
	return res;
}
int main(int argc, char *argv[])
{
	FILE *fp, *fnew;
	char line_string[4096];
	int index,tab_num,id;
	static int flag = 0;

	if(argc<3){
		printf("Usage: %s [file_name] [tab_name] [tab_num]!\n", argv[0]);
		return 0;
	}

	tab_num = findNum(argv[3]);
	id = tab_num;

	if((fp=fopen(argv[1],"r+"))==NULL)
		perror("fopen");

	if((fnew=fopen("new.txt","w+"))==NULL)
		perror("fopen");

	while(!feof(fp)){
		fgets(line_string,sizeof(line_string),fp); //fscanf(fp, "%s\n", line_string);
		printf("in mian: %s\n",line_string);
		if(strstr(line_string, argv[2]))
		{
			if (flag == 0)
			{
				index = findNum(line_string);
				if (index == tab_num)	
					flag = 1;
			}else{
				fprintf(fnew, "%s_%d]\n", argv[2],id++);
				continue;
			}
		}
		fputs(line_string, fnew);
	}
	fclose(fp);
	fclose(fnew);
	return 0;
}