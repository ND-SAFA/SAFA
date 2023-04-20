package edu.nd.crc.safa.features.github.entities.app;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.github.entities.api.GithubGraphQlRepositoriesResponse;
import edu.nd.crc.safa.features.github.entities.api.graphql.EdgeNode;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

/**
 * Plain object representing a GitHub project
 */
@Data
@JsonIgnoreProperties(ignoreUnknown = true)
public class GithubRepositoryDTO {

    private String id;

    private String name;

    private String owner;

    private String nameWithOwner;

    @JsonProperty("private")
    private Boolean isPrivate;

    @JsonProperty("html_url")
    private String url;

    private String description;

    private String visibility;

    @JsonProperty("default_branch")
    private String defaultBranch;

    @JsonProperty("created_at")
    private Date creationDate;

    private String language;

    private List<String> branches;

    public static List<GithubRepositoryDTO> fromGraphQlResponse(GithubGraphQlRepositoriesResponse gqlResponse) {
        if (gqlResponse == null) {
            return new ArrayList<>();
        }

        return gqlResponse.getData().getViewer().getRepositories().getEdges().stream()
            .map(EdgeNode::getNode)
            .map(repo -> {
                GithubRepositoryDTO ghDto = new GithubRepositoryDTO();
                ghDto.setId(repo.getId());
                ghDto.setName(repo.getName());
                ghDto.setOwner(repo.getOwner().getLogin());
                ghDto.setNameWithOwner(repo.getNameWithOwner());
                ghDto.setIsPrivate(repo.isPrivate());
                ghDto.setUrl(repo.getUrl());
                ghDto.setDescription(repo.getDescription());
                ghDto.setVisibility(repo.getVisibility().name());
                ghDto.setDefaultBranch(repo.getDefaultBranchRef().getName());
                ghDto.setCreationDate(repo.getCreatedAt());

                if (repo.getPrimaryLanguage() != null) {
                    ghDto.setLanguage(repo.getPrimaryLanguage().getName());
                }

                List<String> branches = repo.getRefs().getEdges().stream()
                    .map(EdgeNode::getNode)
                    .map(GithubGraphQlRepositoriesResponse.Payload.Branch::getName)
                    .collect(Collectors.toList());
                ghDto.setBranches(branches);

                return ghDto;
            }).collect(Collectors.toList());

    }
}
