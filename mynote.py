#!/usr/bin/python3.8
# port rebol rebnote to python for long term viability. IPython so no () typing.
# but if you can easily type parens (LISP much?) then plain Python 3 is fine.
#print(('%s[' % chr(27) + '1;%dm' % 37)

# errs: import ipy_autoreload
import sys, string, time, calendar
import sqlite3
sys.path.append(r'/home/<UserName>/Documents')
from colorama import *

init(autoreset=True)

#Fore: BLACK, RED, GREEN, GREEN, BLUE, MAGENTA, CYAN, WHITE, RESET.
#Style: DIM, NORMAL, BRIGHT, RESET_ALL

def usage():
    """QUICK guide to pynote3 by Jay H"""

    print('%s[' % chr(27) + '1;%dm' % 37)
    print(Fore.RED + "A NOTE-taking app that uses tagging")
    print(Fore.GREEN + "mn() makes notes.")
    print(Fore.YELLOW + "gn() gets notes. Type 0-3 tags to search on")
    print(Fore.GREEN + "gt() shows all(l) TAGs & (count). Or note_id ")
    print(Fore.GREEN + "gtt() No-Frills gt")
    print(Fore.YELLOW + "ln() is last N notes (prompted for N)")
    print(Fore.MAGENTA + "fs() is fulltext search")
    print(Fore.RED + "mp() to make person names and birthday")
    print(Fore.GREEN + "gp() to get people, optional limit")
    print(Fore.YELLOW + "This is Python3 version")

usage()

def main():
    """Intercept input and restict to pynote UI"""
     
    keepLooping = True
    while keepLooping:
        userTyped = input(">*> ")
        if userTyped == 'mn':
            mn()       
        elif userTyped == 'gn':
            gn() 
        elif userTyped == 'gnn':
            gnn()
        elif userTyped == 'ln':
            ln()
        elif userTyped == 'gt':
            gt() 
        elif userTyped == 'fs':
            fs()
        elif userTyped == 'mp':
            mp() 
        elif userTyped == 'gp':
            gp() 
        elif userTyped == 'dn':
            dn()   
        elif userTyped == 'dt':
            dt()  
        elif userTyped == 'usage':
            usage()
        elif userTyped == 'qt':
            keepLooping = False 
        else:
            continue

TnF = True 

#------------------------------------------------------------------------
# RAW SQL FOR SETUP OF SQLITE DATABASE NEEDED FOR SCRIPT TO WORK
# SQLite3 mynotes.sqlite
# CREATE TABLE note (note_txt TEXT NOT NULL, timestamp)
# CREATE TABLE tag (tag_text TEXT NOT NULL)
# CREATE TABLE fkeys (note_id INTEGER NOT NULL,tag_id INTEGER NOT NULL)
#
# CREATE TRIGGER insert_note_timestamp AFTER INSERT ON note
#   BEGIN
#     UPDATE note SET timestamp = DATETIME('NOW','localtime')
#     WHERE rowid = new.rowid;
#   END
#
# CREATE TRIGGER no_dup_tags
#   BEFORE INSERT ON tag
#   FOR EACH ROW BEGIN
#     SELECT CASE
#       WHEN ((SELECT tag_text FROM tag WHERE tag_text = NEW.tag_text) IS NOT NULL)
#       THEN RAISE(IGNORE)
#     END;
#   END
#
# CREATE TRIGGER [delete_note]
# BEFORE DELETE ON [note]
# FOR EACH ROW BEGIN
#   DELETE FROM fkeys WHERE fkeys.note_id = old.rowid;
# END;
#
# CREATE TRIGGER [delete_tag]
# BEFORE DELETE ON [tag]
# FOR EACH ROW BEGIN
#   DELETE FROM fkeys WHERE fkeys.tag_id = old.rowid;
# END;
#
# CREATE TABLE prsn (lname text, fname text, yrmoda text (10));
#------------------------------------------------------------------------

# REM default sqlite behaviour is case-insensitive search


