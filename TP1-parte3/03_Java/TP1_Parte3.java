import java.util.Random;
import java.util.concurrent.Semaphore;

public class Supermercado {
    public static int cantidadClientes;

    public static void main(String[] args) {
        setCantidadClientes(Integer.parseInt(args[0]));
        Gondola gondola = new Gondola();

        // Crear y comenzar los hilos de repositores
        Repositor repositor1 = new Repositor(gondola, 1, getCantidadClientes());
        Repositor repositor2 = new Repositor(gondola, 2, getCantidadClientes());
        repositor1.start();
        repositor2.start();

        // Crear y comenzar los hilos de clientes
        for (int i = 0; i < getCantidadClientes(); i++) {
            new Cliente(gondola).start();
        }

        try {
            repositor1.join();
            repositor2.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    public static int getCantidadClientes() {
        return cantidadClientes;
    }

    public static void setCantidadClientes(int num) {
        cantidadClientes = num;
    }

}

class Gondola {
    private final int MAX_PRODUCTOS = 10;
    private int productos = MAX_PRODUCTOS;
    private Semaphore repositorLock = new Semaphore(0);
    private Semaphore alternanciaLock = new Semaphore(1);
    private Semaphore clienteLock = new Semaphore(1);
    private int contadorClientes = 0;

    public synchronized void tomarProductos(int cantidad) throws InterruptedException {
        clienteLock.acquire();
        while (productos < cantidad) {
            System.out.println("Cliente esperando reposición.");
            repositorLock.release();
            clienteLock.acquire();
        }

        Thread.sleep(500);
        System.out.println("Cliente comprando.");
        Thread.sleep(500);
        productos -= cantidad;
        System.out.println("Cliente toma " + cantidad + " productos. Quedan " + productos);

        if (productos == 0) {
            repositorLock.release();
        } else {
            clienteLock.release();
        }

        contadorClientes++;
    }

    public void reponer(int repositorId) throws InterruptedException {
        alternanciaLock.acquire();
        if (contadorClientes >= Supermercado.getCantidadClientes()) {
            alternanciaLock.release();
            return;
        }
        repositorLock.acquire();
        Thread.sleep(500);
        System.out.println("Repositor " + repositorId + " reponiendo productos.");
        Thread.sleep(500);
        productos = MAX_PRODUCTOS;
        System.out.println("Repositor " + repositorId + " terminó de reponer productos.");

        clienteLock.release();
        alternanciaLock.release();
    }

    public int getClientesAtendidos() {
        return contadorClientes;
    }
}

class Cliente extends Thread {
    private final Gondola gondola;
    private Random random = new Random();

    public Cliente(Gondola gondola) {
        this.gondola = gondola;
    }

    @Override
    public void run() {
        try {
            int cantidad = random.nextInt(2) + 1;
            gondola.tomarProductos(cantidad);
            Thread.sleep(random.nextInt(1000)); // Simula el tiempo entre compras
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}

class Repositor extends Thread {
    private final Gondola gondola;
    private final int id;
    private final int cantidadClientes;

    public Repositor(Gondola gondola, int id, int cantidadClientes) {
        this.gondola = gondola;
        this.id = id;
        this.cantidadClientes = cantidadClientes;
    }

    @Override
    public void run() {
        try {
            while (gondola.getClientesAtendidos() < cantidadClientes) {
                gondola.reponer(this.id);
                Thread.sleep(1000);
            }
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}