import spock.lang.Specification
import edu.nd.crc.safa.warnings.TreeVerifier

class TreeVerifierSpec extends Specification {
  //Simple Rules
  def "a graph with a hazard that has no requirements should fail a rule that states it must have at least one"(){
    given:
    def verifier = new TreeVerifier()
    def rule = "at-least-one(hazard, child, requirement)"
    def nodes = new HashMap<String,String>()
    def edges = new ArrayList<TreeVerifier.Edge>()

    when:
    verifier.addRule(rule)
    nodes.put("UAV-0001", "Hazard")
    nodes.put("UAV-0002", "Package")
    edges.add(new TreeVerifier.Edge(verifier, "UAV-0001", "UAV-0002", "REQUIRES"))

    then:
    def rules = verifier.getRules()
    rules.size() == 1
    rules.get(0).mTokens.size() == 5
    def warnings = verifier.verify(nodes, edges);
    warnings.size() == 1
    warnings.get("UAV-0001").size() == 1
    warnings.get("UAV-0001").get(0).equals(rule)
  }

  def "a graph with a hazard that has multiple requirements should fail a rule that states it must have exactly one"(){
    given:
    def verifier = new TreeVerifier()
    def rule = "exactly-one(hazard, child, requirement)"
    def nodes = new HashMap<String,String>()
    def edges = new ArrayList<TreeVerifier.Edge>()

    when:
    verifier.addRule(rule)
    nodes.put("UAV-0001", "Hazard")
    nodes.put("UAV-0002", "Requirement")
    nodes.put("UAV-0003", "Requirement")
    edges.add(new TreeVerifier.Edge(verifier, "UAV-0001", "UAV-0002", "REQUIRES"))
    edges.add(new TreeVerifier.Edge(verifier, "UAV-0001", "UAV-0003", "REQUIRES"))

    then:
    def rules = verifier.getRules()
    rules.size() == 1
    rules.get(0).mTokens.size() == 5
    def warnings = verifier.verify(nodes, edges);
    warnings.size() == 1
    warnings.get("UAV-0001").size() == 1
    warnings.get("UAV-0001").get(0).equals(rule)
  }

  def "a graph with a hazard that has multiple requirements should fail a rule that states it must have less than two"(){
    given:
    def verifier = new TreeVerifier()
    def rule = "less-than-n(2, hazard, child, requirement)"
    def nodes = new HashMap<String,String>()
    def edges = new ArrayList<TreeVerifier.Edge>()

    when:
    verifier.addRule(rule)
    nodes.put("UAV-0001", "Hazard")
    nodes.put("UAV-0002", "Requirement")
    nodes.put("UAV-0003", "Requirement")
    edges.add(new TreeVerifier.Edge(verifier, "UAV-0001", "UAV-0002", "REQUIRES"))
    edges.add(new TreeVerifier.Edge(verifier, "UAV-0001", "UAV-0003", "REQUIRES"))

    then:
    def rules = verifier.getRules()
    rules.size() == 1
    rules.get(0).mTokens.size() == 6
    def warnings = verifier.verify(nodes, edges);
    warnings.size() == 1
    warnings.get("UAV-0001").size() == 1
    warnings.get("UAV-0001").get(0).equals(rule)
  }

  // Compount Rules
  def "adding a compound rule for at least one child node of type requirement or design for a requirement nodes"(){
    given:
    def verifier = new TreeVerifier()
    def rule = "at-least-one(requirement, child, requirement) || at-least-one(requirement, child, design)"
    def nodes = new HashMap<String,String>()
    def edges = new ArrayList<TreeVerifier.Edge>()

    when:
    verifier.addRule(rule)
    nodes.put("UAV-0001", "Requirement")
    nodes.put("UAV-0002", "Hazard")
    edges.add(new TreeVerifier.Edge(verifier, "UAV-0001", "UAV-0002", "REQUIRES"))

    then:
    def rules = verifier.getRules()
    rules.size() == 1
    rules.get(0).mTokens.size() == 11
    def warnings = verifier.verify(nodes, edges);
    warnings.size() == 1
    warnings.get("UAV-0001").size() == 1
    warnings.get("UAV-0001").get(0).equals(rule)
  }
}