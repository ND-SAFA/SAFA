package edu.nd.crc.safa.admin.usagestats.entities.app;

import lombok.Data;

@Data
public class AccountCreationStatistics {
    /** Number of accounts that exist within the app */
    private int created;

    /** Number of accounts that have been verified */
    private int verified;

    /**
     * Number of accounts that have actual progress tracking. This is equivalent to the number of accounts that were
     * created since the progress tracking was started, as all accounts created before that will have no account
     * creation time, and the times associated with when they first completed a step are likely to be wrong.
     */
    private int haveProperProgressTracking;
}
