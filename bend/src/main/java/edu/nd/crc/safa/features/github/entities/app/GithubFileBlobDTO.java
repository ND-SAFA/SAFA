package edu.nd.crc.safa.features.github.entities.app;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.Data;

/**
 * Transfer object describing the blob content for a file a repository file
 * at a certain commit
 */
@Data
@JsonIgnoreProperties(ignoreUnknown = true)
public class GithubFileBlobDTO {

    private String sha;

    private Integer size;

    @JsonIgnoreProperties("node_id")
    private String nodeId;

    private String url;

    private String content;

    private String encoding;
}
