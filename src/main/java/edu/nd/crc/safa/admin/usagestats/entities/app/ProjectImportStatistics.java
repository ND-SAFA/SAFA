package edu.nd.crc.safa.admin.usagestats.entities.app;

import lombok.Data;

@Data
public class ProjectImportStatistics {
    /** Statistics for all accounts */
    private ImportStatisticsSingle total;

    /** Statistics for all accounts with github integration completed */
    private ImportStatisticsSingle fromGithub;

    /**
     * Statistics for all accounts with github integration completed and with proper tracking
     * @see AccountCreationStatistics
     */
    private ImportStatisticsSingle fromGithubProper;

    /** Total number of imports performed */
    private int totalPerformed;

    public ProjectImportStatistics() {
        total = new ImportStatisticsSingle();
        fromGithub = new ImportStatisticsSingle();
        fromGithubProper = new ImportStatisticsSingle();
    }

    @Data
    public static class ImportStatisticsSingle {
        /** Number of accounts that have performed a project import */
        private int accounts;

        /** Percentage of accounts that have performed a project import */
        private double percent;

        /**
         * Average amount of time between github being connected and an import being performed.
         * Does not apply to {@link ProjectImportStatistics#total}
         */
        private long averageTime;
    }
}
