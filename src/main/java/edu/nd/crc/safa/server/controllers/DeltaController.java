package edu.nd.crc.safa.server.controllers;

import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.repositories.ProjectRepository;
import edu.nd.crc.safa.server.repositories.ProjectVersionRepository;
import edu.nd.crc.safa.server.entities.api.ServerError;
import edu.nd.crc.safa.server.entities.api.ServerResponse;
import edu.nd.crc.safa.server.services.DeltaService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@CrossOrigin
@RestController
public class DeltaController extends BaseController {

    DeltaService deltaService;

    @Autowired
    public DeltaController(ProjectRepository projectRepository,
                           ProjectVersionRepository projectVersionRepository,
                           DeltaService deltaService) {
        super(projectRepository, projectVersionRepository);
        this.deltaService = deltaService;
    }

    @GetMapping("projects/delta/{sourceVersionId}/{targetVersionId}")
    public ServerResponse getVersionDelta(@PathVariable UUID sourceVersionId,
                                          @PathVariable UUID targetVersionId) throws ServerError {

        Optional<ProjectVersion> sourceQuery = this.projectVersionRepository.findById(sourceVersionId);
        if (!sourceQuery.isPresent()) {
            throw new ServerError("Source version with id not found: " + sourceVersionId);
        }
        Optional<ProjectVersion> targetQuery = this.projectVersionRepository.findById(targetVersionId);
        if (!targetQuery.isPresent()) {
            throw new ServerError("Target version with id not found: " + targetVersionId);
        }
        return new ServerResponse(this.deltaService.calculateProjectDelta(sourceQuery.get(), targetQuery.get()));
    }
}
