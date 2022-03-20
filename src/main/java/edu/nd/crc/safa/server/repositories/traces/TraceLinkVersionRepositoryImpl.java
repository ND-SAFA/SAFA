package edu.nd.crc.safa.server.repositories.traces;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.app.TraceAppEntity;
import edu.nd.crc.safa.server.entities.db.Artifact;
import edu.nd.crc.safa.server.entities.db.ModificationType;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.entities.db.TraceLink;
import edu.nd.crc.safa.server.entities.db.TraceLinkVersion;
import edu.nd.crc.safa.server.entities.db.TraceType;
import edu.nd.crc.safa.server.repositories.GenericVersionRepository;
import edu.nd.crc.safa.server.repositories.artifacts.ArtifactRepository;
import edu.nd.crc.safa.server.services.TraceMatrixService;

import org.springframework.beans.factory.annotation.Autowired;

/**
 * Implements the custom logic for versioning trace links.
 */
public class TraceLinkVersionRepositoryImpl
    extends GenericVersionRepository<TraceLink, TraceLinkVersion, TraceAppEntity> {

    @Autowired
    TraceLinkVersionRepository traceLinkVersionRepository;
    @Autowired
    TraceLinkRepository traceLinkRepository;
    @Autowired
    ArtifactRepository artifactRepository;
    @Autowired
    TraceMatrixRepository traceMatrixRepository;
    @Autowired
    TraceMatrixService traceMatrixService;

    @Override
    public List<TraceLinkVersion> retrieveVersionEntitiesByProject(Project project) {
        return traceLinkVersionRepository.findByProjectVersionProject(project);
    }

    @Override
    public List<TraceLinkVersion> retrieveVersionEntitiesByBaseEntity(TraceLink traceLink) {
        return traceLinkVersionRepository.findByTraceLink(traceLink);
    }

    @Override
    public TraceLinkVersion instantiateVersionEntityWithModification(ProjectVersion projectVersion,
                                                                     ModificationType modificationType,
                                                                     TraceLink traceLink,
                                                                     TraceAppEntity traceAppEntity) {
        if (modificationType == ModificationType.REMOVED || traceAppEntity == null) {
            return (new TraceLinkVersion())
                .withProjectVersion(projectVersion)
                .withTraceLink(traceLink)
                .withModificationType(ModificationType.REMOVED)
                .withManualTraceType();
        }
        return TraceLinkVersion.createLinkWithVersionAndModificationAndTraceAppEntity(projectVersion,
            modificationType,
            traceLink,
            traceAppEntity);
    }

    @Override
    public TraceLink createOrUpdateAppEntity(ProjectVersion projectVersion,
                                             TraceAppEntity trace) throws SafaError {
        Project project = projectVersion.getProject();

        TraceLink traceLink;
        Optional<TraceLink> traceLinkOptional = this.traceLinkRepository
            .getByProjectAndSourceAndTarget(
                project,
                trace.sourceName,
                trace.targetName);
        if (traceLinkOptional.isEmpty()) {
            Artifact sourceArtifact = assertAndFindArtifact(project, trace.sourceName);
            Artifact targetArtifact = assertAndFindArtifact(project, trace.targetName);
            traceLink = new TraceLink(sourceArtifact, targetArtifact);
            traceMatrixService.verifyOrCreateTraceMatrix(project,
                sourceArtifact.getType(),
                targetArtifact.getType());
            this.traceLinkRepository.save(traceLink);
        } else {
            traceLink = traceLinkOptional.get();
        }
        Optional<TraceLinkVersion> traceLinkVersionOptional =
            this.traceLinkVersionRepository.findByProjectVersionAndTraceLink(projectVersion,
                traceLink);
        if (traceLinkVersionOptional.isPresent()) {
            TraceLinkVersion tv = traceLinkVersionOptional.get();
            if (tv.getTraceType() == TraceType.MANUAL && trace.traceType != TraceType.MANUAL) {
                throw new SafaError("Generated link cannot override manual one.");
            }
        }

        return traceLink;
    }

    @Override
    public void createOrUpdateVersionEntity(ProjectVersion projectVersion,
                                            TraceLinkVersion traceLinkVersion) throws SafaError {
        try {
            this.traceLinkVersionRepository
                .findByProjectVersionAndTraceLink(projectVersion, traceLinkVersion.getTraceLink())
                .ifPresent((existingVersionEntity) -> {
                    traceLinkVersionRepository.delete(existingVersionEntity);
                });
            this.traceLinkVersionRepository.save(traceLinkVersion);
        } catch (Exception e) {
            String name = traceLinkVersion.getTraceLink().getTraceName();
            String error = String.format("An error occurred while saving trace links: %s", name);
            throw new SafaError(error, e);
        }
    }

    @Override
    public List<TraceLink> retrieveBaseEntitiesByProject(Project project) {
        return this.traceLinkRepository.getLinksInProject(project);
    }

    @Override
    public Optional<TraceLink> findBaseEntityById(String baseEntityId) {
        return this.traceLinkRepository.findById(UUID.fromString(baseEntityId));
    }

    @Override
    public TraceAppEntity retrieveAppEntityFromVersionEntity(TraceLinkVersion trace) {
        if (trace == null) {
            return null;
        }
        UUID traceLinkId = trace.getTraceLink().getTraceLinkId();
        Artifact sourceArtifact = trace.getTraceLink().getSourceArtifact();
        Artifact targetArtifact = trace.getTraceLink().getTargetArtifact();

        return new TraceAppEntity(
            traceLinkId != null ? traceLinkId.toString() : "",
            sourceArtifact.getName(),
            sourceArtifact.getArtifactId().toString(),
            targetArtifact.getName(),
            targetArtifact.getArtifactId().toString(),
            trace.getApprovalStatus(),
            trace.getScore(),
            trace.getTraceType()
        );
    }

    private Artifact assertAndFindArtifact(Project project, String artifactName) throws SafaError {
        Optional<Artifact> sourceArtifactOptional = this.artifactRepository.findByProjectAndName(project, artifactName);
        if (sourceArtifactOptional.isPresent()) {
            return sourceArtifactOptional.get();
        }
        throw new SafaError("Could not find trace link artifact:" + artifactName);
    }
}
