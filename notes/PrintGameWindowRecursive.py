

## Print Game Window recursive.

self.gameWindow = Hooks.GetGameWindow()


def run(self,gameWindow):
    self.obj_printed = []
    self.gw = gameWindow
    def print_object(self,obj, objname, prev_path):
        import OpenLog
        import types
        if obj in self.obj_printed:
        	return
        self.obj_printed.append(obj)

        if objname=="__weakref__" or "refine_element" in objname or "dlgRefine" in objname:
            return

        OpenLog.DebugPrintNT("")
        OpenLog.DebugPrintNT("#")
        OpenLog.DebugPrintNT("# Object: " + objname )
        OpenLog.DebugPrintNT("#")
        OpenLog.DebugPrintNT("")
        OpenLog.DebugPrintNT("")
        if obj.__doc__:
        	OpenLog.DebugPrintNT(str("Obj. Doc: " + str(obj.__doc__)))
        OpenLog.DebugPrintNT("________")

        for x in dir(obj):
        	#OpenLog.DebugPrintNT("Debug: next is " + str(x))

            try:
                y = getattr(obj,x)
                if callable(y):

                    try:
                        OpenLog.DebugPrintNT("METHOD: "+prev_path +"."+ x + str(y.__code__.co_varnames))
                    except AttributeError:
                        OpenLog.DebugPrintNT("METHOD: "+prev_path +"."+ x + "([unknown args])")
                    continue
                else:

                    OpenLog.DebugPrintNT(str("DATA: "+prev_path +"."+ x + "  =  " + str(y)))

                if isinstance(y,types.ModuleType):
                    continue
                elif not isinstance(y,int) and not isinstance(y,str) and y != None and objname != x and not isinstance(y,dict) and not isinstance(y,list) and not isinstance(y,tuple):
                    print_object(self,y,x,prev_path+"."+x)
            except AttributeError:
                continue

        OpenLog.DebugPrintNT("________")
    print_object(self,self.gw,"GameWindow","GameWindow")

run(self,self.gameWindow)