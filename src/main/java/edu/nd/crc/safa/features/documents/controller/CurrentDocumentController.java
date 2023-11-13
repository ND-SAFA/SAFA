package edu.nd.crc.safa.features.documents.controller;

import java.util.UUID;

import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.documents.entities.db.Document;
import edu.nd.crc.safa.features.documents.services.CurrentDocumentService;
import edu.nd.crc.safa.features.permissions.entities.ProjectPermission;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

/**
 * Responsible for setting and clearing the current document a user is set on.
 */
@RestController
public class CurrentDocumentController extends BaseDocumentController {

    private final CurrentDocumentService currentDocumentService;

    @Autowired
    public CurrentDocumentController(ResourceBuilder resourceBuilder,
                                     ServiceProvider serviceProvider) {
        super(resourceBuilder, serviceProvider);
        this.currentDocumentService = serviceProvider.getCurrentDocumentService();
    }

    /**
     * Sets given document to be the default for the authenticated user.
     *
     * @param documentId The ID of the document to set as the default.
     */
    @PostMapping(AppRoutes.Documents.SET_CURRENT_DOCUMENT)
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void setCurrentDocument(@PathVariable UUID documentId) {
        SafaUser user = getCurrentUser();
        Document document = getResourceBuilder()
            .fetchDocument(documentId)
            .withPermission(ProjectPermission.VIEW, user)
            .get();
        this.currentDocumentService.setCurrentDocumentForCurrentUser(document);
    }

    /**
     * Removes default document for authenticated user.
     */
    @DeleteMapping(AppRoutes.Documents.CLEAR_CURRENT_DOCUMENT)
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void clearCurrentDocument() {
        this.currentDocumentService.clearCurrentDocumentForCurrentUser();
    }
}
