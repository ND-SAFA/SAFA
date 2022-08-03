package unit.project.rule;

import java.util.List;
import java.util.Map;

import edu.nd.crc.safa.builders.entities.DbEntityBuilder;
import edu.nd.crc.safa.server.entities.api.layout.RuleAppEntity;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.warnings.RuleName;

/**
 * Responsible for creating interface for testing a rule.
 */
public interface IRuleTest {

    /**
     * @return The rule to test.
     */
    RuleAppEntity getRule();

    /**
     * @return returns the project name;
     */
    String getProjectName();

    /**
     * Creates entities to violate rules.
     *
     * @param projectVersion T
     */
    void createViolatingRuleEntities(ProjectVersion projectVersion,
                                     DbEntityBuilder entityBuilder);

    /**
     * Performs assertions about the project warnings.
     *
     * @param warnings The warnings about the project.
     */
    void assertWarnings(Map<String, List<RuleName>> warnings);
}
