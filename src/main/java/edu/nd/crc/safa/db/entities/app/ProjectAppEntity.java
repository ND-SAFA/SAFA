package edu.nd.crc.safa.db.entities.app;

import java.util.ArrayList;
import java.util.Hashtable;
import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.db.entities.sql.Artifact;
import edu.nd.crc.safa.db.entities.sql.Project;

public class ProjectAppEntity {

    public String projectId;
    public String name;
    public List<ArtifactAppEntity> artifacts;
    public List<TraceApplicationEntity> traces;
    private Hashtable<String, ArtifactAppEntity> artifactTable;

    public ProjectAppEntity() {
        this.artifacts = new ArrayList<>();
        this.traces = new ArrayList<>();
    }

    public ProjectAppEntity(Project project,
                            List<ArtifactAppEntity> artifacts,
                            List<TraceApplicationEntity> traces) {
        this.projectId = project.getProjectId().toString();
        this.name = project.getName();
        this.artifacts = artifacts;
        this.traces = traces;
        loadArtifactTable();
    }

    private void loadArtifactTable() {
        this.artifactTable = new Hashtable<>();
        for (ArtifactAppEntity artifact : artifacts) {
            this.artifactTable.put(artifact.getName(), artifact);
        }
    }

    public String getProjectId() {
        return this.projectId;
    }

    public void setProjectId(String projectId) {
        this.projectId = projectId;
    }

    public String getName() {
        return this.name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public List<ArtifactAppEntity> getArtifacts() {
        return this.artifacts;
    }

    public void setArtifacts(List<ArtifactAppEntity> artifacts) {
        this.artifacts = artifacts;
    }

    public void addArtifact(ArtifactAppEntity artifact) {
        this.artifacts.add(artifact);
    }

    public List<TraceApplicationEntity> getTraces() {
        return this.traces;
    }

    public void setTraces(List<TraceApplicationEntity> traces) {
        this.traces = traces;
    }

    public ArtifactAppEntity getArtifactWithId(String artifactId) {
        if (artifactTable == null) {
            loadArtifactTable();
        }
        if (artifactTable.containsKey(artifactId)) {
            return artifactTable.get(artifactId);
        }
        return null;
    }

    public List<ArtifactAppEntity> getNewArtifacts(List<Artifact> existingArtifacts) {
        List<String> existingArtifactNames = existingArtifacts
            .stream()
            .map(Artifact::getName)
            .collect(Collectors.toList());
        List<ArtifactAppEntity> newArtifacts = new ArrayList<>();
        for (ArtifactAppEntity potentiallyNewArtifact : artifacts) {
            if (!existingArtifactNames.contains(potentiallyNewArtifact.getName())) {
                // TODO: Replace with hash table if performance is bad
                newArtifacts.add(potentiallyNewArtifact);
            }
        }
        return newArtifacts;
    }

    public ProjectAppEntity withArtifact(ArtifactAppEntity artifact) {
        this.artifacts.add(artifact);
        return this;
    }
}
