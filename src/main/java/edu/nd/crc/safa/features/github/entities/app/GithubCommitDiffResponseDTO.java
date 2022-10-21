package edu.nd.crc.safa.features.github.entities.app;

import java.util.ArrayList;
import java.util.List;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

/**
 * Transfer object describing a diff between two commits for a GitHub
 * repository
 */
@Data
@JsonIgnoreProperties(ignoreUnknown = true)
public class GithubCommitDiffResponseDTO {

    private List<GithubFileDiffDTO> files = new ArrayList<>();

    @JsonProperty("total_commits")
    private Integer commitCount;

    /**
     * Class encapsulating changes made to a single file between
     * two commits
     */
    @Data
    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class GithubFileDiffDTO {

        /**
         * Sha of the commit where the file was last modified
         */
        private String sha;

        private String filename;

        private GitHubFileDiffStatus status;

        @JsonProperty("additions")
        private Integer linesAdded;

        @JsonProperty("deletions")
        private Integer linesRemoved;

        @JsonProperty("changes")
        private Integer linesChanged;

        @JsonProperty("blob_url")
        private String blobUrl;

        public enum GitHubFileDiffStatus {
            @JsonProperty("added")      ADDED,
            @JsonProperty("removed")    REMOVED,
            @JsonProperty("modified")   MODIFIED,
            @JsonProperty("renamed")    RENAMED,
            @JsonProperty("copied")     COPIED,
            @JsonProperty("changed")    CHANGED,
            @JsonProperty("unchanged")  UNCHANGED;
        }
    }
}
