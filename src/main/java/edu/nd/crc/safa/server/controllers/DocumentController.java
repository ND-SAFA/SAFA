package edu.nd.crc.safa.server.controllers;

import java.util.UUID;
import javax.validation.Valid;

import edu.nd.crc.safa.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.api.ServerResponse;
import edu.nd.crc.safa.server.entities.db.Document;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.repositories.DocumentRepository;
import edu.nd.crc.safa.server.repositories.ProjectRepository;
import edu.nd.crc.safa.server.repositories.ProjectVersionRepository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

/**
 * Provides CRUD operations for Document entity.
 */
@RestController
public class DocumentController extends BaseController {

    private final DocumentRepository documentRepository;

    @Autowired
    public DocumentController(ProjectRepository projectRepository,
                              ProjectVersionRepository projectVersionRepository,
                              ResourceBuilder resourceBuilder,
                              DocumentRepository documentRepository) {
        super(projectRepository, projectVersionRepository, resourceBuilder);
        this.documentRepository = documentRepository;
    }

    /**
     * Persists given document object as a new document a part of the specified project.
     *
     * @param document The entity containing name, description, and type of document to be created.
     * @throws SafaError Throws error if authorized user does not have edit permissions.
     */
    @PostMapping(AppRoutes.Projects.createNewDocument)
    @ResponseStatus(HttpStatus.CREATED)
    public ServerResponse createNewDocument(@PathVariable UUID projectId,
                                            @RequestBody @Valid Document document) throws SafaError {
        Project project = resourceBuilder.fetchProject(projectId).withEditProject();
        document.setProject(project);
        this.documentRepository.save(document);
        return new ServerResponse(document);
    }
}
