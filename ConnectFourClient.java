package ConnectFour;

import java.io.*;
import java.net.*;
import ConnectFour.Board.*;

public class ConnectFourClient {
  int playerNum;
  char playerToken;
  String playerName;

  static Board currentBoard = null;

  public static void main(String[] args) {
    String connectionName = args[0];
    int port = Integer.parseInt(args[1]);
    //playerToken = Integer.parseInt(args[2]);
    //playerName = Integer.parseInt(args[3]);
    try {
      System.out.println("Connecting to " + connectionName + " on port " + port);
      Socket client = new Socket(connectionName, port);

      System.out.println("Now connected to " + client.getRemoteSocketAddress());
      OutputStream outToServer = client.getOutputStream();
      DataOutputStream dataOut = new DataOutputStream(outToServer);

      dataOut.writeUTF("Connection from " + client.getLocalSocketAddress());
      InputStream inFromServer = client.getInputStream();
      ObjectInputStream in = new ObjectInputStream(inFromServer);

      currentBoard = (Board) in.readObject();
      in.close();
      client.close();
    } catch (IOException e) {
      e.printStackTrace();
    } catch (ClassNotFoundException c) {
      System.out.println("Board class not found");
      c.printStackTrace();
      return;
    }

    currentBoard.printBoard();

  }
}
