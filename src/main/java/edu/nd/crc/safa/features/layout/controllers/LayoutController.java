package edu.nd.crc.safa.features.layout.controllers;

import java.util.Map;
import java.util.UUID;

import edu.nd.crc.safa.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.documents.entities.db.Document;
import edu.nd.crc.safa.features.layout.entities.app.LayoutPosition;
import edu.nd.crc.safa.features.versions.entities.db.ProjectVersion;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;

/**
 * Responsible for retrieving a project layouts.
 */
public class LayoutController extends BaseController {
    final String NOT_IMPLEMENTED = "Endpoint is under construction";

    @Autowired
    public LayoutController(ResourceBuilder resourceBuilder, ServiceProvider serviceProvider) {
        super(resourceBuilder, serviceProvider);
    }

    /**
     * Returns layout of document in specified version.
     *
     * @param versionId  ID of version for layout.
     * @param documentId ID of document whose layout.
     * @return Map of artifact IDs to their position in document.
     */
    @GetMapping(AppRoutes.Layout.DOCUMENT_LAYOUT)
    public Map<String, LayoutPosition> getDocumentLayout(UUID versionId,
                                                         UUID documentId) {
        ProjectVersion projectVersion = this.resourceBuilder.fetchVersion(versionId).withViewVersion();
        Document document = this.serviceProvider.getDocumentService().getDocumentById(documentId);
        return this.serviceProvider.getArtifactPositionService().retrieveDocumentLayout(projectVersion,
            document.getDocumentId());
    }

    /**
     * Return layout of default project document.
     *
     * @param versionId ID of project version whose layout is returned.
     * @return Map of artifact IDs to position in default document.
     */
    @GetMapping(AppRoutes.Layout.VERSION_LAYOUT)
    public Map<String, LayoutPosition> getVersionLayout(UUID versionId) {
        ProjectVersion projectVersion = this.resourceBuilder.fetchVersion(versionId).withViewVersion();

        return this.serviceProvider.getArtifactPositionService().retrieveDocumentLayout(projectVersion,
            null);
    }
}
