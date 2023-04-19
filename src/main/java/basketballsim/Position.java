package basketballsim;

/**
 * @author Francisco Di Giglio
 */
public enum Position {
    PG(1, "Point Guard"),
    SG(2, "Shooting Guard"),
    SF(3, "Small Forward"),
    PF(4, "Power Forward"),
    C(5, "Center");

    private int pos;
    private String posName;

    private Position(int pos, String posName){
        this.pos = pos;
        this.posName = posName;
    }

    public int getPosNum(){
        return this.pos;
    }

    @Override
    public String toString(){
        return this.posName;
    }

}
