package basketballsim;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Scanner;

/**
 * @author Francisco Di Giglio
 */
public class StatisticalAnalysis{
    /**
     * Make this a multi threaded in order to improve speed on running games in the millions
     */


    public static String getDate(){
        DateTimeFormatter dtf = DateTimeFormatter.ofPattern("MMddyyyy");
        LocalDateTime now = LocalDateTime.now();
        String date = dtf.format(now);
        System.out.println(date);
        return date;
    }
    
    public static String convertCityToName(String city){
        switch(city){
            case "Atlanta":
                return "hawks";
            case "Boston":
                return "celtics";
            case "Brooklyn":
                return "nets";
            case "Charlotte":
                return "hornets";
            case "Chicago":
                return "bulls";
            case "Cleveland":
                return "cavaliers";
            case "Dallas":
                return "mavericks";
            case "Denver":
                return "nuggets";
            case "Detroit":
                return "pistons";
            case "Golden St.":
                return "warriors";
            case "Houston":
                return "rockets";
            case "Indiana":
                return "pacers";
            case "L.A. Clippers":
                return "clippers";
            case "L.A. Lakers":
                return "lakers";
            case "Memphis":
                return "grizzlies";
            case "Miami":
                return "heat";
            case "Milwaukee":
                return "bucks";
            case "Minnesota":
                return "timberwolves";
            case "New Orleans":
                return "pelicans";
            case "New York":
                return "knicks";
            case "Oklahoma City":
                return "thunder";
            case "Orlando":
                return "magic";
            case "Philadelphia":
                return "76ers";
            case "Phoenix":
                return "suns";
            case "Portland":
                return "trailblazers";
            case "Sacramento":
                return "kings";
            case "San Antonio":
                return "spurs";
            case "Toronto":
                return "raptors";
            case "Utah":
                return "jazz";
            case "Washington":
                return "wizards";
        }
        return "NO EXISTING TEAM";
    }


    public static String[][] playNumGames(Team team1, Team team2, int nTimes){
        //Add back player PPG to see how impactful certain players can be
        String[] headers = {"NAME", "WIN %", "# of Wins", "Team AVG PTS/G"};
        Game game = new Game(team1, team2);
        String[][] stats = {
            headers,
            {team1.getName().toUpperCase(), null, null, null},
            {team2.getName().toUpperCase(), null, null, null}
        };

        for(int i=0; i<nTimes; i++){
            game.playGame();
        }
        
        double team1WinPercentage = (double)team1.getWins() / (team1.getGamesPlayed()) * 100;
        double team2WinPercentage = (double)team2.getWins() / (team2.getGamesPlayed()) * 100;
        team1WinPercentage = Math.round(team1WinPercentage);
        team2WinPercentage = Math.round(team2WinPercentage);

        stats[1][1] = team1WinPercentage + "%";
        stats[2][1] = team2WinPercentage + "%";
        stats[1][2] = team1.getWins() + " Total Wins";
        stats[2][2] = team2.getWins() + " Total Wins";
        stats[1][3] = team1.getAveragePointsTeam() + " PTS/G";
        stats[2][3] = team2.getAveragePointsTeam() + " PTS/G";

        return stats;
    }

    public static String createFile(String[][] stats, String filePath){
        String team1 = stats[1][0].toUpperCase();
        String team2 = stats[2][0].toUpperCase();
        filePath = filePath + "/" + team1 + "vs" + team2 + ".csv";

        try(FileWriter filewriter = new FileWriter(filePath); PrintWriter printer = new PrintWriter(filewriter)){
            // printer.write("TEAM NAME,WIN PERCENTAGE\n");
            for(int i=0; i<stats.length; i++){
                printer.write(stats[i][0] + "," + stats[i][1] + "," + stats[i][2] + "," + stats[i][3] + "\n");
            }
        } catch(IOException e){
            System.out.println("FILE NOT FOUND");
        }

        return "Completed " + stats[1][0] + " vs. " + stats[2][0];
    }

