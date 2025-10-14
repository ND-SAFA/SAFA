package edu.nd.crc.safa.test.services.builders;

import java.util.function.BiFunction;
import java.util.function.Consumer;
import java.util.function.Function;

import lombok.AllArgsConstructor;
import org.apache.logging.log4j.util.TriConsumer;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@AllArgsConstructor
public class AndBuilder<Parent, ReturnType> {
    private final Logger logger = LoggerFactory.getLogger(AndBuilder.class);

    Parent parent;
    ReturnType returnValue;
    BuilderState state;

    public ReturnType get() {
        return this.returnValue;
    }

    public Parent and() {
        return this.parent;
    }

    public Parent and(String message) {
        logger.info(message);
        return and();
    }

    public Parent consume(TriConsumer<Parent, BuilderState, ReturnType> consumer) {
        consumer.accept(this.parent, this.state, this.returnValue);
        return this.parent;
    }

    public Parent consume(Consumer<ReturnType> consumer) {
        consumer.accept(this.returnValue);
        return this.parent;
    }

    public <T> AndBuilder<Parent, T> map(Function<ReturnType, T> consumer) {
        T result = consumer.apply(this.returnValue);
        return new AndBuilder<>(this.parent, result, this.state);
    }

    public <T> AndBuilder<Parent, T> map(BiFunction<BuilderState, ReturnType, T> mapFunc) {
        T result = mapFunc.apply(this.state, this.returnValue);
        return new AndBuilder<>(this.parent, result, this.state);
    }

    public <T> AndBuilder<Parent, T> run(BiFunction<BuilderState, Parent, T> func) {
        T result = func.apply(this.state, this.parent);
        return new AndBuilder<>(this.parent, result, this.state);
    }

    public AndBuilder<Parent, ReturnType> save(String name) {
        state.save(name, this.returnValue);
        return this;
    }
}