def mn():
    """Make note in sqlite db and tag it."""
    conn = sqlite3.connect('mynotes.sqlite')
    conn.text_factory = str
    db = conn.cursor()

    print(Fore.GREEN + "Enter note text")
    notetxt = input("note: ")

    gtt() 
    #print("Enter 1 to 3 tags")
    taglist = input("tags: ")
    taglist = taglist.split()

    db.execute('INSERT INTO note (note_txt) VALUES (?)', [notetxt])
    conn.commit()
    db.execute('select last_insert_rowid()')
    fknote = db.fetchone()[0]
    fknote = int(fknote)
    Fore.YELLOW
    print("#: ",fknote)
    Fore.WHITE

    #records new tags since db trigger stops dups, updates many-many tbl

    for tagtxt in taglist:
        db.execute('INSERT INTO tag VALUES (?)',[tagtxt])
        conn.commit()
        db.execute('select rowid from tag where tag_text = (?)',[tagtxt])
        fktag = db.fetchone()[0] 
        fktag = int(fktag)
        print("fktag: ",fktag,"fknote: ",fknote)
        db.execute('INSERT INTO fkeys VALUES (?,?)',[fknote,fktag])
        conn.commit()

    db.close

def gn():
    conn = sqlite3.connect('mynotes.sqlite')
    conn.text_factory = str
    db = conn.cursor()

    print(Fore.GREEN + "Enter 1 to 3 tags")
    taglist = input("tags: ")

    taglist = taglist.split()

    srchtxt0 = taglist[0]

    tagcount = len(taglist)
    if tagcount == 1:
        srchtxt1 = srchtxt0
        srchtxt2 = srchtxt0
    elif tagcount == 2:
        srchtxt1 = taglist[1]
        srchtxt2 = taglist[1]
    elif tagcount == 3:
        srchtxt1 = taglist[1]
        srchtxt2 = taglist[2]
    else:
        srchtxt1 = srchtxt0
        srchtxt2 = srchtxt0

    db.execute('SELECT DISTINCT n.rowid as rowid, n.note_txt as note_txt,\
      date(n.timestamp) as timestamp  FROM note n\
      JOIN fkeys f ON n.rowid = f.note_id\
      JOIN tag t ON t.rowid = f.tag_id\
      WHERE t.tag_text = ?\
    INTERSECT  \
      SELECT DISTINCT n.rowid as rowid, n.note_txt as note_txt,\
      date(n.timestamp) as timestamp FROM note n\
      JOIN fkeys f ON n.rowid = f.note_id\
      JOIN tag t ON t.rowid = f.tag_id\
      WHERE t.tag_text = ?\
   INTERSECT\
      SELECT DISTINCT n.rowid as rowid, n.note_txt as note_txt,\
      date(n.timestamp) as timestamp FROM note n\
      JOIN fkeys f ON n.rowid = f.note_id\
      JOIN tag t ON t.rowid = f.tag_id\
      WHERE t.tag_text = ?\
      ORDER BY timestamp',[srchtxt0,srchtxt1,srchtxt2])

    taggedsuch = db.fetchall()

    for i in taggedsuch:
        print(i[0],i[1],i[2])
        print(Fore.GREEN + "----------------------------------")

    db.close
    print(Fore.GREEN + "----------------------------------")


def gnn():
    conn = sqlite3.connect('mynotes.sqlite')
    conn.text_factory = str
    db = conn.cursor()

    print(Fore.GREEN + "What id #?")
    idx = input("#: ")

    db.execute('SELECT * FROM note n WHERE n.rowid = ?', [idx])

    #db.execute('SELECT n.rowid as rowid \
    #  n.note_txt as note_txt, date(n.timestamp) as timestamp \
    #  FROM note n WHERE n.rowid
      
    numberednote  = db.fetchall()

    print(Fore.WHITE)

    print(numberednote)

    db.close
    print(Fore.GREEN + "----------------------------------")

def gtt():
    """Gett-Tags into tuple, not list, No Count, chrono-sort"""
    conn = sqlite3.connect('mynotes.sqlite')
    conn.text_factory = str
    db = conn.cursor()

    sql = 'select tag_text from tag order by tag_text'

    db.execute(sql)
    tgs = db.fetchall()
    for t in tgs:
        s = (t[0])
        print(Fore.MAGENTA + s, end = ' ')
    print('\n')

