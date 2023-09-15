package edu.nd.crc.safa.features.rules.parser;

import lombok.Getter;

/**
 * A word in a rule definition. Serves as the base entity defines in rule definitions.
 */
@Getter
public class Token {

    private final TokenType tokenType;
    private final String value;

    public Token(TokenType tokenType, String value) {
        this.tokenType = tokenType;
        this.value = value;
    }

    public String toString() {
        if (tokenType == TokenType.FUNC_START) {
            return "FUNCTION<" + value + ">";
        }
        if (tokenType == TokenType.FUNC_END) {
            return "FUNCTION END";
        }
        if (tokenType == TokenType.ARGUMENT) {
            return "ARGUMENT<" + value + ">";
        }
        return tokenType.toString();
    }

    public boolean isBoolean() {
        return tokenType == TokenType.TRUE || tokenType == TokenType.FALSE;
    }
}
