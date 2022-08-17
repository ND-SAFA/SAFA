package edu.nd.crc.safa.features.sync;

import java.util.List;
import java.util.Map;
import java.util.UUID;

import edu.nd.crc.safa.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.documents.entities.app.DocumentAppEntity;
import edu.nd.crc.safa.features.layout.entities.app.LayoutPosition;
import edu.nd.crc.safa.features.memberships.entities.app.ProjectMemberAppEntity;
import edu.nd.crc.safa.features.notifications.entities.Change;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.rules.parser.RuleName;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.types.TypeAppEntity;
import edu.nd.crc.safa.features.versions.entities.db.ProjectVersion;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;

/**
 * Responsible for
 */
public class SyncController extends BaseController {

    public SyncController(ResourceBuilder resourceBuilder,
                          ServiceProvider serviceProvider) {
        super(resourceBuilder, serviceProvider);
    }

    @GetMapping(AppRoutes.Sync.GET_CHANGES)
    public ProjectAppEntity getChanges(@PathVariable UUID versionId,
                                       EntityChangeMessage message) {
        ProjectAppEntity projectAppEntity = new ProjectAppEntity();
        ProjectVersion projectVersion = this.resourceBuilder.fetchVersion(versionId).withViewVersion();
        for (Change change : message.getChanges()) {
            projectAppEntity = updateProjectAppEntity(projectAppEntity, projectVersion, change);
        }

        if (message.isUpdateLayout()) {
            Map<String, LayoutPosition> defaultDocumentLayout = this.serviceProvider
                .getArtifactPositionService().retrieveDocumentLayout(projectVersion, null);
            projectAppEntity.setLayout(defaultDocumentLayout);
        }
        return projectAppEntity;
    }

    private ProjectAppEntity updateProjectAppEntity(ProjectAppEntity projectAppEntity,
                                                    ProjectVersion projectVersion,
                                                    Change change) {
        Project project = projectVersion.getProject();
        List<String> entityIds = change.getStringEntityIds();
        switch (change.getEntity()) {
            case PROJECT:
                projectAppEntity.setName(project.getName());
                projectAppEntity.setDescription(project.getDescription());
                break;
            case MEMBERS:
                List<ProjectMemberAppEntity> projectMemberAppEntities =
                    this.serviceProvider.getMemberService().getAppEntitiesByIds(projectVersion, entityIds);
                projectAppEntity.setMembers(projectMemberAppEntities);
                break;
            case TYPES:
                List<TypeAppEntity> artifactTypes = this.serviceProvider
                    .getTypeService()
                    .getAppEntities(projectVersion);
                projectAppEntity.setArtifactTypes(artifactTypes);
                break;
            case ARTIFACTS:
                List<ArtifactAppEntity> artifacts = this.serviceProvider
                    .getArtifactService()
                    .getAppEntitiesByIds(projectVersion, entityIds);
                projectAppEntity.setArtifacts(artifacts);
                break;
            case TRACES:
                List<TraceAppEntity> traces = this.serviceProvider
                    .getTraceService()
                    .retrieveTracesInProjectVersion(projectVersion, entityIds);
                projectAppEntity.setTraces(traces);
                break;
            case DOCUMENT:
                List<DocumentAppEntity> documents = this.serviceProvider
                    .getDocumentService()
                    .getAppEntitiesByIds(projectVersion, entityIds);
                projectAppEntity.setDocuments(documents);
                break;
            case VERSION:
                return this.serviceProvider
                    .getProjectRetrievalService()
                    .getProjectAppEntity(projectVersion);
            case WARNINGS:
                Map<String, List<RuleName>> warnings = this.serviceProvider
                    .getWarningService()
                    .retrieveWarningsInProjectVersion(projectVersion);
                projectAppEntity.setWarnings(warnings);
                break;
            default:
                throw new UnsupportedOperationException("Could not identify entity: " + change.getEntity());
        }
        return projectAppEntity;
    }
}
