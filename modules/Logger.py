from SystemParameters import LOGFILE_NAME

class Logger(object):

    @staticmethod
    def writeout(msg):
        """
        Write out to file
        """

        with open('../' + LOGFILE_NAME, 'a') as file:
            file.write('\n' + str(msg))

    @staticmethod
    def log(msg):
        """
        Default log method - prints and writes to file
        """

        print(msg)
        Logger.writeout(msg)
