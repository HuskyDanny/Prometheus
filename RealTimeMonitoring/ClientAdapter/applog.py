'''
#Usage:
from AppLog import AppLog
appLog = AppLog('MyAppName')

appLog.Write('App.Start','Hello World')
appLog.Write('WebApi.Request', {'action': 'api', 'path': request.path})
try: 1/0
except: appLog.Write('App.Exception', sys.exc_info(), AppLog.Level.Error)
appLog.Flush()

Note: manual .Flush() is not strictly required - it is called every _flush_interval seconds and @atexit
'''

try: import queue
except: import Queue as queue
import platform, os, io, time, threading, random, json, requests, sys, traceback, atexit

class AppLog(object):
    _max_queue_size = 5000 # events
    _flush_interval = 10 # seconds
    _flush_timeout  = 10 # seconds

    debug   = False
    domain  = os.environ.get('REGION_NAME', 'None').replace(' ','')
    machine = platform.node()
    user    = os.environ.get('USERNAME', os.environ.get('USER'))
    pid     = os.getpid()
    tag     = None
    cor     = None
    seq     = 0

    class Level:
        Critical    = 1
        Error       = 2
        Warning     = 3
        Information = 4
        Verbose     = 5

    def __init__(self, app, host='https://client:clobotix@dab615002f1f0e4533dfffad060755dc.us-east-1.aws.found.io:9243/', index='applog-%Y%m%d'):
        self.app   = app
        self.host  = host
        self.index = index
        self.queue = AppLog._Queue(self._max_queue_size)
        AppLog._Poll(self.Flush, self._flush_interval).start()
        atexit.register(self.Flush)

    def Write(self, eventType, data = None, level = Level.Information):
        ''' Writes an event to AppLog
        eventType: event type/name
        data: str, dict or Exception/sys.exc_info()
        level: severity level
        '''

        self.seq += 1
        envelope = dict(
            time    = int(1000 * time.time()),
            type    = eventType,
            app     = self.app,
            domain  = self.domain,
            machine = self.machine,
            user    = self.user,
            pid     = self.pid,
            seq     = self.seq,
            level   = level
        )

        if self.tag:
            envelope['tag'] = self.tag

        if self.cor:
            envelope['cor'] = self.cor

        if isinstance(data, dict):
            envelope['data'] = data
        elif isinstance(data, str):
            envelope['text'] = data
        elif isinstance(data, BaseException):
            envelope['error'] = dict(
                type = type(data).__name__,
                message = str(data),
                stackTrace = traceback.format_tb(data.__traceback__) if hasattr(data,'__traceback__') else None
            )
        elif isinstance(data, tuple) and len(data)==3:
            envelope['error'] = dict(
                type = data[0].__name__,
                message = str(data[1]),
                stackTrace = traceback.format_tb(data[2]) if data[2] else None
            )

        self.queue.Enqueue(envelope)

        if self.debug:
            print(json.dumps(envelope, ensure_ascii=False, separators=(',',':'), default=lambda o:None if o is None else str(o)));

    def Flush(self):
        ''' Flushes events queue (bulk-posts them to ElasticSearch) '''
        (cc, bulk) = self.queue.ESBulk()
        if bulk and self.host:
            try:
                with Stopwatch() as sw:
                    res = requests.post("http://localhost:5000/write", 
                                        headers = {'Content-type':'application/json'},
                                        timeout = (3.1, self._flush_timeout),
                                        data = bulk)

                if res.status_code == 200:
                    print('AppLog.Flush: OK %d items in %d ms' % (cc, sw.ElapsedMs))
                else:
                    print('?AppLog.Flush: FAIL %d items in %d ms: %s' % (cc, sw.ElapsedMs, res.text or '?'))

            except Exception as ex:
                print('?AppLog.Flush: DROP %d items in %d ms: %s' % (cc, sw.ElapsedMs, ex))

    class _Queue(queue.Queue):
        def __init__(self, maxsize = 0):
            queue.Queue.__init__(self, maxsize)

        def Enqueue(self, envelope):
            try: self.put_nowait(envelope)
            except queue.Full: pass

        def ESBulk(self):
            # Serializes itself into ElasticSearch-specific bulk format
            # https://www.elastic.co/guide/en/elasticsearch/reference/5.5/docs-bulk.html

            cc = 0
            try:
                import cStringIO
                bw = cStringIO.StringIO()
            except:
                bw = io.StringIO()
            
            bw.write('[')
            json.dump(self.get_nowait(), bw, ensure_ascii=False, separators=(',',':'), default=lambda o:None if o is None else str(o))
            for envelope in self:
                cc += 1
                bw.write(',')
                json.dump(envelope, bw, ensure_ascii=False, separators=(',',':'), default=lambda o:None if o is None else str(o))
            bw.write(']')
            print(bw.getvalue())
            return (cc, bw.getvalue())
        
        def __iter__(self):
            while 1:
                try: yield self.get_nowait()
                except queue.Empty: break

    class _Poll(threading.Thread):
        def __init__(self, action, interval):
            threading.Thread.__init__(self)
            self.setDaemon(True)
            self.action = action
            self.interval = interval

        def run(self):
            while True:
                time.sleep(self.interval + 2.5 - random.random()*5)
                self.action()

class Stopwatch(object):
    def __init__(self): self.tt = time.time(); self._ms = None
    def __enter__(self): return self
    def __exit__(self,et,ev,tb): self._ms = int(round((time.time() - self.tt) * 1000))
    @property
    def ElapsedMs(self): return self._ms or int(round((time.time() - self.tt) * 1000))

