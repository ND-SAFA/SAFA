package edu.nd.crc.safa.features.documents.controller;

import java.util.UUID;

import edu.nd.crc.safa.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.documents.entities.db.Document;
import edu.nd.crc.safa.features.documents.repositories.DocumentRepository;
import edu.nd.crc.safa.features.documents.services.CurrentDocumentService;

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
                                     DocumentRepository documentRepository,
                                     CurrentDocumentService currentDocumentService) {
        super(resourceBuilder, documentRepository);
        this.currentDocumentService = currentDocumentService;
    }

    /**
     * Sets given document to be the default for the authenticated user.
     *
     * @param documentId The ID of the document to set as the default.
     */
    @PostMapping(AppRoutes.Documents.SET_CURRENT_DOCUMENT)
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void setCurrentDocument(@PathVariable UUID documentId) {
        Document document = getDocumentById(this.documentRepository, documentId);
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
