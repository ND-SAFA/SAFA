package edu.nd.crc.safa.server.services;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import edu.nd.crc.safa.server.entities.db.ArtifactVersion;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.entities.db.TraceLink;
import edu.nd.crc.safa.server.entities.db.TraceLinkVersion;
import edu.nd.crc.safa.server.entities.db.Warning;
import edu.nd.crc.safa.server.repositories.ArtifactVersionRepository;
import edu.nd.crc.safa.server.repositories.TraceLinkVersionRepository;
import edu.nd.crc.safa.server.repositories.WarningRepository;
import edu.nd.crc.safa.warnings.DefaultTreeRules;
import edu.nd.crc.safa.warnings.Rule;
import edu.nd.crc.safa.warnings.RuleName;
import edu.nd.crc.safa.warnings.TreeVerifier;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

/**
 * Responsible for generating project warnings for a given project version.
 */
@Service
public class WarningService {

    WarningRepository warningRepository;
    TraceLinkVersionRepository traceLinkVersionRepository;
    ArtifactVersionRepository artifactVersionRepository;

    @Autowired
    public WarningService(WarningRepository warningRepository,
                          TraceLinkVersionRepository traceLinkVersionRepository,
                          ArtifactVersionRepository artifactVersionRepository) {
        this.warningRepository = warningRepository;
        this.traceLinkVersionRepository = traceLinkVersionRepository;
        this.artifactVersionRepository = artifactVersionRepository;
    }

    /**
     * Returns mapping of artifact name to the list of violations it is inhibiting.
     *
     * @param projectVersion - Finds violations in artifact tree at time of this version
     * @return A mapping of  artifact name's to their resulting violations
     */
    public Map<String, List<RuleName>> findViolationsInArtifactTree(ProjectVersion projectVersion) {
        List<ArtifactVersion> artifacts = artifactVersionRepository.getEntityVersionsInProjectVersion(projectVersion);
        List<TraceLinkVersion> traceLinkVersions =
            this.traceLinkVersionRepository.getApprovedLinksInVersion(projectVersion);
        System.out.println("APPROVED LINKS:" + traceLinkVersions);
        List<TraceLink> traceLinks =
            traceLinkVersions.stream().map(TraceLinkVersion::getTraceLink).collect(Collectors.toList());
        return findViolationsInArtifactTree(projectVersion, artifacts, traceLinks);
    }

    public Map<String, List<RuleName>> findViolationsInArtifactTree(ProjectVersion projectVersion,
                                                                    List<ArtifactVersion> artifacts,
                                                                    List<TraceLink> traceLinks) {
        Project project = projectVersion.getProject();
        TreeVerifier verifier = new TreeVerifier();
        List<Rule> rulesToApply = new ArrayList<>();
        rulesToApply.addAll(DefaultTreeRules.getDefaultRules());
        rulesToApply.addAll(this.getProjectRules(project));
        return verifier.findRuleViolations(artifacts, traceLinks, rulesToApply);
    }

    /**
     * Returns list of warning rules defined on given project.
     *
     * @param project The project whose rule are returned.
     * @return The project rules.
     */
    public List<Rule> getProjectRules(Project project) {
        List<Warning> projectWarnings = this.warningRepository.findAllByProject(project);
        List<Rule> projectRules = new ArrayList<Rule>();

        for (Warning warning : projectWarnings) {
            projectRules.add(new Rule(warning));
        }
        return projectRules;
    }
}
