package edu.nd.crc.safa.features.flatfiles.controllers.entities;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Depicts request for checking if artifact name exists
 * in some specified version.
 */
@Data
@AllArgsConstructor
@NoArgsConstructor
public class ArtifactNameCheck {
    private String artifactName;
}
