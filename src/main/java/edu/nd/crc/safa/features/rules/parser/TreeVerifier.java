package edu.nd.crc.safa.features.rules.parser;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.db.Artifact;
import edu.nd.crc.safa.features.artifacts.entities.db.ArtifactVersion;
import edu.nd.crc.safa.features.traces.entities.db.TraceLink;

/**
 * Responsible for applying a set of rules to a set of artifacts and links between them
 * generating warnings if the rules are not met.
 */
public class TreeVerifier {

    /**
     * Applies given list of rules to tree formed by given artifacts connected via trace links.
     *
     * @param artifactBodies - The nodes of the graph
     * @param traceLinks     - The traceLinks (links) connecting the nodes (artifacts)
     * @param rulesToApply   - The list of rules to apply to the artifact tree
     * @return A mapping between artifact Ids and the list of rules it violated
     */
    public final Map<UUID, List<RuleName>> findRuleViolations(List<ArtifactVersion> artifactBodies,
                                                              List<TraceLink> traceLinks,
                                                              List<ParserRule> rulesToApply) {
        Map<UUID, List<RuleName>> results = new HashMap<>();

        artifactBodies.forEach(artifactBody -> {

            List<RuleName> artifactWarnings = new ArrayList<>();
            for (ParserRule rule : rulesToApply) {
                rule = new ParserRule(rule);
                while (true) {
                    Optional<Function> ruleFunctionQuery = rule.parseFunction();
                    if (ruleFunctionQuery.isPresent()) {
                        Function ruleFunction = ruleFunctionQuery.get();
                        if (artifactBody.getTypeName().equalsIgnoreCase(ruleFunction.targetArtifactType)) {
                            boolean isSatisfied = isRuleSatisfied(ruleFunction, artifactBody.getArtifact(), traceLinks);
                            rule.setFunctionResult(isSatisfied);
                        } else {
                            rule.setFunctionResult(true);
                        }
                    } else {
                        break;
                    }
                }

                rule.reduce();

                if (!rule.isRuleSatisfied()) {
                    artifactWarnings.add(rule.getMRuleName());
                }
            }
            if (!artifactWarnings.isEmpty()) {
                UUID artifactId = artifactBody.getArtifact().getArtifactId();
                results.put(artifactId, artifactWarnings);
            }
        });

        return results;
    }

    private boolean isRuleSatisfied(final Function ruleToApply,
                                    Artifact targetArtifact,
                                    final List<TraceLink> traceLinks) {
        switch (ruleToApply.artifactRelationship) {
            case BIDIRECTIONAL_LINK:
                return satisfiesLinkCountRule(ruleToApply, targetArtifact, traceLinks);
            case CHILD:
                return satisfiesChildCountRule(ruleToApply, targetArtifact.getName(), traceLinks);
            case SIBLING:
                return handleSiblingFunction(ruleToApply, targetArtifact.getName(), traceLinks);
            default:
                return true;
        }

    }

    public boolean satisfiesLinkCountRule(final Function rule,
                                          final Artifact artifact,
                                          final List<TraceLink> traceLinks) {
        long childCount = traceLinks
            .stream()
            // Get all traceLinks where we are the source or target
            .filter(t -> {
                String typeName = artifact.getType().getName();
                String artifactName = artifact.getName();
                String otherType;
                if (typeName.equalsIgnoreCase(rule.sourceArtifactType)) {
                    otherType = rule.targetArtifactType;
                } else if (typeName.equalsIgnoreCase(rule.targetArtifactType)) {
                    otherType = rule.sourceArtifactType;
                } else {
                    return false;
                }

                if (t.isSourceName(artifactName)) {
                    return t.getTargetType().getName().equalsIgnoreCase(otherType);
                } else if (t.isTargetName(artifactName)) {
                    return t.getSourceType().getName().equalsIgnoreCase(otherType);
                } else {
                    return false;
                }
            })
            .count();
        return matchesRuleCount(rule, childCount);
    }

    public boolean satisfiesChildCountRule(final Function childCountRule,
                                           final String targetArtifact,
                                           final List<TraceLink> traceLinks) {
        long childCount = traceLinks
            .stream()
            // Get all traceLinks where we are the source
            .filter(link -> link
                .isTargetName(targetArtifact))
            // Get all traceLinks where the target matches the required target type
            .filter(link -> link
                .getSourceType()
                .getName()
                .equalsIgnoreCase(childCountRule.sourceArtifactType))
            .count();
        return matchesRuleCount(childCountRule, childCount);
    }

    public boolean handleSiblingFunction(final Function r,
                                         final String artifactName,
                                         final List<TraceLink> traceLinks) {
        Long siblingCountAsTarget = traceLinks
            .stream()
            .filter(t -> t.getTargetName().equals(artifactName)) // Get traceLinks that finish with this node
            .filter(t -> t.getSourceType().toString().equalsIgnoreCase(r.sourceArtifactType))
            .count();
        Long siblingCountAsSource = traceLinks
            .stream()
            .filter(t -> t.getSourceName().equals(artifactName)) // Get traceLinks that finish with this node
            .filter(t -> t.getTargetType().toString().equalsIgnoreCase(r.sourceArtifactType))
            .count();
        long siblingCount = siblingCountAsTarget + siblingCountAsSource;

        return matchesRuleCount(r, siblingCount);
    }

    private boolean matchesRuleCount(Function r, long childCount) {
        switch (r.condition) {
            case AT_LEAST:
                return childCount >= r.count;
            case EXACTLY:
                return childCount == r.count;
            case LESS_THAN:
                return childCount < r.count;
            default:
        }
        return true;
    }
}
