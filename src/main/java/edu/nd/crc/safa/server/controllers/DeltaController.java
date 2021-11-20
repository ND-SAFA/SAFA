package edu.nd.crc.safa.server.controllers;

import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.config.Routes;
import edu.nd.crc.safa.server.entities.api.ServerError;
import edu.nd.crc.safa.server.entities.api.ServerResponse;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.repositories.ProjectRepository;
import edu.nd.crc.safa.server.repositories.ProjectVersionRepository;
import edu.nd.crc.safa.server.services.DeltaService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

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

    /**
     * Returns ProjectDelta response object indicating changes in artifacts between the two versions specified.
     *
     * @param baselineVersionId UUID indicating the baseline version.
     * @param targetVersionId   UUID of the target version to compare the baseline against.
     * @return ProjectDelta with artifacts that were added, removed, and modified between versions.
     * @throws ServerError Throws error if baseline or target version is not found.
     */
    @GetMapping(Routes.calculateProjectDelta)
    public ServerResponse calculateProjectDelta(@PathVariable UUID baselineVersionId,
                                                @PathVariable UUID targetVersionId) throws ServerError {

        Optional<ProjectVersion> sourceQuery = this.projectVersionRepository.findById(baselineVersionId);
        if (!sourceQuery.isPresent()) {
            throw new ServerError("Source version with id not found: " + baselineVersionId);
        }
        Optional<ProjectVersion> targetQuery = this.projectVersionRepository.findById(targetVersionId);
        if (!targetQuery.isPresent()) {
            throw new ServerError("Target version with id not found: " + targetVersionId);
        }
        return new ServerResponse(this.deltaService.calculateProjectDelta(sourceQuery.get(), targetQuery.get()));
    }
}
