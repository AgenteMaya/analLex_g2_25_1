
#include <stdio.h>
#include <stdlib.h>
#include <limits.h>

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

int main(void)
{
    char* Termometro = "Termometro";
    float temperatura = 0;
    char* ventilador = "ventilador";
    float potencia = 0;
    temperatura = 40;
    potencia = 90;
    if (temperatura > 30) {
        ligar(ventilador);
    };

    return 0;
}
