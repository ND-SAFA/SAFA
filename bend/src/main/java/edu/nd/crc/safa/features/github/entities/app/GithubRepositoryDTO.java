package edu.nd.crc.safa.features.github.entities.app;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.github.entities.api.GithubGraphQlRepositoriesResponse;
import edu.nd.crc.safa.features.github.entities.api.GithubGraphQlRepositoryResponse;
import edu.nd.crc.safa.features.github.entities.api.graphql.Branch;
import edu.nd.crc.safa.features.github.entities.api.graphql.Repository;
import edu.nd.crc.safa.utilities.graphql.entities.EdgeNode;

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

    @JsonProperty("private")
    private Boolean isPrivate;

    private String url;

    private String description;

    private String visibility;

    private String defaultBranch;

    private Date creationDate;

    private String language;

    private List<String> branches;

    /**
     * Converts the response from the GraphQL API to a list of objects for the front-end.
     *
     * @param gqlResponse Response from the GraphQL API.
     * @return List of objects for the front-end.
     */
    public static List<GithubRepositoryDTO> fromGraphQlResponse(GithubGraphQlRepositoriesResponse gqlResponse) {
        if (gqlResponse == null) {
            return new ArrayList<>();
        }

        return gqlResponse.getData().getViewer().getRepositories().getEdges().stream()
            .map(EdgeNode::getNode)
            .map(GithubRepositoryDTO::fromGraphQlObject)
            .collect(Collectors.toList());

    }

    /**
     * Converts the response from the GraphQL API to an object for the front-end.
     *
     * @param response Response from the GraphQL API.
     * @return Object for the front-end.
     */
    public static GithubRepositoryDTO fromGraphQlResponse(GithubGraphQlRepositoryResponse response) {
        if (response == null) {
            return null;
        }

        return fromGraphQlObject(response.getData().getRepository());
    }

    /**
     * Converts a GraphQL object to an object for the front-end.
     *
     * @param repo GraphQL object.
     * @return Object for the front-end.
     */
    public static GithubRepositoryDTO fromGraphQlObject(Repository repo) {
        if (repo == null) {
            return null;
        }

        GithubRepositoryDTO ghDto = new GithubRepositoryDTO();
        ghDto.setId(repo.getId());
        ghDto.setName(repo.getName());
        ghDto.setOwner(repo.getOwner().getLogin());
        ghDto.setIsPrivate(repo.isPrivate());
        ghDto.setUrl(repo.getUrl());
        ghDto.setDescription(repo.getDescription());
        ghDto.setVisibility(repo.getVisibility().name());
        ghDto.setCreationDate(repo.getCreatedAt());

        if (repo.getDefaultBranchRef() != null) {
            ghDto.setDefaultBranch(repo.getDefaultBranchRef().getName());
        }

        if (repo.getPrimaryLanguage() != null) {
            ghDto.setLanguage(repo.getPrimaryLanguage().getName());
        }

        List<String> branches = repo.getRefs().getEdges().stream()
            .map(EdgeNode::getNode)
            .map(Branch::getName)
            .collect(Collectors.toList());
        ghDto.setBranches(branches);

        return ghDto;
    }
}
