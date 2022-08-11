package edu.nd.crc.safa.features.flatfiles.entities.common;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;

/**
 * Creates series of mapping data structures for organizing artifacts.
 */
public class ArtifactMaps {
    Map<String, ArtifactAppEntity> name2artifact;
    Map<String, List<ArtifactAppEntity>> type2artifacts;

    public ArtifactMaps(ProjectAppEntity projectAppEntity) {
        this.name2artifact = new HashMap<>();
        this.type2artifacts = new HashMap<>();
        this.createMaps(projectAppEntity);
    }

    private void createMaps(ProjectAppEntity projectAppEntity) {
        for (ArtifactAppEntity artifact : projectAppEntity.artifacts) {
            String artifactType = artifact.type;
            if (type2artifacts.containsKey(artifactType)) {
                type2artifacts.get(artifactType).add(artifact);
            } else {
                List<ArtifactAppEntity> artifacts = new ArrayList<>();
                artifacts.add(artifact);
                type2artifacts.put(artifactType, artifacts);
            }
            name2artifact.put(artifact.name, artifact);
        }
    }

    public Set<String> getArtifactTypes() {
        return this.type2artifacts.keySet();
    }

    public List<ArtifactAppEntity> getArtifactsInType(String artifactType) {
        return this.type2artifacts.get(artifactType);
    }

    public ArtifactAppEntity getArtifactByName(String artifactName) {
        return this.name2artifact.get(artifactName);
    }
}
