import java.io.*;

class Board {
  private int [][] rawData;
  private boolean startingPlayer;
  private int rows;
  private int columns;

  private String[] playerDict = {"x","o"};

  public Board(int rows, int columns, boolean startingPlayer){
    this.rows = rows;
    this.columns = columns;
    this.startingPlayer = startingPlayer;
    createEmptyData();
  }

  private void createEmptyData() {
    int[][] emptyBoard = new int[this.rows][this.columns];
    for(int row = 0; row < this.rows; row = row + 1) {
      for(int column = 0; column < this.columns; column = column + 1) {
        emptyBoard[row][column] = 0;
      }
    }
    this.rawData = emptyBoard;
  }

  public int [][] getRawData(){
    return this.rawData;
  }

  public void printBoard(){
    for(int row = 0; row < this.rows; row += 1){
      for(int column = 0; column < this.columns; column += 1){
        System.out.print(this.rawData[row][column]);
        System.out.print(" ");
      }
      System.out.println("");
    }
    System.out.println("");
  }

  public int getPlayer(){
    int numOfX = 0;
    int numOfO = 0;
    for(int row=0;row < this.rows; row += 1){
      for(int column=0; column < this.columns; column += 1){
        if(this.rawData[row][column] == 1){
          numOfX += 1;
        }
        else if(this.rawData[row][column] == 2){
          numOfO += 1;
        }
      }
    }
    if(numOfX == numOfO){
      return 1;
    } else {
      return 2;
    }
  }

  public boolean play(int column){
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

  public boolean checkWin(){
    int[][] directions = {{1,1},{-1,-1},{1,-1},{-1,1},{0,1},{1,0},{0,-1},{-1,0}};
    int[] directionCheck;
    for(int currentPlayer = 1; currentPlayer < 3; currentPlayer += 1){
      directionCheck = {0,0,0,0,0,0,0,0};
    }
  }

}

public class ConnectFourServer {
  public static void main(String [] args){
    Board testBoard = new Board(7,9,false);
    testBoard.play(4);
    testBoard.printBoard();
    System.out.println("Testing...");
  }
}
