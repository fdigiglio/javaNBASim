package basketballsim;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.Random;

/**
 * @author Francisco Di Giglio
 */
public class Game implements Possession{
    private int gameTime = 4 * 12 * 60;
    private int overtimeTime = 5 * 60;
    private Team homeTeam;
    private Team awayTeam;
    private int totalPossessions;
    private Random random = new Random();
    private int homeTeamPoints = 0;
    private int awayTeamPoints = 0;
    private ArrayList<Integer> totalTime = new ArrayList<>();

    /**
     * 
     * @param homeTeam
     * @param awayTeam
     */
    public Game(Team homeTeam, Team awayTeam){
        this.homeTeam = homeTeam;
        this.awayTeam = awayTeam;
        // Print Statement for debugging games
        // System.out.println(Arrays.toString(homeTeam.getFiveOnCourt()) + "STARTING 5 HOME TEAM");
        // System.out.println(Arrays.toString(homeTeam.getFiveOnBench()) + "BENCH 5 HOME TEAM");
        // System.out.println(Arrays.toString(awayTeam.getFiveOnCourt()) + "STARTING 5 AWAY TEAM");
        // System.out.println(Arrays.toString(awayTeam.getFiveOnBench()) + "BENCH 5 AWAY TEAM");
        // Set Possession Counter for each team
        int homePossessionCounter = 0;
        int awayPossessionCounter = 0;
        // compute total possessions in said gametime
        int time = 0;
        int turn = 0;
        while(time < gameTime){
            if(turn == 0){
                int homeTime = homeTeam.getPossesion();
                time += homeTime;
                homeTeam.addTime(homeTime);
                totalTime.add(homeTime);
                homePossessionCounter++;
                turn = 1;
            } else if(turn == 1){
                int awayTime = awayTeam.getPossesion();
                time += awayTime;
                awayTeam.addTime(awayTime);
                totalTime.add(awayTime);
                awayPossessionCounter++;
                turn = 0;
            }
        }
        // System.out.println(homeTeam.getAbbrv() + " POSSESSION TOTAL " + homePossessionCounter);
        // System.out.println(awayTeam.getAbbrv() + " POSSESSION TOTAL " + awayPossessionCounter);

        // get the average of the two and that will be the amount of possessions played in given game
        this.totalPossessions = (int) (homePossessionCounter + awayPossessionCounter);
        // System.out.println(totalPossessions);
        // System.out.println(homeTeam.getTeamTime().size());
        // System.out.println(awayTeam.getTeamTime().size());

        
        homeTeam.totalUsageRate();
        awayTeam.totalUsageRate();
    }

    public void playGame(){
        tipBall();
        if(homeTeam.getHasPossession()){
            playPossession(homeTeam, awayTeam, 0);
        } else if(awayTeam.getHasPossession()){
            playPossession(awayTeam, homeTeam, 0);
        }

        // OVERTIME
        while(true){
            if(homeTeamPoints == awayTeamPoints){
                homeTeam.updateFiveOn(homeTeam.getOriginalFiveOnCourt());
                homeTeam.updateBench(homeTeam.getOriginalFiveBench());
                awayTeam.updateFiveOn(awayTeam.getOriginalFiveOnCourt());
                awayTeam.updateBench(awayTeam.getOriginalFiveBench());
                // System.out.println("ENTERING OVERTIME\n\n");
                tipBall();
                possessions(overtimeTime);
                if(homeTeam.getHasPossession()){
                    playPossession(homeTeam, awayTeam, 0);
                    // System.out.println("OVERTIME!!!!!!");
                } else if(awayTeam.getHasPossession()){
                    playPossession(awayTeam, homeTeam, 0);
                    // System.out.println("OVERTIME!!!!!!");
                }
            } else {
                break;
            }
        }

        // Check who won
        if(homeTeamPoints > awayTeamPoints){
            homeTeam.win();
            awayTeam.loss();
            homeTeam.addPoints(homeTeamPoints);
            awayTeam.addPoints(awayTeamPoints);
        } else if(homeTeamPoints < awayTeamPoints){
            homeTeam.loss();
            awayTeam.win();
            homeTeam.addPoints(homeTeamPoints);
            awayTeam.addPoints(awayTeamPoints);
        }


        // System.out.println("HOME TEAM " + homeTeamPoints + " vs. " + awayTeamPoints + " AWAY TEAM");
        homeTeam.updateFiveOn(homeTeam.getOriginalFiveOnCourt());
        homeTeam.updateBench(homeTeam.getOriginalFiveBench());
        awayTeam.updateFiveOn(awayTeam.getOriginalFiveOnCourt());
        awayTeam.updateBench(awayTeam.getOriginalFiveBench());
        homeTeam.resetPlayerMinutes();
        awayTeam.resetPlayerMinutes();
        totalTime.clear();
        possessions(gameTime);
        homeTeam.lostPossession();
        awayTeam.lostPossession();
        homeTeamPoints = 0;
        awayTeamPoints = 0;
        // System.out.println(homeTeam.getFiveOnCourt()[0].getTimePlayed());
    }

