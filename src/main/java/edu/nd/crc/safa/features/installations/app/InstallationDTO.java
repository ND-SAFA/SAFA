package edu.nd.crc.safa.features.installations.app;

import java.util.Date;

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
     * @param installationId JIRA project id/GitHub repository name
     * @param lastUpdate     Timestamp of the last update
     * @param type           Instance of {@link InstallationTypeEnum}
     */
    public InstallationDTO(String installationId,
                           Date lastUpdate,
                           String type) {
        this(installationId, lastUpdate, InstallationTypeEnum.valueOf(type));
    }
}
