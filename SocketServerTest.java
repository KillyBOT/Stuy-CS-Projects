import java.net.*;
import java.io.*;

public class SocketServerTest extends Thread{
  private ServerSocket serverSocket;

  public SocketServerTest(int port) throws IOException {
    serverSocket = new ServerSocket(port);
    serverSocket.setSoTimeout(100000);
  }

  public void run() {
    while(true) {
       try {
          System.out.println("Waiting for client on port " +
             serverSocket.getLocalPort() + "...");
          Socket server = serverSocket.accept();

          System.out.println("Connected to " + server.getRemoteSocketAddress());
          DataInputStream in = new DataInputStream(server.getInputStream());

          System.out.println(in.readUTF());
          DataOutputStream out = new DataOutputStream(server.getOutputStream());

          out.writeUTF("You connected to " + server.getLocalSocketAddress()
             + "\nNow get out!");
          server.close();

       } catch (SocketTimeoutException s) {
          System.out.println("Socket timed out!");
          break;
       } catch (IOException e) {
          e.printStackTrace();
          break;
       }
    }
  }

  public static void main(String [] args) {
    int port = Integer.parseInt(args[0]);
    try {
       Thread t = new SocketServerTest(port);
       t.start();
    } catch (IOException e) {
       e.printStackTrace();
    }
  }
}
