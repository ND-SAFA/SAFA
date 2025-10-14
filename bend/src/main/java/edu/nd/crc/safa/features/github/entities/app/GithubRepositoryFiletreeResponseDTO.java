package edu.nd.crc.safa.features.github.entities.app;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

/**
 * Object defining the response received when getting the filetree of
 * a GitHub repository
 */
@NoArgsConstructor
@AllArgsConstructor
@Getter
@Setter
@JsonIgnoreProperties(ignoreUnknown = true)
public class GithubRepositoryFiletreeResponseDTO {

    private String sha;

    private List<GithubRepositoryFileDTO> tree = new ArrayList<>();

    public GithubRepositoryFiletreeResponseDTO filesOnly() {
        List<GithubRepositoryFileDTO> tree = this.tree
                .stream()
                .filter(file -> GithubRepositoryFileType.FILE.equals(file.getType()))
                .collect(Collectors.toList());

        return new GithubRepositoryFiletreeResponseDTO(this.sha, tree);
    }
}
