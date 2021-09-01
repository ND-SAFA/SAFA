package edu.nd.crc.safa.services;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;
import javax.transaction.Transactional;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.entities.application.ArtifactApplicationEntity;
import edu.nd.crc.safa.entities.application.ProjectApplicationEntity;
import edu.nd.crc.safa.entities.application.TraceApplicationEntity;
import edu.nd.crc.safa.entities.sql.ApplicationActivity;
import edu.nd.crc.safa.entities.sql.Artifact;
import edu.nd.crc.safa.entities.sql.ArtifactBody;
import edu.nd.crc.safa.entities.sql.ArtifactType;
import edu.nd.crc.safa.entities.sql.ParserError;
import edu.nd.crc.safa.entities.sql.Project;
import edu.nd.crc.safa.entities.sql.ProjectVersion;
import edu.nd.crc.safa.entities.sql.TraceLink;
import edu.nd.crc.safa.repositories.sql.ArtifactBodyRepository;
import edu.nd.crc.safa.repositories.sql.ArtifactRepository;
import edu.nd.crc.safa.repositories.sql.ArtifactTypeRepository;
import edu.nd.crc.safa.repositories.sql.ParserErrorRepository;
import edu.nd.crc.safa.repositories.sql.ProjectRepository;
import edu.nd.crc.safa.repositories.sql.ProjectVersionRepository;
import edu.nd.crc.safa.repositories.sql.TraceLinkRepository;
import edu.nd.crc.safa.responses.ProjectCreationResponse;
import edu.nd.crc.safa.responses.ProjectErrors;
import edu.nd.crc.safa.responses.ServerError;
import edu.nd.crc.safa.utilities.OSHelper;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service

public class ProjectService {
    /**
     * Responsible for all providing an API for performing the
     * business logic involved in ProjectsController.
     */
    ProjectRepository projectRepository;
    ProjectVersionRepository projectVersionRepository;
    ArtifactRepository artifactRepository;
    ArtifactTypeRepository artifactTypeRepository;
    ArtifactBodyRepository artifactBodyRepository;
    TraceLinkRepository traceLinkRepository;
    ParserErrorRepository parserErrorRepository;
    ParserErrorService parserErrorService;
    SynchronizeService synchronizeService;

    @Autowired
    public ProjectService(ProjectRepository projectRepository,
                          ProjectVersionRepository projectVersionRepository,
                          ArtifactRepository artifactRepository,
                          ArtifactTypeRepository artifactTypeRepository,
                          ArtifactBodyRepository artifactBodyRepository,
                          TraceLinkRepository traceLinkRepository,
                          ParserErrorRepository parserErrorRepository,
                          ParserErrorService parserErrorService,
                          SynchronizeService synchronizeService) {
        this.projectRepository = projectRepository;
        this.projectVersionRepository = projectVersionRepository;
        this.artifactRepository = artifactRepository;
        this.artifactTypeRepository = artifactTypeRepository;
        this.artifactBodyRepository = artifactBodyRepository;
        this.traceLinkRepository = traceLinkRepository;
        this.parserErrorRepository = parserErrorRepository;
        this.parserErrorService = parserErrorService;
        this.synchronizeService = synchronizeService;
    }

    public void deleteProject(Project project) throws ServerError {
        this.projectRepository.delete(project);
        OSHelper.deletePath(ProjectPaths.getPathToStorage(project));
    }

    @Transactional
    public ProjectCreationResponse createOrUpdateProject(ProjectApplicationEntity appEntity) {
        Project project = new Project(appEntity);
        this.projectRepository.save(project);
        ProjectVersion projectVersion = new ProjectVersion(project);
        this.projectVersionRepository.save(projectVersion);

        if (appEntity.artifacts != null) {
            appEntity
                .getArtifacts()
                .forEach(a -> createArtifact(projectVersion, a));
        }

        if (appEntity.traces != null) {
            appEntity
                .getTraces()
                .forEach(t -> createTrace(projectVersion, t));
        }

        ProjectApplicationEntity projectApplicationEntity = createApplicationEntity(projectVersion);
        ProjectErrors projectErrors = this.parserErrorService.collectionProjectErrors(projectVersion);
        return new ProjectCreationResponse(projectApplicationEntity, projectErrors);
    }

    public ProjectApplicationEntity createApplicationEntity(ProjectVersion newProjectVersion) {
        Project project = newProjectVersion.getProject();
        List<ArtifactApplicationEntity> artifacts = this.artifactBodyRepository
            .findByProjectVersion(newProjectVersion)
            .stream()
            .map(ArtifactApplicationEntity::new)
            .collect(Collectors.toList());
        List<TraceApplicationEntity> traces = this.traceLinkRepository
            .findByProject(project)
            .stream()
            .map(TraceApplicationEntity::new)
            .collect(Collectors.toList());
        return new ProjectApplicationEntity(newProjectVersion, artifacts, traces);
    }

    private void createArtifact(ProjectVersion projectVersion,
                                ArtifactApplicationEntity a) {
        Project project = projectVersion.getProject();
        Optional<ArtifactType> artifactTypeQuery = this.artifactTypeRepository
            .findByProjectAndNameIgnoreCase(project, a.getType());
        ArtifactType artifactType;
        if (!artifactTypeQuery.isPresent()) {
            artifactType = new ArtifactType(project, a.getType());
            this.artifactTypeRepository.save(artifactType);
        } else {
            artifactType = artifactTypeQuery.get();
        }

        Optional<Artifact> artifactQuery = this.artifactRepository.findByProjectAndName(project, a.getName());
        Artifact artifact;
        artifact = artifactQuery.orElseGet(() -> new Artifact(project, artifactType, a.getName()));
        this.artifactRepository.save(artifact);

        ArtifactBody body = new ArtifactBody(projectVersion, artifact, a.getSummary(), a.getBody());
        this.artifactBodyRepository.save(body);
    }

    private void createTrace(ProjectVersion projectVersion,
                             TraceApplicationEntity t) {
        Project project = projectVersion.getProject();
        Optional<Artifact> source = this.artifactRepository.findByProjectAndName(project, t.source);
        if (!source.isPresent()) {
            ParserError sourceError = new ParserError(projectVersion,
                "Could not find source artifact: " + t.source,
                ApplicationActivity.PARSING_TRACES);
            this.parserErrorRepository.save(sourceError);
            return;
        }
        Optional<Artifact> target = this.artifactRepository.findByProjectAndName(project, t.target);
        if (!target.isPresent()) {
            ParserError targetError = new ParserError(projectVersion,
                "Could not find target artifact: " + t.target,
                ApplicationActivity.PARSING_TRACES);
            this.parserErrorRepository.save(targetError);
            return;
        }
        try {
            TraceLink traceLink = new TraceLink(source.get(), target.get());
            traceLink.setIsManual();
            this.traceLinkRepository.save(traceLink);
        } catch (ServerError e) {
            ParserError linkError = new ParserError(projectVersion,
                e.getMessage(),
                ApplicationActivity.PARSING_TRACES);
            this.parserErrorRepository.save(linkError);
        }
    }
}
