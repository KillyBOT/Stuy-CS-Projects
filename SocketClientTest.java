import java.net.*;
import java.io.*;

public class SocketClientTest {
  public static void main(String [] args){
    String name = args[0];
    int port = Integer.parseInt(args[1]);
    try {
      System.out.println("Connecting to " + name + " on port " + port);
      Socket client = new Socket(name, port);

      System.out.println("Now connected to " + client.getRemoteSocketAddress());
      OutputStream outToServer = client.getOutputStream();
      DataOutputStream dataOut = new DataOutputStream(outToServer);

      dataOut.writeUTF("Connection from " + client.getLocalSocketAddress());
      InputStream inFromServer = client.getInputStream();
      DataInputStream dataIn = new DataInputStream(inFromServer);

      System.out.println("Server says: " + dataIn.readUTF());
      client.close();

    } catch (IOException e) {
      e.printStackTrace();
    }
  }
}
