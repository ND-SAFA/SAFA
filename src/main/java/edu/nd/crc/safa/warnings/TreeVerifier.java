package edu.nd.crc.safa.warnings;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

public class TreeVerifier {
    public class MultipleRuleException extends Exception {
        public MultipleRuleException(String errorMessage) {
            super(errorMessage);
        }
    }

    public class InvalidRuleException extends Exception {
        public InvalidRuleException(String errorMessage) {
            super(errorMessage);
        }
    }


    List<Rule> mRules = new ArrayList<>();

    public boolean addRule(final String name, final String longname, final String rule) throws Exception {
        mRules.add(new Rule(name, longname, rule));
        return true;
    }

    public boolean addRule(final Rule rule) throws Exception {
        mRules.add(rule);
        return true;
    }

    public final List<Rule> getRules() {
        return mRules;
    }

    public class Edge {
        public String Source;
        public String Target;
        public String Type;

        public Edge() {
            Source = "";
            Target = "";
            Type = "";
        }

        public Edge(String source, String target, String relType) {
            Source = source;
            Target = target;
            Type = relType;
        }
    }

    public final Map<String, List<Rule.Name>> verify(final List<org.neo4j.driver.types.Node> nodes,
                                                     final Map<Long, String> ids,
                                                     final List<Map<String, Object>> values) {
        Map<String, String> nodeList = new HashMap<>();
        for (int i = 0; i < nodes.size(); i++) {
            final org.neo4j.driver.types.Node node = nodes.get(i);
            if (node.get("id") == null || node.get("id").toString() == "NULL") {
                continue;
            }
            nodeList.put(node.get("id").asString(), ((List<String>) node.labels()).get(0).toString());
        }

        List<Edge> edgeList = new ArrayList<>();
        for (Map<String, Object> value : values) {
            final String relType = (String) value.getOrDefault("type", "");
            if (relType.equals("UPDATES")) {
                continue;
            }

            final String source = (String) value.getOrDefault("source", "");
            if (source.isEmpty()) {
                continue;
            }

            final String target = (String) value.getOrDefault("target", "");
            if (target.isEmpty()) {
                continue;
            }

            edgeList.add(new Edge(source, target, relType));
        }

        return verify(nodeList, edgeList);
    }

    public final Map<String, List<Rule.Name>> verify(final Map<String, String> nodes, final List<Edge> edges) {
        Map<String, List<Rule.Name>> results = new HashMap<>();

        nodes.forEach((id, type) -> {
            List<Rule.Name> nodeWarnings = new ArrayList<Rule.Name>();
            for (int i = 0; i < mRules.size(); i++) {
                Rule r = new Rule(mRules.get(i));
                while (true) {
                    Optional<Rule.Function> of = r.nextFunction();
                    if (of.isPresent()) {
                        Rule.Function f = of.get();
                        if (type.toLowerCase().equals(f.Target)) {
                            r.setFunctionResult(handleFunction(f, id, nodes, edges));
                        } else {
                            r.setFunctionResult(true);
                        }
                    } else {
                        break;
                    }
                }

                r.reduce();
                if (!r.result()) {
                    nodeWarnings.add(r.getName());
                }
            }
            if (!nodeWarnings.isEmpty()) {
                results.put(id, nodeWarnings);
            }
        });

        return results;
    }

    private boolean handleFunction(final Rule.Function r,
                                   final String index,
                                   final Map<String, String> nodes,
                                   final List<Edge> edges) {
        switch (r.Relationship) {
            case CHILD:
                return handleChildFunction(r, index, nodes, edges);
            case SIBLING:
                return handleSiblingFunction(r, index, nodes, edges);
            default:
        }
        return true;
    }

    public boolean handleChildFunction(final Rule.Function r,
                                       final String index,
                                       final Map<String,
                                           String> nodes,
                                       final List<Edge> edges) {
        long childCount = edges.stream()
            .filter(e -> e.Source.equals(index)) // Get all edges where we are the source
            // Get all edges where the target matches the required target type
            .filter(e -> nodes.get(e.Target).toLowerCase().equals(r.RequiredTarget))
            .count();
        switch (r.Requirement) {
            case ATLEAST:
                return childCount >= r.Count;
            case EXACTLY:
                return childCount == r.Count;
            case LESSTHAN:
                return childCount < r.Count;
            default:
        }
        return true;
    }

    public boolean handleSiblingFunction(final Rule.Function r,
                                         final String index,
                                         final Map<String, String> nodes,
                                         final List<Edge> edges) {
        Integer childCount = edges.stream()
            .filter(e -> e.Target.equals(index)) // Get edges that finish with this node
            .map(e -> e.Source) // Convert to parent id
            .map(n ->
                edges.stream()
                    .filter(e -> e.Source.equals(n)) // Get all edges where we are the source
                    // Get all edges where the target matches the required target type
                    .filter(e -> nodes.get(e.Target).toLowerCase().equals(r.RequiredTarget))
                    .count()
            )
            .map(v -> v.intValue())
            .reduce(0, Integer::sum);

        switch (r.Requirement) {
            case ATLEAST:
                return childCount >= r.Count;
            case EXACTLY:
                return childCount == r.Count;
            case LESSTHAN:
                return childCount < r.Count;
            default:
        }
        return true;
    }
}