    public void simulateGamesAutomatically(){

        String filepath = "data/statsOfGames/2023-2024-Season/Games/testing/" + getDate();

        File file = new File(filepath);
        file.mkdir();

        ArrayList<String> homeTeams = new ArrayList<>();
        ArrayList<String> awayTeams = new ArrayList<>();

        String filename = "data/schedule/todaySchedule.csv";
        try(FileReader filereader = new FileReader(filename); BufferedReader buffer = new BufferedReader(filereader)){
            // Skip header
            buffer.readLine();
            // Reads games
            String games = buffer.readLine();
            while(games!=null){
                String[] matchup = games.split(",");
                // System.out.println(matchup[0] + ":" + matchup[1] + "\n");
                homeTeams.add(matchup[0]);
                awayTeams.add(matchup[1]);

                games = buffer.readLine();
            }
        } catch(IOException ie){
            System.out.println(filename + "File Not Found");
        }

        int amountOfTimes = 13500;
        long start = System.currentTimeMillis();
        for(int i=0; i<homeTeams.size(); i++){
            String[][] teamStats = playNumGames(new Team(convertCityToName(homeTeams.get(i)), 'H'), new Team(convertCityToName(awayTeams.get(i)), 'A'), amountOfTimes);
            System.out.println(createFile(teamStats, filepath));
        }
        long end = System.currentTimeMillis();
        double totalTime = (end - start) / 1000.0;
        System.out.println("Took " + totalTime + " seconds to simulate " + homeTeams.size() + " number of fixtures " + amountOfTimes + " times each");

    }

    public void simulateGamesManually(){
        Scanner scan = new Scanner(System.in);

        //Comment these out unless for preseason testing
        // System.out.print("Enter Team for preseason testing >> ");
        // String teamCurrent = scan.nextLine();

        // System.out.print("Enter home or away >> ");
        // String homeOrAway = scan.nextLine();

        System.out.print("Enter number of teams playing >> ");
        int sizeOfArray = scan.nextInt();
        while(sizeOfArray % 2 != 0){
            System.out.print("Not an even number, enter number of teams playing >> ");
            sizeOfArray = scan.nextInt();
        }

        System.out.print("Enter today's date (12052023)>> ");
        String date = scan.next();

        // For Season Games
        String filepath = "data/statsOfGames/2023-2024-Season/Games/" + date;
        // For preseason predictions
        // String filepath = "data/statsOfGames/2023-2024-Season/Preseason-Predictions/" + teamCurrent + "/" + homeOrAway;
        
        File file = new File(filepath);
        file.mkdir();

        Team[] arrayOfTeams = new Team[sizeOfArray];
        System.out.print("Enter team names separated with a space >> ");
        String input = scan.next().trim();
        int index = 0;
        // For Season simulation turn isHome to true
        boolean isHome = false;
        while(!input.equals("q")){
            System.out.println(input);
            Team team;
            //Adds margin depending if home team or not
            if(isHome) {
                team = new Team(input, 'H');
                isHome = false;
            }
            else {
                team = new Team(input, 'A');
                isHome = true;
            }
            arrayOfTeams[index] = team;
            index++;
            input = scan.next().trim();
        }

        scan.close();
        int amountOfTimes = 13500;
        long start = System.currentTimeMillis();
        for(int i=0; i<arrayOfTeams.length; i+=2){
            Team team1 = arrayOfTeams[i];
            Team team2 = arrayOfTeams[i+1];
            String[][] stats = playNumGames(team1, team2, amountOfTimes);
            System.out.println(createFile(stats, filepath));
        }
        long end = System.currentTimeMillis();
        double totalTime = (end - start) / 1000.0;
        System.out.println("Took " + totalTime + " seconds to simulate " + (arrayOfTeams.length / 2) + " number of fixtures " + amountOfTimes + " times each");

        System.out.println(Arrays.toString(arrayOfTeams));

    }

    public static void main(String[] args) {
        /**
         * ADD ANOTHER COLUMN TO GAME STATS COMPARING HOW MANY GAMES ONE 
         * AUTOMATE THIS ()
         * Create a season directory to (DONE)
         * Add homecourt advantage shooting percentage (implemented in the scrape file) (DONE)
         * Add functionality of newly added home and away shooting percentages (DONE)
         */

        StatisticalAnalysis stat = new StatisticalAnalysis();

        //Call this function when simulating manually
        // stat.simulateGamesManually();

        //Call this function to simulate automatically
        // Need to run python program to get the schedule
        stat.simulateGamesAutomatically();
        

        //Call this function when simulating automatically
            //Before calling function, we need the games for the day, order them in 2 separate arrays in order to mainting the home away adv
                //COMPLETED CSV CREATION USING PYTHON
            //Simulate and store game results in the date simulating
            //Prior to simulating it should have updated the injury list (Low priority for now)
            //https://theathletic.com/nba/schedule/ --> good link to scrape from since it only shows today's games on one page
    }
}
