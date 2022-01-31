package edu.nd.crc.safa.server.controllers;

import java.util.Hashtable;
import java.util.List;
import java.util.Map;
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
import org.springframework.web.bind.annotation.DeleteMapping;
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
    public ServerResponse getTraceMatricesInProject(@PathVariable UUID projectId) throws SafaError {
        Project project = this.resourceBuilder.fetchProject(projectId).withViewProject();
        List<TraceMatrix> projectTraceMatrices = traceMatrixRepository.findByProject(project);
        Map<String, List<String>> traceLinkDirections = new Hashtable<>();
        for (TraceMatrix tm : projectTraceMatrices) {
            String sourceTypeName = tm.getSourceArtifactType().getName();
            String targetTypeName = tm.getTargetArtifactType().getName();
            if (traceLinkDirections.containsKey(sourceTypeName)) {
                traceLinkDirections.get(sourceTypeName).add(targetTypeName);
            } else {
                traceLinkDirections.put(sourceTypeName, List.of(targetTypeName));
            }
        }
        return new ServerResponse(traceLinkDirections);
    }

    /**
     * Creates a new trace matrix between given artifact types names in
     * specified project.
     *
     * @param projectId              UUID of project whose versions are returned.
     * @param sourceArtifactTypeName The name of the source artifact type.
     * @param targetArtifactTypeName The name of the target artifact type.
     * @throws SafaError Throws error if project with ID is not found.
     */
    @PostMapping(AppRoutes.Projects.createTraceMatrix)
    public void createTraceMatrix(@PathVariable UUID projectId,
                                  @PathVariable String sourceArtifactTypeName,
                                  @PathVariable String targetArtifactTypeName) throws SafaError {
        Project project = this.resourceBuilder.fetchProject(projectId).withViewProject();
        Optional<TraceMatrix> traceMatrixQuery = traceMatrixRepository.queryForMatrixInProject(project,
            sourceArtifactTypeName, targetArtifactTypeName);
        if (traceMatrixQuery.isPresent()) {
            String error = String.format("Trace matrix already exists between %s and %s.",
                sourceArtifactTypeName,
                targetArtifactTypeName);
            throw new SafaError(error);
        }

        ArtifactType sourceArtifactType = getArtifactType(project, sourceArtifactTypeName);
        ArtifactType targetArtifactType = getArtifactType(project, targetArtifactTypeName);
        TraceMatrix traceMatrix = new TraceMatrix(project, sourceArtifactType, targetArtifactType);
        this.traceMatrixRepository.save(traceMatrix);
    }

    /**
     * Deletes trace matrix with given id if user has edit permission on associated project.
     *
     * @param traceMatrixId The traceMatrixId uniquely identifying the matrix.
     * @throws SafaError Throws error if user does not have edit permissions on project.
     */
    @DeleteMapping(AppRoutes.Projects.deleteTraceMatrix)
    public void deleteTraceMatrix(@PathVariable UUID traceMatrixId) throws SafaError {
        Optional<TraceMatrix> traceMatrixOptional = this.traceMatrixRepository.findById(traceMatrixId);
        if (traceMatrixOptional.isPresent()) {
            TraceMatrix traceMatrixToDelete = traceMatrixOptional.get();
            this.resourceBuilder.setProject(traceMatrixToDelete.getProject()).withEditProject();
            this.traceMatrixRepository.delete(traceMatrixToDelete);
        }
    }

    private ArtifactType getArtifactType(Project project, String artifactTypeName) throws SafaError {
        Optional<ArtifactType> artifactTypeQuery = this.artifactTypeRepository.findByProjectAndNameIgnoreCase(project,
            artifactTypeName);
        if (artifactTypeQuery.isEmpty()) {
            throw new SafaError("Could not find artifact type: " + artifactTypeName);
        }
        return artifactTypeQuery.get();
    }
}
