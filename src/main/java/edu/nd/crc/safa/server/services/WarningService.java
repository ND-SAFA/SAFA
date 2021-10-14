package edu.nd.crc.safa.server.services;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import edu.nd.crc.safa.server.db.entities.sql.ArtifactBody;
import edu.nd.crc.safa.server.db.entities.sql.Project;
import edu.nd.crc.safa.server.db.entities.sql.ProjectVersion;
import edu.nd.crc.safa.server.db.entities.sql.TraceLink;
import edu.nd.crc.safa.server.db.entities.sql.Warning;
import edu.nd.crc.safa.server.db.repositories.TraceLinkRepository;
import edu.nd.crc.safa.server.db.repositories.WarningRepository;
import edu.nd.crc.safa.warnings.Rule;
import edu.nd.crc.safa.warnings.RuleName;
import edu.nd.crc.safa.warnings.TreeRules;
import edu.nd.crc.safa.warnings.TreeVerifier;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class WarningService {

    WarningRepository warningRepository;
    ArtifactService artifactService;
    TraceLinkRepository traceLinkRepository;

    @Autowired
    public WarningService(WarningRepository warningRepository,
                          ArtifactService artifactService,
                          TraceLinkRepository traceLinkRepository) {
        this.warningRepository = warningRepository;
        this.artifactService = artifactService;
        this.traceLinkRepository = traceLinkRepository;
    }

    /**
     * Returns mapping of artifact name to the list of violations it is inhibiting.
     *
     * @param projectVersion - Finds violations in artifact tree at time of this version
     * @return A mapping of  artifact name's to their resulting violations
     */
    public Map<String, List<RuleName>> findViolationsInArtifactTree(ProjectVersion projectVersion) {
        Project project = projectVersion.getProject();
        List<ArtifactBody> artifacts = artifactService.getArtifactBodiesAtVersion(projectVersion);
        List<TraceLink> traceLinks = this.traceLinkRepository.getApprovedLinks(project);
        return findViolationsInArtifactTree(projectVersion, artifacts, traceLinks);
    }

    public Map<String, List<RuleName>> findViolationsInArtifactTree(ProjectVersion projectVersion,
                                                                    List<ArtifactBody> artifacts,
                                                                    List<TraceLink> traceLinks) {
        Project project = projectVersion.getProject();
        TreeVerifier verifier = new TreeVerifier();
        List<Rule> rulesToApply = new ArrayList<>();
        rulesToApply.addAll(TreeRules.getDefaultRules());
        rulesToApply.addAll(this.getProjectRules(project));

        return verifier.findRuleViolations(artifacts, traceLinks, rulesToApply);
    }

    public List<Rule> getProjectRules(Project project) {
        List<Warning> projectWarnings = this.warningRepository.findAllByProject(project);
        List<Rule> projectRules = new ArrayList<Rule>();

        for (Warning warning : projectWarnings) {
            projectRules.add(new Rule(warning));
        }
        return projectRules;
    }
}
