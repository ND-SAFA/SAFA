package edu.nd.crc.safa.server.services;

import java.util.List;
import java.util.Optional;

import edu.nd.crc.safa.server.db.entities.sql.Project;
import edu.nd.crc.safa.server.db.entities.sql.ProjectVersion;
import edu.nd.crc.safa.server.db.repositories.ProjectRepository;
import edu.nd.crc.safa.server.db.repositories.ProjectVersionRepository;
import edu.nd.crc.safa.server.responses.ServerError;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.bind.annotation.PathVariable;

@Service
public class VersionService {
    ProjectRepository projectRepository;
    ProjectVersionRepository projectVersionRepository;

    @Autowired
    public VersionService(ProjectRepository projectRepository,
                          ProjectVersionRepository projectVersionRepository) {
        this.projectRepository = projectRepository;
        this.projectVersionRepository = projectVersionRepository;
    }

    public List<ProjectVersion> getProjectVersions(@PathVariable Project project) {
        return this.projectVersionRepository.findByProject(project);
    }

    public ProjectVersion createNewMajorVersion(Project project) throws ServerError {
        ProjectVersion projectVersion = getCurrentVersion(project);
        ProjectVersion newVersion = new ProjectVersion(project,
            projectVersion.getMajorVersion() + 1,
            1,
            1);
        this.projectVersionRepository.save(newVersion);
        return newVersion;
    }

    public ProjectVersion createNewMinorVersion(Project project) throws ServerError {
        ProjectVersion projectVersion = getCurrentVersion(project);
        ProjectVersion newVersion = new ProjectVersion(project,
            projectVersion.getMajorVersion(),
            projectVersion.getMinorVersion() + 1,
            1);
        this.projectVersionRepository.save(newVersion);
        return newVersion;
    }

    public ProjectVersion createNextRevision(Project project) throws ServerError {
        ProjectVersion projectVersion = getCurrentVersion(project);
        ProjectVersion newVersion = new ProjectVersion(project,
            projectVersion.getMajorVersion(),
            projectVersion.getMinorVersion(),
            projectVersion.getRevision() + 1);
        this.projectVersionRepository.save(newVersion);
        return newVersion;
    }

    public ProjectVersion getCurrentVersion(Project project) throws ServerError {
        Optional<ProjectVersion> projectVersionQuery = this.projectVersionRepository.getCurrentVersion(project);
        if (projectVersionQuery.isPresent()) {
            return projectVersionQuery.get();
        } else {
            throw new ServerError("Expected given project to contain an initial version");
        }
    }
}
