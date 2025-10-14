package edu.nd.crc.safa.features.rules.parser;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.artifacts.entities.db.ArtifactVersion;
import edu.nd.crc.safa.features.common.ProjectEntities;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.traces.entities.db.TraceLink;

import lombok.AllArgsConstructor;

/**
 * Responsible for applying a set of rules to a set of artifacts and links between them
 * generating warnings if the rules are not met.
 */
public class TreeVerifier {

    public static final Retrievers<ArtifactVersion, TraceLink> dbEntityRetrievers = new Retrievers<>(
        a -> a.getArtifact().getArtifactId(),
        ArtifactVersion::getTypeName,
        t -> t.getSourceArtifact().getArtifactId(),
        t -> t.getTargetArtifact().getArtifactId()
    );

    public static final Retrievers<ArtifactAppEntity, TraceAppEntity> appEntityRetrievers = new Retrievers<>(
        ArtifactAppEntity::getId,
        ArtifactAppEntity::getType,
        TraceAppEntity::getSourceId,
        TraceAppEntity::getTargetId
    );

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
        return findRuleViolations(artifactBodies, traceLinks, rulesToApply, dbEntityRetrievers);
    }

    /**
     * Applies given list of rules to tree formed by given artifacts connected via trace links.
     *
     * @param projectEntities - The entities of the graph
     * @param rulesToApply    - The list of rules to apply to the artifact tree
     * @return A mapping between artifact Ids and the list of rules it violated
     */
    public final Map<UUID, List<RuleName>> findRuleViolations(ProjectEntities projectEntities,
                                                              List<ParserRule> rulesToApply) {
        List<ArtifactAppEntity> artifactBodies = projectEntities.getArtifacts();
        List<TraceAppEntity> traceLinks = projectEntities.getTraces();

        return findRuleViolations(artifactBodies, traceLinks, rulesToApply, appEntityRetrievers);
    }

    /**
     * Applies given list of rules to tree formed by given artifacts connected via trace links.
     *
     * @param artifactBodies - The nodes of the graph
     * @param traceLinks     - The traceLinks (links) connecting the nodes (artifacts)
     * @param rulesToApply   - The list of rules to apply to the artifact tree
     * @param retrievers     - Used to resolve the differences between types
     * @return A mapping between artifact Ids and the list of rules it violated
     */
    private <A, T> Map<UUID, List<RuleName>> findRuleViolations(List<A> artifactBodies,
                                                                List<T> traceLinks,
                                                                List<ParserRule> rulesToApply,
                                                                Retrievers<A, T> retrievers) {
        Map<UUID, List<RuleName>> results = new HashMap<>();

        Map<UUID, A> idToArtifact = new HashMap<>();
        artifactBodies.forEach(a -> idToArtifact.put(retrievers.idRetriever.apply(a), a));

        artifactBodies.forEach(artifactBody -> {

            List<RuleName> artifactWarnings = new ArrayList<>();
            for (ParserRule rule : rulesToApply) {
                rule = new ParserRule(rule);
                while (true) {
                    Optional<Function> ruleFunctionQuery = rule.parseFunction();
                    if (ruleFunctionQuery.isPresent()) {
                        Function ruleFunction = ruleFunctionQuery.get();
                        String type = retrievers.typeRetriever.apply(artifactBody);

                        if (type.equalsIgnoreCase(ruleFunction.getTargetArtifactType())) {
                            boolean isSatisfied = isRuleSatisfied(ruleFunction, artifactBody, traceLinks,
                                idToArtifact, retrievers);
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
                UUID artifactId = retrievers.idRetriever.apply(artifactBody);
                results.put(artifactId, artifactWarnings);
            }
        });

        return results;
    }

    private <A, T> boolean isRuleSatisfied(final Function ruleToApply, A targetArtifact, final List<T> traceLinks,
                                           final Map<UUID, A> idToArtifact, Retrievers<A, T> retrievers) {
        UUID artifactId = retrievers.idRetriever.apply(targetArtifact);

        switch (ruleToApply.getArtifactRelationship()) {
            case BIDIRECTIONAL_LINK:
                return satisfiesLinkCountRule(ruleToApply, artifactId, traceLinks, idToArtifact, retrievers);
            case CHILD:
                return satisfiesChildCountRule(ruleToApply, artifactId, traceLinks, idToArtifact, retrievers);
            case SIBLING:
                return handleSiblingFunction(ruleToApply, artifactId, traceLinks, idToArtifact, retrievers);
            default:
                return true;
        }

    }

    public <A, T> boolean satisfiesLinkCountRule(final Function rule, final UUID artifactId, final List<T> traceLinks,
                                                 final Map<UUID, A> idToArtifact, Retrievers<A, T> retrievers) {

        long childCount = traceLinks
            .stream()
            // Get all traceLinks where we are the source or target
            .filter(t -> {
                A sourceEntity = idToArtifact.get(retrievers.sourceIdRetriever.apply(t));
                A targetEntity = idToArtifact.get(retrievers.targetIdRetriever.apply(t));

                UUID sourceId = retrievers.idRetriever.apply(sourceEntity);
                UUID targetId = retrievers.idRetriever.apply(targetEntity);

                if (sourceId.equals(artifactId) || targetId.equals(artifactId)) {
                    String sourceType = retrievers.typeRetriever.apply(sourceEntity);
                    String targetType = retrievers.typeRetriever.apply(targetEntity);

                    return rule.getSourceArtifactType().equalsIgnoreCase(sourceType)
                        && rule.getTargetArtifactType().equalsIgnoreCase(targetType);
                } else {
                    return false;
                }
            })
            .count();
        return matchesRuleCount(rule, childCount);
    }

    public <A, T> boolean satisfiesChildCountRule(final Function childCountRule, final UUID targetArtifactId,
                                                  final List<T> traceLinks, final Map<UUID, A> idToArtifact,
                                                  Retrievers<A, T> retrievers) {
        long childCount = traceLinks
            .stream()
            // Get all traceLinks where we are the source
            .filter(link -> retrievers.targetIdRetriever.apply(link).equals(targetArtifactId))
            // Get all traceLinks where the target matches the required target type
            .filter(link -> {
                A artifact = idToArtifact.get(retrievers.sourceIdRetriever.apply(link));
                String type = retrievers.typeRetriever.apply(artifact);
                return type.equalsIgnoreCase(childCountRule.getSourceArtifactType());
            })
            .count();
        return matchesRuleCount(childCountRule, childCount);
    }

    public <A, T> boolean handleSiblingFunction(final Function r, final UUID artifactId, final List<T> traceLinks,
                                                final Map<UUID, A> idToArtifact, Retrievers<A, T> retrievers) {

        Long siblingCountAsTarget = traceLinks
            .stream()
            // Get traceLinks that finish with this node
            .filter(t -> retrievers.targetIdRetriever.apply(t).equals(artifactId))
            .filter(t -> {
                A artifact = idToArtifact.get(retrievers.sourceIdRetriever.apply(t));
                String type = retrievers.typeRetriever.apply(artifact);
                return type.equalsIgnoreCase(r.getSourceArtifactType());
            })
            .count();

        Long siblingCountAsSource = traceLinks
            .stream()
            // Get traceLinks that finish with this node
            .filter(t -> retrievers.sourceIdRetriever.apply(t).equals(artifactId))
            .filter(t -> {
                A artifact = idToArtifact.get(retrievers.targetIdRetriever.apply(t));
                String type = retrievers.typeRetriever.apply(artifact);
                return type.equalsIgnoreCase(r.getSourceArtifactType());
            })
            .count();
        long siblingCount = siblingCountAsTarget + siblingCountAsSource;

        return matchesRuleCount(r, siblingCount);
    }

    private boolean matchesRuleCount(Function r, long childCount) {
        switch (r.getCondition()) {
            case AT_LEAST:
                return childCount >= r.getCount();
            case EXACTLY:
                return childCount == r.getCount();
            case LESS_THAN:
                return childCount < r.getCount();
            default:
        }
        return true;
    }

    @AllArgsConstructor
    private static class Retrievers<A, T> {
        private java.util.function.Function<A, UUID> idRetriever;
        private java.util.function.Function<A, String> typeRetriever;
        private java.util.function.Function<T, UUID> sourceIdRetriever;
        private java.util.function.Function<T, UUID> targetIdRetriever;
    }
}
