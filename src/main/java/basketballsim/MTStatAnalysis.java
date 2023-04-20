package basketballsim;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Scanner;

public class MTStatAnalysis {
    private final Object lock = new Object();

    private void playNGames(Game game, int x){
        for(int i=0; i<x; i++){
            game.playGame();
        }
    }

    public String[][] playNumGames(Team team1, Team team2, int nTimes){
        String[] headers = {"NAME", "WIN %", "# of Wins"};
        Game game = new Game(team1, team2);
        String[][] stats = {
            headers,
            {team1.getName().toUpperCase(), null, null},
            {team2.getName().toUpperCase(), null, null}
        };

        final int chunk = (int) (nTimes / 1000);

        ArrayList<Thread> threads = new ArrayList<>();
        for(int i=0; i<nTimes; i+=chunk){
            Thread thread = new Thread(() ->{
                synchronized(game){
                    playNGames(game, chunk);
                }
            });
            thread.start();
            threads.add(thread);
        }

        for(Thread thread: threads){
            try {
                thread.join();
            } catch (InterruptedException e) {}
        }
        
        double team1WinPercentage = (double)team1.getWins() / (team1.getGamesPlayed()) * 100;
        double team2WinPercentage = (double)team2.getWins() / (team2.getGamesPlayed()) * 100;
        team1WinPercentage = Math.round(team1WinPercentage);
        team2WinPercentage = Math.round(team2WinPercentage);

        stats[1][1] = team1WinPercentage + "%";
        stats[2][1] = team2WinPercentage + "%";
        stats[1][2] = team1.getWins() + " Total Wins";
        stats[2][2] = team2.getWins() + " Total Wins";

        return stats;
    }

    public static String createFile(String[][] stats, String filePath){
        String team1 = stats[1][0].toUpperCase();
        String team2 = stats[2][0].toUpperCase();
        filePath = filePath + "/" + team1 + "vs" + team2 + ".csv";

        try(FileWriter filewriter = new FileWriter(filePath); PrintWriter printer = new PrintWriter(filewriter)){
            // printer.write("TEAM NAME,WIN PERCENTAGE\n");
            for(int i=0; i<stats.length; i++){
                printer.write(stats[i][0] + "," + stats[i][1] + "," + stats[i][2] + "\n");
            }
        } catch(IOException e){
            System.out.println("FILE NOT FOUND");
        }

        return "Completed " + stats[1][0] + " vs. " + stats[2][0];
    }

    public static void main(String[] args) {
        /**
         * ADD ANOTHER COLUMN TO GAME STATS COMPARING HOW MANY GAMES ONE 
         */
        Scanner scan = new Scanner(System.in);
        System.out.print("Enter number of teams playing >> ");
        int sizeOfArray = scan.nextInt();
        while(sizeOfArray % 2 != 0){
            System.out.print("Not an even number, enter number of teams playing >> ");
            sizeOfArray = scan.nextInt();
        }
        

        System.out.print("Enter today's date (12052023)>> ");
        String date = scan.next();
        String filepath = "data/statsOfGames/" + date;
        File file = new File(filepath);
        file.mkdir();

        Team[] arrayOfTeams = new Team[sizeOfArray];
        System.out.print("Enter team names separated with a space >> ");
        String input = scan.next().trim();
        int index = 0;
        while(!input.equals("q")){
            System.out.println(input);
            Team team = new Team(input);
            arrayOfTeams[index] = team;
            index++;
            input = scan.next().trim();
        }

        scan.close();
        long start = System.currentTimeMillis();
        for(int i=0; i<arrayOfTeams.length; i+=2){
            Team team1 = arrayOfTeams[i];
            Team team2 = arrayOfTeams[i+1];
            MTStatAnalysis mt = new MTStatAnalysis();
            String[][] stats = mt.playNumGames(team1, team2, 13000);
            System.out.println(createFile(stats, filepath));
        }
        long end = System.currentTimeMillis();
        double totalTime = (end - start) / 1000.0;
        System.out.println("Took " + totalTime + " seconds to simulate " + (arrayOfTeams.length / 2) + " number of fixtures 13000 times each");

        System.out.println(Arrays.toString(arrayOfTeams));
    }


    
}
