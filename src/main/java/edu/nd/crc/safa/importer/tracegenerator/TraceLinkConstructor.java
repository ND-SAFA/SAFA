package edu.nd.crc.safa.importer.tracegenerator;

public interface TraceLinkConstructor<Key, Value> {

    Value createTracelink(Key source, Key target, double score);
}
