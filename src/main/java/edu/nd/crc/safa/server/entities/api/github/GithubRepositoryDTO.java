package edu.nd.crc.safa.server.entities.api.github;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

/**
 * Plain object representing a GitHub project
 */
@Data
@JsonIgnoreProperties(ignoreUnknown = true)
public class GithubRepositoryDTO {

    private Long id;

    private String name;

    @JsonProperty("private")
    private Boolean isPrivate;

    @JsonProperty("html_url")
    private String url;

    private String description;

    private String visibility;
}
