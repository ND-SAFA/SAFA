package edu.nd.crc.safa.server.controllers;

import java.util.HashMap;
import java.util.Map;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.server.db.entities.app.ArtifactAppEntity;
import edu.nd.crc.safa.server.db.entities.sql.Artifact;
import edu.nd.crc.safa.server.db.entities.sql.Project;
import edu.nd.crc.safa.server.db.entities.sql.ProjectVersion;
import edu.nd.crc.safa.server.db.repositories.ArtifactRepository;
import edu.nd.crc.safa.server.db.repositories.ProjectRepository;
import edu.nd.crc.safa.server.db.repositories.ProjectVersionRepository;
import edu.nd.crc.safa.server.messages.ServerError;
import edu.nd.crc.safa.server.messages.ServerResponse;
import edu.nd.crc.safa.server.services.ArtifactService;
import edu.nd.crc.safa.server.services.ProjectService;
import edu.nd.crc.safa.server.services.VersionService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.configurationprocessor.json.JSONException;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@CrossOrigin
@RestController
public class ArtifactController extends BaseController {

    ProjectService projectService;
    ArtifactService artifactService;
    VersionService versionService;

    ArtifactRepository artifactRepository;

    @Autowired
    public ArtifactController(ProjectRepository projectRepository,
                              ProjectVersionRepository projectVersionRepository,
                              ProjectService projectService,
                              ArtifactService artifactService,
                              VersionService versionService,
                              ArtifactRepository artifactRepository) {
        super(projectRepository, projectVersionRepository);
        this.projectService = projectService;
        this.artifactService = artifactService;
        this.versionService = versionService;
        this.artifactRepository = artifactRepository;
    }

    @PostMapping(value = "projects/{projectId}/artifacts")
    @ResponseStatus(HttpStatus.CREATED)
    public ServerResponse updateProjectVersionFromFlatFiles(
        @PathVariable UUID projectId,
        @RequestBody ArtifactAppEntity artifact) throws ServerError {
        Project project = this.projectRepository.findByProjectId(projectId);
        ProjectVersion projectVersion = this.versionService.getCurrentVersion(project);
        this.artifactService.addArtifactToVersion(projectVersion, artifact);
        return new ServerResponse(artifact);
    }

    @GetMapping("projects/{projectId}/artifacts/validate/{artifactName}")
    public ServerResponse checkIfNameExists(@PathVariable UUID projectId, @PathVariable String artifactName)
        throws JSONException {
        Project project = this.projectRepository.findByProjectId(projectId);
        Optional<Artifact> artifactQuery = this.artifactRepository.findByProjectAndName(project, artifactName);
        Map<String, Boolean> response = new HashMap<>();
        response.put("artifactExists", artifactQuery.isPresent());
        return new ServerResponse(response);
    }
}
