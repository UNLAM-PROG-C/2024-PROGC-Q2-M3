#include <iostream>
#include <fstream>
#include <vector>
#include <thread>
#include <mutex>
#include <chrono>

std::mutex mtx;                   // Mutex para proteger el acceso a los resultados parciales
std::vector<int> partial_results; // Vector para almacenar los resultados parciales de cada thread

// Función que cuenta los caracteres de una parte del archivo
void count_characters(const std::vector<std::string> &lines, int start, int end, int thread_id)
{
    int local_count = 0;

    // Contar caracteres en las líneas asignadas al thread
    for (int i = start; i < end; ++i)
    {
        local_count += lines[i].size();
    }

    // Almacenar el resultado parcial de manera segura
    std::lock_guard<std::mutex> lock(mtx);
    partial_results[thread_id] = local_count;
}

int main(int argc, char *argv[])
{
    if (argc < 3)
    {
        std::cerr << "Uso: " << argv[0] << " <path_al_archivo> <num_threads>" << std::endl;
        return 1;
    }

    std::string filepath = argv[1];
    int num_threads = std::stoi(argv[2]);

    // Leer el archivo y almacenar cada línea en un vector
    std::ifstream file(filepath);
    if (!file.is_open())
    {
        std::cerr << "No se pudo abrir el archivo: " << filepath << std::endl;
        return 1;
    }

    std::vector<std::string> lines;
    std::string line;
    while (std::getline(file, line))
    {
        lines.push_back(line);
    }
    file.close();

    int total_lines = lines.size();
    partial_results.resize(num_threads, 0); // Inicializar el vector de resultados parciales

    // Determinar el rango de líneas que procesará cada thread
    int lines_per_thread = total_lines / num_threads;
    int remaining_lines = total_lines % num_threads;

    std::vector<std::thread> threads;

    auto start_time = std::chrono::high_resolution_clock::now(); // Iniciar el cronómetro

    // Crear threads para contar caracteres
    int start_line = 0;
    for (int i = 0; i < num_threads; ++i)
    {
        int end_line = start_line + lines_per_thread + (i < remaining_lines ? 1 : 0); // Distribuir líneas de manera equitativa
        threads.push_back(std::thread(count_characters, std::ref(lines), start_line, end_line, i));
        start_line = end_line;
    }

    // Esperar a que todos los threads terminen
    for (auto &t : threads)
    {
        t.join();
    }

    // Sumar los resultados parciales
    int total_characters = 0;
    for (int result : partial_results)
    {
        total_characters += result;
    }

    auto end_time = std::chrono::high_resolution_clock::now(); // Finalizar el cronómetro
    std::chrono::duration<double, std::milli> elapsed = end_time - start_time;

    // Mostrar el resultado total y el tiempo de procesamiento
    std::cout << "Total de caracteres: " << total_characters << std::endl;
    std::cout << "Tiempo de procesamiento: " << elapsed.count() << " ms" << std::endl;

    return 0;
}