    @Override
    public void playPossession(Team offensiveTeam, Team defensiveTeam, int possessionCounter) {
        // Condition is reversed because it will not call itself again once the possession counter reaches total possessions
        if(possessionCounter <= totalPossessions){
            // Check for subs before possession
            // System.out.println(checkLowestMinutes(offensiveTeam) + ":::" + checkLowestMinutes(offensiveTeam).getTimePlayed() + ":::" + checkLowestMinutes(offensiveTeam).getMinutesPlayed());
            if(checkLowestMinutes(offensiveTeam).getTimePlayed() <= 0 && !benchMinZero(offensiveTeam.getFiveOnBench())){
                // System.out.println("SUBS FOR " + offensiveTeam.getName());
                subs(offensiveTeam); 
                offensiveTeam.totalUsageRate();
            }
            if(checkLowestMinutes(defensiveTeam).getTimePlayed() <= 0 && !benchMinZero(defensiveTeam.getFiveOnBench())){
                // System.out.println("SUBS FOR " + defensiveTeam.getName());
                subs(defensiveTeam);
                defensiveTeam.totalUsageRate();
            }

            // Possession counter acts as index in time arraylist
            // System.out.println("TEAM TIME SIZE" + offensiveTeam.getTeamTime().size());
            if(totalTime.size() > possessionCounter){
                playersTimePlayed(offensiveTeam, totalTime.get(possessionCounter));
                playersTimePlayed(defensiveTeam, totalTime.get(possessionCounter));
            }

            Random rand = new Random();
            double chance = rand.nextDouble(0, offensiveTeam.getUsage());
            int index = 0;
            double sum1 = 0;
            Player[] fiveOn = offensiveTeam.getFiveOnCourt();
            double sum2 = fiveOn[0].getUsageRate();
            while(index < fiveOn.length){
                // System.out.println(chance + " >= " + sum1);
                // System.out.println(chance + " <= " + sum2);
                if(chance >= sum1 && chance <= sum2){
                    // Proceed with shooting
                    Player player = fiveOn[index];
                    double threePointTendency = rand.nextDouble();
                    // System.out.println(threePointTendency + " <= " + player.getThreePointTendency());
                    if(threePointTendency <= player.getThreePointTendency()){
                        // Go through threepoint shooting stats
                        double threePointerConverted = rand.nextDouble();
                        // System.out.println(threePointerConverted + " <= " + player.getThreePointPercentage());
                        if(threePointerConverted <= player.getThreePointPercentage()){
                            // Score three points
                            if(homeTeam.equals(offensiveTeam)){
                                homeTeamPoints = teamScoresThree(homeTeamPoints);
                            } else if(awayTeam.equals(offensiveTeam)){
                                awayTeamPoints = teamScoresThree(awayTeamPoints);
                            }
                            // System.out.println(player.getName() + " shoots and scores 3" + " (" + homeTeamPoints + "-" + awayTeamPoints + ")");
                            break;
                        }
                        // System.out.println(player.getName() + " shoots a 3 and its a miss");
                    } else{
                        double twoPointTendency = rand.nextDouble();
                        // System.out.println(twoPointT`endency + " <= " + player.getTwoPointTendency());
                        if(twoPointTendency <= player.getTwoPointTendency()){
                            // Go through two point shooting stats
                            double twoPointerConverted = rand.nextDouble();
                            // System.out.println(twoPointerConverted + " <= " + player.getTwoPointPercentage());
                            if(twoPointerConverted <= player.getTwoPointPercentage()){
                                // Score two points
                                if(homeTeam.equals(offensiveTeam)){
                                    homeTeamPoints = teamScoresTwo(homeTeamPoints);
                                } else if(awayTeam.equals(offensiveTeam)){
                                    awayTeamPoints = teamScoresTwo(awayTeamPoints);
                                }
                                // System.out.println(player.getName() + " shoots and scores a 2" + " (" + homeTeamPoints + "-" + awayTeamPoints + ")");
                                break;
                            }
                            // System.out.println(player.getName() + " shoots for 2 and MISS");
                        } else {
                            // System.out.println("EMPTY POSSESSION");
                            break;
                        }
                    }
                    // end with break
                    break;
                } 
                index++;
                sum1 = sum2;
                try{
                    sum2 = fiveOn[index].getUsageRate() + sum1;
                } catch(ArrayIndexOutOfBoundsException ie){
                    System.out.println(Arrays.toString(fiveOn));
                    System.out.println("INDEX = " + index);
                    break;
                }
            }
            // System.out.println(Arrays.toString(fiveOn));
            // System.out.println(possessionCounter);
            // System.out.println(Arrays.toString(offensiveTeam.getFiveOnCourt()));
            playPossession(defensiveTeam, offensiveTeam, possessionCounter + 1);
        }
    }

