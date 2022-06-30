package edu.nd.crc.safa.warnings;

import java.util.ArrayList;
import java.util.List;

/**
 * The default list of rules applied to projects when generating warnings.
 */
public class DefaultTreeRules {
    public static List<ParserRule> getDefaultRules() {
        List<ParserRule> defaultRules = new ArrayList<>();
        defaultRules.add(atLeastOneRequirementOrDesignOrProcessForRequirement());
        defaultRules.add(requirementHasNoPackageLinks());
        defaultRules.add(atLeastOnePackageForDesigns());
        return defaultRules;
    }

    public static ParserRule atLeastOneRequirementOrDesignOrProcessForRequirement() {
        return new ParserRule("Missing child",
            "Requirement should have at least one child requirement, design, or process.",
            "at-least-one(Requirement, child, Requirement) || at-least-one(Requirement, child, Design) || "
                + "at-least-one(Requirement, child, Process)");
    }

    public static ParserRule requirementHasNoPackageLinks() {
        return new ParserRule("Missing child",
            "Requirements must not have package children.",
            "exactly-n(0, Requirement, child, Package)");
    }

    public static ParserRule atLeastOnePackageForDesigns() {
        return new ParserRule("Missing child",
            "Design Definitions should have at least one child package.",
            "at-least-one(Designs, child, Package)");
    }
}
