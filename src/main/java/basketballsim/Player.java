package basketballsim;

/**
 * @author Francisco Di Giglio
 */
public class Player implements Comparable<Player>{
    private String[] data;
    private String name;
    private Position position;
    private String age;
    private int height;
    private double minutesPlayed;
    private double fieldGoals;
    private double fieldGoalsAttempted;
    private double fieldGoalPercentage;
    private double threePoint;
    private double threePointAttempted;
    private double threePointPercentage;
    private double twoPoint;
    private double twoPointAttempted;
    private double twoPointPercentage;
    private double usageRate;
    private int currentTimePlayed;
    // private int totalPoints;

    /**
     * @param data - String array that holds a players stats like PTS/G, USG%, NAME
     */
    public Player(String[] data){
        this.data = data;
        this.name = data[0];
        String pos = data[1];
        this.age = data[3];
        this.height = this.convertHeightToInches(data[2]);
        this.minutesPlayed = Double.parseDouble(data[6]) * 60;
        this.currentTimePlayed = (int)(minutesPlayed);
        this.fieldGoals = Double.parseDouble(data[7]);
        this.fieldGoalsAttempted = Double.parseDouble(data[8]);
        this.fieldGoalPercentage = Double.parseDouble(data[9]);
        this.threePoint = Double.parseDouble(data[10]);
        this.threePointAttempted = Double.parseDouble(data[11]);
        if(data[12].equals("")){
            this.threePointPercentage = 0.0;
        } else{
            this.threePointPercentage = Double.parseDouble(data[12]);
        }
        this.twoPoint = Double.parseDouble(data[13]);
        this.twoPointAttempted = Double.parseDouble(data[14]);
        if(data[15].equals("")){
            this.twoPointPercentage = 0.0;
        } else{
            this.twoPointPercentage = Double.parseDouble(data[15]);
        }
        this.usageRate = Double.parseDouble(data[41]);

        // Needs to be last
        switch(pos){
            case "PG":
                this.position = Position.PG;
                break;
            case "SG":
                this.position = Position.SG;
                break;
            case "SF":
                this.position = Position.SF;
                break;
            case "PF":
                this.position = Position.PF;
                break;
            case "C":
                this.position = Position.C;
                break;

        }
    }

    /**
     * 
     * @return String array data
     */
    public String[] getData(){
        return this.data;
    }

    /**
     * @param height - in the form of "<feet>-<inches>"
     * @return Integer of the height in inches
     */
    public int convertHeightToInches(String height){
        String[] split = height.split("-");
        int feet = Integer.parseInt(split[0]);
        int inches = Integer.parseInt(split[1]);
        int feetToInches = feet * 12;
        return feetToInches + inches;
    }

    public String getName() {
        return name;
    }

    public Position getPosition() {
        return position;
    }

    public String getAge() {
        return age;
    }

    public int getHeight() {
        return height;
    }

    public double getMinutesPlayed() {
        return minutesPlayed;
    }

    public double getFieldGoals() {
        return fieldGoals;
    }

    public double getFieldGoalsAttempted() {
        return fieldGoalsAttempted;
    }

    public double getFieldGoalPercentage() {
        return fieldGoalPercentage;
    }

    public double getThreePoint() {
        return threePoint;
    }

    public double getThreePointAttempted() {
        return threePointAttempted;
    }

    public double getThreePointPercentage() {
        return threePointPercentage;
    }

    public double getTwoPoint() {
        return twoPoint;
    }

    public double getTwoPointAttempted() {
        return twoPointAttempted;
    }

    public double getTwoPointPercentage() {
        return twoPointPercentage;
    }

    public double getUsageRate() {
        return usageRate;
    }

    public int getTimePlayed(){
        return this.currentTimePlayed;
    }

    public void playedTime(int time){
        this.currentTimePlayed -= time;
    }

    public void resetCurrentTime(){
        this.currentTimePlayed = (int) this.minutesPlayed;
    }

    public void setTimePlayedZero(){
        this.currentTimePlayed = 0;
    }

    public double getThreePointTendency(){
        return this.threePointAttempted / (this.twoPointAttempted + this.threePointAttempted);
    }

    public double getTwoPointTendency(){
        return this.twoPointAttempted / (this.twoPointAttempted + this.threePointAttempted);
    }

    @Override
    public String toString(){
        return "P{" + this.name + ", " + this.position.toString() + ", " + this.age + ", "
        + this.height + "\"" +  ", TMIN=" + this.minutesPlayed + ", CMIN=" + this.currentTimePlayed + "}";
    }

    @Override
    public int compareTo(Player o2) {
        if(this.position.getPosNum() - o2.position.getPosNum() == 0){
            return this.getHeight() - o2.getHeight();
        }
        return this.position.getPosNum() - o2.position.getPosNum();
    }

}
