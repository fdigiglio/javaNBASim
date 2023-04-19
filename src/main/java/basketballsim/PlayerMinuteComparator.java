package basketballsim;

import java.util.Comparator;

/**
 * @author Francisco Di Giglio
 */
public class PlayerMinuteComparator implements Comparator<Player>{
    @Override
    public int compare(Player o1, Player o2) {
        return (int) (o2.getTimePlayed() - o1.getTimePlayed());
    }
}
