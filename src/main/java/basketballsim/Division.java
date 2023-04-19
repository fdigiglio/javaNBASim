package basketballsim;

/**
 * @author Francisco Di Giglio
 */
public enum Division {
    ATLANTIC("Atlantic"),
    CENTRAL("Central"), 
    SOUTHEAST("South East"),
    NORTHWEST("North West"),
    PACIFIC("Pacific"),
    SOUTHWEST("South West");

    private String divName;

    private Division(String name){
        this.divName = name;
    }

    @Override
    public String toString(){
        return this.divName;
    }
}
