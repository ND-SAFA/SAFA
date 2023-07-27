package edu.nd.crc.safa.features.installations;

import java.util.Date;
import java.util.UUID;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Transfer object describing an external project imported into a Safa project
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class InstallationDTO {

    /**
     * JIRA project id/GitHub repository name
     */
    private String installationId;

    /**
     * The Jira or GitHub organization id that the project is within.
     */
    private String installationOrgId;

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
     * @param installationId    JIRA project id/GitHub repository name
     * @param installationOrgId The Jira or GitHub organization id that the project is within
     * @param lastUpdate        Timestamp of the last update
     * @param type              Instance of {@link InstallationTypeEnum}
     */
    public InstallationDTO(String installationId,
                           String installationOrgId,
                           Date lastUpdate,
                           String type) {
        this(installationId, installationOrgId, lastUpdate, InstallationTypeEnum.valueOf(type));
    }

    /**
     * Required for JPQL query projection
     *
     * @param installationId    JIRA project id/GitHub repository name
     * @param installationOrgId The Jira or GitHub organization id that the project is within
     * @param lastUpdate        Timestamp of the last update
     * @param type              Instance of {@link InstallationTypeEnum}
     */
    public InstallationDTO(String installationId,
                           UUID installationOrgId,
                           Date lastUpdate,
                           String type) {
        this(installationId, installationOrgId.toString(), lastUpdate, InstallationTypeEnum.valueOf(type));
    }
}
