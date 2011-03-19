#!/usr/bin/python2
#
# Author: Victor Ananjevsky, 2007 - 2010
# based on xdg-menu.py, written by Piotr Zielinski (http://www.cl.cam.ac.uk/~pz215/)
# License: GPL
#
# This script takes names of menu files conforming to the XDG Desktop
# Menu Specification, and outputs their FVWM equivalents to the
# standard output.
#
#   http://standards.freedesktop.org/menu-spec/latest/
#
# Requirements:
#   pyxdg, pygtk, gnome-menus
#
# Syntax:
#   fvwm-xdg-menu.py [-d Menu] menufile1 menufile2 menufile3 ...
#
# Each menufile is an XDG menu description file.
# Icons of menu entries cached in $XDG_CACHE_HOME/fvwm/icons/menu
#
# For menufile name `recent' will be generated menu of recently opened files
#
# -d mean not print headers for toplevel menu (useful in DynamicPopupAction)
#
# Example:
#   fvwm-xdg-menu.py /etc/xdg/menus/applications.menu
#   fvwm-xdg-menu.py applications
#


import sys
import os
from optparse import OptionParser

import xdg.Menu
from xdg.DesktopEntry import *
from xdg.RecentFiles import *
from xdg.BaseDirectory import xdg_config_dirs, xdg_cache_home

import gtk

# fix for correct output of unicode chars without terminal
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

def cache_icon (icon):
    ''' cache an icon  '''
    icon_file = "%s/%s.png" % (cache_path, os.path.basename(icon))
    if os.path.exists(icon_file):
        return
    full_icon = "%s.png" % icon
    if os.path.exists(full_icon):
        gtk.gdk.pixbuf_new_from_file_at_size(full_icon, options.icon_size, options.icon_size).save(icon_file, 'png')
        return
    try:
        icon_theme.load_icon(icon, options.icon_size, gtk.ICON_LOOKUP_NO_SVG).save(icon_file, "png")
    except:
        pass

def parse_menu (menu, fvwm_menu = None):
    ''' parse menu file '''
    prefix = "+"
    if fvwm_menu == None:
        print ''
        print 'DestroyMenu "%s"' % menu
        print 'AddToMenu "%s"' % menu
    else:
        print 'DestroyMenu recreate %s' % fvwm_menu
        prefix = "AddToMenu %s" % fvwm_menu

    for entry in menu.getEntries():
	if isinstance(entry, xdg.Menu.Menu):
            icon = entry.getIcon()
            print u'%s "%s%%menu/folder.png%%" Popup "%s"' % (prefix, entry.getName(), entry)
	elif isinstance(entry, xdg.Menu.MenuEntry):
            desktop = DesktopEntry(entry.DesktopEntry.getFileName())
            icon = desktop.getIcon()
            ind = icon.rfind('.')
            if ind != -1:
                icon = icon[0:ind]
            cmd = desktop.getExec().rstrip('%FUfu')
            cache_icon(icon)
            print u'%s "%s%%menu/%s.png%%" Exec exec %s' % (prefix, desktop.getName(), os.path.basename(icon), cmd)
	else:
	    pass

    for entry in menu.getEntries():
	if isinstance(entry, xdg.Menu.Menu):
	    parse_menu(entry)

def parse_recent (fvwm_menu = None):
    ''' parse recently opened files '''
    prefix = "+"
    if fvwm_menu == None:
        print ''
        print 'DestroyMenu "Recent"'
        print 'AddToMenu "Recent"'
    else:
        print 'DestroyMenu recreate %s' % fvwm_menu
        prefix="AddToMenu %s" % fvwm_menu
    
    rm = gtk.RecentManager()
    for rf in rm.get_items():
        print '%s "%s" Exec exec xdg-open "%s"' % (prefix, rf.get_display_name(), rf.get_uri())

# Start

cache_path = "%s/fvwm/menu" % xdg_cache_home
icon_theme = gtk.icon_theme_get_default()

if not os.path.exists(cache_path):
    os.makedirs(cache_path)

# Parse commandline

parser = OptionParser()
parser.add_option("-d", "--dynamic", dest="fvwm_menu", default=None, help="Use in DynamicPopupAction", metavar="MENU")
parser.add_option("-i", "--icons", dest="icon_size", default=16, help="Set icons size", metavar="SIZE")
(options, args) = parser.parse_args()

for arg in args:
    filename = ""
    if os.path.exists(arg) or arg == "recent":
        filename = arg
    else:
        tmpfile = "%s/menus/%s.menu" % (xdg_config_home, arg)
        if os.path.exists(tmpfile):
            filename = tmpfile
        else:
            for dir in xdg_config_dirs:
                tmpfile = "%s/menus/%s.menu" % (dir, arg)
                if os.path.exists(tmpfile):
                    filename = tmpfile
                    break
    if filename == "":
        continue
    elif filename == "recent":
        parse_recent (options.fvwm_menu)
    else:
        parse_menu(xdg.Menu.parse(filename), options.fvwm_menu)
