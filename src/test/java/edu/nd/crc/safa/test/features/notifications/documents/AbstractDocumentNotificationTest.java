package edu.nd.crc.safa.test.features.notifications.documents;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.features.documents.entities.app.DocumentAppEntity;
import edu.nd.crc.safa.test.features.notifications.AbstractNotificationTest;

import org.json.JSONObject;

public abstract class AbstractDocumentNotificationTest extends AbstractNotificationTest {
    /**
     * ID of document being manipulated.
     */
    protected UUID documentId;
    /**
     * Instance of constants, including document being manipulated
     */
    protected DocumentConstants documentConstants = new DocumentConstants();

    protected void createDocumentAndVerifyMessage() throws Exception {
        this.createDocument();

        // TODO https://www.notion.so/nd-safa/BE-Tests-Occasionally-Fail-9500d5c1f1d84a76acf429ee3653bb86
        /*
        this.rootBuilder.notifications((s, n) -> n.getEntityMessage(s.getIUser("sharee-user"))).consume(m -> {
            this.messageVerificationService.verifyDocumentChange(
                m,
                this.documentId,
                NotificationAction.UPDATE
            );
            this.messageVerificationService.verifyUpdateLayout(m, false);
        });
         */
    }

    protected void createDocument() throws Exception {
        DocumentAppEntity documentAppEntity = this.documentConstants.document;
        JSONObject response = this.creationService.createOrUpdateDocument(
            this.projectVersion,
            documentAppEntity);
        this.documentId = documentAppEntity.getDocumentId();
    }

    public static class DocumentConstants {
        private final String name = "document-name";
        private final String description = "document-description";
        private final List<UUID> artifactIds = new ArrayList<>();
        public final DocumentAppEntity document = new DocumentAppEntity(
            null,
            name,
            description,
            artifactIds,
            new HashMap<>()
        );
    }
}