def gt():
    """Get-Tags, optionally with Count, optionally alpha-sort (vs chrono-sort)"""
    conn = sqlite3.connect('mynotes.sqlite')
    conn.text_factory = str
    db = conn.cursor()

    arg = input("Enter all(l) or some note_id: ")

    arg2 = input("Sorted? y or n: ")

    sql = 'select tag_text from tag'

    # missing rebol refinement mechanism right about now.
    if arg2 == "y":
        opt = ' order by tag_text'
    else:
        opt = ""
        
    if arg == "all" or arg == "alll":
        db.execute(sql + opt)
        tagsofa = db.fetchall()

        for t in tagsofa:
            #print("t is ", t)
            s = (t[0])
            db.execute('SELECT COUNT(*) FROM fkeys WHERE tag_id = \
                    (SELECT rowid FROM tag WHERE tag_text = ?)',[s])
            cnt = db.fetchone()
            if arg == "all":
                print(Fore.RED + s,end = ' ')
            if arg == "alll":
                print(Fore.RED + s,"-",cnt[0],end =' ')

#print("[",s,"-",cnt[0],"]",)

    else:
        #print("tags for note ",arg,)
        db.execute('SELECT tag_text FROM tag\
        JOIN fkeys on tag.rowid = fkeys.tag_id\
        WHERE fkeys.note_id = ?',[arg])
        tagsfornoteid = db.fetchall()

        for i in tagsfornoteid:
            print(Fore.RED + i[0],)

    db.close

    print("")
    print(Fore.GREEN + "----------------------------------")


def dn():
    conn = sqlite3.connect('mynotes.sqlite')
    db = conn.cursor()

    n = input("Enter note_id to DELETE: ")
    note2delete = n

    db.execute('DELETE FROM note WHERE note.rowid = ?',[note2delete])
    conn.commit()
    db.close()

    print("")
    print(Fore.GREEN + "----------------------------------")

def dtt():
    """Interctively delete tags"""
    conn = sqlite3.connect('mynotes.sqlite')
    db = conn.cursor()

    for tag2delete in db.execute('SELECT tag_text FROM tag;'):
        print(tag2delete[0])
        dok = input("ok to delete?")
        if dok == "y":
           db.execute('DELETE FROM tag WHERE tag_text = ?',[tag2delete[0]])
           conn.commit()

    db.close()
 
    print("") 
    print(Fore.GREEN + "----------------------------------")


def dt():
    conn = sqlite3.connect('mynotes.sqlite')
    db = conn.cursor()

    t = input("Enter TAG to DELETE: ")
    tag2delete = t

    db.execute('DELETE FROM tag WHERE tag_text = ?',[tag2delete])
    conn.commit()
    db.close()
 
    print("") 
    print(Fore.GREEN + "----------------------------------")

def fs():
    conn = sqlite3.connect('mynotes.sqlite')
    conn.text_factory = str
    db = conn.cursor()

    print(Fore.GREEN + "Enter search txt")
    srchtxt0 = input("srch txt: ")

    db.execute('SELECT n.rowid as rowid, n.note_txt as note_txt,\
      n.timestamp as timestamp FROM note n\
      WHERE note_txt LIKE ?\
      ORDER BY timestamp',['%'+srchtxt0+'%'])

    foundsuch = db.fetchall()

    for i in foundsuch:
        print(i[0],i[1],i[2])
        print("")
        print(Fore.GREEN + "----------------------------------")

    db.close


def ln():
    #"Last note(s)"
    conn = sqlite3.connect('mynotes.sqlite')
    conn.text_factory = str
    db = conn.cursor()

    print(Fore.GREEN + "How far back?")
    depth = input("Depth: ")

    print(Fore.YELLOW + "Last " + depth)
                  # + depth + '-1' would require >= instead of > 
    db.execute('SELECT max(n.rowid) from note n')
    nrows = str(int(db.fetchone()[0])-int(depth))

    db.execute('SELECT n.rowid as rowid, n.note_txt as note_txt,\
      n.timestamp as timestamp FROM note n\
      WHERE rowid > ?',[nrows])

    foundsuch = db.fetchall()

    for i in foundsuch:
        print(i[0],i[1],i[2])
        print(Fore.GREEN + "----------------------------------")

    print(Fore.WHITE)

    db.close
