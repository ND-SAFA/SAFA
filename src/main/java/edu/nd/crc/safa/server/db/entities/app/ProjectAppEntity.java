package edu.nd.crc.safa.server.db.entities.app;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import edu.nd.crc.safa.server.db.entities.sql.Artifact;
import edu.nd.crc.safa.server.db.entities.sql.Project;
import edu.nd.crc.safa.server.db.entities.sql.ProjectVersion;
import edu.nd.crc.safa.warnings.RuleName;

import org.json.JSONObject;

public class ProjectAppEntity {
    public String projectId;
    public String name;
    public String description;
    public ProjectVersion projectVersion;
    public List<ArtifactAppEntity> artifacts;
    public List<TraceApplicationEntity> traces;
    public Map<String, List<RuleName>> warnings;

    public ProjectAppEntity() {
        this.artifacts = new ArrayList<>();
        this.traces = new ArrayList<>();
    }

    public ProjectAppEntity(ProjectVersion projectVersion,
                            List<ArtifactAppEntity> artifacts,
                            List<TraceApplicationEntity> traces,
                            Map<String, List<RuleName>> warnings) {
        Project project = projectVersion.getProject();
        this.projectId = project.getProjectId().toString();
        this.projectVersion = projectVersion;
        this.name = project.getName();
        this.artifacts = artifacts;
        this.traces = traces;
        this.warnings = warnings;
        System.out.println("Project App Entity: " + this.warnings);
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

    public List<TraceApplicationEntity> getTraces() {
        return this.traces;
    }

    public void setTraces(List<TraceApplicationEntity> traces) {
        this.traces = traces;
    }

    public Map<String, List<RuleName>> getWarnings() {
        return warnings;
    }

    public void setWarnings(Map<String, List<RuleName>> warnings) {
        this.warnings = warnings;
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
