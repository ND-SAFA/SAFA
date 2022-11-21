package edu.nd.crc.safa.features.installations.app;

import java.util.Date;
import java.util.UUID;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * DTO describing a SAFA project with a JIRA/GitHub installation imported into it
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class ProjectWithInstallationDTO {

    /**
     * Corresponding SAFA project's id
     */
    private UUID projectId;

    /**
     * Corresponding SAFA project's name
     */
    private String projectName;

    /**
     * JIRA project id/GitHub repository name
     */
    private String installationId;

    /**
     * When installation data was last updated
     */
    private Date lastUpdate;

    /**
     * Installation type
     */
    private InstallationTypeEnum type;

    /**
     * Required for JPQL query projection
     *
     * @param projectId      Safa project id
     * @param projectName    Safa project name
     * @param installationId JIRA project id/GitHub repository name
     * @param lastUpdate     Timestamp of the last update
     * @param type           Instance of {@link InstallationTypeEnum}
     */
    public ProjectWithInstallationDTO(UUID projectId,
                                      String projectName,
                                      String installationId,
                                      Date lastUpdate,
                                      String type) {
        this(projectId, projectName, installationId, lastUpdate, InstallationTypeEnum.valueOf(type));
    }
}
