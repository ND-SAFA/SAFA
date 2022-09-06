package common;

public interface IShareTest {

    /**
     * @return {@link String} Email who project is shared with.
     */
    String getShareeEmail();

    /**
     * @return {@link String} Password of account who project is shared with.
     */
    String getShareePassword();
}
