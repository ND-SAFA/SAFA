package edu.nd.crc.safa.features.permissions.checks;

import lombok.Data;

@Data
public class ProjectStatistics {
    private int artifactsTotal;
    private int linksTotal;
    private int unsummarizedCodeArtifactsTotal;
}
