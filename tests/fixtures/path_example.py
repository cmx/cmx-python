if __name__ == '__main__':

    from cmx import doc
    from cmx.utils import SimpleLogger

    logger = SimpleLogger()
    doc.config("README.md", logger=logger)
    logger.job_started()
    doc @ """
    # README

    This is an example for using `cmx` with a simple logger.
    """
    doc.flush()


