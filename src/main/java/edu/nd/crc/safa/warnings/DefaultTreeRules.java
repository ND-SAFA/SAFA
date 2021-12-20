package edu.nd.crc.safa.warnings;

import java.util.ArrayList;
import java.util.List;

/**
 * The default list of rules applied to projects when generating warnings.
 */
public class DefaultTreeRules {
    public static List<Rule> getDefaultRules() {
        List<Rule> defaultRules = new ArrayList<>();
        defaultRules.add(atLeastOneRequirementOrDesignOrProcessForRequirement());
        defaultRules.add(requirementHasNoPackageLinks());
        defaultRules.add(atLeastOnePackageForDesigns());
        return defaultRules;
    }

    public static Rule atLeastOneRequirementOrDesignOrProcessForRequirement() {
        return new Rule("Missing child",
            "Requirement should have at least one child requirement, design or process",
            "at-least-one(Requirement, child, Requirement) || at-least-one(Requirement, child, Design) || "
                + "at-least-one(Requirement, child, Process)");
    }

    public static Rule requirementHasNoPackageLinks() {
        return new Rule("Missing child",
            "Requirements must not have package children",
            "exactly-n(0, Requirement, child, Package)");
    }

    public static Rule atLeastOnePackageForDesigns() {
        return new Rule("Missing child",
            "Design Definitions should have at least one child package",
            "at-least-one(DesignDefinition, child, Package)");
    }
}
