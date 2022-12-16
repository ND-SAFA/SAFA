package edu.nd.crc.safa.features.github.entities.app;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.Getter;

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

    @JsonProperty("url")
    private String blobApiUrl;

    @AllArgsConstructor
    @Getter
    public enum GithubRepositoryFileType {
        @JsonProperty("blob")
        FILE("GitHub File"),

        @JsonProperty("tree")
        FOLDER("GitHub Folder"),

        @JsonProperty("commit")
        SUBMODULE("GitHub Submodule");

        private final String artifactTypeName;
    }

}
