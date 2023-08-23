package edu.nd.crc.safa.features.commits.sync;

import java.util.List;
import java.util.Map;
import java.util.UUID;

import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.documents.entities.app.DocumentAppEntity;
import edu.nd.crc.safa.features.layout.entities.app.LayoutPosition;
import edu.nd.crc.safa.features.memberships.entities.app.ProjectMemberAppEntity;
import edu.nd.crc.safa.features.notifications.entities.Change;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;
import edu.nd.crc.safa.features.permissions.entities.ProjectPermission;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.rules.parser.RuleName;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.traces.entities.app.TraceMatrixAppEntity;
import edu.nd.crc.safa.features.types.entities.TypeAppEntity;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

/**
 * Responsible for
 */
@RestController
public class SyncController extends BaseController {

    public SyncController(ResourceBuilder resourceBuilder,
                          ServiceProvider serviceProvider) {
        super(resourceBuilder, serviceProvider);
    }

    @PostMapping(AppRoutes.Sync.GET_CHANGES)
    public ProjectAppEntity getChanges(@PathVariable UUID versionId,
                                       @RequestBody EntityChangeMessage message) {
        ProjectAppEntity projectAppEntity = new ProjectAppEntity();
        SafaUser user = serviceProvider.getSafaUserService().getCurrentUser();
        ProjectVersion projectVersion = this.resourceBuilder.fetchVersion(versionId)
                .withPermission(ProjectPermission.VIEW, user).get();
        for (Change change : message.getChanges()) {
            projectAppEntity = updateProjectAppEntity(projectAppEntity, projectVersion, change);
        }

        if (message.isUpdateLayout()) {
            Map<UUID, LayoutPosition> defaultDocumentLayout = this.serviceProvider
                .getArtifactPositionService().retrieveDocumentLayout(projectVersion, null);
            projectAppEntity.setLayout(defaultDocumentLayout);
        }
        return projectAppEntity;
    }

    private ProjectAppEntity updateProjectAppEntity(ProjectAppEntity projectAppEntity,
                                                    ProjectVersion projectVersion,
                                                    Change change) {
        Project project = projectVersion.getProject();
        List<UUID> entityIds = change.getEntityIds();
        SafaUser user = serviceProvider.getSafaUserService().getCurrentUser();
        switch (change.getEntity()) {
            case PROJECT:
                projectAppEntity.setName(project.getName());
                projectAppEntity.setDescription(project.getDescription());
                break;
            case MEMBERS:
                List<ProjectMemberAppEntity> projectMemberAppEntities =
                    this.serviceProvider.getMemberService().getAppEntitiesByIds(projectVersion, user, entityIds);
                projectAppEntity.setMembers(projectMemberAppEntities);
                break;
            case TYPES:
                List<TypeAppEntity> artifactTypes = this.serviceProvider
                    .getTypeService()
                    .getAppEntities(projectVersion, user);
                projectAppEntity.setArtifactTypes(artifactTypes);
                break;
            case ARTIFACTS:
                List<ArtifactAppEntity> artifacts = this.serviceProvider
                    .getArtifactService()
                    .getAppEntitiesByIds(projectVersion, user, entityIds);
                projectAppEntity.setArtifacts(artifacts);
                break;
            case TRACES:
                List<TraceAppEntity> traces = this.serviceProvider
                    .getTraceService()
                    .getAppEntities(projectVersion, user, TraceAppEntity::isVisible);
                projectAppEntity.setTraces(traces);
                break;
            case DOCUMENT:
                List<DocumentAppEntity> documents = this.serviceProvider
                    .getDocumentService()
                    .getAppEntitiesByIds(projectVersion, user, entityIds);
                projectAppEntity.setDocuments(documents);
                break;
            case VERSION:
                return this.serviceProvider
                    .getProjectRetrievalService()
                    .getProjectAppEntity(projectVersion);
            case WARNINGS:
                Map<UUID, List<RuleName>> warnings = this.serviceProvider
                    .getWarningService()
                    .retrieveWarningsInProjectVersion(projectVersion);
                projectAppEntity.setWarnings(warnings);
                break;
            case TRACE_MATRICES:
                List<TraceMatrixAppEntity> traceMatrixAppEntities = this.serviceProvider
                    .getTraceMatrixService()
                    .getAppEntities(projectVersion, null);
                projectAppEntity.setTraceMatrices(traceMatrixAppEntities);
                break;
            default:
                throw new UnsupportedOperationException("Could not identify entity: " + change.getEntity());
        }
        return projectAppEntity;
    }
}
