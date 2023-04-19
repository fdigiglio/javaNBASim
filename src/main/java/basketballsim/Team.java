package basketballsim;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Random;

/**
 * @author Francisco Di Giglio
 */
public class Team {
    private String name;
    private final String filename;
    private String abbrv;
    private Player[] arrayOfPlayers = new Player[10];
    private Player[] fiveOnCourt = new Player[5];
    private Player[] fiveBench = new Player[5];
    private Player[] originalLineup = new Player[10];
    private Player[] originalFiveOnCourt = new Player[5];
    private Player[] originalFiveBench = new Player[5];
    // private ArrayList<Player> fiveBench = new ArrayList<>(5);
    private int wins = 0;
    private int losses = 0;
    private double timePerPossession;
    private Random random;
    private boolean hasPossession = false;
    private ArrayList<Integer> teamTime = new ArrayList<>();
    private double usage;
    private int totalPointsForSim;
    // Find team division and conference
    

    /**
     * @param name - String of team name and uses the string to find the team statistic file in order to create each player
     */
    public Team(String name){
        this.name = name;
        filename = "data/teamStats/" + name + ".csv";
        try(FileReader filereader = new FileReader(filename); BufferedReader buffer = new BufferedReader(filereader)){
            // Skip header
            buffer.readLine();
            // Reads the second line for player
            String player = buffer.readLine();
            
            String possessionLine = "";
            int index = 0;
            while(player != null && index < 11){
                // Checks if the index is 10 because after that it is supposed to represent the teams abbreviation and seconds per possession
                if(index == 10){
                    possessionLine = player;
                    break;
                }
                // Otherwise splits the string on commas because the file is a .csv
                String[] playerStats = player.split(",");
                // Creates a new player using that String array
                Player playerObject = new Player(playerStats);
                arrayOfPlayers[index] = playerObject;
                originalLineup[index] = playerObject;

                player = buffer.readLine();
                index++;
            }
            String[] possArray = possessionLine.split(",");
            this.abbrv = possArray[0];
            this.timePerPossession = Double.parseDouble(possArray[1]);

            for(int i=0; i<arrayOfPlayers.length / 2; i++){
                fiveOnCourt[i] = arrayOfPlayers[i];  
                originalFiveOnCourt[i] = arrayOfPlayers[i];  
            }

            for(int i=arrayOfPlayers.length/2; i<arrayOfPlayers.length; i++){
                fiveBench[i-5] = arrayOfPlayers[i];    
                originalFiveBench[i-5] = arrayOfPlayers[i];
            }

        } catch(IOException ie){
            System.out.println(filename + "File Not Found");
        }
    }

    public String getName(){
        return this.name;
    }

    public String getAbbrv(){
        return this.abbrv;
    }

    public Player[] getArrayOfPlayers() {
        return arrayOfPlayers;
    }

    public Player[] getFiveOnCourt(){
        return this.fiveOnCourt;
    }

    public Player[] getFiveOnBench(){
        return this.fiveBench;
    }

    public int getWins() {
        return wins;
    }

    public int getLosses() {
        return losses;
    }

    public double getTimePerPossession() {
        return timePerPossession;
    }

    /**
     * @return integer - represents the amount of time in seconds that a possession will take
     */
    public int getPossesion(){
        random = new Random();
        // return the a random possession time with 1 second negative margin and 2 second positive margin
        int negativeMargin = (int) Math.round(this.timePerPossession - 2);
        int positiveMargin = (int) Math.round(this.timePerPossession + 2);
        return random.nextInt(negativeMargin, positiveMargin);
    }
    public boolean getHasPossession(){
        return this.hasPossession;
    }
    
    public void possession(){
        this.hasPossession = true;
    }

    public void lostPossession(){
        this.hasPossession = false;
    }

    public void addTime(int time){
        this.teamTime.add(time);
    }

    public ArrayList<Integer> getTeamTime(){
        return this.teamTime;
    }

    /**
     * Sets the total usage rate for the five players on the court at that given moment
     */
    public void totalUsageRate(){
        double usg = 0.0;
        Player[] fiveOn = this.getFiveOnCourt();
        for(int i=0; i<fiveOn.length; i++){
            usg += fiveOn[i].getUsageRate();
        }
        this.usage = usg;
    }

    public double getUsage(){
        return this.usage;
    }

    public void updateFiveOn(Player[] players){
        this.fiveOnCourt = players;
    }

    public void updateBench(Player[] players){
        this.fiveBench = players;
    }

    public void win(){
        this.wins++;
    }

    public void loss(){
        this.losses++;
    }

    public void resetLoss(){
        this.losses = 0;
    }

    public void resetWins(){
        this.wins = 0;
    }

    public int getGamesPlayed(){
        return this.wins + this.losses;
    }

    public void resetPlayerMinutes(){
        for(int i=0; i<this.fiveOnCourt.length; i++){
            fiveOnCourt[i].resetCurrentTime();
        }
        
        for(int i=0; i<this.fiveBench.length; i++){
            fiveBench[i].resetCurrentTime();
        }
    }

    public String getFilename() {
        return filename;
    }

    public Player[] getFiveBench() {
        return fiveBench;
    }

    public Player[] getOriginalLineup() {
        return originalLineup;
    }

    public Player[] getOriginalFiveOnCourt() {
        return originalFiveOnCourt;
    }

    public Player[] getOriginalFiveBench() {
        return originalFiveBench;
    }

    public Random getRandom() {
        return random;
    }

    public int getTotalPointsForSim() {
        return totalPointsForSim;
    }

    public double getAveragePointsTeam(){
        return this.totalPointsForSim / (this.wins + this.losses);
    }

    public void addPoints(int points){
        this.totalPointsForSim += points;
    } 
    
    public void resetTotalPoints(){
        this.totalPointsForSim = 0;
    }

    @Override
    public String toString(){
        return this.name;
    }

    @Override
    public boolean equals(Object other){
        if(other instanceof Team){
            Team otherTeam = (Team) other;
            if(this.name.equals(otherTeam.name)){
                return true;
            }
        }

        return false;
    }
    
    public static void main(String[] args) {
        Team heat = new Team("heat");
        // System.out.println(Arrays.toString(heat.getArrayOfPlayers()));
        Player[] arr  = heat.getArrayOfPlayers();
        // System.out.println(Arrays.toString(arr));
        Arrays.sort(arr);
        Player[] fiveOn = heat.getFiveOnCourt();
        Arrays.sort(fiveOn);
        System.out.println(Arrays.toString(fiveOn));
        // System.out.println(Arrays.toString(heat.getFiveOnBench().toArray()));
        heat.getFiveOnCourt();
        // System.out.println(Arrays.toString(arr));
        // System.out.println(heat.getTimePerPossession());
        // System.out.println(heat.getAbbrv());
    }

}
