# pyinstaller main.py --clean --name heatmap --onefile -i"icon.ico" --paths "admix" --add-data "admix/data/K36.alleles;./data" --add-data "admix/data/K36.36.F;./data" --add-data "sciter/main.html;./sciter" --add-data="sciter/about.html;./sciter" --add-data="sciter/favicon.png;./sciter" --add-data="sciter/loading.png;./sciter" --add-data="sciter/sciter.png;./sciter" --add-data="sciter/simpleheat/heatmap.js;./sciter/simpleheat" --add-data="sciter/taux-de-similitude/index.js;./sciter/taux-de-similitude" --add-data="sciter/taux-de-similitude/fn.js;./sciter/taux-de-similitude" --add-data="sciter/taux-de-similitude/data.js;./sciter/taux-de-similitude" --add-data="sciter/taux-de-similitude/cells.js;./sciter/taux-de-similitude" --add-data="sciter/taux-de-similitude/america.png;./sciter" --add-data="sciter/taux-de-similitude/europe.png;./sciter" --add-data="sciter/taux-de-similitude/asia.png;./sciter" --add-data="sciter/128x128.png;./sciter" --windowed

import os
from admix.main import main
from threading import Thread

if os.name == 'nt': # making sure we're on Windows
	os.environ['PATH'] = os.getcwd() + ';' + os.environ['PATH']

import sciter
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class RootEventHandler(sciter.EventHandler):
    def __init__(self, el, frame):
        super().__init__(element=el)
        self.parent = frame
        pass

    def on_event(self, source, target, code, phase, reason):
        he = sciter.Element(source)
        #print("-> event:", code, phase, he)
        pass

    @sciter.script("mcall")
    def method_call(self, *args):
        #
        # `root.mcall()` (see handlers.htm) calls behavior method of the root dom element (native equivalent is `Element.call_method()`),
        #  so we need to attach a "behavior" to that element to catch and handle such calls.
        # Also it can be handled at script by several ways:
        # * `behavior` - Element subclassing with full control
        # * `aspect` - provides partial handling by attaching a single function to the dom element
        # *  manually attaching function to Element via code like `root.mcall = function(args..) {};`
        #
        print("->mcall args:", "\t".join(map(str, args)))
        # explicit null for example, in other cases you can return any python object like None or True
        return sciter.Value.null()

    pass

# main frame
class Frame(sciter.Window):
    def __init__(self):
        super().__init__(ismain=True, uni_theme=True)
        pass

    def on_subscription(self, groups):
        from sciter.event import EVENT_GROUPS
        return EVENT_GROUPS.HANDLE_ALL

    def on_script_call(self, name, args):
        return self.dispatch(name, args)


    def on_load_data(self, nm):
        print("loading", nm.uri)
        #nm.uri = sys._MEIPASS + '/' + nm.uri
        #print("changed to", nm.uri)
        pass

    @sciter.script
    def foo(self, input_filename):
        thread = Thread(target=main, args=(self, input_filename))
        thread.start()

    @sciter.script
    def bob(self, continent):
        from PIL import Image, ImageFilter
        import cv2
        import numpy as np

        print("bob(self, " + continent + ")")
        print(sys._MEIPASS + '/output.jpeg')

        img = Image.open(sys._MEIPASS + '/output.jpeg')

        img = img.filter(ImageFilter.GaussianBlur(radius=20))
        print(sys._MEIPASS + '/blurred.jpeg')
        img.save(sys._MEIPASS + '/blurred.jpeg')

        img = cv2.imread(sys._MEIPASS + '/blurred.jpeg')
        cv2.imwrite(sys._MEIPASS + '/blurred.jpg', img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

        img = cv2.imread(sys._MEIPASS + '/blurred.jpeg', cv2.IMREAD_GRAYSCALE)
        cv2.imwrite(sys._MEIPASS + '/grayscale.jpeg', img)


        img = cv2.applyColorMap(img, cv2.COLORMAP_JET)

        cv2.imwrite(sys._MEIPASS + '/' + continent + '.jpeg', img)

        #cv2.imshow('RESULT', img)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        return 'done'


if __name__ == '__main__':
    sciter.runtime_features(file_io=True, allow_sysinfo=True)
    frame = Frame()

    #read input file
    fin = open(resource_path('sciter/main.html'), "rt")
    #read file contents to string
    data = fin.read()
    #replace all occurrences of the required string
    data = data.replace('TEMP_FOLDER', "'" + sys._MEIPASS.replace("\\", '/') + "'")
    #close the input file
    fin.close()
    #open the input file in write mode
    fin = open(resource_path('sciter/main.html'), "wt")
    #overrite the input file with the resulting data
    fin.write(data)
    #close the file
    fin.close()

    frame.load_file(resource_path('sciter/main.html'))
    ev2 = RootEventHandler(frame.get_root(), frame)
    #frame.expand()
    frame.run_app()
