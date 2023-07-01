package edu.nd.crc.safa.features.github.entities.api;

import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import lombok.AllArgsConstructor;
import lombok.Data;

/**
 * Information for identifying GitHub project.
 */
@Data
@AllArgsConstructor
public class GithubIdentifier {

    private ProjectVersion projectVersion;

    private String repositoryOwner;

    private String repositoryName;

}
