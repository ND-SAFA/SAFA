package edu.nd.crc.safa.server.controllers;

import java.util.HashMap;
import java.util.Map;
import java.util.Optional;
import java.util.UUID;
import javax.validation.Valid;

import edu.nd.crc.safa.server.entities.api.ServerError;
import edu.nd.crc.safa.server.entities.api.ServerResponse;
import edu.nd.crc.safa.server.entities.app.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.db.Artifact;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.repositories.ArtifactRepository;
import edu.nd.crc.safa.server.repositories.ProjectRepository;
import edu.nd.crc.safa.server.repositories.ProjectVersionRepository;
import edu.nd.crc.safa.server.services.ArtifactVersionService;
import edu.nd.crc.safa.server.services.ProjectService;
import edu.nd.crc.safa.server.services.RevisionNotificationService;
import edu.nd.crc.safa.server.services.VersionService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@CrossOrigin
@RestController
public class ArtifactController extends BaseController {

    ArtifactRepository artifactRepository;

    ProjectService projectService;
    ArtifactVersionService artifactVersionService;
    VersionService versionService;
    RevisionNotificationService revisionNotificationService;

    @Autowired
    public ArtifactController(ProjectRepository projectRepository,
                              ProjectVersionRepository projectVersionRepository,
                              ProjectService projectService,
                              ArtifactVersionService artifactVersionService,
                              VersionService versionService,
                              ArtifactRepository artifactRepository,
                              RevisionNotificationService revisionNotificationService) {
        super(projectRepository, projectVersionRepository);
        this.projectService = projectService;
        this.artifactVersionService = artifactVersionService;
        this.versionService = versionService;
        this.artifactRepository = artifactRepository;
        this.revisionNotificationService = revisionNotificationService;
    }

    /**
     * Creates a new artifact at the specified version within the verion's associated project.
     *
     * @param versionId UUID of versionId of associated project verison.
     * @param artifact  The artifact to be created.
     * @return The artifact created.
     * @throws ServerError Throws error if artifact already exists in project.
     */
    @PostMapping(value = "projects/versions/{versionId}/artifacts")
    @ResponseStatus(HttpStatus.CREATED)
    public ServerResponse createArtifactAtVersion(
        @PathVariable UUID versionId,
        @Valid @RequestBody ArtifactAppEntity artifact) throws ServerError {
        ProjectVersion projectVersion = this.projectVersionRepository.findByVersionId(versionId);
        this.artifactVersionService.setArtifactAtProjectVersion(projectVersion, artifact);
        this.revisionNotificationService.broadcastArtifact(projectVersion, artifact);
        return new ServerResponse(artifact);
    }

    /**
     * Deletes artifact with given name within given project.
     *
     * @param projectId    UUID of versionId of associated project version.
     * @param artifactName The name of the artifact to be deleted.
     * @throws ServerError Throws error if artifact already exists in project.
     */
    @DeleteMapping(value = "projects/{projectId}/artifacts/{artifactName}")
    @ResponseStatus(HttpStatus.OK)
    public ServerResponse deleteArtifact(
        @PathVariable UUID projectId,
        @PathVariable String artifactName) {
        Project project = this.projectRepository.findByProjectId(projectId);
        Optional<Artifact> artifactQuery = this.artifactRepository.findByProjectAndName(project, artifactName);
        artifactQuery.ifPresent(artifact -> this.artifactRepository.delete(artifact));
        return new ServerResponse(String.format("%s successfully deleted.", artifactName));
    }

    /**
     * Returns flag `artifactExists` indicating whether artifact exists in the project.
     *
     * @param projectId  UUID identifying unique project.
     * @param artifactId The name / identifier of the artifact.
     * @return `artifactExists` flag indicating presence of artifact in project.
     */
    @GetMapping("projects/{projectId}/artifacts/validate/{artifactId}")
    public ServerResponse checkIfNameExists(@PathVariable UUID projectId, @PathVariable String artifactId) {
        Project project = this.projectRepository.findByProjectId(projectId);
        Optional<Artifact> artifactQuery = this.artifactRepository.findByProjectAndName(project, artifactId);
        Map<String, Boolean> response = new HashMap<>();
        response.put("artifactExists", artifactQuery.isPresent());
        return new ServerResponse(response);
    }
}
