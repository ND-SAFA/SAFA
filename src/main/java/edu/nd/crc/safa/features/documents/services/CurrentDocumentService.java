package edu.nd.crc.safa.features.documents.services;

import java.util.Optional;

import edu.nd.crc.safa.features.documents.entities.db.CurrentDocument;
import edu.nd.crc.safa.features.documents.entities.db.Document;
import edu.nd.crc.safa.features.documents.repositories.CurrentDocumentRepository;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.users.services.SafaUserService;

import jakarta.annotation.Nullable;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

/**
 * Responsible for setting, clearing, and retrieving the last document
 * a user was on.
 */
@Service
@AllArgsConstructor
public class CurrentDocumentService {
    private final CurrentDocumentRepository currentDocumentRepository;
    private final SafaUserService safaUserService;

    /**
     * Creates or updates the user's current document preferences to point to given document.
     *
     * @param document The document that should be set as the user's preference.
     */
    public void setCurrentDocumentForCurrentUser(Document document) {
        SafaUser user = safaUserService.getCurrentUser();
        Optional<CurrentDocument> currentDocumentOptional = this.currentDocumentRepository.findByUser(user);

        CurrentDocument currentDocument;
        if (currentDocumentOptional.isPresent()) {
            currentDocument = currentDocumentOptional.get();
        } else {
            currentDocument = new CurrentDocument();
            currentDocument.setUser(user);
        }

        currentDocument.setDocument(document);
        this.currentDocumentRepository.save(currentDocument);
    }

    /**
     * Deletes the current document for the current user
     */
    public void clearCurrentDocumentForCurrentUser() {
        SafaUser user = safaUserService.getCurrentUser();
        this.currentDocumentRepository
            .findByUser(user)
            .ifPresent(this.currentDocumentRepository::delete);
    }

    /**
     * Returns the id of the last document the user was on, or null if
     * they were on the default document.
     *
     * @param user The user to get the document for
     * @return String or Null
     */
    @Nullable
    public String getCurrentDocumentId(SafaUser user) {
        Optional<CurrentDocument> currentDocumentOptional = this.currentDocumentRepository.findByUser(user);
        return currentDocumentOptional
            .map(currentDocument -> currentDocument.getDocument().getDocumentId().toString())
            .orElse(null);
    }

    /**
     * Returns the id of the last document the user was on, or null if
     * they were on the default document.
     *
     * @return String or Null
     */
    @Nullable
    public String getCurrentDocumentIdForCurrentUser() {
        return getCurrentDocumentId(this.safaUserService.getCurrentUser());
    }
}
