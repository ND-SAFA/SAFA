package edu.nd.crc.safa.test.features.rules.logic.tokenizer;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;

import edu.nd.crc.safa.features.rules.parser.Token;
import edu.nd.crc.safa.features.rules.parser.TokenType;
import edu.nd.crc.safa.features.rules.parser.Tokenizer;

import org.junit.jupiter.api.Test;

/**
 * Tests that a rule definitions is correctly split into tokens.
 */
class TestTokenizerParsing {

    @Test
    void testLexicalParsing() {
        String functionName = "exactly-n";
        String query = String.format("%s(0, Requirement, child, Package)", functionName);
        List<Token> tokens = Tokenizer.lex(query);

        assertThat(tokens).hasSize(6);
        assertThat(tokens.get(0).getValue()).isEqualTo(functionName);
        assertThat(tokens.get(0).getTokenType()).isEqualTo(TokenType.FUNC_START);

        assertThat(tokens.get(1).getValue()).isEqualTo("0");
        assertThat(tokens.get(1).getTokenType()).isEqualTo(TokenType.ARGUMENT);

        assertThat(tokens.get(2).getValue()).isEqualTo("Requirement");
        assertThat(tokens.get(2).getTokenType()).isEqualTo(TokenType.ARGUMENT);

        assertThat(tokens.get(3).getValue()).isEqualTo("child");
        assertThat(tokens.get(3).getTokenType()).isEqualTo(TokenType.ARGUMENT);

        assertThat(tokens.get(4).getValue()).isEqualTo("Package");
        assertThat(tokens.get(4).getTokenType()).isEqualTo(TokenType.ARGUMENT);

        assertThat(tokens.get(5).getValue()).isEqualTo(")");
        assertThat(tokens.get(5).getTokenType()).isEqualTo(TokenType.FUNC_END);
    }
}
