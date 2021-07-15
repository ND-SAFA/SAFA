package edu.nd.crc.safa.warnings;

import java.util.ArrayList;
import java.util.List;

public class Tokenizer {
    public static enum Type {
        LPAREN, RPAREN, FUNCS, FUNCE, ARGUMENT, NOT, AND, OR, TRUE, FALSE;
    }

    public static class Token {
        public final Type t;
        public final String c;

        public Token(Type t, String c) {
            this.t = t;
            this.c = c;
        }

        public String toString() {
            if (t == Type.FUNCS) {
                return "FUNCTION<" + c + ">";
            }
            if (t == Type.FUNCE) {
                return "FUNCTION END";
            }
            if (t == Type.ARGUMENT) {
                return "ARGUMENT<" + c + ">";
            }
            return t.toString();
        }

        public boolean isBoolean() {
            return t == Type.TRUE || t == Type.FALSE;
        }
    }

    public static List<Token> lex(String input) {
        String buffer = "";
        int depth = 0;
        boolean isFunc = false;

        List<Token> result = new ArrayList<Token>();
        for (int i = 0; i < input.length(); i++) {
            switch (input.charAt(i)) {
                case '(':
                    if (!buffer.isEmpty()) {
                        result.add(new Token(Type.FUNCS, buffer));
                        depth = 1;
                        isFunc = true;
                        buffer = "";
                    } else {
                        result.add(new Token(Type.LPAREN, "("));
                        depth++;
                    }
                    break;
                case ')':
                    depth--;

                    if (depth == 0 && isFunc) {
                        isFunc = false;
                        if (!buffer.isEmpty()) {
                            result.add(new Token(Type.ARGUMENT, buffer));
                            buffer = "";
                        }
                        result.add(new Token(Type.FUNCE, ")"));
                    } else {
                        result.add(new Token(Type.RPAREN, ")"));
                    }
                    break;
                case ',':
                    if (!buffer.isEmpty()) {
                        result.add(new Token(Type.ARGUMENT, buffer));
                        buffer = "";
                    }
                    break;
                case '&':
                    if (input.charAt(i + 1) == '&') {
                        result.add(new Token(Type.AND, "&&"));
                        i++;
                    } else {
                        buffer += input.charAt(i);
                    }
                    break;
                case '|':
                    if (input.charAt(i + 1) == '|') {
                        result.add(new Token(Type.OR, "||"));
                        i++;
                    } else {
                        buffer += input.charAt(i);
                    }
                    break;
                case '!':
                    result.add(new Token(Type.NOT, "!"));
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
