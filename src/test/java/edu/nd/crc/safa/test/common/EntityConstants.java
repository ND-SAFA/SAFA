package edu.nd.crc.safa.test.common;

import java.util.HashMap;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.documents.entities.db.DocumentType;

public class EntityConstants {
    public static class DocumentConstants {
        public final String name = "test-document";
        public final String description = "this is a description";
        public final DocumentType type = DocumentType.ARTIFACT_TREE;
    }

    public static class ArtifactConstants {
        public final String name = "RE-10";
        public final String summary = "summary";
        public final String body = "content";
        public final String type = "requirement";
        public final DocumentType documentType = DocumentType.ARTIFACT_TREE;
        public final ArtifactAppEntity artifact = new ArtifactAppEntity(
            null,
            type,
            name,
            summary,
            body,
            documentType,
            new HashMap<>()
        );
    }
}
