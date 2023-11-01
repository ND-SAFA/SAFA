from tgen.scripts.run import run_rq


def run_rq_tool(rq: str):
    """
    Runs RQ.
    :param rq: RQ path.
    :return:
    """
    run_rq(rq)


RQ_TOOLS = [run_rq_tool]
