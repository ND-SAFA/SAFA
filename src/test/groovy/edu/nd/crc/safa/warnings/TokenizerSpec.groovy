import spock.lang.Specification

import edu.nd.crc.safa.warnings.Tokenizer
import edu.nd.crc.safa.warnings.Tokenizer.Type
import edu.nd.crc.safa.warnings.Tokenizer.Token


class TokenizerSpec extends Specification {
    def "a function should be tokenized properly"(){
        given:
        def rule = "exactly-one(hazard, child, requirement)"

        when:
        def tokens = Tokenizer.lex(rule);

        then:
        tokens.size() == 5
        tokens.get(0).t == Type.FUNCS
        tokens.get(0).c == "exactly-one"
        tokens.get(1).t == Type.ARGUMENT
        tokens.get(1).c == "hazard"
        tokens.get(2).t == Type.ARGUMENT
        tokens.get(2).c == "child"
        tokens.get(3).t == Type.ARGUMENT
        tokens.get(3).c == "requirement"
        tokens.get(4).t == Type.FUNCE
        tokens.get(4).c == ")"
    }

    def "a function anded with another function should be tokenized properly"(){
        given:
        def rule = "test() && test()"

        when:
        def tokens = Tokenizer.lex(rule);

        then:
        tokens.size() == 5
        tokens.get(0).t == Type.FUNCS
        tokens.get(0).c == "test"
        tokens.get(1).t == Type.FUNCE
        tokens.get(1).c == ")"
        tokens.get(2).t == Type.AND
        tokens.get(2).c == "&&"
        tokens.get(3).t == Type.FUNCS
        tokens.get(3).c == "test"
        tokens.get(4).t == Type.FUNCE
        tokens.get(4).c == ")"
    }
}