package edu.nd.crc.safa.features.versions.services;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.traces.entities.db.TraceMatrixEntry;
import edu.nd.crc.safa.features.traces.services.TraceMatrixService;
import edu.nd.crc.safa.features.types.entities.db.ArtifactType;
import edu.nd.crc.safa.features.types.entities.db.ArtifactTypeCount;
import edu.nd.crc.safa.features.types.services.ArtifactTypeCountService;
import edu.nd.crc.safa.features.types.services.TypeService;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.features.versions.repositories.ProjectVersionRepository;

import lombok.RequiredArgsConstructor;
import lombok.Setter;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Lazy;
import org.springframework.stereotype.Service;
import org.springframework.web.bind.annotation.PathVariable;

/**
 * Responsible for creating new versions and retrieving old ones.
 */
@Service
@RequiredArgsConstructor
public class VersionService {
    private final ProjectVersionRepository projectVersionRepository;
    private final ArtifactTypeCountService typeCountService;
    private final TraceMatrixService traceMatrixService;
    @Setter(onMethod = @__({@Autowired, @Lazy}))
    private TypeService typeService;

    public List<ProjectVersion> getProjectVersions(@PathVariable Project project) {
        return this.projectVersionRepository.findByProjectInBackwardsOrder(project);
    }

    public ProjectVersion createNewVersion(Project project, int major, int minor, int revision) {
        return createNewVersion(project, major, minor, revision, getCurrentVersionOptional(project).orElse(null));
    }

    public ProjectVersion createNewVersion(Project project, int major, int minor,
                                           int revision, ProjectVersion prevVersion) {

        ProjectVersion newVersion = new ProjectVersion(project, major, minor, revision);
        newVersion = this.projectVersionRepository.save(newVersion);
        createTypeCountEntries(newVersion, prevVersion);
        createTraceCountEntries(newVersion, prevVersion);
        return newVersion;
    }

    public ProjectVersion createNewMajorVersion(Project project) throws SafaError {
        ProjectVersion projectVersion = getCurrentVersion(project);
        return createNewVersion(project, projectVersion.getMajorVersion() + 1, 0, 0, projectVersion);
    }

    public ProjectVersion createNewMinorVersion(Project project) throws SafaError {
        ProjectVersion projectVersion = getCurrentVersion(project);
        return createNewVersion(project, projectVersion.getMajorVersion(), projectVersion.getMinorVersion() + 1,
            0, projectVersion);
    }

    public ProjectVersion createNextRevision(Project project) throws SafaError {
        ProjectVersion projectVersion = getCurrentVersion(project);
        return createNewVersion(project,
            projectVersion.getMajorVersion(),
            projectVersion.getMinorVersion(),
            projectVersion.getRevision() + 1,
            projectVersion);
    }

    /**
     * Returns the current version of given project.
     *
     * @param project The project whose current version is returned.
     * @return {@link ProjectVersion} Current version.
     * @throws SafaError Throws error if
     */
    public ProjectVersion getCurrentVersion(Project project) throws SafaError {
        Optional<ProjectVersion> projectVersionQuery = getCurrentVersionOptional(project);
        return projectVersionQuery.orElseThrow(() ->
            new SafaError("Expected given project to contain an initial version."));
    }

    private Optional<ProjectVersion> getCurrentVersionOptional(Project project) {
        return this.projectVersionRepository.getCurrentVersion(project);
    }

    public ProjectVersion createInitialProjectVersion(Project project) {
        ProjectVersion projectVersion = new ProjectVersion(project, 1, 0, 0);
        projectVersion = this.projectVersionRepository.save(projectVersion);
        createTypeCountEntries(projectVersion, null);
        return projectVersion;
    }

    /**
     * Create type count entities for the given version for all types in a project
     *
     * @param version     The version to add counts for
     * @param prevVersion The previous version
     */
    private void createTypeCountEntries(ProjectVersion version, ProjectVersion prevVersion) {
        for (ArtifactType type : typeService.getTypes(version.getProject())) {
            ArtifactTypeCount typeCount = new ArtifactTypeCount(version, type);

            if (prevVersion != null) {
                ArtifactTypeCount prevTypeCount =
                    typeCountService.getByProjectVersionAndType(prevVersion, type).orElseThrow();
                typeCount.setCount(prevTypeCount.getCount());
            }

            typeCountService.save(typeCount);
        }
    }

    /**
     * Copy trace count entries from one version to another
     *
     * @param version     The version to add counts for
     * @param prevVersion The previous version
     */
    private void createTraceCountEntries(ProjectVersion version, ProjectVersion prevVersion) {
        if (prevVersion == null) {
            return;
        }

        for (TraceMatrixEntry traceEntry : traceMatrixService.getEntries(prevVersion)) {
            TraceMatrixEntry newEntry = traceMatrixService.createEntry(version, traceEntry.getSourceType(),
                traceEntry.getTargetType());
            newEntry.setCount(traceEntry.getCount());
            newEntry.setGeneratedCount(traceEntry.getGeneratedCount());
            newEntry.setApprovedCount(traceEntry.getApprovedCount());
            traceMatrixService.updateEntry(newEntry);
        }
    }

    /**
     * Retrieve a project version by its ID
     *
     * @param versionId The ID of the project version
     * @return The project version with that ID
     */
    public ProjectVersion getVersionById(UUID versionId) {
        return projectVersionRepository.findByVersionId(versionId);
    }
}
