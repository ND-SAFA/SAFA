package edu.nd.crc.safa.server.repositories.impl;

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
import edu.nd.crc.safa.server.repositories.ArtifactRepository;
import edu.nd.crc.safa.server.repositories.TraceLinkRepository;
import edu.nd.crc.safa.server.repositories.TraceLinkVersionRepository;
import edu.nd.crc.safa.server.repositories.TraceMatrixRepository;
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
    public List<TraceLinkVersion> getEntitiesInProject(Project project) {
        return traceLinkVersionRepository.findByProjectVersionProject(project);
    }

    @Override
    public List<TraceLinkVersion> findByEntity(TraceLink traceLink) {
        return traceLinkVersionRepository.findByTraceLink(traceLink);
    }

    @Override
    public TraceLinkVersion createEntityVersionWithModification(ProjectVersion projectVersion,
                                                                ModificationType modificationType,
                                                                TraceLink traceLink,
                                                                TraceAppEntity traceAppEntity) {
        switch (modificationType) {
            case ADDED:
                return new TraceLinkVersion(projectVersion,
                    ModificationType.ADDED,
                    traceLink,
                    traceAppEntity);
            case REMOVED:
                return new TraceLinkVersion(projectVersion,
                    ModificationType.REMOVED,
                    traceLink);
            default:
                throw new RuntimeException("Missing case in delta service.");
        }
    }

    @Override
    public TraceLink findOrCreateBaseEntityFromAppEntity(ProjectVersion projectVersion,
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

    private Artifact assertAndFindArtifact(Project project, String artifactName) throws SafaError {
        Optional<Artifact> sourceArtifactOptional = this.artifactRepository.findByProjectAndName(project, artifactName);
        if (sourceArtifactOptional.isPresent()) {
            return sourceArtifactOptional.get();
        }
        throw new SafaError("Could not find trace link artifact:" + artifactName);
    }

    @Override
    public void saveOrOverrideVersionEntity(ProjectVersion projectVersion,
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
    public List<TraceLink> getBaseEntitiesInProject(Project project) {
        return this.traceLinkRepository.getLinksInProject(project);
    }

    @Override
    public TraceLinkVersion createRemovedVersionEntity(ProjectVersion projectVersion,
                                                       TraceLink traceLink) {
        return new TraceLinkVersion(
            projectVersion,
            ModificationType.REMOVED,
            traceLink
        );
    }

    @Override
    public Optional<TraceLink> findBaseEntityByName(Project project, String name) {
        return this.traceLinkRepository.findById(UUID.fromString(name));
    }

    @Override
    public List<TraceLinkVersion> findVersionEntitiesWithBaseEntity(TraceLink baseEntity) {
        return this.traceLinkVersionRepository.findByTraceLink(baseEntity);
    }

    @Override
    public TraceAppEntity createAppFromVersion(TraceLinkVersion versionEntity) {
        return new TraceAppEntity(versionEntity);
    }
}
