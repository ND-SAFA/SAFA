package edu.nd.crc.safa.features.versions.services;

import java.util.List;
import java.util.Optional;

import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
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

    @Setter(onMethod = @__({@Autowired, @Lazy}))  // Prevents circular dependency
    private TypeService typeService;

    public List<ProjectVersion> getProjectVersions(@PathVariable Project project) {
        return this.projectVersionRepository.findByProjectInBackwardsOrder(project);
    }

    public ProjectVersion createNewVersion(Project project, int major, int minor, int revision) {
        ProjectVersion newVersion = new ProjectVersion(project, major, minor, revision);
        newVersion = this.projectVersionRepository.save(newVersion);
        createTypeCountEntries(newVersion);
        return newVersion;
    }

    public ProjectVersion createNewMajorVersion(Project project) throws SafaError {
        ProjectVersion projectVersion = getCurrentVersion(project);
        return createNewVersion(project, projectVersion.getMajorVersion() + 1, 0, 0);
    }

    public ProjectVersion createNewMinorVersion(Project project) throws SafaError {
        ProjectVersion projectVersion = getCurrentVersion(project);
        return createNewVersion(project, projectVersion.getMajorVersion(), projectVersion.getMinorVersion() + 1, 0);
    }

    public ProjectVersion createNextRevision(Project project) throws SafaError {
        ProjectVersion projectVersion = getCurrentVersion(project);
        return createNewVersion(project,
            projectVersion.getMajorVersion(),
            projectVersion.getMinorVersion(),
            projectVersion.getRevision() + 1);
    }

    /**
     * Returns the current version of given project.
     *
     * @param project The project whose current version is returned.
     * @return {@link ProjectVersion} Current version.
     * @throws SafaError Throws error if
     */
    public ProjectVersion getCurrentVersion(Project project) throws SafaError {
        Optional<ProjectVersion> projectVersionQuery = this.projectVersionRepository.getCurrentVersion(project);
        if (projectVersionQuery.isPresent()) {
            return projectVersionQuery.get();
        } else {
            throw new SafaError("Expected given project to contain an initial version.");
        }
    }

    public ProjectVersion createInitialProjectVersion(Project project) {
        ProjectVersion projectVersion = new ProjectVersion(project, 1, 0, 0);
        projectVersion = this.projectVersionRepository.save(projectVersion);
        createTypeCountEntries(projectVersion);
        return projectVersion;
    }

    /**
     * Create type count entities for the given version for all types in a project
     *
     * @param version The version to add counts for
     */
    private void createTypeCountEntries(ProjectVersion version) {
        for (ArtifactType type : typeService.getTypes(version.getProject())) {
            ArtifactTypeCount typeCount = new ArtifactTypeCount(version, type);
            typeCountService.save(typeCount);
        }
    }
}
