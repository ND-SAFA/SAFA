package edu.nd.crc.safa.features.github.entities.app;

import java.util.Date;
import java.util.List;
import java.util.Map;

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

    @JsonProperty("fork")
    private Boolean isFork;

    private Long size;

    @JsonProperty("default_branch")
    private String defaultBranch;

    private List<String> topics;

    @JsonProperty("created_at")
    private Date creationDate;

    private String language;

    @JsonProperty("forks_count")
    private String forksCount;

    private String ownerLoginHandler;

    @JsonProperty("owner")
    public void setOwnerLoginHandler(Map<String, String> ownerData) {
        this.ownerLoginHandler = ownerData.get("login");
    }
}
