package edu.nd.crc.safa.features.commits.entities.app;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import javax.validation.Valid;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.delta.entities.app.ProjectChange;
import edu.nd.crc.safa.features.delta.entities.db.ModificationType;
import edu.nd.crc.safa.features.errors.entities.db.CommitError;
import edu.nd.crc.safa.features.projects.entities.app.IAppEntity;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.utilities.StringUtil;

import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * The model used to commit a change to the versioning system.
 */
@NoArgsConstructor
@Data
public class ProjectCommit {
    private ProjectVersion commitVersion;
    private ProjectChange<@Valid ArtifactAppEntity> artifacts = new ProjectChange<>();
    private ProjectChange<@Valid TraceAppEntity> traces = new ProjectChange<>();
    private List<CommitError> errors = new ArrayList<>();
    private boolean failOnError = true;

    public ProjectCommit(ProjectAppEntity projectAppEntity) {
        this.commitVersion = projectAppEntity.getProjectVersion();
        this.addArtifacts(ModificationType.ADDED, projectAppEntity.getArtifacts());
        this.addTraces(ModificationType.ADDED, projectAppEntity.getTraces());
    }

    public ProjectCommit(ProjectVersion commitVersion, boolean failOnError) {
        this.commitVersion = commitVersion;
        this.failOnError = failOnError;
    }

    public ProjectCommit(ProjectVersion projectVersion,
                         ProjectChange<ArtifactAppEntity> artifacts,
                         ProjectChange<TraceAppEntity> traces,
                         List<CommitError> errors,
                         boolean failOnError) {
        this.commitVersion = projectVersion;
        this.artifacts = artifacts;
        this.traces = traces;
        this.errors = errors;
        this.failOnError = failOnError;
    }

    public void addArtifacts(ModificationType modificationType,
                             List<ArtifactAppEntity> artifacts) {
        this.addEntities(modificationType, this.artifacts, artifacts);
    }

    public void addArtifact(ModificationType modificationType,
                            ArtifactAppEntity artifactAppEntity) {
        this.addEntity(modificationType, this.artifacts, artifactAppEntity);
    }

    public void addTraces(ModificationType modificationType,
                          List<TraceAppEntity> traces) {
        this.addEntities(modificationType, this.traces, traces);
    }

    public void addTrace(ModificationType modificationType,
                         TraceAppEntity trace) {
        this.addEntity(modificationType, this.traces, trace);
    }

    @JsonIgnore
    public boolean shouldUpdateDefaultLayout() {
        return this.getArtifacts().getAdded().size()
            + this.getArtifacts().getRemoved().size()
            + this.getTraces().getAdded().size()
            + this.getTraces().getRemoved().size() > 0;
    }

    @JsonIgnore
    public ArtifactAppEntity getArtifact(ModificationType modificationType, int index) {
        return getArtifactList(modificationType).get(index);
    }

    @JsonIgnore
    public ArtifactAppEntity getArtifact(ModificationType modificationType, String name) {
        List<ArtifactAppEntity> queryByName =
            this.getArtifactList(modificationType)
                .stream()
                .filter(a -> a.getName().equals(name))
                .collect(Collectors.toList());
        if (queryByName.isEmpty()) {
            throw new IllegalArgumentException("Could not find artifact with name:" + name);
        }
        if (queryByName.size() > 1) {
            String error = String.format("More than one artifact with name [%s] found (%s).", name, queryByName.size());
            throw new IllegalArgumentException(error);
        }
        return queryByName.get(0);
    }

    @JsonIgnore
    public List<ArtifactAppEntity> getArtifactList(ModificationType modificationType) {
        return this.generateMod2Entities(this.artifacts).get(modificationType);
    }

    private <T extends IAppEntity> void addEntities(ModificationType modificationType,
                                                    ProjectChange<T> projectChange,
                                                    List<T> artifacts) {
        List<T> existingEntities = this.generateMod2Entities(projectChange).get(modificationType);
        List<T> newEntities = artifacts
            .stream()
            .filter(a -> !existingEntities.contains(a))
            .collect(Collectors.toList());
        existingEntities.addAll(newEntities);
    }

    private <T extends IAppEntity> void addEntity(ModificationType modificationType,
                                                  ProjectChange<T> projectChange,
                                                  T entity) {

        this.generateMod2Entities(projectChange).get(modificationType).add(entity);
    }

    private <T extends IAppEntity> Map<ModificationType, List<T>> generateMod2Entities(
        ProjectChange<T> projectChange
    ) {
        Map<ModificationType, List<T>> mod2entities = new HashMap<>();
        mod2entities.put(ModificationType.ADDED, projectChange.getAdded());
        mod2entities.put(ModificationType.MODIFIED, projectChange.getModified());
        mod2entities.put(ModificationType.REMOVED, projectChange.getRemoved());
        return mod2entities;
    }

    /**
     * @return A human-readable summaries of the changes in commit.
     */
    @JsonIgnore
    public String getSummary() {
        List<String> logs = new ArrayList<>();
        logs.add(this.artifacts.getSummary("Artifacts"));
        logs.add(this.traces.getSummary("Trace Links"));
        return StringUtil.join(logs, "\n");
    }
}
