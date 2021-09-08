package edu.nd.crc.safa.server.services;

import java.util.List;

import edu.nd.crc.safa.db.entities.sql.Project;
import edu.nd.crc.safa.db.entities.sql.ProjectVersion;
import edu.nd.crc.safa.db.repositories.ProjectRepository;
import edu.nd.crc.safa.db.repositories.ProjectVersionRepository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

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

    public List<ProjectVersion> getProjectVersions(Project project) {
        return this.projectVersionRepository.findByProject(project);
    }

    public ProjectVersion createNextRevision(Project project) {
        ProjectVersion projectVersion = this.projectVersionRepository.getCurrentVersion(project);
        ProjectVersion newVersion = new ProjectVersion(project,
            projectVersion.getMajorVersion(),
            projectVersion.getMinorVersion(),
            projectVersion.getRevision() + 1);
        this.projectVersionRepository.save(newVersion);
        return newVersion;
    }
}
