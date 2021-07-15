import edu.nd.crc.safa.warnings.Rule
import edu.nd.crc.safa.warnings.Tokenizer.Token
import edu.nd.crc.safa.warnings.Tokenizer.Type
import spock.lang.Specification

class RuleSpec extends Specification {
    def "a rule with only a true token returns true"() {
        given:
        def rule = new Rule()

        when:
        rule.mTokens.add(new Token(Type.TRUE, "True"))

        then:
        rule.result() == true
    }

    def "a rule with a true surrounded by parenthesis tokens returns true"() {
        given:
        def rule = new Rule()

        when:
        rule.mTokens.add(new Token(Type.LPAREN, "("))
        rule.mTokens.add(new Token(Type.TRUE, "True"))
        rule.mTokens.add(new Token(Type.RPAREN, ")"))

        then:
        rule.reduce() == true
        rule.result() == true
    }

    def "a rule with only a false token returns false"() {
        given:
        def rule = new Rule()

        when:
        rule.mTokens.add(new Token(Type.FALSE, "False"))

        then:
        rule.result() == false
    }

    def "a rule with a false surrounded by parenthesis tokens returns true"() {
        given:
        def rule = new Rule()

        when:
        rule.mTokens.add(new Token(Type.LPAREN, "("))
        rule.mTokens.add(new Token(Type.FALSE, "False"))
        rule.mTokens.add(new Token(Type.RPAREN, ")"))

        then:
        rule.reduce() == true
        rule.result() == false
    }

    def "a rule with a not and true should be reduced to a false"() {
        given:
        def rule = new Rule()

        when:
        rule.mTokens.add(new Token(Type.NOT, "!"))
        rule.mTokens.add(new Token(Type.TRUE, "True"))

        then:
        rule.reduce() == true
        rule.result() == false
    }

    def "a rule with a not and a true within parenthesis should be reduced to a false"() {
        given:
        def rule = new Rule()

        when:
        rule.mTokens.add(new Token(Type.NOT, "!"))
        rule.mTokens.add(new Token(Type.LPAREN, "("))
        rule.mTokens.add(new Token(Type.TRUE, "True"))
        rule.mTokens.add(new Token(Type.RPAREN, ")"))

        then:
        rule.reduce() == true
        rule.result() == false
    }

    def "a rule with a true and false should be reduced to a false"() {
        given:
        def rule = new Rule()

        when:
        rule.mTokens.add(new Token(Type.TRUE, "True"))
        rule.mTokens.add(new Token(Type.AND, "&"))
        rule.mTokens.add(new Token(Type.FALSE, "False"))

        then:
        rule.reduce() == true
        rule.result() == false
    }

    def "a rule with a true or false should be reduced to a true"() {
        given:
        def rule = new Rule()

        when:
        rule.mTokens.add(new Token(Type.TRUE, "True"))
        rule.mTokens.add(new Token(Type.OR, "|"))
        rule.mTokens.add(new Token(Type.FALSE, "False"))

        then:
        rule.reduce() == true
        rule.result() == true
    }

    def "a rule with a function should return the function correctly"() {
        given:
        def rule = new Rule()

        when:
        rule.mTokens.add(new Token(Type.FUNCS, "at-least-one"))
        rule.mTokens.add(new Token(Type.ARGUMENT, "hazard"))
        rule.mTokens.add(new Token(Type.ARGUMENT, "child"))
        rule.mTokens.add(new Token(Type.ARGUMENT, "requirement"))
        rule.mTokens.add(new Token(Type.FUNCE, ")"))

        then:
        def of = rule.nextFunction()
        of.isPresent() == true
        def f = of.get()
        f.Count == 1
        f.Requirement == Rule.Requirement.ATLEAST
        f.Target == "hazard"
        f.Relationship == Rule.Relationship.CHILD
        f.RequiredTarget == "requirement"
    }

    def "a rule with a function should allow replacing the function with its result"() {
        given:
        def rule = new Rule()

        when:
        rule.mTokens.add(new Token(Type.FUNCS, "at-least-one"))
        rule.mTokens.add(new Token(Type.ARGUMENT, "hazard"))
        rule.mTokens.add(new Token(Type.ARGUMENT, "child"))
        rule.mTokens.add(new Token(Type.ARGUMENT, "requirement"))
        rule.mTokens.add(new Token(Type.FUNCE, ")"))
        rule.setFunctionResult(true)
        rule.reduce()

        then:
        rule.mTokens.size() == 1
        rule.result() == true
    }

    def "a rule with an unbalanced number of brackets is invalid"() {
        given:
        def rule = new Rule()

        when:
        rule.mTokens.add(new Token(Type.LPAREN, "("))
        rule.mTokens.add(new Token(Type.TRUE, "True"))

        then:
        rule.isValid() == false
    }

    def "a rule with a function start but no function end is invalid"() {
        given:
        def rule = new Rule()

        when:
        rule.mTokens.add(new Token(Type.FUNCS, "at-least-one"))
        rule.mTokens.add(new Token(Type.ARGUMENT, "hazard"))
        rule.mTokens.add(new Token(Type.ARGUMENT, "child"))
        rule.mTokens.add(new Token(Type.ARGUMENT, "requirement"))

        then:
        rule.isValid() == false
    }

    def "a rule with a function that is not implemented is invalid"() {
        given:
        def rule = new Rule()

        when:
        rule.mTokens.add(new Token(Type.FUNCS, "test"))
        rule.mTokens.add(new Token(Type.FUNCE, ")"))

        then:
        rule.isValid() == false
    }
}
