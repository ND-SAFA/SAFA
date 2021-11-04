package edu.nd.crc.safa.importer.tracegenerator;

public interface PairConstructor<Key, Value> {

    Value createPair(Key source, Key target);
}
