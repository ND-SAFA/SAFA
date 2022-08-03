package edu.nd.crc.safa.warnings;

import java.util.ArrayList;
import java.util.List;

import lombok.AccessLevel;
import lombok.NoArgsConstructor;

/**
 * The default list of rules applied to projects when generating warnings.
 */
@NoArgsConstructor(access = AccessLevel.PRIVATE)
public class DefaultTreeRules {
    private static final String MISSING_CHILD = "Missing child";

    public static List<ParserRule> getDefaultRules() {
        List<ParserRule> defaultRules = new ArrayList<>();
        defaultRules.add(atLeastOneRequirementOrDesignOrProcessForRequirement());
        defaultRules.add(requirementHasNoPackageLinks());
        defaultRules.add(atLeastOnePackageForDesigns());
        return defaultRules;
    }

    public static ParserRule atLeastOneRequirementOrDesignOrProcessForRequirement() {
        return new ParserRule(MISSING_CHILD,
            "Requirement should have at least one child requirement, design, or process.",
            "at-least-one(Requirement, child, Requirement) || at-least-one(Requirement, child, Design) || "
                + "at-least-one(Requirement, child, Process)");
    }

    public static ParserRule requirementHasNoPackageLinks() {
        return new ParserRule(MISSING_CHILD,
            "Requirements must not have package children.",
            "exactly-n(0, Requirement, child, Package)");
    }

    public static ParserRule atLeastOnePackageForDesigns() {
        return new ParserRule(MISSING_CHILD,
            "Design Definitions should have at least one child package.",
            "at-least-one(Designs, child, Package)");
    }
}
