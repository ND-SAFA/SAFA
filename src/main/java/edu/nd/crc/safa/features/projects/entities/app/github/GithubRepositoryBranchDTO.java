package edu.nd.crc.safa.server.entities.api.github;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

import java.util.Map;

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
     * @param commit object child situated at .commit in the JSON object tree
     */
    @JsonProperty("commit")
    public void setCommit(Map<String, String> commit) {
        this.lastCommitSha = commit.get(COMMIT_SHA_KEY);
    }
}
