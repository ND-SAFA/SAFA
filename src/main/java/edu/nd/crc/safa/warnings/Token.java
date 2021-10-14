package edu.nd.crc.safa.warnings;

public class Token {

    public final TokenType tokenType;
    public final String value;

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
