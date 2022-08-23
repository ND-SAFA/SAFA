package edu.nd.crc.safa.features.traces.repositories;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.db.Artifact;
import edu.nd.crc.safa.features.artifacts.repositories.ArtifactRepository;
import edu.nd.crc.safa.features.commits.repositories.GenericVersionRepository;
import edu.nd.crc.safa.features.delta.entities.db.ModificationType;
import edu.nd.crc.safa.features.matrices.services.TraceMatrixService;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.projects.entities.db.ProjectEntity;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.traces.entities.db.ApprovalStatus;
import edu.nd.crc.safa.features.traces.entities.db.TraceLink;
import edu.nd.crc.safa.features.traces.entities.db.TraceLinkVersion;
import edu.nd.crc.safa.features.traces.entities.db.TraceType;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

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
    public TraceLinkVersion save(TraceLinkVersion traceLinkVersion) {
        return this.traceLinkVersionRepository.save(traceLinkVersion);
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
                .withManualTraceType()
                .withApprovalStatus(ApprovalStatus.DECLINED);
        }
        return TraceLinkVersion.createLinkWithVersionAndModificationAndTraceAppEntity(projectVersion,
            modificationType,
            traceLink,
            traceAppEntity);
    }

    @Override
    protected ProjectEntity getProjectActivity() {
        return ProjectEntity.TRACES;
    }

    @Override
    public TraceLink createOrUpdateRelatedEntities(ProjectVersion projectVersion,
                                                   TraceAppEntity newTrace) throws SafaError {
        Project project = projectVersion.getProject();

        Optional<TraceLink> traceLinkOptional = this.traceLinkRepository
            .getByProjectAndSourceAndTarget(
                project,
                newTrace.getSourceName(),
                newTrace.getTargetName());
        TraceLink traceLink = traceLinkOptional.isEmpty() ? createNewTraceLink(newTrace, project) :
            traceLinkOptional.get();
        assertNotOverridingManualLink(projectVersion, newTrace, traceLink);

        return traceLink;
    }

    @Override
    public Optional<TraceLink> findBaseEntityById(String baseEntityId) {
        return this.traceLinkRepository.findById(UUID.fromString(baseEntityId));
    }

    @Override
    public Optional<TraceLinkVersion> findExistingVersionEntity(TraceLinkVersion traceLinkVersion) {
        return this.traceLinkVersionRepository
            .findByProjectVersionAndTraceLink(traceLinkVersion.getProjectVersion(), traceLinkVersion.getTraceLink());
    }

    @Override
    public List<TraceLink> retrieveBaseEntitiesByProject(Project project) {
        return this.traceLinkRepository.getLinksInProject(project);
    }

    @Override
    public List<TraceLinkVersion> retrieveVersionEntitiesByProject(Project project) {
        return traceLinkVersionRepository.findByProjectVersionProject(project);
    }

    @Override
    public List<TraceLinkVersion> retrieveVersionEntitiesByBaseEntity(TraceLink traceLink) {
        return traceLinkVersionRepository.findByTraceLink(traceLink);
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

    private TraceLink createNewTraceLink(TraceAppEntity newTrace, Project project) throws SafaError {
        Optional<TraceLink> traceLinkOptional = this.traceLinkRepository
            .findBySourceArtifactProjectAndSourceArtifactNameAndTargetArtifactName(project,
                newTrace.getSourceName(),
                newTrace.getTargetName());
        if (traceLinkOptional.isPresent()) {
            return traceLinkOptional.get();
        }

        Artifact sourceArtifact = assertAndFindArtifact(project, newTrace.getSourceName());
        Artifact targetArtifact = assertAndFindArtifact(project, newTrace.getTargetName());
        TraceLink traceLink = new TraceLink(sourceArtifact, targetArtifact);
        traceMatrixService.assertOrCreateTraceMatrix(project,
            sourceArtifact.getType(),
            targetArtifact.getType());
        this.traceLinkRepository.save(traceLink);

        return traceLink;
    }

    private void assertNotOverridingManualLink(ProjectVersion projectVersion,
                                               TraceAppEntity newTrace,
                                               TraceLink traceLink) throws SafaError {
        Optional<TraceLinkVersion> existingLinkOptional =
            this.traceLinkVersionRepository.findByProjectVersionAndTraceLink(projectVersion,
                traceLink);
        if (existingLinkOptional.isPresent()) {
            TraceLinkVersion previousTraceLinkVersion = existingLinkOptional.get();
            if (previousTraceLinkVersion.getTraceType() == TraceType.MANUAL
                && newTrace.getTraceType() != TraceType.MANUAL) {
                throw new SafaError("Generated link cannot override manual one.");
            }
        }
    }

    private Artifact assertAndFindArtifact(Project project, String artifactName) throws SafaError {
        Optional<Artifact> sourceArtifactOptional = this.artifactRepository.findByProjectAndName(project, artifactName);
        if (sourceArtifactOptional.isPresent()) {
            return sourceArtifactOptional.get();
        }
        throw new SafaError("Could not find trace link artifact:" + artifactName);
    }
}
