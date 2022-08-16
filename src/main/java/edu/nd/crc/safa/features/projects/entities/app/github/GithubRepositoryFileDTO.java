package edu.nd.crc.safa.server.entities.api.github;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

/**
 * Transfer object describing metadata for a GitHub repository file
 */
@Data
@JsonIgnoreProperties(ignoreUnknown = true)
public class GithubRepositoryFileDTO {

    private String mode;

    private String path;

    private String sha;

    private Integer size;

    private GithubRepositoryFileType type;

    public enum GithubRepositoryFileType {
        @JsonProperty("blob")
        FILE,

        @JsonProperty("tree")
        FOLDER;
    }

}
