package basketballsim;

/**
 * @author Francisco Di Giglio
 */
public enum Conference {
    EAST("East"),
    WEST("West");

    private String conf;

    private Conference(String conf){
        this.conf = conf;
    }

    @Override
    public String toString(){
        return this.conf;
    }
}
