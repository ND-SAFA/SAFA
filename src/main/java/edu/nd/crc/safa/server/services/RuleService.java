package edu.nd.crc.safa.server.services;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import edu.nd.crc.safa.server.entities.db.ArtifactVersion;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.Rule;
import edu.nd.crc.safa.server.entities.db.TraceLink;
import edu.nd.crc.safa.server.repositories.RuleRepository;
import edu.nd.crc.safa.warnings.DefaultTreeRules;
import edu.nd.crc.safa.warnings.ParserRule;
import edu.nd.crc.safa.warnings.RuleName;
import edu.nd.crc.safa.warnings.TreeVerifier;

import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

/**
 * Responsible for generating project warnings for a given project version.
 */
@Service
@AllArgsConstructor
public class RuleService {

    private final RuleRepository ruleRepository;

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
        List<ParserRule> rulesToApply = new ArrayList<>();
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
    public List<ParserRule> getProjectRules(Project project) {
        List<Rule> databaseRules = this.ruleRepository.findByProject(project);
        List<ParserRule> projectRules = new ArrayList<>();

        for (Rule rule : databaseRules) {
            projectRules.add(new ParserRule(
                rule.getName(),
                rule.getDescription(),
                rule.getRule()));
        }
        return projectRules;
    }
}
