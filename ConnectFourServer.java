package ConnectFour;

import java.io.*;
import ConnectFour.Board.*;
import java.net.*;

public class ConnectFourServer extends Thread{
  ServerSocket serverSocket;
  Board currentBoard;

  public ConnectFourServer(int port, int boardRows, int boardCols, int startingPlayer) throws IOException {
    serverSocket = new ServerSocket(port);
    serverSocket.setSoTimeout(10000000);

    currentBoard = new Board(boardRows, boardCols, startingPlayer);
  }

  public void run() {
    while(true){
      try {
        currentBoard.printBoard();
        System.out.println("Connect four server started on port " + serverSocket.getLocalPort());
        System.out.println("Waiting for clients...");
        Socket server = serverSocket.accept();

        System.out.println("Now connected to " + server.getRemoteSocketAddress());
        DataInputStream checkIn = new DataInputStream(server.getInputStream());
        currentBoard.registerPlayer(checkIn.readUTF().charAt(0),0);

        boolean running = true;

        while(running) {
          DataOutputStream out = new DataOutputStream(server.getOutputStream());
          ObjectOutputStream outObj = new ObjectOutputStream(out);
          outObj.writeObject(currentBoard);

          DataInputStream in = new DataInputStream(server.getInputStream());
          ObjectInputStream objIn = new ObjectInputStream(in);
          currentBoard = (Board) objIn.readObject();
          currentBoard.printBoard();

          if (currentBoard.checkWin() != 0) {
            running = false;
          }
        }
        server.close();

      } catch (SocketTimeoutException s) {
        System.out.println("Socket timed out!");
      } catch (IOException e) {
        e.printStackTrace();
      } catch (ClassNotFoundException c) {
        System.out.println("Could not find class");
        c.printStackTrace();
      }
    }
  }
  public static void main(String [] args){
    int connectionPort = Integer.parseInt(args[0]);
    int boardRows = Integer.parseInt(args[1]);
    int boardCols = Integer.parseInt(args[2]);
    int startingPlayer = Integer.parseInt(args[3]);

    try {
      Thread serverThread = new ConnectFourServer(connectionPort, boardRows, boardCols, startingPlayer);
      serverThread.start();
    } catch (IOException e) {
      e.printStackTrace();
    }
  }
}
