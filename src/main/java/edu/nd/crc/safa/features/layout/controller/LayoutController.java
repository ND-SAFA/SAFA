package edu.nd.crc.safa.features.layout.controller;

import java.util.Map;
import java.util.UUID;

import edu.nd.crc.safa.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.documents.entities.db.Document;
import edu.nd.crc.safa.features.layout.entities.api.LayoutGenerationRequestDTO;
import edu.nd.crc.safa.features.layout.entities.api.LayoutGenerationResponseDTO;
import edu.nd.crc.safa.features.layout.entities.app.LayoutManager;
import edu.nd.crc.safa.features.layout.entities.app.LayoutPosition;
import edu.nd.crc.safa.features.notifications.builders.EntityChangeBuilder;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class LayoutController extends BaseController {
    public LayoutController(ResourceBuilder resourceBuilder, ServiceProvider serviceProvider) {
        super(resourceBuilder, serviceProvider);
    }

    @PostMapping(AppRoutes.Layout.REGENERATE_LAYOUT)
    public LayoutGenerationResponseDTO resetLayout(@PathVariable UUID versionId,
                                                   @RequestBody LayoutGenerationRequestDTO layoutGeneration) {
        ProjectVersion projectVersion = this.resourceBuilder.fetchVersion(versionId).withEditVersion();
        LayoutManager layoutManager = new LayoutManager(this.serviceProvider, projectVersion);
        EntityChangeBuilder notificationBuilder = EntityChangeBuilder.create(versionId);
        LayoutGenerationResponseDTO response = new LayoutGenerationResponseDTO();

        if (layoutGeneration.isDefaultDocument()) {
            Map<UUID, LayoutPosition> defaultDocumentLayout = layoutManager.generateDefaultDocumentLayout();
            response.setDefaultDocumentLayout(defaultDocumentLayout);
            notificationBuilder.withUpdateLayout();
        }

        for (UUID documentId : layoutGeneration.getDocumentIds()) {
            Document document = this.serviceProvider.getDocumentService().getDocumentById(documentId);
            Map<UUID, LayoutPosition> documentLayout = layoutManager.generateDocumentLayout(document);
            response.addDocumentLayout(documentId, documentLayout);
        }
        notificationBuilder.withDocumentUpdate(layoutGeneration.getDocumentIds());

        this.serviceProvider.getNotificationService().broadcastChange(notificationBuilder);
        return response;
    }
}
