import java.util.Scanner;

public class pin {
    public static void main(String[] args) {
        
        Scanner scanner = new Scanner(System.in);

        int pins[] = {1, 2, 3, 4, 5};
        boolean pinUsed[] = new boolean[6];

        //initialize pins
        for (int i = 0; i < pinUsed.length; i++) {

            pinUsed[i] = false;

        } 

        // check pin if free 
        System.out.print("Enter your chosen pin : ");
        int pinChoice = scanner.nextInt();
        for (int i = 0 ; i < pins.length; i++) {

            if (pins[i] == pinChoice) {

                pinUsed[i] = true;

            } else {
                pinUsed[i] = false;
            }

        }

        for (int i = 0; i < pinUsed.length; i++) {
            System.out.println(pinUsed[i]);
        }

    }
}