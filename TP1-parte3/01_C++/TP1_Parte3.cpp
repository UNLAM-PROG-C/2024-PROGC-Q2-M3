#include <iostream>
#include <thread>
#include <mutex>
#include <condition_variable>
#include <chrono>

using namespace std;

const int MAX_BABOONS = 10;  // Máximo número de babuinos que se pueden ingresar
mutex mtx;  // Mutex para proteger las variables compartidas
condition_variable cv;  // Para sincronizar el cruce de babuinos
int baboons_on_rope = 0;  // Número de babuinos en la cuerda
int direction = 0;  // 0 significa que no hay babuinos, 1 para Este-Oeste, -1 para Oeste-Este

void cross_rope(int id, int dir) 
{
    unique_lock<mutex> lock(mtx);

    // Esperar hasta que sea seguro cruzar
    cv.wait(lock, [&]() 
    { 
        return (baboons_on_rope < MAX_BABOONS && (direction == 0 || direction == dir)); 
    });

    // Un babuino comienza a cruzar
    baboons_on_rope++;
    direction = dir;
    cout << "Babuino " << id << " comienza a cruzar en dirección " << (dir == 1 ? "Este-Oeste" : "Oeste-Este") << ". Babuinos en la cuerda: " << baboons_on_rope << endl;

    lock.unlock();
    // Simular el tiempo que tarda en cruzar
    this_thread::sleep_for(chrono::milliseconds(rand() % 3000 + 3000));
    lock.lock();

    // El babuino ha terminado de cruzar
    baboons_on_rope--;
    cout << "Babuino " << id << " ha terminado de cruzar. Babuinos en la cuerda: " << baboons_on_rope << endl;

    if (baboons_on_rope == 0) 
    {
        direction = 0;
    }

    cv.notify_all();  
}

void baboon(int id, int dir) 
{
    while (true)
     {
        cross_rope(id, dir);
        this_thread::sleep_for(chrono::milliseconds(rand() % 2000 + 1000));  
    }
}

int main() 
{
    srand(time(NULL));  
    int total_baboons;

    cout << "Ingrese el número de babuinos que cruzarán (máximo " << MAX_BABOONS << "): ";
    cin >> total_baboons;

    
    if (total_baboons > MAX_BABOONS) 
    {
        total_baboons = MAX_BABOONS;
        cout << "Se ha establecido la cantidad máxima a 10." << endl;
    }

    thread baboons[MAX_BABOONS];

    // Crear babuinos que cruzan en ambas direcciones
    for (int i = 0; i < total_baboons / 2; i++) 
    {
        baboons[i] = thread(baboon, i + 1, 1);  // Este-Oeste
    }
    for (int i = total_baboons / 2; i < total_baboons; i++) 
    {
        baboons[i] = thread(baboon, i + 1, -1);  // Oeste-Este
    }

    // Esperar a que los babuinos terminen (en este caso nunca termina porque están en un bucle infinito)
    for (int i = 0; i < total_baboons; i++) 
    {
        baboons[i].join();
    }

    return 0;
}