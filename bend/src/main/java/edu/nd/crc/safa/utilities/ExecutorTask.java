package edu.nd.crc.safa.utilities;

/**
 * No input or output function that might throw {@link Exception}
 */
@FunctionalInterface
public interface ExecutorTask {

    void run() throws Exception;
}
