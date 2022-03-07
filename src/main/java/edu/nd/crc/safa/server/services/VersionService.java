package edu.nd.crc.safa.server.services;

import java.util.List;
import java.util.Optional;

import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.repositories.projects.ProjectVersionRepository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.bind.annotation.PathVariable;

/**
 * Responsible for creating new versions and retrieving old ones.
 */
@Service
public class VersionService {
    private final ProjectVersionRepository projectVersionRepository;

    @Autowired
    public VersionService(ProjectVersionRepository projectVersionRepository) {
        this.projectVersionRepository = projectVersionRepository;
    }

    public List<ProjectVersion> getProjectVersions(@PathVariable Project project) {
        return this.projectVersionRepository.findByProjectInBackwardsOrder(project);
    }

    public ProjectVersion createNewMajorVersion(Project project) throws SafaError {
        ProjectVersion projectVersion = getCurrentVersion(project);
        ProjectVersion newVersion = new ProjectVersion(project,
            projectVersion.getMajorVersion() + 1,
            1,
            1);
        this.projectVersionRepository.save(newVersion);
        return newVersion;
    }

    public ProjectVersion createNewMinorVersion(Project project) throws SafaError {
        ProjectVersion projectVersion = getCurrentVersion(project);
        ProjectVersion newVersion = new ProjectVersion(project,
            projectVersion.getMajorVersion(),
            projectVersion.getMinorVersion() + 1,
            1);
        this.projectVersionRepository.save(newVersion);
        return newVersion;
    }

    public ProjectVersion createNextRevision(Project project) throws SafaError {
        ProjectVersion projectVersion = getCurrentVersion(project);
        ProjectVersion newVersion = new ProjectVersion(project,
            projectVersion.getMajorVersion(),
            projectVersion.getMinorVersion(),
            projectVersion.getRevision() + 1);
        this.projectVersionRepository.save(newVersion);
        return newVersion;
    }

    public ProjectVersion getCurrentVersion(Project project) throws SafaError {
        Optional<ProjectVersion> projectVersionQuery = this.projectVersionRepository.getCurrentVersion(project);
        if (projectVersionQuery.isPresent()) {
            return projectVersionQuery.get();
        } else {
            throw new SafaError("Expected given project to contain an initial version");
        }
    }
}
