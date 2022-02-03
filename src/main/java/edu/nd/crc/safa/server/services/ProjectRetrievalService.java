package edu.nd.crc.safa.server.services;

import java.util.Hashtable;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import edu.nd.crc.safa.server.entities.api.ProjectEntities;
import edu.nd.crc.safa.server.entities.api.ProjectParsingErrors;
import edu.nd.crc.safa.server.entities.app.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.server.entities.app.TraceAppEntity;
import edu.nd.crc.safa.server.entities.db.ArtifactVersion;
import edu.nd.crc.safa.server.entities.db.ProjectMembership;
import edu.nd.crc.safa.server.entities.db.ProjectRole;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.repositories.ArtifactVersionRepository;
import edu.nd.crc.safa.server.repositories.ProjectMembershipRepository;
import edu.nd.crc.safa.server.repositories.TraceLinkVersionRepository;
import edu.nd.crc.safa.warnings.RuleName;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

/**
 * Responsible for all providing an API to retrieve and collect project related enities including:
 * 1. ProjectCreationResponse
 * 2. ProjectAppEntity
 */
@Service
public class ProjectRetrievalService {

    private final TraceLinkVersionRepository traceLinkVersionRepository;
    private final ArtifactVersionRepository artifactVersionRepository;
    private final ProjectMembershipRepository projectMembershipRepository;
    private final CommitErrorRetrievalService commitErrorRetrievalService;
    private final WarningService warningService;

    @Autowired
    public ProjectRetrievalService(TraceLinkVersionRepository traceLinkVersionRepository,
                                   ProjectMembershipRepository projectMembershipRepository,
                                   ArtifactVersionRepository artifactVersionRepository,
                                   CommitErrorRetrievalService commitErrorRetrievalService,
                                   WarningService warningService) {
        this.traceLinkVersionRepository = traceLinkVersionRepository;
        this.artifactVersionRepository = artifactVersionRepository;
        this.projectMembershipRepository = projectMembershipRepository;
        this.commitErrorRetrievalService = commitErrorRetrievalService;
        this.warningService = warningService;
    }

    /**
     * Finds project, artifact, traces, errors, and warnings related with given project version.
     *
     * @param projectVersion Version whose artifacts are used to generate warnings and error
     * @return ProjectCreationResponse containing all relevant project entities
     */
    public ProjectEntities retrieveAndCreateProjectResponse(ProjectVersion projectVersion) {
        ProjectAppEntity projectAppEntity = this.retrieveApplicationEntity(projectVersion);
        ProjectParsingErrors projectParsingErrors = this.commitErrorRetrievalService
            .collectionProjectErrors(projectVersion);
        Map<String, List<RuleName>> projectWarnings = this.warningService.findViolationsInArtifactTree(projectVersion);
        return new ProjectEntities(projectAppEntity, projectVersion, projectParsingErrors, projectWarnings);
    }

    /**
     * Creates a project application entity containing the entities (e.g. traces, artifacts) from
     * the given version. Further, gathers the list of project members at the time of being called.
     *
     * @param projectVersion The point in the project whose entities are being retrieved.
     * @return ProjectAppEntity Entity containing project name, description, artifacts, and traces.
     */
    public ProjectAppEntity retrieveApplicationEntity(ProjectVersion projectVersion) {
        List<ArtifactVersion> artifactBodies = artifactVersionRepository
            .getEntityVersionsInProjectVersion(projectVersion);

        List<ArtifactAppEntity> artifacts =
            artifactBodies
                .stream()
                .map(ArtifactAppEntity::new)
                .collect(Collectors.toList());
        List<String> artifactIds = artifacts.stream().map(ArtifactAppEntity::getId).collect(Collectors.toList());

        List<TraceAppEntity> traces =
            this.traceLinkVersionRepository
                .getEntityVersionsInProjectVersion(projectVersion)
                .stream()
                .map(TraceAppEntity::new)
                .filter(t -> artifactIds.contains(t.sourceId)
                    && artifactIds.contains(t.targetId))
                .collect(Collectors.toList());

        Hashtable<String, ProjectRole> projectMembers = new Hashtable<>();
        for (ProjectMembership pm : this.projectMembershipRepository.findByProject(projectVersion.getProject())) {
            projectMembers.put(pm.getMember().getEmail(), pm.getRole());
        }

        return new ProjectAppEntity(projectVersion, artifacts, traces, projectMembers);
    }
}
