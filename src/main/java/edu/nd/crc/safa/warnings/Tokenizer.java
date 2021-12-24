package edu.nd.crc.safa.warnings;

import java.util.ArrayList;
import java.util.List;

/**
 * The modules that parses a rule definition into a list of tokens.
 */
public class Tokenizer {

    public static List<Token> lex(String input) {
        String buffer = "";
        int depth = 0;
        boolean isFunc = false;

        List<Token> result = new ArrayList<Token>();
        for (int i = 0; i < input.length(); i++) {
            switch (input.charAt(i)) {
                case '(':
                    if (!buffer.isEmpty()) {
                        result.add(new Token(TokenType.FUNC_START, buffer));
                        depth = 1;
                        isFunc = true;
                        buffer = "";
                    } else {
                        result.add(new Token(TokenType.LEFT_PAREN, "("));
                        depth++;
                    }
                    break;
                case ')':
                    depth--;

                    if (depth == 0 && isFunc) {
                        isFunc = false;
                        if (!buffer.isEmpty()) {
                            result.add(new Token(TokenType.ARGUMENT, buffer));
                            buffer = "";
                        }
                        result.add(new Token(TokenType.FUNC_END, ")"));
                    } else {
                        result.add(new Token(TokenType.RIGHT_PAREN, ")"));
                    }
                    break;
                case ',':
                    if (!buffer.isEmpty()) {
                        result.add(new Token(TokenType.ARGUMENT, buffer));
                        buffer = "";
                    }
                    break;
                case '&':
                    if (input.charAt(i + 1) == '&') {
                        result.add(new Token(TokenType.AND, "&&"));
                        i++;
                    } else {
                        buffer += input.charAt(i);
                    }
                    break;
                case '|':
                    if (input.charAt(i + 1) == '|') {
                        result.add(new Token(TokenType.OR, "||"));
                        i++;
                    } else {
                        buffer += input.charAt(i);
                    }
                    break;
                case '!':
                    result.add(new Token(TokenType.NOT, "!"));
                    break;
                default:
                    if (!Character.isWhitespace(input.charAt(i))) {
                        buffer += input.charAt(i);
                    }
                    break;
            }
        }
        return result;
    }
}
