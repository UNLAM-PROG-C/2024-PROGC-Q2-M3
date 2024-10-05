import java.io.IOException;

public class ParentProcess 
{
    public static void main(String[] args) throws IOException, InterruptedException 
    {
        Process[] childs;
        char[] letters;

        System.out.println("PID: " + getPID() + " PPID: " + getPPID() + " Letra: A");
        letters = new char[] { 'B' };
        childs = new Process[letters.length];
        for (int i = 0; i < letters.length; i++) 
        {
            childs[i] = createChild(letters[i]);
        }
        waitChilds(letters.length, childs);
        System.exit(0);
    }

    public static long getPID() 
    {
        return ProcessHandle.current().pid();
    }

    public static long getPPID() 
    {
        return ProcessHandle.current().parent().get().pid();
    }

    public static Process createChild(char letter) throws IOException 
    {
        ProcessBuilder builder = new ProcessBuilder("java", "./src/ChildProcess.java", Character.toString(letter));
        builder.inheritIO();
        return builder.start();
    }

    public static void waitChilds(int numberOfChilds, Process[] childs) throws InterruptedException 
    {
        for (int i = 0; i < numberOfChilds; i++) 
        {
            childs[i].waitFor();
        }
    }
}
