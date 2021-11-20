package edu.nd.crc.safa.server.controllers;

import java.util.HashMap;
import java.util.Map;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.config.Routes;
import edu.nd.crc.safa.server.entities.api.ServerResponse;
import edu.nd.crc.safa.server.entities.db.Artifact;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.repositories.ArtifactBodyRepository;
import edu.nd.crc.safa.server.repositories.ArtifactRepository;
import edu.nd.crc.safa.server.repositories.ProjectRepository;
import edu.nd.crc.safa.server.repositories.ProjectVersionRepository;
import edu.nd.crc.safa.server.services.ArtifactVersionService;
import edu.nd.crc.safa.server.services.ProjectService;
import edu.nd.crc.safa.server.services.RevisionNotificationService;
import edu.nd.crc.safa.server.services.VersionService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ArtifactController extends BaseController {

    ArtifactRepository artifactRepository;
    ArtifactBodyRepository artifactBodyRepository;

    ProjectService projectService;
    ArtifactVersionService artifactVersionService;
    VersionService versionService;
    RevisionNotificationService revisionNotificationService;

    @Autowired
    public ArtifactController(ProjectRepository projectRepository,
                              ArtifactBodyRepository artifactBodyRepository,
                              ProjectVersionRepository projectVersionRepository,
                              ProjectService projectService,
                              ArtifactVersionService artifactVersionService,
                              VersionService versionService,
                              ArtifactRepository artifactRepository,
                              RevisionNotificationService revisionNotificationService) {
        super(projectRepository, projectVersionRepository);
        this.artifactBodyRepository = artifactBodyRepository;
        this.projectService = projectService;
        this.artifactVersionService = artifactVersionService;
        this.versionService = versionService;
        this.artifactRepository = artifactRepository;
        this.revisionNotificationService = revisionNotificationService;
    }
    
    /**
     * Returns flag `artifactExists` indicating whether artifact exists in the project.
     *
     * @param projectId    UUID identifying unique project.
     * @param artifactName The name / identifier of the artifact.
     * @return `artifactExists` flag indicating presence of artifact in project.
     */
    @GetMapping(Routes.checkIfArtifactExists)
    public ServerResponse checkIfNameExists(@PathVariable UUID projectId, @PathVariable String artifactName) {
        Project project = this.projectRepository.findByProjectId(projectId);
        Optional<Artifact> artifactQuery = this.artifactRepository.findByProjectAndName(project, artifactName);
        Map<String, Boolean> response = new HashMap<>();
        response.put("artifactExists", artifactQuery.isPresent());
        return new ServerResponse(response);
    }
}
