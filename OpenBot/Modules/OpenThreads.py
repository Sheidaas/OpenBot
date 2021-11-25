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
        if not threadName in self.thread_names:
            self.thread_names.append(threadName)
            thread.start_new_thread(self.loopMethod,args)
        else:
            chat.appendChat(7,"Error: ThreadName already in use. Aborting." )

    def createLoopedThread_buffered(self, pauseTime, print_result, debugLog_result, save_result, threadName):
        """
        This will create a buffered looped Thread. An Array called "threadName_Buffer" will be created in the Thread instance (self).
        This thread will sleep in loop until an methodObj is added to the list. see OpenThreads.methodObj(method, args) for more details.
        After each execution the result is Printed, logged, and/or saved inside an Array in the Thread Object with the passedThreadName + "Result" 
        -> threadName = "test" -> self.testResult <- Array!  

        The Method needs to import any necessary modules itself, otherwise pass them along as arguments where applicable.
        """

        args = (pauseTime,print_result,debugLog_result,save_result,threadName,)
        if not threadName in self.thread_names:

            self.thread_names.append(threadName)
            thread.start_new_thread(self.loopMethod_buffered,args)
        else: 
            chat.appendChat(7,"Error: ThreadName already in use. Aborting.")

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


    def loopMethod_buffered(self, pauseTime, print_result, debugLog_result, save_result, threadName ):
        import time, OpenLog, chat 
        """
        Do not Call manually. Use createLoopedThread_buffered instead.
        """
        
        setattr(self, threadName+"_Buffer", [])
        buffer = getattr(self,threadName+"_Buffer")

        if(save_result):
            setattr(self, threadName+"Results", [])
            x = getattr(self, threadName + "Results")

        while threadName in self.thread_names:
            chat.AppendChat(7,"while loop running.")
            
            arg_list = []
            method = None

            if len(buffer)<1:
                time.sleep(pauseTime)
                continue
            else:
                obj:methodObj = buffer.pop(0)

                for arg in obj.args:
                    arg_list.append(arg)


            if not None == obj.method:
                result = method(*arg_list)    
            else: 
                chat.AppendChat(7,"Warning: loop-method got object without method!")
                OpenLog.DebugPrint("Warning: loop-method got object without method! Printing Arg_List: " + str(arg_list))
            
            if not None == result:
                for s in result:
                    if(print_result):
                        chat.AppendChat(7, str(s))
                    if(debugLog_result):
                        OpenLog.DebugPrint(str(s))
                    if(save_result):
                        x.append(s)
            #chat.AppendChat(7,"sleep Started " + str(pauseTime) + " ms")
            time.sleep(pauseTime)
            #chat.AppendChat(7,"sleepDone")
        #chat.AppendChat(7,"Debug: Thread " + threadName + " interrupted and stopped.")

    
    def stopThread(self,name):
        chat.AppendChat(7,"stopThread executed")
        if (name in self.thread_names):
            self.thread_names.remove(name)
        else :
            chat.AppendChat(7,"Thread Name not defined.")


#Wrapper Class for methods, to be able to create array "Buffer" containing those objects. 
class methodObj: 
    def __init__(self,method, method_args) -> None:
        self.method = method
        self.args = method_args
