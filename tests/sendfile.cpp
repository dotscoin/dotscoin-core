#include<iostream>
#include<sys/socket.h>
#include<sys/types.h>
#include<netinet/in.h>
#include<netdb.h>
#include <sys/uio.h>
#include <unistd.h>
#include <fcntl.h>
#include<stdio.h>
#include<string.h>

using namespace std;

#define PORT 5555
#define BACKLOG 5

int main(){
  
  int fd1,fd2;
  int bnd,lstn;
  char buf[100]={' '};  
  struct sockaddr_in server,client;
  
  fd1=socket(AF_INET,SOCK_STREAM,0);
  if(fd1<0){
    cout<<"Error creating socket\n";
    return 0;
  }
  cout<<"Socket created\n";

  server.sin_family=AF_INET;
  server.sin_port=htons(PORT);
  server.sin_addr.s_addr=INADDR_ANY;
  
  
  bnd=bind(fd1,(struct sockaddr *)&server,sizeof(server));
  if(bnd<0){
    cout<<"Error binding\n";
    return 0;
  }
  
  lstn=listen(fd1,BACKLOG);
  if(lstn<0){
    cout<<"Error listening\n";
    return 0;
  }
  
  cout<<"Server is listening\n";
  
  socklen_t len=sizeof(client);

  fd2=accept(fd1,(struct sockaddr*)&client,&len);
  if(fd2<0){
    cout<<"Error accepting\n";
    return 0;
  }

  int from;
  from=open("/home/rishav4101/12345.mkv",O_RDONLY);
  if(from<0){
	cout<<"Error opening file\n";
    return 0;
  }
  int n=1;
  int s;
  while((n=read(from,buf,sizeof(buf)))!=0){
    //s=send(fd2,buf,sizeof(buf),0);
    s=write(fd2,buf,n);
    if(s<0){cout<<"error sending\n";return 0;}
  }

  close(fd1);
  close(fd2);
  shutdown(fd1,0);
  shutdown(fd2,0);
  
  return 0;
}