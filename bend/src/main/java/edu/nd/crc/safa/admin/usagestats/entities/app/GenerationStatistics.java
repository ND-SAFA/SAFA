package edu.nd.crc.safa.admin.usagestats.entities.app;

import lombok.Data;

@Data
public class GenerationStatistics {
    /** Statistics for all accounts */
    private GenerationStatisticsSingle total;

    /** Statistics for all accounts with a project imported */
    private GenerationStatisticsSingle fromImport;

    /**
     * Statistics for all accounts with a project imported and with proper tracking
     * @see AccountCreationStatistics
     */
    private GenerationStatisticsSingle fromImportProper;

    /** Total number of generations that have been performed */
    private int totalGenerations;

    /** Total number of lines that have been generated on */
    private long linesGeneratedOn;

    public GenerationStatistics() {
        total = new GenerationStatisticsSingle();
        fromImport = new GenerationStatisticsSingle();
        fromImportProper = new GenerationStatisticsSingle();
    }

    @Data
    public static class GenerationStatisticsSingle {
        /** Number of accounts that have performed a hierarchy generation */
        private int accounts;

        /** Percentage of accounts that have performed a hierarchy generation */
        private double percent;

        /**
         * Average amount of time between a project being import and a generation being performed.
         * Does not apply to {@link GenerationStatistics#total}
         */
        private long averageTime;
    }
}
