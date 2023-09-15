package edu.nd.crc.safa.features.rules.parser;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;

/**
 * Defines the client-facing entity for defining a new rule that generates project warnings.
 */
public class ParserRule {
    private static final String FALSE = "False";
    private static final String TRUE = "True";
    private static final List<String> IMPLEMENTED_FUNCTIONS = Arrays.asList(
        "at-least-one",
        "at-least-n",
        "exactly-one",
        "exactly-n",
        "less-than-n"
    );
    private final RuleName mRuleName;
    private final List<Token> mTokens;
    private final String mText;
    private final String ruleString;

    public ParserRule(ParserRule that) {
        mRuleName = that.mRuleName;
        mText = that.mText;
        mTokens = new ArrayList<>(that.mTokens);
        this.ruleString = that.ruleString;
    }

    public ParserRule(final String name, final String description, final String rule) {
        mRuleName = new RuleName(name, description);
        mText = rule;
        mTokens = Tokenizer.lex(mText);
        this.ruleString = rule;
    }

    public String getRule() {
        return this.ruleString;
    }

    public RuleName getMRuleName() {
        return mRuleName;
    }

    public boolean isRuleSatisfied() {
        return mTokens.get(0).getTokenType() == TokenType.TRUE;
    }

    public boolean isValid() {
        // Handle unbalanced parenthesis
        long lParenCount = mTokens.stream().filter(t -> t.getTokenType() == TokenType.LEFT_PAREN).count();
        long rParenCount = mTokens.stream().filter(t -> t.getTokenType() == TokenType.RIGHT_PAREN).count();
        if (lParenCount != rParenCount) {
            return false;
        }

        // Handle unbalanced function
        long fStartCount = mTokens.stream().filter(t -> t.getTokenType() == TokenType.FUNC_START).count();
        long fEndCount = mTokens.stream().filter(t -> t.getTokenType() == TokenType.FUNC_END).count();
        if (fStartCount != fEndCount) {
            return false;
        }

        // Handle functions that are not implemented
        return mTokens
            .stream()
            .filter(t -> t.getTokenType() == TokenType.FUNC_START)
            .anyMatch(t -> IMPLEMENTED_FUNCTIONS.contains(t.getValue()));
    }

    public Optional<Function> parseFunction() {
        Function function = new Function();

        String functionName = "";
        List<String> arguments = new ArrayList<>();
        for (final Token t : mTokens) {
            if (t.getTokenType() == TokenType.FUNC_START) {
                functionName = t.getValue();
            }

            if (t.getTokenType() == TokenType.ARGUMENT) {
                arguments.add(t.getValue());
            }

            if (t.getTokenType() == TokenType.FUNC_END) {
                break;
            }
        }

        if (functionName.equals("")) {
            return Optional.empty();
        }

        int argOffset = 0;
        switch (functionName) {
            case "at-least-one":
                function.setCondition(Condition.AT_LEAST);
                function.setCount(1);
                break;
            case "at-least-n":
                function.setCondition(Condition.AT_LEAST);
                function.setCount(Integer.parseInt(arguments.get(0).trim()));
                argOffset++;
                break;
            case "exactly-one":
                function.setCondition(Condition.EXACTLY);
                function.setCount(1);
                break;
            case "exactly-n":
                function.setCondition(Condition.EXACTLY);
                function.setCount(Integer.parseInt(arguments.get(0).trim()));
                argOffset++;
                break;
            case "less-than-n":
                function.setCondition(Condition.LESS_THAN);
                function.setCount(Integer.parseInt(arguments.get(0).trim()));
                argOffset++;
                break;
            default:
        }

        function.setTargetArtifactType(arguments.get(argOffset).trim().toLowerCase());
        String nextArgument = arguments.get(argOffset + 1).trim().toLowerCase();
        switch (nextArgument) {
            case "child":
                function.setArtifactRelationship(ArtifactRelationship.CHILD);
                break;
            case "sibling":
                function.setArtifactRelationship(ArtifactRelationship.SIBLING);
                break;
            default:
        }
        function.setSourceArtifactType(arguments.get(argOffset + 2).trim().toLowerCase());

        return Optional.of(function);
    }

    public void setFunctionResult(final boolean rulePassed) {
        int start = -1;
        int end = -1;
        for (int i = 0; i < mTokens.size(); i++) {
            final Token t = mTokens.get(i);
            if (t.getTokenType() == TokenType.FUNC_START) {
                start = i;
            }

            if (t.getTokenType() == TokenType.FUNC_END) {
                end = i;
                break;
            }
        }

        if (rulePassed) {
            mTokens.set(start, new Token(TokenType.TRUE, TRUE));
        } else {
            mTokens.set(start, new Token(TokenType.FALSE, FALSE));
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
            if (t.getTokenType() == TokenType.LEFT_PAREN) {
                leftParen = i;
            }
            if (leftParen != -1 && t.getTokenType() == TokenType.RIGHT_PAREN) {
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
            if (t.getTokenType() == TokenType.NOT) {
                final Token b = input.get(i + 1);
                assert b.isBoolean();

                if (b.getTokenType() == TokenType.TRUE) {
                    input.set(i, new Token(TokenType.FALSE, FALSE));
                } else {
                    input.set(i, new Token(TokenType.TRUE, TRUE));
                }
                input.remove(i + 1);
                return true;
            }
        }

        // Handle AND
        for (int i = 0; i < input.size(); i++) {
            final Token t = input.get(i);
            if (t.getTokenType() == TokenType.AND) {
                final Token left = input.get(i - 1);
                assert left.isBoolean();
                final boolean leftBool = left.getTokenType() == TokenType.TRUE;

                final Token right = input.get(i + 1);
                assert right.isBoolean();
                final boolean rightBool = right.getTokenType() == TokenType.TRUE;

                if (leftBool && rightBool) {
                    input.set(i - 1, new Token(TokenType.TRUE, TRUE));
                } else {
                    input.set(i - 1, new Token(TokenType.FALSE, FALSE));
                }
                input.remove(i);
                input.remove(i);
                return true;
            }
        }

        // Handle OR
        for (int i = 0; i < input.size(); i++) {
            final Token t = input.get(i);
            if (t.getTokenType() == TokenType.OR) {
                final Token left = input.get(i - 1);
                assert left.isBoolean();
                final boolean leftBool = left.getTokenType() == TokenType.TRUE;

                final Token right = input.get(i + 1);
                assert right.isBoolean();
                final boolean rightBool = right.getTokenType() == TokenType.TRUE;

                if (leftBool || rightBool) {
                    input.set(i - 1, new Token(TokenType.TRUE, TRUE));
                } else {
                    input.set(i - 1, new Token(TokenType.FALSE, FALSE));
                }
                input.remove(i);
                input.remove(i);
                return true;
            }
        }

        return false;
    }
}
