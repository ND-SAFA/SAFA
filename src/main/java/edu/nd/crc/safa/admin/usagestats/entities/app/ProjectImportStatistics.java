package edu.nd.crc.safa.admin.usagestats.entities.app;

import lombok.Data;

@Data
public class ProjectImportStatistics {
    private ImportStatisticsSingle total;
    private ImportStatisticsSingle fromGithub;

    @Data
    public static class ImportStatisticsSingle {
        private int accounts;
        private double percent;
        private long averageTime;
    }
}
