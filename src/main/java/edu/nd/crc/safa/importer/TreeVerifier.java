package edu.nd.crc.safa.importer;

import java.util.Map;
import java.util.HashMap;
import java.util.List;
import java.util.ArrayList;

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

    public enum Requirement {
        ATLEASTONE, EXACTLYONE,
    }


    public enum Relationship {
        CHILD,
    }

    public class Rule {
        public Requirement Requirement;
        public String Target;
        public Relationship Relationship;
        public String RequiredTarget;
    }

    public class RuleGroup {
        public List<Rule> SubRule;
    }

    public class Edge {
        public String Source;
        public String Target;
        public String Type;

        public Edge(){
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

    List<Rule> mRules = new ArrayList<Rule>();

    public boolean addRule(final String rule) throws Exception{
        Rule r = new Rule();

        if( rule.chars().filter(ch -> ch == '(').count() != 1 && rule.chars().filter(ch -> ch == ')').count() != 1){
            throw new MultipleRuleException("only a single rule is allowed");
        }

        String command = rule.split("\\(")[0].trim().toLowerCase();
        String[] arguments = rule.split("\\(")[1].split("\\)")[0].split(",");
        if( arguments.length != 3 ){
            throw new InvalidRuleException("rule contains an invalid number of arguments");
        }

        switch(command){
            case "at-least-one":
                r.Requirement = Requirement.ATLEASTONE;
                break;
            case "exactly-one":
                r.Requirement = Requirement.EXACTLYONE;
                break;
        }

        r.Target = arguments[0].trim().toLowerCase();
        switch(arguments[1].trim().toLowerCase()){
            case "child":
                r.Relationship = Relationship.CHILD;
                break;
        }
        r.RequiredTarget = arguments[2].trim().toLowerCase();

        mRules.add(r);

        return true;
    }

    public final List<Rule> getRules(){
        return mRules;
    }

    public final Map<String, List<String>> verify(final List<org.neo4j.driver.v1.types.Node> nodes, final Map<Long, String> ids, final List<Map<String, Object>> values){
        Map<String,String> nodeList = new HashMap<>();
        for(int i = 0; i < nodes.size(); i++) {
            final org.neo4j.driver.v1.types.Node node = nodes.get(i);
            if (node.get("id") == null || node.get("id").toString() == "NULL") {
                continue;
            }
            nodeList.put(node.get("id").asString(), ((List<String>)node.labels()).get(0).toString());
        }

        List<Edge> edgeList = new ArrayList<>();
        for( Map<String,Object> value : values ){
            final String relType = (String)value.getOrDefault("type", "");
            if( relType.equals("UPDATES") ){
                continue;
            }

            final String source = (String)value.getOrDefault("source", "");
            if( source.isEmpty() ){
                continue;
            }

            final String target = (String)value.getOrDefault("target", "");
            if( target.isEmpty() ){
                continue;
            }

            edgeList.add(new Edge(source, target, relType));
        }

        return verify(nodeList, edgeList);
    }

    public final Map<String, List<String>> verify(final Map<String,String> nodes, final List<Edge> edges){
        Map<String, List<String>> results = new HashMap<>();

        nodes.forEach((id, type) -> {
            List<String> warnings = new ArrayList<String>();
            for( Rule r : mRules ){
                if( type.toLowerCase().equals(r.Target) ){
                    String warning = handleRule(r, id, nodes, edges);
                    if( !warning.isEmpty() ){
                        warnings.add(warning);
                    }
                }
            }
            if( !warnings.isEmpty() ) {
                results.put(id, warnings);
            }
        });

        return results;
    }

    private String handleRule(final Rule r, final String index, final Map<String,String> nodes, final List<Edge> edges){
        String result = "";
        switch(r.Relationship){
            case CHILD:
                result = handleChildRule(r, index, nodes, edges);
                break;
        }
        return result;
    }

    public String handleChildRule(final Rule r, final String index, final Map<String,String> nodes, final List<Edge> edges){
        long childCount = edges.stream()
            .filter( e -> e.Source.equals(index) ) // Get all edges where we are the source
            .filter( e -> nodes.get(e.Target).toLowerCase().equals(r.RequiredTarget) ) // Get all edges where the target matches the required target type
            .count();

        String result = "";
        switch(r.Requirement){
            case ATLEASTONE:
                if(!(childCount >= 1)){
                    result = String.format("is missing at least one child of type %s", r.RequiredTarget);  
                }
                break;
            case EXACTLYONE:
                if(!(childCount == 1)){
                    result = String.format("does not have exactly one child of type %s", r.RequiredTarget);  
                }
                break;
        }
        return result;
    }
}