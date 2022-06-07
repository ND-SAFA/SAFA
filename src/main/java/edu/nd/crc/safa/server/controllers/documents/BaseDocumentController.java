package edu.nd.crc.safa.server.controllers.documents;

import edu.nd.crc.safa.builders.ResourceBuilder;
import edu.nd.crc.safa.server.controllers.BaseController;
import edu.nd.crc.safa.server.repositories.documents.DocumentRepository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RestController;

/**
 * Used by DocumentController, DocumentArtifactController, and CurrentDocumentController
 * to generalize any repeated code.
 */
@RestController
public class BaseDocumentController extends BaseController {

    protected final DocumentRepository documentRepository;

    @Autowired
    public BaseDocumentController(ResourceBuilder resourceBuilder,
                                  DocumentRepository documentRepository) {
        super(resourceBuilder);
        this.documentRepository = documentRepository;
    }
}
