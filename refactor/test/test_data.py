TEST_SOURCE_LAYERS = [{"s1": "token1",
                       "s2": "token2",
                       "s3": "token3"}, {"s4": "token4",
                                         "s5": "token5",
                                         "s6": "token6"}]

TEST_TARGET_LAYERS = [{"t1": "token1",
                       "t2": "token2",
                       "t3": "token3"}, {"t4": "token4",
                                         "t5": "token5",
                                         "t6": "token6"}]
ALL_TEST_SOURCES = {id_: token for artifacts in TEST_SOURCE_LAYERS for id_, token in artifacts.items()}
ALL_TEST_TARGETS = {id_: token for artifacts in TEST_TARGET_LAYERS for id_, token in artifacts.items()}
TEST_POS_LINKS = [("s1", "t1"), ("s2", "t1"), ("s3", "t2"), ("s4", "t4"), ("s4", "t5"), ("s5", "t6")]
