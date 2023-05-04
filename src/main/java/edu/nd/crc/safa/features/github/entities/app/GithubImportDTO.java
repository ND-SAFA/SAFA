package edu.nd.crc.safa.features.github.entities.app;

import java.util.List;

import lombok.Data;

@Data
public class GithubImportDTO {
    private String branch;
    private List<String> include;
    private List<String> exclude;
    private String artifactType;
}
