from SystemParameters import LOGFILE_NAME, OUTPUT_PATH

class Logger(object):

    @staticmethod
    def writeout(msg, newline):
        """
        Write out to file
        """

        with open(OUTPUT_PATH + LOGFILE_NAME, 'a') as file:
            if newline:
                file.write('\n')
            file.write(str(msg))

    @staticmethod
    def log(msg):
        """
        Default log method - prints and writes to file
        """

        print(msg)
        Logger.writeout(msg, newline=False)

    @staticmethod
    def logn(msg):
        """
        Log method - prints and writes to file with line break
        """

        print(msg)
        Logger.writeout(msg, newline=True)
