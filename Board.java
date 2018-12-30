package ConnectFour;

import java.io.*;

public class Board implements java.io.Serializable{
  private int [][] rawData;
  private int startingPlayer;
  private int rows;
  private int columns;

  private boolean isOver;

  private char[] playerDict = {'x','o'};
  private String[] playerNameDict = {"Player 1","Player 2"};

  public Board(int rows, int columns, int startingPlayer){
    this.rows = rows;
    this.columns = columns;
    if(startingPlayer <= 0 || startingPlayer > 2){
      this.startingPlayer = 1;
    } else {
      this.startingPlayer = startingPlayer;
    }
    this.isOver = false;
    createEmptyData();
  }

  private void createEmptyData() {
    int[][] emptyBoard = new int[this.rows][this.columns];
    for(int row = 0; row < this.rows; row++) {
      for(int column = 0; column < this.columns; column++) {
        emptyBoard[row][column] = 0;
      }
    }
    this.rawData = emptyBoard;
  }

  public int [][] getRawData(){
    return this.rawData.clone();
  }

  public int getStartingPlayer(){
    return this.startingPlayer;
  }

  public void printBoard(){
    for(int row = 0; row < this.rows; row++){
      for(int column = 0; column < this.columns; column++){
        if(this.rawData[row][column] > 0) {
          System.out.print(this.playerDict[this.rawData[row][column]-1]);
        } else {
          System.out.print(".");
        }
        System.out.print(" ");
      }
      System.out.print(row);
      System.out.println("");
    }

    for(int column = 0; column < this.columns; column++){
      System.out.print(Integer.toString(column) + " ");
    }
    System.out.println("");
  }


  public String getBoardString(){
    String retString = "";
    retString = retString + Integer.toString(this.rows);
    retString = retString + Integer.toString(this.columns);
    for(int row = 0; row < this.rows; row++){
      for(int column = 0; column < this.columns; column++){
        retString = retString + Integer.toString(this.rawData[row][column]);
      }
    }

    return retString;
  }

  public int getPlayer(){
    int numOfX = 0;
    int numOfO = 0;
    for(int row=0;row < this.rows; row++){
      for(int column=0; column < this.columns; column++){
        if(this.rawData[row][column] == 1){
          numOfX += 1;
        }
        else if(this.rawData[row][column] == 2){
          numOfO += 1;
        }
      }
    }
    if(numOfX == numOfO){
      return this.startingPlayer;
    } else {
      return (this.startingPlayer == 1) ? 2: 1;
    }
  }

  public int getPos(int row, int column) {
    return this.rawData[row][column];
  }

  public int getRows() {
    return this.rows;
  }

  public int getColumns() {
    return this.columns;
  }

  public boolean play(int colIn){
    int column = colIn;
    if(column < 0) {
      column = 0;
    } else if (column >= getRows()) {
      column = getRows() - 1;
    }
    
    if(this.rawData[0][column] != 0) {
      return false;
    } else {
      for(int row = 0; row < this.rows; row+=1){
        if(row+1 == this.rows){
          this.rawData[row][column] = getPlayer();
          return true;
        }
        else if(this.rawData[row+1][column] != 0) {
          this.rawData[row][column] = getPlayer();
          return true;
        }
      }
    }
    System.out.println("Dunno how this happened");
    return false;
  }

  public static boolean checkTheoretical(Board theoreticalBoard, int column){
    if(theoreticalBoard.getRawData()[0][column] != 0) {
      return false;
    } else {
      return true;
    }
  }

  public static Board cloneBoard(Board inBoard) {
    Board retBoard = null;
    try {
      ByteArrayOutputStream bout = new ByteArrayOutputStream();
      ObjectOutputStream out = new ObjectOutputStream(bout);
      out.writeObject(inBoard);
      out.flush();
      out.close();

      ObjectInputStream in = new ObjectInputStream( new ByteArrayInputStream(bout.toByteArray()) );
      retBoard = (Board) in.readObject();
    } catch(IOException e) {
      e.printStackTrace();
    } catch(ClassNotFoundException c) {
      c.printStackTrace();
    }

    return retBoard;
  }

  private int checkWinPos(int row, int column){
    int[][] directions = {{1,1},{-1,-1},{1,-1},{-1,1},{0,1},{1,0},{0,-1},{-1,0}};
    int currentPlayer = this.rawData[row][column];
    if(currentPlayer == 0) {
      return 0;
    }
    for(int currentDirection = 0; currentDirection < 8; currentDirection++){
      boolean ifGood = true;
      for(int out = 1; out < 4; out += 1){
        int nextRow = row + (directions[currentDirection][0] * out);
        int nextColumn = column + (directions[currentDirection][1] * out);
        if(nextRow >= 0 && nextRow < this.rows && nextColumn >= 0 && nextColumn < this.columns) {
          if(this.rawData[nextRow][nextColumn] != currentPlayer) {
            ifGood = false;
          }
        } else {
          ifGood = false;
        }
      }
      if(ifGood == true) {
        return currentPlayer;
      }
    }
    return 0;
  }

  public int checkWin(){
    if(isOver == true){
      return 4;
    }

    boolean anyEmpty = true;
    for(int row = 0; row < this.rows; row++) {
      for(int column = 0; column < this.columns; column++) {
        if(this.rawData[row][column] == 0) {
          anyEmpty = false;
        }
        int ifWinPos = checkWinPos(row, column);
        if(ifWinPos == 1 || ifWinPos == 2) {
          return ifWinPos;
        }
      }
    }
    return (anyEmpty == false) ? 0: 3;
  }

  public char getToken(int playerNum){
    return this.playerDict[playerNum-1];
  }

  public void registerPlayer(char playerToken, int playerNum) {
    this.playerDict[playerNum] = playerToken;
  }

  public void setOver(boolean toSet){
    this.isOver = toSet;
  }
}