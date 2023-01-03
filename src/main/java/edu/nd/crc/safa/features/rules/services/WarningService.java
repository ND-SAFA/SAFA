package edu.nd.crc.safa.features.rules.services;

import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.artifacts.entities.db.versions.ArtifactVersion;
import edu.nd.crc.safa.features.artifacts.repositories.ArtifactVersionRepository;
import edu.nd.crc.safa.features.rules.parser.RuleName;
import edu.nd.crc.safa.features.traces.entities.db.ApprovalStatus;
import edu.nd.crc.safa.features.traces.entities.db.TraceLink;
import edu.nd.crc.safa.features.traces.entities.db.TraceLinkVersion;
import edu.nd.crc.safa.features.traces.repositories.TraceLinkVersionRepository;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

@AllArgsConstructor
@Service
public class WarningService {

    private final ArtifactVersionRepository artifactVersionRepository;
    private final TraceLinkVersionRepository traceLinkVersionRepository;
    private final RuleService ruleService;

    /**
     * Returns mapping of artifact name to the list of violations it is inhibiting.
     *
     * @param projectVersion - Finds violations in artifact tree at time of this version
     * @return A mapping of  artifact name's to their resulting violations
     */
    public Map<UUID, List<RuleName>> retrieveWarningsInProjectVersion(ProjectVersion projectVersion) {
        List<ArtifactVersion> artifacts = this.artifactVersionRepository
            .retrieveVersionEntitiesByProjectVersion(projectVersion);
        List<TraceLink> traceLinks =
            this.traceLinkVersionRepository
                .retrieveVersionEntitiesByProjectVersion(projectVersion)
                .stream()
                .filter(t -> t.getApprovalStatus() == ApprovalStatus.APPROVED)
                .map(TraceLinkVersion::getTraceLink)
                .collect(Collectors.toList());
        return this.ruleService.generateWarningsOnEntities(projectVersion.getProject(),
            artifacts, traceLinks);
    }
}
