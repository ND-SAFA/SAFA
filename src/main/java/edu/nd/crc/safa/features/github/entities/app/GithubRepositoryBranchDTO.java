package edu.nd.crc.safa.features.github.entities.app;

import java.util.Map;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;
import lombok.NonNull;

/**
 * Transfer object describing a GitHub repository branch
 */
@Data
@JsonIgnoreProperties(ignoreUnknown = true)
public class GithubRepositoryBranchDTO {

    private static final String COMMIT_SHA_KEY = "sha";

    private String name;

    @JsonProperty("protected")
    private Boolean isProtected;

    private String lastCommitSha;

    /**
     * Retrieve last commit sha
     *
     * @param commitJson object child situated at .commit in the JSON object tree
     */
    @JsonProperty("commit")
    public void setCommit(@NonNull Map<String, Object> commitJson) {
        this.lastCommitSha = (String) commitJson.get(COMMIT_SHA_KEY);
    }
}
