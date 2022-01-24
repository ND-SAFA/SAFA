package edu.nd.crc.safa.server.controllers;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.api.ServerResponse;
import edu.nd.crc.safa.server.entities.db.ArtifactType;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.TraceMatrix;
import edu.nd.crc.safa.server.repositories.ArtifactTypeRepository;
import edu.nd.crc.safa.server.repositories.ProjectRepository;
import edu.nd.crc.safa.server.repositories.ProjectVersionRepository;
import edu.nd.crc.safa.server.repositories.TraceMatrixRepository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * Provides endpoints for retrieving and creating new trace link matrices.
 */
@RestController
public class TraceMatrixController extends BaseController {

    TraceMatrixRepository traceMatrixRepository;
    ArtifactTypeRepository artifactTypeRepository;

    @Autowired
    public TraceMatrixController(ProjectRepository projectRepository,
                                 ProjectVersionRepository projectVersionRepository,
                                 ResourceBuilder resourceBuilder,
                                 TraceMatrixRepository traceMatrixRepository,
                                 ArtifactTypeRepository artifactTypeRepository) {
        super(projectRepository, projectVersionRepository, resourceBuilder);
        this.traceMatrixRepository = traceMatrixRepository;
        this.artifactTypeRepository = artifactTypeRepository;
    }

    /**
     * Returns list of trace matrices in a specified project.
     *
     * @param projectId UUID of project whose matrices are returned.
     * @return List of project matrices defined in project.
     * @throws SafaError Throws error if project with ID is not found.
     */
    @GetMapping(AppRoutes.Projects.getTraceMatrices)
    public ServerResponse getVersions(@PathVariable UUID projectId) throws SafaError {
        Project project = this.resourceBuilder.fetchProject(projectId).withViewProject();
        List<TraceMatrix> projectTraceMatrices = traceMatrixRepository.findByProject(project);
        return new ServerResponse(projectTraceMatrices);
    }

    /**
     * Creates a new trace matrix between given artifact types names in
     * specified project.
     *
     * @param projectId          UUID of project whose versions are returned.
     * @param sourceArtifactName The name of the source artifact type.
     * @param targetArtifactName The name of the target artifact type.
     * @throws SafaError Throws error if project with ID is not found.
     */
    @PostMapping(AppRoutes.Projects.createTraceMatrix)
    public void createTraceMatrix(@PathVariable UUID projectId,
                                  @PathVariable String sourceArtifactName,
                                  @PathVariable String targetArtifactName) throws SafaError {
        Project project = this.resourceBuilder.fetchProject(projectId).withViewProject();
        Optional<TraceMatrix> traceMatrixQuery = traceMatrixRepository.queryForMatrixInProject(project,
            sourceArtifactName, targetArtifactName);
        if (traceMatrixQuery.isPresent()) {
            String error = String.format("Trace matrix already exists between %s and %s.",
                sourceArtifactName,
                targetArtifactName);
            throw new SafaError(error);
        }

        ArtifactType sourceArtifactType = getArtifactType(project, sourceArtifactName);
        ArtifactType targetArtifactType = getArtifactType(project, targetArtifactName);
        TraceMatrix traceMatrix = new TraceMatrix(project, sourceArtifactType, targetArtifactType);
        this.traceMatrixRepository.save(traceMatrix);
    }

    private ArtifactType getArtifactType(Project project, String artifactTypeName) throws SafaError {
        Optional<ArtifactType> artifactTypeQuery = this.artifactTypeRepository.findByProjectAndNameIgnoreCase(project,
            artifactTypeName);
        if (artifactTypeQuery.isEmpty()) {
            throw new SafaError("Could not find artifact type with name: " + artifactTypeName);
        }
        return artifactTypeQuery.get();
    }
}
