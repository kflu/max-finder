from threading import Thread
import logging
import subprocess2 as sp
logging.basicConfig(level=logging.DEBUG)

class FindstrWorker(Thread):
    def __init__(self, queue, pattern, conf = None):
        Thread.__init__(self)
        self.__q = queue
        self.__pattern = pattern
        self.__conf = conf or {}

        self.__fill_conf()
        self.__validate_conf()

        self.__cmd = self.__build_cmd()

    def __fill_conf(self):
        '''Fill the conf dict with default values.
        '''
        logging.debug("before: %s" % self.__conf)
        defs = {
                "ignore_case":True,
                "printable_only":True,
                "recursive":True,
                "target_dir":['.'],
                "include_cwd":False,
                "filename_patterns":["*"],
                }
        for key in defs:
            self.__conf[key] = self.__conf.get(key, defs[key])
        logging.debug("after: %s" % self.__conf)
        return self.__conf

    def __validate_conf(self):
        '''Some validation.'''
        if len(self.__conf['target_dir']) > 1:
            # FindStr always return relative filename (relative to /d arguments).
            # It's hard to deduct which dir it is relative to. So let's restrict to
            # use only one target_dir.
            raise ValueError("multiple target directories are not supported.")

    def __normalize_result(self, line):
        '''Return a found line in the form of (file, line_num, line).
        '''
        # An example findstr return:
        # subprocess2.py:1513:            while read_set or write_set:
        res = line.split(':',2)
        # Let's simply trust res has the correct format: (file, line_num, line)
        return res

    def __build_cmd(self):
        '''Build command line list from the conf dict that Popen can use.
        '''
        logging.debug("Building command line list from the config: %s" % self.__conf)
        cmd = []
        cmd.append('findstr')

        # mandatory
        cmd.append('/n')    # prints line number

        # from conf dict
        if self.__conf['ignore_case'] == True:
            cmd.append('/i')
        if self.__conf['printable_only'] == True:
            cmd.append('/p')
        if self.__conf['recursive'] == True:
            cmd.append('/s')

        # Target dirs:
        if self.__conf['target_dir'][0] != '.':
            cmd.append('/d:%s' % self.__conf['target_dir'][0])

        cmd.append(self.__pattern)
        cmd.extend(self.__conf['filename_patterns'])

        logging.debug("Final command line list built: %s:" % cmd)
        return cmd

    def run(self):
        p = sp.Popen(self.__cmd, stdout=sp.PIPE, stderr=sp.PIPE)
        while p.poll() == None:
            buf = p.asyncread()
            if not buf: continue
            for line in buf.splitlines():
                self.__q.put( self.__normalize_result(line) )

if __name__ == '__main__':
    import Queue,sys
    q = Queue.Queue()

    f = FindstrWorker(q, sys.argv[1])
    logging.debug("running..")
    f.run()
    while f.is_alive():
        try:
            print q.get_nowait()
        except:
            pass

    while True:
        try:
            print q.get_nowait()
        except:
            break