    public void tipBall(){
        Team[] game = {homeTeam, awayTeam};
        int index = random.nextInt(0, 1);
        game[0].lostPossession();
        game[1].lostPossession();
        game[index].possession();
    }

    public int teamScoresTwo(int score){
        score += 2;
        return score;
    }
    
    public int teamScoresThree(int score){
        score += 3;
        return score;
    }

    public Player checkLowestMinutes(Team team){
        Player[] fiveOnFloor = team.getFiveOnCourt();
        Arrays.sort(fiveOnFloor, new Comparator<Player>() {
            @Override
            public int compare(Player o1, Player o2) {
                return (int) (o1.getTimePlayed() - o2.getTimePlayed());
            }
        });
        Player lowMin = fiveOnFloor[0];
        // Arrays.sort(fiveOnFloor);
        return lowMin;
    }

    public void playersTimePlayed(Team team, int time){
        Player[] players = team.getFiveOnCourt();
        players[0].playedTime(time);
        players[1].playedTime(time);
        players[2].playedTime(time);
        players[3].playedTime(time);
        players[4].playedTime(time);
        team.updateFiveOn(players);
    }

    public boolean benchMinZero(Player[] bench){
        if(bench[0].getTimePlayed() == 0 && bench[1].getTimePlayed() == 0 && bench[2].getTimePlayed() == 0 && 
        bench[3].getTimePlayed() == 0 && bench[4].getTimePlayed() == 0){
            return true;
        }
        return false;
    }

    public void subs(Team team){
        // ADD A CHECK IF ALL PLAYERS ON BENCH HAVE 0 MIN then put ALL STARTERS IN THE GAME
        Player[] fiveFloor = team.getFiveOnCourt();
        Player[] bench = team.getFiveOnBench();

        Arrays.sort(bench, new PlayerMinuteComparator());

        for(int i=0; i<fiveFloor.length; i++){
            Player player = fiveFloor[i];
            if(player.getTimePlayed() <= 0){
                if(bench[0].getTimePlayed() > 0){
                    fiveFloor[i] = bench[0];
                    bench[0] = player;
                    if(player.getTimePlayed() < 0){
                        player.setTimePlayedZero();
                    }
                    Arrays.sort(bench, new PlayerMinuteComparator());
                }
                
            }
        }
        Arrays.sort(fiveFloor);
        team.updateFiveOn(fiveFloor);
        team.updateBench(bench);

        // System.out.println(Arrays.toString(bench) + "BENCH MINUTES SORT");

    }

    public void resetStats(){

    }
    
    public void possessions(int gameTime){
        // Set Possession Counter for each team
        int homePossessionCounter = 0;
        int awayPossessionCounter = 0;
        // compute total possessions in said gametime
        int time = 0;
        int turn = 0;
        while(time < gameTime){
            if(turn == 0){
                int homeTime = homeTeam.getPossesion();
                time += homeTime;
                homeTeam.addTime(homeTime);
                totalTime.add(homeTime);
                homePossessionCounter++;
                turn = 1;
            } else if(turn == 1){
                int awayTime = awayTeam.getPossesion();
                time += awayTime;
                awayTeam.addTime(awayTime);
                totalTime.add(awayTime);
                awayPossessionCounter++;
                turn = 0;
            }
        }
        // System.out.println(homeTeam.getAbbrv() + " POSSESSION TOTAL " + homePossessionCounter);
        // System.out.println(awayTeam.getAbbrv() + " POSSESSION TOTAL " + awayPossessionCounter);

        // get the average of the two and that will be the amount of possessions played in given game
        this.totalPossessions = (int) (homePossessionCounter + awayPossessionCounter);
    }

    public static void main(String[] args) {
        Team heat = new Team("heat");
        Team bucks = new Team("bucks");

        Game game = new Game(heat, bucks);
        long startTime = System.currentTimeMillis();
        for(int i=0; i<12500; i++){
            game.playGame();
        }
        long endTime = System.currentTimeMillis();
        double totalTime = (endTime - startTime) / 1000.0;
        System.out.println(totalTime + " seconds");

        // game.playGame();
        // game.playGame();
        System.out.println(heat.getName() + " PTS/G -> " + heat.getAveragePointsTeam());
        System.out.println(bucks.getName() + " PTS/G -> " + bucks.getAveragePointsTeam());
        System.out.println(heat.getWins());
        System.out.println(bucks.getWins());
        
    }
    
}
