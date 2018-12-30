package ConnectFour;

import java.io.*;
import java.net.*;
import ConnectFour.Board.*;
import java.util.Random;
import java.util.Scanner;

class AI{

  public static Board AIPlay(Board currentBoard, int maxDepth, int player) {
    int highest = -99999;
    int colToPlay = 0;
    Board retBoard = currentBoard.cloneBoard(currentBoard);

    for(int col = 0; col < currentBoard.getColumns(); col++){
      if(currentBoard.checkTheoretical(currentBoard, col) == true) {
        Board newBoard = currentBoard.cloneBoard(currentBoard);
        newBoard.play(col);
        int maxScore = playMin(newBoard, player, 1, maxDepth);
        if(maxScore > highest) {
          highest = maxScore;
          colToPlay = col;
        }
      }

    }

    retBoard.play(colToPlay);

    return retBoard;
  }

  private static int playMax(Board currentBoard, int player, int depth, int maxDepth) {
    if(depth >= maxDepth) {
      return calcScore(currentBoard, player);
    }

    int highest = -99999;

    for(int col = 0; col < currentBoard.getColumns(); col++){
      if(currentBoard.checkTheoretical(currentBoard, col) == true){
        Board newBoard = currentBoard.cloneBoard(currentBoard);
        newBoard.play(col);
        int maxScore = playMin(newBoard, player, depth + 1, maxDepth);
        if(maxScore >= highest) {
          highest = maxScore;
        }
      }
    }

    return highest;
  }

  private static int playMin(Board currentBoard, int player, int depth, int maxDepth) {
    if(depth >= maxDepth) {
      return calcScore(currentBoard, player);
    }

    int lowest = 99999;

    for(int col = 0; col < currentBoard.getColumns(); col++){
      if(currentBoard.checkTheoretical(currentBoard, col) == true){
        Board newBoard = currentBoard.cloneBoard(currentBoard);
        newBoard.play(col);
        int minScore = playMax(newBoard, player, depth + 1, maxDepth);
        if(minScore <= lowest) {
          lowest = minScore;
        }
      }
    }

    return lowest;
  }

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
      if(score >= 3) {
        finalScore += 30;
      } else {
        finalScore += score;

      }
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
}

class Client{

  private Socket client;

  private int port;
  private String connectionName;
  private String playerToken;
  private int difficulty;
  private boolean isAI = false;
  private int playerNum;
  private Board currentBoard;

  public Client(String connectionName, int port, String playerToken, int isAI, int difficulty){
    
    this.connectionName = connectionName;
    this.port = port;
    this.playerToken = playerToken;
    this.isAI = isAI == 0 ? false : true;
    this.difficulty = difficulty;

  }

  public boolean connect() {
    try {
      System.out.println("Connecting to " + this.connectionName + " on port " + this.port);
      this.client = new Socket(this.connectionName, this.port);

      System.out.println("Now connected to " + this.client.getRemoteSocketAddress());

      InputStream checkIn = client.getInputStream();
      DataInputStream checkDataIn = new DataInputStream(checkIn);
      playerNum = Integer.parseInt(checkDataIn.readUTF());
      System.out.println(playerNum);

      OutputStream checkOut = client.getOutputStream();
      DataOutputStream checkDataOut = new DataOutputStream(checkOut);
      checkDataOut.writeUTF(playerToken);
      checkDataOut.flush();
      boolean running = true;
      System.out.println(playerToken);
    } catch (IOException e) {
      e.printStackTrace();
      return false;
    }
    return true;
  }

  public boolean run(){
    boolean running = true;
    try {
      if(connect()) {
        while(running){
          InputStream inFromServer = this.client.getInputStream();
          ObjectInputStream in = new ObjectInputStream(inFromServer);
          this.currentBoard = (Board) in.readObject();

          if(this.currentBoard.checkWin() != 0){
            if(this.currentBoard.checkWin() == 3) {
              System.out.println("Tie!");
            } else if (this.currentBoard.checkWin() < 3){
              System.out.print(this.currentBoard.getToken(this.currentBoard.checkWin()));
              System.out.print(" wins!\n");
            } else {
              System.out.println("Someone disconnected!");
            }
            running = false;
          }
          else {
            if(this.isAI == false) {
              currentBoard.printBoard();
              BufferedReader userInput = new BufferedReader( new InputStreamReader(System.in) );

              System.out.println("Type which column you want to play:");
              System.out.println("(Make it a number)");
              System.out.println("(You can also type quit if you want to quit)");

              String userIn = userInput.readLine();

              if(userIn.toLowerCase().equals("quit")) {
                this.currentBoard.setOver(true);
                running = false;
              } else {
                this.currentBoard.play(Integer.parseInt(userIn));
              }

              this.currentBoard.printBoard();
            } else {
              this.currentBoard.printBoard();
              this.currentBoard = AI.AIPlay(currentBoard, difficulty, playerNum);
              this.currentBoard.printBoard();
            }

            OutputStream boardToServer = this.client.getOutputStream();
            ObjectOutputStream out = new ObjectOutputStream(boardToServer);
            out.writeObject(this.currentBoard);
          }  
        }
      }

      System.out.println("Do you want to play again? Type yes if you do, and anything else if no:");
      BufferedReader userInput = new BufferedReader( new InputStreamReader(System.in) );
      String userIn = userInput.readLine();
      if(userIn.toLowerCase().equals("yes")) {

        return true;
      }

      return false;

    } catch (IOException e){
        e.printStackTrace();
    } catch (ClassNotFoundException c){
      c.printStackTrace();
    }
    return false;
  }
}

public class ConnectFourClient{
  private String playerName;

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

  public static void main(String[] args) {
    String connectionName;// = args[0];
    int port;// = Integer.parseInt(args[1]);
    String playerToken;// = args[2];
    int isAI;// = Integer.parseInt(args[3]);
    int difficulty;// = Integer.parseInt(args[4]);

    int playerNum;

    connectionName = getInput("Type the address of the server:");
    port = Integer.parseInt(getInput("What port are you connecting to?"));
    playerToken = getInput("Your pieces will be represented by a single character. Type that character below:");
    String checkIsAI = getInput("Are you an AI? Y for yes and N for no");
    if(checkIsAI.toLowerCase().equals("y")){
      isAI = 1;
      difficulty = Integer.parseInt(getInput("How many moves do you want to look ahead? I recommend about 4."));
    } else {
      isAI = 0;
      difficulty = 0;
    }

    Client cd = new Client(connectionName,port,playerToken,isAI,difficulty);
    boolean running = cd.run();
    while(running == true) {
      running = cd.run();
    }
  }
}