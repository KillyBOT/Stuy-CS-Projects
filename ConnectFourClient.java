package ConnectFour;

import java.io.*;
import java.net.*;
import ConnectFour.Board.*;

public class ConnectFourClient {
  private int playerNum;
  private String playerName;

  //private Board AIPlay(Board currentBoard) {}

  //private int playMax(Board currentBoard, int player) {}

  //private int playMin(Board currentBoard, int player) {}

  private static int calcScorePos(Board currentBoard, int row, int column) {
    int player = currentBoard.getPos(row, column);
    int finalScore = 0;

    if(player == 0) {
      return finalScore;
    }

    int[][] directions = {{1,1},{-1,-1},{1,0},{0,1},{-1,0},{0,-1},{1,-1},{-1,1}};
    int[] directionScore = {0,0,0,0,0,0,0,0};

    for(int directionNum = 0; directionNum < directions.length; directionNum++){
      int[] direction = directions[directionNum];
      for(int out = 1; out < 4; out++){

        int rowPos = row + (out * direction[0]);
        int colPos = column+(out * direction[1]);

        if(rowPos >= 0 && colPos >= 0 && rowPos < currentBoard.getRows() && colPos < currentBoard.getColumns()){
          if(currentBoard.getPos(rowPos, colPos) == 0) {
            if(currentBoard.getPos(rowPos-direction[0],colPos-direction[1]) == 0) {
              break;
            } else {
              if(rowPos + 1 < currentBoard.getRows()){
                if(currentBoard.getPos(rowPos+1,colPos) == 0) {
                  directionScore[directionNum] = 0;
                  break;
                }
              }
            }
          } else if(currentBoard.getPos(rowPos, colPos) == player) {
            directionScore[directionNum] += 1;
          } else {
            directionScore[directionNum] = 0;
            break;
          }
        } else {
          directionScore[directionNum] = 0;
          break;
        }
      }
    }

    for(int score: directionScore) {
      finalScore += score;
    }

    return finalScore;
  }

  private static int calcScore(Board currentBoard, int player) {
    int finalScore = 0;

    for(int row = 0; row < currentBoard.getRows(); row++) {
      for(int column = 0; column < currentBoard.getColumns(); column++){
        if(currentBoard.getPos(row, column) == player) {
          finalScore += calcScorePos(currentBoard, row, column);
        } else if(currentBoard.getPos(row, column) != 0) {
          finalScore -= calcScorePos(currentBoard, row, column);
        }
      }
    }

    return finalScore;
  }

  public static void main(String[] args) {
    String connectionName = args[0];
    int port = Integer.parseInt(args[1]);
    String playerToken = args[2];
    int isAI = Integer.parseInt(args[3]);

    try {
      System.out.println("Connecting to " + connectionName + " on port " + port);
      Socket client = new Socket(connectionName, port);

      System.out.println("Now connected to " + client.getRemoteSocketAddress());
      OutputStream checkOut = client.getOutputStream();
      DataOutputStream checkDataOut = new DataOutputStream(checkOut);
      checkDataOut.writeUTF(playerToken);
      checkDataOut.flush();
      boolean running = true;

      while(running) {
        InputStream inFromServer = client.getInputStream();
        ObjectInputStream in = new ObjectInputStream(inFromServer);
        Board currentBoard = (Board) in.readObject();

        currentBoard.play(1);
        currentBoard.play(2);
        currentBoard.printBoard();
        System.out.println(calcScore(currentBoard, 1));
        System.out.println(calcScore(currentBoard, 2));

        if(currentBoard.checkWin() == 0){
          running = false;
        }

        OutputStream boardToServer = client.getOutputStream();
        ObjectOutputStream out = new ObjectOutputStream(boardToServer);
        out.writeObject(currentBoard);
        out.flush();

      }

      client.close();
    } catch (IOException e) {
      e.printStackTrace();
    } catch (ClassNotFoundException c) {
      System.out.println("Board class not found");
      c.printStackTrace();
      return;
    }

  }
}
