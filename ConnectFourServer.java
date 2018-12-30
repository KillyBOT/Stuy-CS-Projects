package ConnectFour;

import java.io.*;
import ConnectFour.Board.*;
import java.net.*;

class CFServer extends Thread{
  ServerSocket serverSocket;
  Board currentBoard;
  private int boardRows;
  private int boardCols;
  private int startingPlayer;

  public CFServer(int port, int boardRows, int boardCols, int startingPlayer) throws IOException {
    serverSocket = new ServerSocket(port);
    serverSocket.setSoTimeout(10000000);

    this.boardRows = boardRows;
    this.boardCols = boardCols;
    this.startingPlayer = startingPlayer;
    currentBoard = new Board(this.boardRows, this.boardCols, this.startingPlayer);
  }

  public void sendBoardToSocket(Board boardToSend, Socket playerSocket) {
    try {

      DataOutputStream out = new DataOutputStream(playerSocket.getOutputStream());
      ObjectOutputStream outObj = new ObjectOutputStream(out);
      outObj.writeObject(boardToSend);
      outObj.flush();

    } catch (IOException e) {
      e.printStackTrace();
    }
  }

  public Board getBoardFromSocket(Board currentBoard, Socket playerSocket) {

    try {

      DataInputStream in = new DataInputStream(playerSocket.getInputStream());
      ObjectInputStream objIn = new ObjectInputStream(in);
      return (Board) objIn.readObject();

    } catch (IOException e) {
      e.printStackTrace();
    } catch (ClassNotFoundException c) {
      c.printStackTrace();
    }

    return currentBoard;
  }

  public void run() {
    boolean totalRunning = true;
    while(totalRunning){
      try {
        currentBoard.printBoard();
        System.out.println("Connect four server started on port " + serverSocket.getLocalPort());
        System.out.println("Waiting for clients...");
        Socket player1Socket = serverSocket.accept();
        Socket player2Socket = serverSocket.accept();

        DataOutputStream checkOut1 = new DataOutputStream(player1Socket.getOutputStream());
        checkOut1.writeUTF("1");
        checkOut1.flush();

        System.out.println("Player 1 is: " + player1Socket.getRemoteSocketAddress());
        DataInputStream checkIn1 = new DataInputStream(player1Socket.getInputStream());
        currentBoard.registerPlayer(checkIn1.readUTF().charAt(0),0);

        DataOutputStream checkOut2 = new DataOutputStream(player2Socket.getOutputStream());
        checkOut2.writeUTF("2");   
        checkOut2.flush();

        System.out.println("Player 2 is: " + player2Socket.getRemoteSocketAddress());
        DataInputStream checkIn2 = new DataInputStream(player2Socket.getInputStream());
        currentBoard.registerPlayer(checkIn2.readUTF().charAt(0),1);

        boolean running = true;

        while(running) {
          sendBoardToSocket(currentBoard, player1Socket);

          currentBoard = getBoardFromSocket(currentBoard, player1Socket);
          currentBoard.printBoard();

          if (currentBoard.checkWin() != 0) {
            sendBoardToSocket(currentBoard, player1Socket);
            sendBoardToSocket(currentBoard, player2Socket);
            currentBoard = new Board(this.boardRows, this.boardCols, this.startingPlayer);
            running = false;
          }

          sendBoardToSocket(currentBoard, player2Socket);

          currentBoard = getBoardFromSocket(currentBoard, player2Socket);
          currentBoard.printBoard();

          if (currentBoard.checkWin() != 0) {
            sendBoardToSocket(currentBoard, player1Socket);
            sendBoardToSocket(currentBoard, player2Socket);
            currentBoard = new Board(this.boardRows, this.boardCols, this.startingPlayer);
            running = false;
          }
        }
        player1Socket.close();
        player2Socket.close();

      } catch (SocketTimeoutException s) {
        System.out.println("Socket timed out!");
        totalRunning = false;
      } catch (IOException e) {
        e.printStackTrace();
        System.out.println("Someone probably prematurely disconnected!");
        totalRunning = false;
      }
    }
  }
}

public class ConnectFourServer{

  public static String getInput(String prompt) {
    try {
      System.out.println(prompt);
      BufferedReader userInput = new BufferedReader( new InputStreamReader(System.in) );
      String result = userInput.readLine();
      if(result.equals("")) {
        return getInput("You didn\'t type anything...");
      } else {
        return result;
      }
    } catch (IOException e) {
      e.printStackTrace();
    }
    return "";
  }

  public static void main(String [] args){
    int connectionPort;
    int boardRows;
    int boardCols;
    int startingPlayer;

    connectionPort = Integer.parseInt(getInput("What port do you want this server to be on?"));
    boardRows = Integer.parseInt(getInput("How many rows do you want the board on this server to have?"));
    boardCols = Integer.parseInt(getInput("How many columns?"));
    startingPlayer = Integer.parseInt(getInput("Who do you want the starting player to be? Type 1 for player 1 and 2 for player 2:"));

    try {
      Thread serverThread = new CFServer(connectionPort, boardRows, boardCols, 0);
      serverThread.start();
    } catch (IOException e) {
      e.printStackTrace();
    }
  }
}