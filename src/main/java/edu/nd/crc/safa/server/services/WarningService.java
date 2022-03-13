package edu.nd.crc.safa.server.services;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import edu.nd.crc.safa.server.entities.db.ArtifactVersion;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.TraceLink;
import edu.nd.crc.safa.server.entities.db.Warning;
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

    private final WarningRepository warningRepository;

    @Autowired
    public WarningService(WarningRepository warningRepository) {
        this.warningRepository = warningRepository;
    }

    /**
     * Returns the warnings of given artifacts using default and project rules.
     *
     * @param project    The project whose rules are applied.
     * @param artifacts  The artifacts who are being checked for violations.
     * @param traceLinks The links between artifacts.
     * @return Returns a map of artifact id's to a list of warning associated with that artifact.
     */
    public Map<String, List<RuleName>> generateWarningsOnEntities(Project project,
                                                                  List<ArtifactVersion> artifacts,
                                                                  List<TraceLink> traceLinks) {
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
