package edu.nd.crc.safa.warnings;

import java.util.ArrayList;
import java.util.List;

public class TreeRules {
    public static List<Rule> getDefaultRules() {
        List<Rule> defaultRules = new ArrayList<>();
        defaultRules.add(atLeastOneRequirementForHazard());
        defaultRules.add(atLeastOneRequirementOrDesignOrProcessForRequirement());
        defaultRules.add(requirementHasNoPackageLinks());
        defaultRules.add(atLeastOnePackageForDesigns());
        return defaultRules;
    }

    public static Rule atLeastOneRequirementForHazard() {
        return new Rule("Missing child",
            "At least one requirement child for hazards",
            "at-least-one(Hazard, child, Requirement)");
    }

    public static Rule atLeastOneRequirementOrDesignOrProcessForRequirement() {
        return new Rule("Missing child",
            "At least one requirement, design or process child for requirements",
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
            "At least one package child for design definitions",
            "at-least-one(DesignDefinition, child, Package)");
    }
}
