import datetime

class FileSystem:
    """The file system stub."""

    def __init__(self):
        self.__files = ["file1.txt", "file2.txt"]
        self.__space = 12345

    def files(self):
        """Return the list of files."""
        return self.__files

    def space(self):
        """Return the free space in storage."""
        return self.__space

class Service:
    """Any service."""

    @staticmethod
    def name():
        """Return the name of service."""
        raise NotImplementedError

    def handle_request(self, command, *args):
        """Handle request."""
        raise NotImplementedError



class Comp:                                                                     
    """Computer."""

    def __init__(self):                                                         
        self.__iface = NetworkInterface()                                       
        self.__data = []                                                        
        self.handlers = {}
        self.__fs = FileSystem()

    def send_request(self, dst, name, command, *args):
        """Send to destination (dst) some (name) request with command
        and optional args."""
        ans = dst.handlers[name](command, *args)
        print(ans)

    def add_service(self, srv):
        """Add service to computer."""
        self.handlers[srv.name()] = srv.handle_request

    def file_system(self):
        """Give access to the file system."""
        return self.__fs
    
    def iface(self):                                                            
        """Return network interface."""
        return self.__iface                                                     

    def ping(self, addr):                                                      
        """Send ping to address."""
        return self.iface().ping(addr)     


class NetworkInterface:                                                         
    """Network interface."""

    def __init__(self):                                                         
        self.net = None                                                         
        self.addr = None                                                        
                                                               

    def setup(self, net, addr):                                                 
        """Set net and address to interface."""
        self.net = net                                                          
        self.addr = addr                                                        

    def ping(self, addr):                                                       
        """Send ping to address."""
        if not self.net:                                                        
            return "No network"                                                 
        return self.net.ping(self.addr, addr)     



class Files(Service):
    """The service providing the work with files."""

    @staticmethod
    def name():
        return "files"

    def __init__(self, comp):
        self.__comp = comp

    def handle_request(self, command, *args):
        if command == "list":
            return self.list_of_files()

        if command == "space":
            return self.free_space()

        return "Error"

    def list_of_files(self):
        """Return the list of files."""
        return self.__comp.file_system().files()

    def free_space(self):
        """Return the free space in storage."""
        return self.__comp.file_system().space()


class Clock(Service):
    """Time service."""

    @staticmethod
    def name():
        return "clock"

    def handle_request(self, command, *args):
        if command == "now":
            if args[0] == "local":
                return '{0:%Y-%m-%d %H:%M:%S}'.format(
                    datetime.datetime.now())

            if args[0] == "utc":
                return '{0:%Y-%m-%d %H:%M:%S}'.format(
                    datetime.datetime.utcnow())

            return "Wrong args"

        return "Unknown command"                             
                                     


class Network:                                                                  
    """Network represents net."""

    def __init__(self):                                                        
        self.mailstore = None
        self.__hosts = {}                                                       

    def add_host(self, comp, addr):                                             
        """Add host to net."""
        self.__hosts[addr] = comp                                               
        comp.iface().setup(self, addr)                                          

    def ping(self, src, dst):                                                   
        """Ping sends ping to host."""
        if dst in self.__hosts:                                                 
            return f"ping from {src} to {dst}"                                  
        return "Unknown host"                                                   

def main():
    """Run example."""

    comp1 = Comp()
    comp2 = Comp()

    comp2.add_service(Files(comp2))
    comp2.add_service(Clock())

    comp1.send_request(comp2, "files", "list")
    comp1.send_request(comp2, "files", "space")
    print()

    comp1.send_request(comp2, "clock", "now", "local")
    comp1.send_request(comp2, "clock", "now", "utc")
    comp1.send_request(comp2, "clock", "now", "+3")
    comp1.send_request(comp2, "clock", "date of birth", "Pushkin")


if __name__ == "__main__":
    main()                             
