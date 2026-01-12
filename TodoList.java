// This is a simple command line todolist
// Using Queue, it stores in RAM( Siya ram)
import java.util.Scanner;
public class TodoList {
    public static void main(String[] args) {
        boolean exit = false;
        int front=0,back=0;
        String choice;
        String text[] = new String[20];
        text[0] = ""; 
        Scanner s = new Scanner(System.in);
        do {
            System.out.println("\n\nTODO LIST (Using Queue):-\n1. Add\n2. Remove\n3. Show");
            choice = s.nextLine();
            switch (choice) {
                case "1":
                    text[back] = s.nextLine();
                    System.out.println("Task added: "+text[back++]);
                    break;
                case "2":
                    if (text[front] == "" || text[front] == null) System.out.println("Empty list.");
                    else{
                        System.out.println("Removed: "+text[front++]);
                    }
                    break;
                case "3":
                    if (text[front] == "" || text[front] == null) System.out.println("Empty list.");
                    else {
                        System.out.println("Task:-");
                        for(int j=front,k=1;j<=back-1;j++,k++)
                            System.out.println(k+"."+text[j]);
                    }
                    break;
                case "4":
                    System.out.println("Thanks for Using!");
                    exit = true;
                    break;

                default:
                    System.out.println("Invalid Choice");
                    break;
            }
        } while (!exit);
        s.close();
    }
}