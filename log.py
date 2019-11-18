import logging
import os
def logerr(e):
    pat=os.getcwd()
    pathh= os.path.join(pat, 'BMJ_log_file.log')
    logging.basicConfig(filename=pathh, filemode='w', format='%(name)s - %(levelname)s - %(message)s')
    logger=logging.getLogger(__name__)
    logger.error(e)
    print("log file created",pathh)


