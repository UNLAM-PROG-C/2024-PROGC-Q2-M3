#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

#define TIME_WAIT 5

int main()
{
    pid_t pid_B, pid_C, pid_D, pid_E, pid_F, pid_G, pid_H, pid_I;

    pid_B = fork();    // A crea B
    if (pid_B == 0)
    {

        pid_C = fork();    // B crea C

        if (pid_C == 0)
        {

            pid_E = fork();    // C crea E
            if (pid_E == 0)
            {

                pid_H = fork();    // E crea H
                if (pid_H == 0)
                {
                    sleep(TIME_WAIT);
                    return EXIT_SUCCESS;    // Detener H
                }

                pid_I = fork();    // E crea I
                if (pid_I == 0)
                {
                    sleep(TIME_WAIT);
                    return EXIT_SUCCESS;    // Detener I
                }

                wait(NULL);                     // Esperar a H e I
                wait(NULL);                     // Esperar a H e I
                return EXIT_SUCCESS;    // Detener E
            }

            wait(NULL);                     // Esperar a E
            return EXIT_SUCCESS;    // Detener C
        }

        pid_D = fork();    // B crea D
        if (pid_D == 0)
        {

            pid_F = fork();    // D crea F
            if (pid_F == 0)
            {
                sleep(TIME_WAIT);
                return EXIT_SUCCESS;    // Detener F
            }

            pid_G = fork();    // D crea G
            if (pid_G == 0)
            {
                sleep(TIME_WAIT);
                return EXIT_SUCCESS;    // Detener G
            }

            wait(NULL);                     // Esperar a F y G
            wait(NULL);                     // Esperar a F y G
            return EXIT_SUCCESS;    // Detener D
        }

        wait(NULL);                     // Esperar a C y D
        wait(NULL);                     // Esperar a C y D
        return EXIT_SUCCESS;    // Detener B
    }

    wait(NULL);                     // Esperar a B
    return EXIT_SUCCESS;    // Detener A
}