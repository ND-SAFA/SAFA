package edu.nd.crc.safa.features.layout.controllers;

import java.util.Map;
import java.util.UUID;

import edu.nd.crc.safa.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.layout.entities.app.LayoutPosition;

import org.apache.commons.lang3.NotImplementedException;
import org.springframework.web.bind.annotation.GetMapping;

/**
 * Responsible for retrieving a project layouts.
 */
public class LayoutController extends BaseController {
    final String NOT_IMPLEMENTED = "Endpoint is under construction";

    public LayoutController(ResourceBuilder resourceBuilder) {
        super(resourceBuilder);
    }

    /**
     * Returns layout of document in specified version.
     *
     * @param versionId  ID of version for layout.
     * @param documentId ID of document whose layout.
     * @return Map of artifact IDs to their position in document.
     */
    @GetMapping(AppRoutes.Layout.GET_DOCUMENT_LAYOUT)
    public Map<String, LayoutPosition> getDocumentLayout(UUID versionId,
                                                         UUID documentId) {
        throw new NotImplementedException(NOT_IMPLEMENTED);
    }

    /**
     * Return layout of default project document.
     *
     * @param projectId ID of project.
     * @return Map of artifact IDs to position in default document.
     */
    @GetMapping(AppRoutes.Layout.GET_PROJECT_LAYOUT)
    public Map<String, LayoutPosition> getProjectLayout(UUID projectId) {
        throw new NotImplementedException(NOT_IMPLEMENTED);
    }
}
