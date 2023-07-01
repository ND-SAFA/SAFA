package edu.nd.crc.safa.features.tgen.entities;

import java.util.ArrayList;
import java.util.List;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@AllArgsConstructor
@NoArgsConstructor
@Data
public class ArtifactLevel {
    /**
     * The artifact type of the source artifacts.
     */
    List<ArtifactAppEntity> sources = new ArrayList<>();
    /**
     * The artifact type of target artifacts.
     */
    List<ArtifactAppEntity> targets = new ArrayList<>();
}
