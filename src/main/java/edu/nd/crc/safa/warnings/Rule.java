package edu.nd.crc.safa.warnings;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;

import edu.nd.crc.safa.db.entities.sql.Warning;

public class Rule {
    private final RuleName mRuleName;
    public List<Token> mTokens;
    List<String> ImplementedFunctions = Arrays.asList(
        "at-least-one",
        "at-least-n",
        "exactly-one",
        "exactly-n",
        "less-than-n"
    );
    String mText;

    public Rule(Rule that) {
        mRuleName = that.mRuleName;
        mText = that.mText;
        mTokens = new ArrayList<>(that.mTokens);
    }

    public Rule(final String name, final String longname, final String rule) {
        mRuleName = new RuleName(name, longname);
        mText = rule;
        mTokens = Tokenizer.lex(mText);
    }

    public Rule(Warning warning) {
        this(warning.getNShort(), warning.getNLong(), warning.getRule());
    }

    public RuleName getName() {
        return mRuleName;
    }

    public String unprocessedRule() {
        return mText;
    }

    public boolean isRuleSatisfied() {
        return mTokens.get(0).tokenType == TokenType.TRUE;
    }

    public boolean isValid() {
        // Handle unbalanced parenthesis
        long lParenCount = mTokens.stream().filter(t -> t.tokenType == TokenType.LEFT_PAREN).count();
        long rParenCount = mTokens.stream().filter(t -> t.tokenType == TokenType.RIGHT_PAREN).count();
        if (lParenCount != rParenCount) {
            return false;
        }

        // Handle unbalanced function
        long fStartCount = mTokens.stream().filter(t -> t.tokenType == TokenType.FUNC_START).count();
        long fEndCount = mTokens.stream().filter(t -> t.tokenType == TokenType.FUNC_END).count();
        if (fStartCount != fEndCount) {
            return false;
        }

        // Handle functions that are not implemented
        return mTokens
            .stream()
            .filter(t -> t.tokenType == TokenType.FUNC_START)
            .anyMatch(t -> ImplementedFunctions.contains(t.value));
    }

    public Optional<Function> parseFunction() {
        Function function = new Function();

        String functionName = "";
        List<String> arguments = new ArrayList<>();
        for (final Token t : mTokens) {
            if (t.tokenType == TokenType.FUNC_START) {
                functionName = t.value;
            }

            if (t.tokenType == TokenType.ARGUMENT) {
                arguments.add(t.value);
            }

            if (t.tokenType == TokenType.FUNC_END) {
                break;
            }
        }

        if (functionName.equals("")) {
            return Optional.empty();
        }

        int argOffset = 0;
        switch (functionName) {
            case "at-least-one":
                function.condition = Condition.AT_LEAST;
                function.count = 1;
                break;
            case "at-least-n":
                function.condition = Condition.AT_LEAST;
                function.count = Integer.parseInt(arguments.get(0).trim());
                argOffset++;
                break;
            case "exactly-one":
                function.condition = Condition.EXACTLY;
                function.count = 1;
                break;
            case "exactly-n":
                function.condition = Condition.EXACTLY;
                function.count = Integer.parseInt(arguments.get(0).trim());
                argOffset++;
                break;
            case "less-than-n":
                function.condition = Condition.LESS_THAN;
                function.count = Integer.parseInt(arguments.get(0).trim());
                argOffset++;
                break;
            default:
        }

        function.targetArtifactType = arguments.get(argOffset).trim().toLowerCase();
        String nextArgument = arguments.get(argOffset + 1).trim().toLowerCase();
        switch (nextArgument) {
            case "child":
                function.relationship = Relationship.CHILD;
                break;
            case "sibling":
                function.relationship = Relationship.SIBLING;
                break;
            default:
        }
        function.sourceArtifactType = arguments.get(argOffset + 2).trim().toLowerCase();

        return Optional.of(function);
    }

    public void setFunctionResult(final boolean result) {
        int start = -1;
        int end = -1;
        for (int i = 0; i < mTokens.size(); i++) {
            final Token t = mTokens.get(i);
            if (t.tokenType == TokenType.FUNC_START) {
                start = i;
            }

            if (t.tokenType == TokenType.FUNC_END) {
                end = i;
                break;
            }
        }

        if (result) {
            mTokens.set(start, new Token(TokenType.TRUE, "True"));
        } else {
            mTokens.set(start, new Token(TokenType.FALSE, "False"));
        }

        for (int i = start; i < end; i++) {
            mTokens.remove(start + 1);
        }
    }

    public boolean reduce() {
        return reduceSingle(mTokens);
    }

    public boolean reduceSingle(List<Token> input) {
        // Handle Parenthesis groups
        int leftParen = -1;
        int rightParen = -1;
        for (int i = 0; i < input.size(); i++) {
            final Token t = input.get(i);
            if (t.tokenType == TokenType.LEFT_PAREN) {
                leftParen = i;
            }
            if (leftParen != -1 && t.tokenType == TokenType.RIGHT_PAREN) {
                rightParen = i;
                break;
            }
        }

        if (leftParen != -1 && rightParen != -1) {
            List<Token> group = input.subList(leftParen + 1, rightParen);
            reduceSingle(group);

            if (group.size() > 1) {
                return false;
            }

            final Token t = group.get(0);
            input.set(leftParen, t);
            input.remove(leftParen + 1);
            input.remove(leftParen + 1);
            return true;
        }

        // Handle Not
        for (int i = 0; i < input.size(); i++) {
            final Token t = input.get(i);
            if (t.tokenType == TokenType.NOT) {
                final Token b = input.get(i + 1);
                assert b.isBoolean();

                if (b.tokenType == TokenType.TRUE) {
                    input.set(i, new Token(TokenType.FALSE, "False"));
                } else {
                    input.set(i, new Token(TokenType.TRUE, "True"));
                }
                input.remove(i + 1);
                return true;
            }
        }

        // Handle AND
        for (int i = 0; i < input.size(); i++) {
            final Token t = input.get(i);
            if (t.tokenType == TokenType.AND) {
                final Token left = input.get(i - 1);
                assert left.isBoolean();
                final boolean leftBool = left.tokenType == TokenType.TRUE;

                final Token right = input.get(i + 1);
                assert right.isBoolean();
                final boolean rightBool = right.tokenType == TokenType.TRUE;

                if (leftBool && rightBool) {
                    input.set(i - 1, new Token(TokenType.TRUE, "True"));
                } else {
                    input.set(i - 1, new Token(TokenType.FALSE, "False"));
                }
                input.remove(i);
                input.remove(i);
                return true;
            }
        }

        // Handle OR
        for (int i = 0; i < input.size(); i++) {
            final Token t = input.get(i);
            if (t.tokenType == TokenType.OR) {
                final Token left = input.get(i - 1);
                assert left.isBoolean();
                final boolean leftBool = left.tokenType == TokenType.TRUE;

                final Token right = input.get(i + 1);
                assert right.isBoolean();
                final boolean rightBool = right.tokenType == TokenType.TRUE;

                if (leftBool || rightBool) {
                    input.set(i - 1, new Token(TokenType.TRUE, "True"));
                } else {
                    input.set(i - 1, new Token(TokenType.FALSE, "False"));
                }
                input.remove(i);
                input.remove(i);
                return true;
            }
        }

        return false;
    }
}
