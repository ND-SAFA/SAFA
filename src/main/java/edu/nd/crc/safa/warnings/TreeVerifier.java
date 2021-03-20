package edu.nd.crc.safa.warnings;

import java.util.Map;
import java.util.HashMap;
import java.util.List;
import java.util.ArrayList;
import java.util.Optional;
import static java.util.stream.Collectors.toList;

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

    public boolean addRule(final String rule) throws Exception{
        if( rule.chars().filter(ch -> ch == '(').count() != rule.chars().filter(ch -> ch == ')').count()){
            throw new MultipleRuleException("there are an unbalanced amount of brackets");
        }

        mRules.add(new Rule(rule));

        return true;
    }

    public final List<Rule> getRules(){
        return mRules;
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
            List<String> nodeWarnings = new ArrayList<String>();
            for( int i = 0; i < mRules.size(); i++ ){
                Rule r = new Rule(mRules.get(i));
                while(true){   
                    Optional<Rule.Function> of = r.NextFunction();
                    if( of.isPresent() ){
                        Rule.Function f = of.get();
                        if( type.toLowerCase().equals(f.Target) ){
                            r.SetFunctionResult(handleFunction(f, id, nodes, edges));
                        }else{
                            r.SetFunctionResult(true);
                        }
                    }else{
                        break;
                    }
                }

                r.Reduce();
                if( !r.Result() ){
                    nodeWarnings.add(r.toString());
                }
            }
            if( !nodeWarnings.isEmpty() ) {
                results.put(id, nodeWarnings);
            }
        });

        return results;
    }

    private boolean handleFunction(final Rule.Function r, final String index, final Map<String,String> nodes, final List<Edge> edges){
        switch(r.Relationship){
            case CHILD:
                return handleChildFunction(r, index, nodes, edges);
        }
        return true;
    }

    public boolean handleChildFunction(final Rule.Function r, final String index, final Map<String,String> nodes, final List<Edge> edges){
        long childCount = edges.stream()
            .filter( e -> e.Source.equals(index) ) // Get all edges where we are the source
            .filter( e -> nodes.get(e.Target).toLowerCase().equals(r.RequiredTarget) ) // Get all edges where the target matches the required target type
            .count();
        switch(r.Requirement){
            case ATLEAST:
                return childCount >= r.Count;
            case EXACTLY:
                return childCount == r.Count;
            case LESSTHAN:
                return childCount < r.Count;
        }
        return true;
    }
}