import java.io.*;
import java.util.*;
import java.util.concurrent.*;
import java.time.Duration;
import java.time.Instant;

public class Main 
{
    private static final List<Integer> partialResults = Collections.synchronizedList(new ArrayList<>());


    public static void countCharacters(List<String> lines, int startLine, int endLine, int threadId) 
    {
        Instant startTime = Instant.now();  // Tiempo de inicio del hilo
        int charCount = 0;

       
        for (int i = startLine; i < endLine; i++) 
        {
            charCount += lines.get(i).length();
        }

      
        partialResults.set(threadId, charCount);

        Instant endTime = Instant.now();
        long timeElapsed = Duration.between(startTime, endTime).toMillis();  // Tiempo en milisegundos

       
        System.out.println("Hilo " + threadId + ": caracteres contados = " + charCount + ", tiempo = " + timeElapsed + " ms");
    }

    public static void main(String[] args) throws IOException, InterruptedException 
    {
        if (args.length < 2) 
        {
            System.out.println("Uso: java Main <path_al_archivo> <num_threads>");
            return;
        }

        String filePath = args[0];
        int numThreads = Integer.parseInt(args[1]);

     
        List<String> lines = new ArrayList<>();
        try (BufferedReader reader = new BufferedReader(new FileReader(filePath))) 
        {
            String line;
            while ((line = reader.readLine()) != null) 
            {
                lines.add(line);
            }
        }

        int totalLines = lines.size();
        partialResults.clear();
        for (int i = 0; i < numThreads; i++) 
        {
            partialResults.add(0);  // Inicializar los resultados parciales a 0
        }

      
        numThreads = Math.min(numThreads, totalLines);

       
        int linesPerThread = totalLines / numThreads;
        int remainingLines = totalLines % numThreads;

        ExecutorService executor = Executors.newFixedThreadPool(numThreads);
        List<Future<?>> futures = new ArrayList<>();

        
        Instant globalStartTime = Instant.now();

       
        int startLine = 0;
        for (int i = 0; i < numThreads; i++) 
        {
            // Distribuir líneas de manera equitativa, asignando 1 línea extra a los primeros 'remainingLines' hilos
            final int endLine = startLine + linesPerThread + (i < remainingLines ? 1 : 0);
            final int threadId = i;
            final int currentStartLine = startLine; 
            Future<?> future = executor.submit(() -> countCharacters(lines, currentStartLine, endLine, threadId));
            futures.add(future);
            startLine = endLine;
        }


        for (Future<?> future : futures) 
        {
            try 
            {
                future.get();
            } catch (ExecutionException e) 
            {
                e.printStackTrace(); 
            }
        }

   
        Instant globalEndTime = Instant.now();
        long globalTimeElapsed = Duration.between(globalStartTime, globalEndTime).toMillis();

   
        int totalCharacters = partialResults.stream().mapToInt(Integer::intValue).sum();

       
        System.out.println("Total de caracteres contados: " + totalCharacters);
        System.out.println("Tiempo total de procesamiento: " + globalTimeElapsed + " ms");

      
        executor.shutdown();
    }
}
