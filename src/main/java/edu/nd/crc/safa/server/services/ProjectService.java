package edu.nd.crc.safa.server.services;

import java.util.ArrayList;
import java.util.Hashtable;
import java.util.List;
import java.util.stream.Collectors;
import javax.transaction.Transactional;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.server.db.entities.app.ArtifactAppEntity;
import edu.nd.crc.safa.server.db.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.server.db.entities.app.TraceApplicationEntity;
import edu.nd.crc.safa.server.db.entities.sql.ArtifactBody;
import edu.nd.crc.safa.server.db.entities.sql.ModificationType;
import edu.nd.crc.safa.server.db.entities.sql.Project;
import edu.nd.crc.safa.server.db.entities.sql.ProjectVersion;
import edu.nd.crc.safa.server.db.repositories.ArtifactBodyRepository;
import edu.nd.crc.safa.server.db.repositories.ArtifactRepository;
import edu.nd.crc.safa.server.db.repositories.ArtifactTypeRepository;
import edu.nd.crc.safa.server.db.repositories.ParserErrorRepository;
import edu.nd.crc.safa.server.db.repositories.ProjectRepository;
import edu.nd.crc.safa.server.db.repositories.ProjectVersionRepository;
import edu.nd.crc.safa.server.db.repositories.TraceLinkRepository;
import edu.nd.crc.safa.server.responses.ProjectCreationResponse;
import edu.nd.crc.safa.server.responses.ProjectErrors;
import edu.nd.crc.safa.server.responses.ServerError;
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
    ArtifactService artifactService;
    TraceLinkService traceLinkService;

    @Autowired
    public ProjectService(ProjectRepository projectRepository,
                          ProjectVersionRepository projectVersionRepository,
                          ArtifactRepository artifactRepository,
                          ArtifactTypeRepository artifactTypeRepository,
                          ArtifactBodyRepository artifactBodyRepository,
                          TraceLinkRepository traceLinkRepository,
                          ParserErrorRepository parserErrorRepository,
                          ParserErrorService parserErrorService,
                          ArtifactService artifactService,
                          TraceLinkService traceLinkService) {
        this.projectRepository = projectRepository;
        this.projectVersionRepository = projectVersionRepository;
        this.artifactRepository = artifactRepository;
        this.artifactTypeRepository = artifactTypeRepository;
        this.artifactBodyRepository = artifactBodyRepository;
        this.traceLinkRepository = traceLinkRepository;
        this.parserErrorRepository = parserErrorRepository;
        this.parserErrorService = parserErrorService;
        this.artifactService = artifactService;
        this.traceLinkService = traceLinkService;
    }

    @Transactional
    public ProjectCreationResponse createProject(ProjectVersion projectVersion,
                                                 ProjectAppEntity appEntity) {

        if (appEntity.artifacts != null) {
            artifactService.createOrUpdateArtifacts(projectVersion, appEntity.getArtifacts());
        }

        if (appEntity.traces != null) {
            traceLinkService.createTraceLinks(projectVersion, appEntity.getTraces());
        }

        ProjectAppEntity projectAppEntity = createApplicationEntity(projectVersion);
        ProjectErrors projectErrors = this.parserErrorService.collectionProjectErrors(projectVersion);
        return new ProjectCreationResponse(projectAppEntity, projectVersion, projectErrors);
    }

    @Transactional
    public ProjectCreationResponse updateProject(ProjectVersion projectVersion,
                                                 ProjectAppEntity appEntity) {

        artifactService.createOrUpdateArtifacts(projectVersion, appEntity.getArtifacts());

        //TODO: Update trace links

        ProjectErrors projectErrors = this.parserErrorService.collectionProjectErrors(projectVersion);
        return new ProjectCreationResponse(appEntity, projectVersion, projectErrors); // TODO: Actually retrieve new
    }

    public ProjectAppEntity createApplicationEntity(ProjectVersion projectVersion) {
        Project project = projectVersion.getProject();
        List<ArtifactAppEntity> artifacts = new ArrayList<>();

        Hashtable<String, List<ArtifactBody>> artifactBodyTable = new Hashtable<>();
        List<ArtifactBody> projectBodies = this.artifactBodyRepository.findByProject(projectVersion.getProject());
        for (ArtifactBody body : projectBodies) {
            String key = body.getArtifact().getArtifactId().toString();
            if (artifactBodyTable.containsKey(key)) {
                artifactBodyTable.get(key).add(body);
            } else {
                List<ArtifactBody> newList = new ArrayList<>();
                newList.add(body);
                artifactBodyTable.put(key, newList);
            }
        }

        for (String key : artifactBodyTable.keySet()) {
            List<ArtifactBody> bodyVersions = artifactBodyTable.get(key);
            ArtifactBody latest = null;
            for (ArtifactBody body : bodyVersions) {
                if (body.getProjectVersion().isLessThanOrEqualTo(projectVersion)) {
                    if (latest == null || body.getProjectVersion().isGreaterThan(latest.getProjectVersion())) {
                        latest = body;
                    }
                }
            }

            if (latest != null && latest.getModificationType() != ModificationType.REMOVED) {
                artifacts.add(new ArtifactAppEntity(latest));
            }
        }
        List<TraceApplicationEntity> traces = this.traceLinkRepository
            .getManualLinks(project)
            .stream()
            .map(TraceApplicationEntity::new)
            .collect(Collectors.toList());
        return new ProjectAppEntity(projectVersion, artifacts, traces);
    }

    public void deleteProject(Project project) throws ServerError {
        this.projectRepository.delete(project);
        OSHelper.deletePath(ProjectPaths.getPathToStorage(project));
    }
}
