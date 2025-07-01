
#include <stdio.h>
#include <stdlib.h>

void ligar ( char* namedevice )
{
    printf("%s ligado!\n", namedevice);
}

void desligar ( char* namedevice )
{
     printf("%s desligado!\n", namedevice);
}

void alerta ( char* namedevice , char* msg )
{
     printf("%s recebeu o alerta: \n", namedevice);
     printf ("%s\n", msg);
}

void alertaComObs ( char* namedevice , char* msg , int var )
{
    printf("%s recebeu o alerta: \n", namedevice);
    printf ("%s %d\n", msg, var);
}

void alertaTodos(char* namedevices[], char* msg, int qtd)
{
    for (int i = 0; i < qtd; i++)
    {
        alerta(namedevices[i], msg);
    }
}

int main(void)
{
    char* monitor = "monitor";
    char* celular = "celular";
    char* Termometro = "Termometro";
    char* temperatura = "temperatura";
    if (temperatura > 30) {
        char* broadcast_devices_1[] = { "monitor", "celular" };
    for (int i = 0; i < 2; i++) { alertaComObs(broadcast_devices_1[i], " Temperatura em ", temperatura); };
    };

    return 0;
}
