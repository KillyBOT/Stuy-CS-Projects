import java.io.*;

public class ConnectFourServer {
  public static void main(String [] args){
    Board testBoard = new Board(7,9,1);
    testBoard.play(4);
    testBoard.play(5);
    testBoard.play(4);
    testBoard.play(5);
    testBoard.play(4);
    testBoard.play(5);
    testBoard.printBoard();
    System.out.println(testBoard.checkWin());
    System.out.println("Testing complete!");
  }
}
