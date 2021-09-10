package edu.nd.crc.safa.db.entities.app;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.db.entities.sql.Artifact;
import edu.nd.crc.safa.db.entities.sql.Project;

import org.json.JSONObject;

public class ProjectAppEntity {

    public String projectId;
    public String name;
    public List<ArtifactAppEntity> artifacts;
    public List<TraceApplicationEntity> traces;

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

    public List<ArtifactAppEntity> findNewArtifacts(List<Artifact> existingArtifacts) {
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

    public boolean hasDefinedId() {
        return this.projectId != null && !this.projectId.equals("");
    }

    public String toString() {
        JSONObject json = new JSONObject();
        json.put("projectId", this.projectId);
        json.put("name", this.name);
        json.put("artifacts", artifacts);
        json.put("traces", traces);
        return json.toString();
    }
}
