
    #include <stdio.h>
    #include <stdlib.h>

    void ligar ( char* namedevice )
    {
        printf("%s ligado!
", namedevice);
    }
    
    void desligar ( char* namedevice )
    {
         printf("%s desligado!
", namedevice);
    }
    
    void alerta ( char* namedevice , char* msg )
    {
         printf("%s recebeu o alerta: 
", namedevice);
         printf ("%s", msg);
    }
    
    void alertaComObs ( char* namedevice , char* msg , int var )
    {
        printf("%s recebeu o alerta: 
", namedevice);
        printf ("%s %d", msg, var);
    }

    void alertaTodos(char** namedevices, char* msg, int qtd)
    {
        for (int i = 0; i < qtd; i++)
        {
            alerta(namedevices[i], msg);
        }
    }

    int main(void)
    {
        char** vNamedevices [100] [100];

    
return 0;
}
