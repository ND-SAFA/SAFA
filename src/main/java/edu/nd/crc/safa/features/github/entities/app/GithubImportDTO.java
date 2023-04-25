package edu.nd.crc.safa.features.github.entities.app;

import java.util.List;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

@Data
public class GithubImportDTO {
    private String branch;
    private List<String> include;
    private List<String> exclude;

    @JsonProperty("artifact_type_id")
    private String artifactTypeId;
}
