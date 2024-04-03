package edu.nd.crc.safa.admin.usagestats.entities.app;

import lombok.Data;

@Data
public class GithubIntegrationStatistics {
    /** Github integration statistics for all accounts */
    private GithubIntegrationStatisticsSingle total;

    /**
     * Github integration statistics for accounts with proper tracking
     * @see AccountCreationStatistics
     */
    private GithubIntegrationStatisticsSingle withProperTracking;

    public GithubIntegrationStatistics() {
        total = new GithubIntegrationStatisticsSingle();
        withProperTracking = new GithubIntegrationStatisticsSingle();
    }

    @Data
    public static class GithubIntegrationStatisticsSingle {
        /** Number of accounts with github integrated */
        private int accounts;

        /** Percentage of created accounts with github integrated */
        private double percent;

        /**
         * Average amount of time in seconds between account creation and github integration.
         * Only applies to accounts with proper tracking.
         */
        private long averageTime;
    }
}
