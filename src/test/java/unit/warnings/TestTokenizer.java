package unit.warnings;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import java.util.List;

import edu.nd.crc.safa.warnings.Token;
import edu.nd.crc.safa.warnings.TokenType;
import edu.nd.crc.safa.warnings.Tokenizer;

import org.junit.jupiter.api.Test;

public class TestTokenizer {

    @Test
    public void testLexicalParsing() {
        String functionName = "exactly-n";
        String query = String.format("%s(0, Requirement, child, Package)", functionName);
        List<Token> tokens = Tokenizer.lex(query);

        assertThat(tokens.size()).isEqualTo(6);
        assertThat(tokens.get(0).value).isEqualTo(functionName);
        assertThat(tokens.get(0).tokenType).isEqualTo(TokenType.FUNC_START);

        assertThat(tokens.get(1).value).isEqualTo("0");
        assertThat(tokens.get(1).tokenType).isEqualTo(TokenType.ARGUMENT);

        assertThat(tokens.get(2).value).isEqualTo("Requirement");
        assertThat(tokens.get(2).tokenType).isEqualTo(TokenType.ARGUMENT);

        assertThat(tokens.get(3).value).isEqualTo("child");
        assertThat(tokens.get(3).tokenType).isEqualTo(TokenType.ARGUMENT);

        assertThat(tokens.get(4).value).isEqualTo("Package");
        assertThat(tokens.get(4).tokenType).isEqualTo(TokenType.ARGUMENT);

        assertThat(tokens.get(5).value).isEqualTo(")");
        assertThat(tokens.get(5).tokenType).isEqualTo(TokenType.FUNC_END);
    }
}
