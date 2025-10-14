package edu.nd.crc.safa.features.documents.controller;

import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.documents.repositories.DocumentRepository;

import lombok.AccessLevel;
import lombok.Getter;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RestController;

/**
 * Used by DocumentController, DocumentArtifactController, and CurrentDocumentController
 * to generalize any repeated code.
 */
@RestController
public class BaseDocumentController extends BaseController {

    @Getter(AccessLevel.PROTECTED)
    private final DocumentRepository documentRepository;

    @Autowired
    public BaseDocumentController(ResourceBuilder resourceBuilder,
                                  ServiceProvider serviceProvider) {
        super(resourceBuilder, serviceProvider);
        this.documentRepository = serviceProvider.getDocumentRepository();
    }
}
