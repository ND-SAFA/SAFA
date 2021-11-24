package edu.nd.crc.safa.server.entities.app;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;
import javax.validation.Valid;
import javax.validation.constraints.NotNull;

import edu.nd.crc.safa.server.entities.db.Artifact;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;

import org.json.JSONObject;

/**
 * Represents the front-end model of a project.
 */
public class ProjectAppEntity {
    @NotNull
    public String projectId;

    @NotNull
    public String name;

    @NotNull
    public String description;

    @Valid
    public ProjectVersion projectVersion;

    @NotNull
    public List<@Valid @NotNull ArtifactAppEntity> artifacts;

    @NotNull
    public List<@Valid @NotNull TraceAppEntity> traces;

    public ProjectAppEntity() {
        this.artifacts = new ArrayList<>();
        this.traces = new ArrayList<>();
    }

    public ProjectAppEntity(ProjectVersion projectVersion,
                            List<ArtifactAppEntity> artifacts,
                            List<TraceAppEntity> traces) {
        Project project = projectVersion.getProject();
        this.projectId = project.getProjectId().toString();
        this.projectVersion = projectVersion;
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

    public ProjectVersion getProjectVersion() {
        return this.projectVersion;
    }

    public void setProjectVersion(ProjectVersion projectVersion) {
        this.projectVersion = projectVersion;
    }

    public String getName() {
        return this.name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getDescription() {
        return this.description;
    }

    public void setDescription(String description) {
        this.description = description;
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

    public List<TraceAppEntity> getTraces() {
        return this.traces;
    }

    public void setTraces(List<TraceAppEntity> traces) {
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

    public String toString() {
        JSONObject json = new JSONObject();
        json.put("projectId", this.projectId);
        json.put("name", this.name);
        json.put("artifacts", artifacts);
        json.put("traces", traces);
        return json.toString();
    }
}
