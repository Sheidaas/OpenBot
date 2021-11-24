import thread
import time
import chat

class OpenThread:

    
    thread_names = []
    

    def createThread(self,method, args):

        """
        Creates a new Thread with the passed method. This thread is anonymous, 
        cannot be controled and will exit itself when method execution is done.
        """

        arg_list = []
        for arg in args:
            arg_list.append(arg)

        thread.start_new_thread(method, tuple(arg_list))

    def createLoopedThread(self, method, method_args, pauseTime, print_result, debugLog_result, save_result, threadName):
        """
        This will create a looped Thread with the specified Method and the specified args.
        After each execution the result is Printed, logged, and/or saved inside an Array in the Thread Object with the passedThreadName + "Result" 
        -> threadName = "test" -> self.testResult <- Array!  

        The Method needs to import any necessary modules itself, otherwise pass them along as arguments where applicable.
        """

        args = (method,method_args,pauseTime,print_result,debugLog_result,save_result,threadName,)
        self.thread_names.append(threadName)
        thread.start_new_thread(self.loopMethod,args)

    def loopMethod(self, method, method_args, pauseTime, print_result, debugLog_result, save_result, threadName ):
        import time, OpenLog, chat 
        """
        Do not Call manually. Use createLoopedThread instead.
        """
        arg_list = []
        for arg in method_args:
            arg_list.append(arg)

        if(save_result):
            setattr(self, threadName+"Results", [])
            x = getattr(self, threadName + "Results")

        while threadName in self.thread_names:
            chat.AppendChat(7,"while loop running.")
            
            result = method(*arg_list)
            if not None == result:
                for s in result:
                    if(print_result):
                        chat.AppendChat(7, str(s))
                    if(debugLog_result):
                        OpenLog.DebugPrint(str(s))
                    if(save_result):
                        x.append(s)
            chat.AppendChat(7,"sleep Started " + str(pauseTime) + " ms")
            time.sleep(pauseTime)
            chat.AppendChat(7,"sleepDone")
        chat.AppendChat(7,"Thread with name " + threadName + " interrupted and stopped.")
    
    def stopThread(self,name):
        chat.AppendChat(7,"stopThread executed")
        if (name in self.thread_names):
            self.thread_names.remove(name)
        else :
            chat.AppendChat(7,"Thread Name not defined.")