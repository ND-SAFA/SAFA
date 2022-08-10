package edu.nd.crc.safa.features.flatfiles.entities.app;

import lombok.Data;

/**
 * Depicts request for checking if artifact name exists
 * in some specified version.
 */
@Data
public class ArtifactNameCheck {
    String artifactName;
}
