package edu.nd.crc.safa.admin.usagestats.entities.app;

import lombok.Data;

@Data
public class ProjectGenerationStatistics {
    private GenerationStatisticsSingle total;
    private GenerationStatisticsSingle fromSummarization;

    @Data
    public static class GenerationStatisticsSingle {
        private int accounts;
        private double percent;
        private long averageTime;
    }
}
