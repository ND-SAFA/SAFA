package edu.nd.crc.safa.features.rules.parser;

import java.util.ArrayList;
import java.util.List;

import lombok.AccessLevel;
import lombok.NoArgsConstructor;

/**
 * The modules that parses a rule definition into a list of tokens.
 */
@NoArgsConstructor(access = AccessLevel.PRIVATE)
public class Tokenizer {

    public static List<Token> lex(String input) {
        StringBuilder buffer = new StringBuilder();
        int depth = 0;
        boolean isFunc = false;

        List<Token> result = new ArrayList<>();
        for (int i = 0; i < input.length(); i++) {
            switch (input.charAt(i)) {
                case '(':
                    if (!buffer.toString().isEmpty()) {
                        result.add(new Token(TokenType.FUNC_START, buffer.toString()));
                        depth = 1;
                        isFunc = true;
                        buffer = new StringBuilder();
                    } else {
                        result.add(new Token(TokenType.LEFT_PAREN, "("));
                        depth++;
                    }
                    break;
                case ')':
                    depth--;

                    if (depth == 0 && isFunc) {
                        isFunc = false;
                        if (!buffer.toString().isEmpty()) {
                            result.add(new Token(TokenType.ARGUMENT, buffer.toString()));
                            buffer = new StringBuilder();
                        }
                        result.add(new Token(TokenType.FUNC_END, ")"));
                    } else {
                        result.add(new Token(TokenType.RIGHT_PAREN, ")"));
                    }
                    break;
                case ',':
                    if (!buffer.toString().isEmpty()) {
                        result.add(new Token(TokenType.ARGUMENT, buffer.toString()));
                        buffer = new StringBuilder();
                    }
                    break;
                case '&':
                    if (input.charAt(i + 1) == '&') {
                        result.add(new Token(TokenType.AND, "&&"));
                        i++;
                    } else {
                        buffer.append(input.charAt(i));
                    }
                    break;
                case '|':
                    if (input.charAt(i + 1) == '|') {
                        result.add(new Token(TokenType.OR, "||"));
                        i++;
                    } else {
                        buffer.append(input.charAt(i));
                    }
                    break;
                case '!':
                    result.add(new Token(TokenType.NOT, "!"));
                    break;
                default:
                    if (!Character.isWhitespace(input.charAt(i))) {
                        buffer.append(input.charAt(i));
                    }
                    break;
            }
        }
        return result;
    }
}
