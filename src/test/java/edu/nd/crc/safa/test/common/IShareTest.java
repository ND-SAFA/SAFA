package edu.nd.crc.safa.test.common;

import edu.nd.crc.safa.features.users.entities.IUser;

public interface IShareTest {

    /**
     * @return {@link String} Email who project is shared with.
     */
    String getShareeEmail();

    /**
     * @return {@link String} Password of account who project is shared with.
     */
    String getShareePassword();

    /**
     * @return Returns the sharee user.
     */
    IUser getSharee();
}
