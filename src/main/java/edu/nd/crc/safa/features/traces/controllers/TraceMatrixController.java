package edu.nd.crc.safa.features.traces.controllers;

import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.permissions.entities.ProjectPermission;
import edu.nd.crc.safa.features.projects.entities.app.SafaItemNotFoundError;
import edu.nd.crc.safa.features.traces.entities.app.TraceMatrixAppEntity;
import edu.nd.crc.safa.features.traces.entities.db.TraceMatrixEntry;
import edu.nd.crc.safa.features.traces.services.TraceMatrixService;
import edu.nd.crc.safa.features.types.entities.db.ArtifactType;
import edu.nd.crc.safa.features.types.services.TypeService;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class TraceMatrixController extends BaseController {

    private final TraceMatrixService traceMatrixService;
    private final TypeService typeService;

    @Autowired
    public TraceMatrixController(ResourceBuilder resourceBuilder, ServiceProvider serviceProvider,
                                 TraceMatrixService traceMatrixService, TypeService typeService) {
        super(resourceBuilder, serviceProvider);
        this.traceMatrixService = traceMatrixService;
        this.typeService = typeService;
    }

    @PostMapping(AppRoutes.TraceMatrix.BY_SOURCE_AND_TARGET_TYPES)
    public TraceMatrixAppEntity createNewTraceMatrixEntry(@PathVariable UUID projectVersionId,
                                                          @PathVariable String sourceTypeName,
                                                          @PathVariable String targetTypeName) {
        SafaUser user = getServiceProvider().getSafaUserService().getCurrentUser();
        ProjectVersion projectVersion = getResourceBuilder().fetchVersion(projectVersionId)
                .withPermission(ProjectPermission.EDIT_DATA, user).get();
        ArtifactType sourceType = typeService.getArtifactType(projectVersion.getProject(), sourceTypeName);
        ArtifactType targetType = typeService.getArtifactType(projectVersion.getProject(), targetTypeName);
        TraceMatrixEntry newEntry = traceMatrixService.createEntry(projectVersion, sourceType, targetType);
        return new TraceMatrixAppEntity(newEntry);
    }

    @DeleteMapping(AppRoutes.TraceMatrix.BY_SOURCE_AND_TARGET_TYPES)
    public void deleteTraceMatrixEntry(@PathVariable UUID projectVersionId,
                                                       @PathVariable String sourceTypeName,
                                                       @PathVariable String targetTypeName) {
        SafaUser user = getServiceProvider().getSafaUserService().getCurrentUser();
        ProjectVersion projectVersion = getResourceBuilder().fetchVersion(projectVersionId)
                .withPermission(ProjectPermission.EDIT_DATA, user).get();
        ArtifactType sourceType = typeService.getArtifactType(projectVersion.getProject(), sourceTypeName);
        ArtifactType targetType = typeService.getArtifactType(projectVersion.getProject(), targetTypeName);
        Optional<TraceMatrixEntry> entryOptional = traceMatrixService.getEntry(projectVersion, sourceType, targetType);
        TraceMatrixEntry entry = entryOptional.orElseThrow(this::createMissingEntryException);
        traceMatrixService.delete(entry);
    }

    @DeleteMapping(AppRoutes.TraceMatrix.BY_ID)
    public void deleteTraceMatrixEntry(@PathVariable UUID projectVersionId, @PathVariable UUID traceMatrixId) {
        SafaUser user = getServiceProvider().getSafaUserService().getCurrentUser();
        ProjectVersion projectVersion = getResourceBuilder().fetchVersion(projectVersionId)
                .withPermission(ProjectPermission.EDIT_DATA, user).get();
        Optional<TraceMatrixEntry> entryOptional = traceMatrixService.getEntry(traceMatrixId);
        TraceMatrixEntry entry = entryOptional.orElseThrow(this::createMissingEntryException);

        if (!entry.getProjectVersion().getVersionId().equals(projectVersion.getVersionId())) {
            throw createMissingEntryException();
        }

        traceMatrixService.delete(entry);
    }

    private SafaItemNotFoundError createMissingEntryException() {
        return new SafaItemNotFoundError("No entry matching the specified parameters found");
    }
}
