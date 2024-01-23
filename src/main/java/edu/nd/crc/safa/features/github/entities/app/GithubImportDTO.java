package edu.nd.crc.safa.features.github.entities.app;

import java.util.List;
import java.util.UUID;

import lombok.Data;

@Data
public class GithubImportDTO {
    private String branch;
    private List<String> include;
    private List<String> exclude;
    private String artifactType;

    private UUID orgId;
    private UUID teamId;

    private boolean summarize;
}
