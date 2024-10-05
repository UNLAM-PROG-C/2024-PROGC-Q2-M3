import java.io.IOException;

public class ChildProcess 
{
    public static void main(String[] args) throws IOException, InterruptedException 
    {
        Process[] childs;
        char[] letters;

        switch (args[0]) 
        {
            case "B":
                System.out.println("PID: " + getPID() + " PPID: " + getPPID() + " Letra: " + args[0]);
                letters = new char[] { 'C', 'D' };
                childs = new Process[letters.length];
                for (int i = 0; i < letters.length; i++) 
                {
                    childs[i] = createChild(letters[i]);
                }
                waitChilds(letters.length, childs);
                System.exit(0);
            case "C":
                System.out.println("PID: " + getPID() + " PPID: " + getPPID() + " Letra: " + args[0]);
                letters = new char[] { 'E' };
                childs = new Process[letters.length];
                for (int i = 0; i < letters.length; i++) 
                {
                    childs[i] = createChild(letters[i]);
                }
                waitChilds(letters.length, childs);
                System.exit(0);
            case "D":
                System.out.println("PID: " + getPID() + " PPID: " + getPPID() + " Letra: " + args[0]);
                letters = new char[] { 'F', 'G' };
                childs = new Process[letters.length];
                for (int i = 0; i < letters.length; i++) 
                {
                    childs[i] = createChild(letters[i]);
                }
                waitChilds(letters.length, childs);
                System.exit(0);
            case "E":
                System.out.println("PID: " + getPID() + " PPID: " + getPPID() + " Letra: " + args[0]);
                letters = new char[] { 'H', 'I' };
                childs = new Process[letters.length];
                for (int i = 0; i < letters.length; i++) 
                {
                    childs[i] = createChild(letters[i]);
                }
                waitChilds(letters.length, childs);
                System.exit(0);
            case "F":
            case "G":
            case "H":
            case "I":
                System.out.println("PID: " + getPID() + " PPID: " + getPPID() + " Letra: " + args[0]);
                Thread.sleep(3000);
                System.exit(0);
            default:
                break;
        }
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
