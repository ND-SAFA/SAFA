package features.rules.logic;

import java.util.List;
import java.util.Map;

import builders.DbEntityBuilder;

import edu.nd.crc.safa.features.rules.entities.app.RuleAppEntity;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.features.rules.parser.RuleName;

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
