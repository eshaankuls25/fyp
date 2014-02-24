import itertools, execnet, sys

#Source: http://www.packtpub.com/article/using-execnet-parallel-and-distributed-processing-nltk
def map(mod, args, options=[('popen', 2)]): #2 = no of processes to spawn
        gateways = []
        channels = []

        for option, count in options:
                for i in range(count):
                        gw = execnet.makegateway(option)
                        gateways.append(gw)
                        channels.append(gw.remote_exec(mod))
        cyc = itertools.cycle(channels)

        for i, arg in enumerate(args):
                channel = cyc.next()
                channel.send((i, arg))

        mch = execnet.MultiChannel(channels)
        queue = mch.make_receive_queue()
        l = len(args)
        results = [None] * l

        for j in range(l):
                if j+1 <= sys.maxint:
                        print "\nProcessing document no. %d..." %(j+1)
                channel, (i, result) = queue.get()
                results[i] = result

        for gw in gateways:
                gw.exit()
        return results
