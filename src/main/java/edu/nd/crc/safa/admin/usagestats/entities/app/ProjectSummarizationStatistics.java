package edu.nd.crc.safa.admin.usagestats.entities.app;

import lombok.Data;

@Data
public class ProjectSummarizationStatistics {
    private SummarizationStatisticsSingle total;
    private SummarizationStatisticsSingle fromImport;

    @Data
    public static class SummarizationStatisticsSingle {
        private int accounts;
        private double percent;
        private long averageTime;
    }
}
