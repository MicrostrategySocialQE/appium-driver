import json
import requests


class Component:
    button = "b"
    input = "i"
    view = "v"
    label = "l"
    table = "t"
    cell = "c"
    image = "im"
    scroll = "s"
    ctcLabel = "cl"
    ctcView = "cv"
    TextView = 'tv'
    TextArea = 'ta'


class MTDriver(object):
    """
    Controls a mobile device by sending commands to the MonkeyTalk agent server.
    """

    def __init__(self, host):
        """
        @param host: ip address and port number related to a device, example: 10.197.115.18:16863
        """
        self.host = host
        self.device, self.port = self.host.split(':')
        self.type = 'iOS' if self.port == "16863" else "Android"

    def componentType(self, component):
        """
        return the actual type of component for iOS or Android
        """
        if component == "*" or len(component) > 3:
            return component

        ios_type = dict(
            i="UITextField",
            v="UIView",
            b="UIButton",
            t="UITableView",
            c="UITableViewCell",
            im="MIImageView",
            l="UILabel",
            cl="UILabel",
            tv="UITextView",
            ta="UITextArea",
            s="UIScrollView"
        )
        android_type = dict(
            i="Input",
            b="Button",
            t="Table",
            v="View",
            cv="CTCView",
            cl="CTCLabel",
            l="Label",
            ta='TextArea'
        )

        table = ios_type if self.type == "iOS" else android_type
        if component in table:
            return table[component]
        return component

    def execute(self, monkeyId, action, component, args=[]):
        """
        execute monkey talk command
        """
        if not isinstance(args, list):
            args = [args]
        component = self.componentType(component)

        body = dict(
            timestamp=1360000000,
            mtcommand="PLAY",
            monkeyId=monkeyId,
            args=args,
            action=action,
            componentType=component,
            modifiers={"thinktime": 1000, "timeout": 2000}
        )

        print '[ ', action, monkeyId, component, args, ' ]'

        try:
            response = requests.post(
                ''.join(["http://", self.host, "/fonemonkey/"]),
                json.dumps(body)
            )
            response = json.loads(response.text)
            print json.dumps(response, indent=4)
            return response
        except Exception, e:
            print e
            return False


if __name__ == "__main__":
    t = MTDriver("10.197.116.235:16863")
    #t.execute("*", "Swipe", "t", "up")

    #t.Swipe("device", '*', 'down')
    #print t.DumpViewData("t")
    #t.execute("#1", 'Swipe', 'MIUInboxCellMainView', 'left')
    #t.execute("*", "Scroll", "t", ['cust', '{0, -180}'])
    t.execute("#1", "Drag", 't', ["{50, 400};{50, 500}"])