package edu.nd.crc.safa.features.github.entities.app;

import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.github.entities.api.GithubGraphQlTreeObjectsResponse;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.Data;

/**
 * Transfer object describing metadata for a GitHub repository file
 */
@Data
@JsonIgnoreProperties(ignoreUnknown = true)
public class GithubRepositoryFileDTO {

    private String name;

    private String path;

    private GithubRepositoryFileType type;

    private String contents;

    private boolean isBinary;

    /**
     * Convert a GitHub GraphQL API response to a list of repository files. This list will only contain items
     * in the folder that was originally requested, and will contain items that are a mix of files, folders,
     * and submodules.
     *
     * @param response GraphQL API response.
     * @return List of repository files.
     */
    public static List<GithubRepositoryFileDTO> fromGithubGraphQlResponse(GithubGraphQlTreeObjectsResponse response) {
        List<GithubGraphQlTreeObjectsResponse.Entry> entries =
            response.getData().getRepository().getObject().getEntries();

        return entries.stream().map(entry -> {
            GithubRepositoryFileDTO file = new GithubRepositoryFileDTO();
            file.setName(entry.getName());
            file.setPath(entry.getPath());
            file.setType(entry.getType());

            if (entry.getObject() != null) {
                file.setContents(entry.getObject().getText());
                file.setBinary(entry.getObject().isBinary());
            }

            return file;
        }).collect(Collectors.toList());
    }

}
