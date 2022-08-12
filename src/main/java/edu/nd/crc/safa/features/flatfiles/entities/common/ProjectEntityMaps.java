package edu.nd.crc.safa.features.flatfiles.entities.common;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.documents.entities.db.Document;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;

import lombok.AllArgsConstructor;
import lombok.Data;

/**
 * Creates series of mapping data structures for organizing artifacts.
 */
public class ProjectEntityMaps {
    List<ArtifactAppEntity> artifacts;
    List<TraceAppEntity> traces;
    Map<String, ArtifactAppEntity> name2artifact;
    Map<String, ArtifactAppEntity> id2artifact;
    Map<String, List<ArtifactAppEntity>> type2artifacts;

    public ProjectEntityMaps(List<ArtifactAppEntity> artifacts, List<TraceAppEntity> traces) {
        this.artifacts = artifacts;
        this.traces = traces;
        this.name2artifact = new HashMap<>();
        this.type2artifacts = new HashMap<>();
        this.id2artifact = new HashMap<>();
    }

    public ProjectEntityMaps(ProjectAppEntity projectAppEntity) {
        this(projectAppEntity.getArtifacts(), projectAppEntity.getTraces());
        this.createMaps(projectAppEntity.artifacts);
    }

    private void createMaps(List<ArtifactAppEntity> artifacts) {
        for (ArtifactAppEntity artifact : artifacts) {
            String artifactType = artifact.type;
            if (type2artifacts.containsKey(artifactType)) {
                type2artifacts.get(artifactType).add(artifact);
            } else {
                List<ArtifactAppEntity> typeArtifacts = new ArrayList<>();
                typeArtifacts.add(artifact);
                type2artifacts.put(artifactType, typeArtifacts);
            }
            name2artifact.put(artifact.name, artifact);
            id2artifact.put(artifact.id, artifact);
        }
    }

    public Set<String> getArtifactTypes() {
        return this.type2artifacts.keySet();
    }

    public List<ArtifactAppEntity> getArtifactsInType(String artifactType) {
        return this.type2artifacts.get(artifactType);
    }

    public ArtifactAppEntity getArtifactByName(String artifactName) {
        return getArtifactByKey(this.name2artifact, artifactName);
    }

    public ArtifactAppEntity getArtifactById(String artifactId) {
        return getArtifactByKey(this.id2artifact, artifactId);
    }

    private ArtifactAppEntity getArtifactByKey(Map<String, ArtifactAppEntity> key2artifact,
                                               String key) {
        if (!key2artifact.containsKey(key)) {
            String error = String.format("Artifact not in map: %s", key);
            throw new IllegalArgumentException(error);
        }
        return key2artifact.get(key);
    }

    public Entities getEntitiesInDocument(Document document) {
        List<ArtifactAppEntity> documentArtifacts = this.artifacts
            .stream()
            .filter((a) -> a.getDocumentIds().contains(document.getDocumentId().toString()))
            .collect(Collectors.toList());
        List<String> documentArtifactNames = documentArtifacts
            .stream()
            .map(ArtifactAppEntity::getName)
            .collect(Collectors.toList());
        List<TraceAppEntity> documentTraces = this.traces
            .stream()
            .filter((t) -> documentArtifactNames.contains(t.getSourceName()) ||
                documentArtifactNames.contains(t.getTargetName()))
            .collect(Collectors.toList());
        return new Entities(documentArtifacts, documentTraces);
    }

    @AllArgsConstructor
    @Data
    public static class Entities {
        List<ArtifactAppEntity> artifacts;
        List<TraceAppEntity> traces;
    }
}
