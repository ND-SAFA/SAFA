package edu.nd.crc.safa.features.common;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.documents.entities.db.Document;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;

import lombok.Getter;

/**
 * Creates series of mapping data structures for organizing artifacts.
 */
public class ProjectEntities {
    @Getter
    private List<ArtifactAppEntity> artifacts;
    @Getter
    private List<TraceAppEntity> traces;
    private Map<String, ArtifactAppEntity> name2artifact;
    private Map<UUID, ArtifactAppEntity> id2artifact;
    private Map<String, List<ArtifactAppEntity>> type2artifacts;

    private ProjectEntities() {
        this.artifacts = new ArrayList<>();
        this.traces = new ArrayList<>();
        this.name2artifact = new HashMap<>();
        this.type2artifacts = new HashMap<>();
        this.id2artifact = new HashMap<>();
    }

    public ProjectEntities(List<ArtifactAppEntity> artifacts) {
        this();
        this.artifacts = artifacts;
        this.createMaps();
    }

    public ProjectEntities(List<ArtifactAppEntity> artifacts, List<TraceAppEntity> traces) {
        this();
        this.artifacts = artifacts;
        this.traces = traces;
        this.createMaps();
    }

    public ProjectEntities(ProjectAppEntity projectAppEntity) {
        this(projectAppEntity.getArtifacts(), projectAppEntity.getTraces());
    }

    private void createMaps() {
        for (ArtifactAppEntity artifact : this.artifacts) {
            String artifactType = artifact.getType();
            if (type2artifacts.containsKey(artifactType)) {
                type2artifacts.get(artifactType).add(artifact);
            } else {
                List<ArtifactAppEntity> typeArtifacts = new ArrayList<>();
                typeArtifacts.add(artifact);
                type2artifacts.put(artifactType, typeArtifacts);
            }
            name2artifact.put(artifact.getName(), artifact);
            id2artifact.put(artifact.getId(), artifact);
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

    public ArtifactAppEntity getArtifactById(UUID artifactId) {
        return getArtifactByKey(this.id2artifact, artifactId);
    }

    private <T> ArtifactAppEntity getArtifactByKey(Map<T, ArtifactAppEntity> key2artifact,
                                                   T key) {
        if (!key2artifact.containsKey(key)) {
            String error = String.format("Artifact not in map: %s.", key);
            throw new IllegalArgumentException(error);
        }
        return key2artifact.get(key);
    }

    public ProjectEntities getEntitiesInDocument(Document document) {
        List<ArtifactAppEntity> documentArtifacts = this.artifacts
            .stream()
            .filter(a -> a.getDocumentIds().contains(document.getDocumentId()))
            .collect(Collectors.toList());
        List<String> documentArtifactNames = documentArtifacts
            .stream()
            .map(ArtifactAppEntity::getName)
            .collect(Collectors.toList());
        List<TraceAppEntity> documentTraces = this.traces
            .stream()
            .filter(t -> documentArtifactNames.contains(t.getSourceName())
                || documentArtifactNames.contains(t.getTargetName()))
            .collect(Collectors.toList());
        return new ProjectEntities(documentArtifacts, documentTraces);
    }
}
