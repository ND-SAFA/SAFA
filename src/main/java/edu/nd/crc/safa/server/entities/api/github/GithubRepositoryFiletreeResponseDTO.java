package edu.nd.crc.safa.server.entities.api.github;

import edu.nd.crc.safa.server.entities.api.github.GithubRepositoryFileDTO.GithubRepositoryFileType;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

/**
 * Object defining the response received when getting the filetree of
 * a GitHub repository
 */
@NoArgsConstructor
@AllArgsConstructor
@Getter
@Setter
public class GithubRepositoryFiletreeResponseDTO {

    private String sha;

    private List<GithubRepositoryFileDTO> tree = new ArrayList<>();

    public GithubRepositoryFiletreeResponseDTO filterOutFolders() {
        List<GithubRepositoryFileDTO> tree = this.tree
                .stream()
                .filter(file -> !GithubRepositoryFileType.FOLDER.equals(file.getType()))
                .collect(Collectors.toList());

        return new GithubRepositoryFiletreeResponseDTO(this.sha, tree);
    }
}
