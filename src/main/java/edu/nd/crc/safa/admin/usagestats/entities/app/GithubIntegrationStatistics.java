package edu.nd.crc.safa.admin.usagestats.entities.app;

import lombok.Data;

@Data
public class GithubIntegrationStatistics {
    private int accounts;
    private double percent;
    private long averageTime;
}
