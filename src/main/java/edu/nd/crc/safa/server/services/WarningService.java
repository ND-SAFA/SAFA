package edu.nd.crc.safa.server.services;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import edu.nd.crc.safa.server.db.entities.sql.ArtifactBody;
import edu.nd.crc.safa.server.db.entities.sql.Project;
import edu.nd.crc.safa.server.db.entities.sql.TraceLink;
import edu.nd.crc.safa.server.db.entities.sql.Warning;
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

    @Autowired
    public WarningService(WarningRepository warningRepository) {
        this.warningRepository = warningRepository;
    }

    /**
     * Returns mapping of artifact name to the list of violations it is inhibiting.
     *
     * @param project    - The project
     * @param artifacts  - The project artifacts representing the nodes in a graph
     * @param traceLinks - The trace links representing edges connecting the nodes
     * @return A mapping of  artifact name's to their resulting violations
     */
    public Map<String, List<RuleName>> findViolationsInArtifactTree(Project project,
                                                                    List<ArtifactBody> artifacts,
                                                                    List<TraceLink> traceLinks) {

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
