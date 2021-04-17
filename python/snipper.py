from __future__ import print_function, unicode_literals, absolute_import
from Xlib import X, display, Xutil
import mathpix, pyperclip, os, json, base64, io, gi, sys
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib, GdkPixbuf
from playsound import playsound
from PIL import Image

class Snipper:
    def __init__(self):               
        path = os.environ['HOME'] + '/.config/mathpixsnipper/'
        with open(path+'conf.json') as json_file:
            data = json.load(json_file)
        mathpix.default_headers['app_id'] =  data['app_id'] 
        mathpix.default_headers['app_key'] =  data['app_key']
                        
    def cdir(self):
        print(os.getcwd())

    def callmathpixapi(self, img):        
        os.getcwd()
        r = mathpix.latex({ 
            'src': mathpix.image_uri2(img),
            'formats': ['latex_simplified']
        })

        if 'error' in r:      
            return 'error_info ' + json.dumps(r['error_info'])
        
        return r'$$'+r['latex_simplified']+'$$'
        
class ClipboardWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Clipboard Example")

        grid = Gtk.Grid()

        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        self.entry = Gtk.Entry()
        self.image = Gtk.Image.new_from_icon_name("process-stop", Gtk.IconSize.MENU)

        button_copy_text = Gtk.Button(label="Copy Text")
        button_paste_text = Gtk.Button(label="Paste Text")
        button_copy_image = Gtk.Button(label="Copy Image")
        button_paste_image = Gtk.Button(label="Paste Image")

        grid.add(self.entry)
        grid.attach(self.image, 0, 1, 1, 1)
        grid.attach(button_copy_text, 1, 0, 1, 1)
        grid.attach(button_paste_text, 2, 0, 1, 1)
        grid.attach(button_copy_image, 1, 1, 1, 1)
        grid.attach(button_paste_image, 2, 1, 1, 1)

        button_copy_text.connect("clicked", self.copy_text)
        button_paste_text.connect("clicked", self.paste_text)
        button_copy_image.connect("clicked", self.copy_image)
        button_paste_image.connect("clicked", self.paste_image)

        self.add(grid)

    def copy_text(self, widget):
        self.clipboard.set_text(self.entry.get_text(), -1)

    def set_text(self, text):
        self.clipboard.set_text(text, -1)
        
    def paste_text(self, widget):
        text = self.clipboard.wait_for_text()
        if text is not None:
            self.entry.set_text(text)
        else:
            print("No text on the clipboard.")

    def copy_image(self, widget):
        if self.image.get_storage_type() == Gtk.ImageType.PIXBUF:
            self.clipboard.set_image(self.image.get_pixbuf())
        else:
            print("No image has been pasted yet.")

    def paste_image(self, widget):
        print('paste image pressed')
        image = self.clipboard.wait_for_image()
        if image is not None:
            self.image.set_from_pixbuf(image)
            
    def get_buffer(self):
        self.img = self.clipboard.wait_for_image()
        if self.img is not None:
            print('is not none')
            print(type(self.img))
            self.image.set_from_pixbuf(self.img)
            return self.pixbuf2image(self.img)

    def pixbuf2image(self, pix):
        """Convert gdkpixbuf to PIL image"""
        data = pix.get_pixels()
        w = pix.props.width
        h = pix.props.height
        stride = pix.props.rowstride
        mode = "RGB"
        if pix.props.has_alpha == True:
            mode = "RGBA"
        im = Image.frombytes(mode, (w, h), data, "raw", mode, stride)
        return im

def main():
    import os
    os.system('maim -s | xclip -selection clipboard -t image/png')

    # get image    
    win = ClipboardWindow()
    pil_image = win.get_buffer()

    # plot
    #%pylab inline
    #import matplotlib.pyplot as plt
    #import matplotlib.image as mpimg
    #imgplot = plt.imshow(pil_image)
    #plt.show()   

    snp = Snipper()  
    buf = io.BytesIO()
    pil_image.save(buf, format='PNG')
    byte_im = buf.getvalue()

    r = snp.callmathpixapi(byte_im)
    import pandas as pd
    df=pd.DataFrame([r])
    df.to_clipboard(index=False,header=False)
    os.system('beep')

if __name__ == "__main__":
    main()


