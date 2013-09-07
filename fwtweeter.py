import tweepy, sys, os
from collections import Counter
import re
import argparse # requires 2.7
import time


class TweepyHelper:
    def __init__(self,keyfile):
        f = open(keyfile)
        lines = f.readlines()
        f.close()
        consumerkey = lines[0].split("#")[0]
        consumersecret = lines[1].split("#")[0]
        accesstoken = lines[2].split("#")[0]
        accesssec = lines[3].split("#")[0]

        auth = tweepy.OAuthHandler(consumerkey, consumersecret)
        auth.set_access_token(accesstoken, accesssec)
        self.api = tweepy.API(auth)


def handle_command_line():
    parser = argparse.ArgumentParser(description="Tweets a text format book, line by line.")
    parser.add_argument("-t", "--test", help="Run a test run, get nth tweet",
            type=int,default=-1 )
    parser.add_argument("-k", "--keyfile", help="Twitter account consumer and accesstokens")
    parser.add_argument("-b", "--bookfile", help="Book to be read")
    parser.add_argument("-l", "--logfile", help="File contains ino about Line we are on.", default="tweetedids.txt")
    args = parser.parse_args()
    return args

def get_tweeted_file(args):
    try:
        f = open(args.logfile,"r+")
    except:
        f = open(args.logfile,"w+")
    return (f, f.readlines())


def log_tweeted(tid, args):
    f, ignred = get_tweeted_file(args)
    f.write(str(time.time()))
    f.write("\t")
    f.write(tid)
    f.write("\n")
    f.close()

def read_tweeted(args):
    f, lines = get_tweeted_file(args)
    if len(lines) < 1:
        return 0
    f.close()
    result = int(lines[-1].split()[1])
    return result

if __name__ == "__main__":
    args = handle_command_line()

    api = (TweepyHelper(args.keyfile)).api

    f = open(args.bookfile)
    lines = f.readlines()
    f.close()

    if args.test < 0:
    	tid = read_tweeted(args)
        tid = tid + 1
        print "Tweeted line %d." % tid
        line = lines[tid]
        line = re.sub(r"^\d+\s+","",line)   
        line = re.sub(r"\s*\d+$","",line)   

        try:
            api.update_status(line)
        except tweepy.TweepError:
            api.update_status("%s, (%d)" % (line, tid))
        log_tweeted("%d" % tid,args)

    else:
    	print "%d/%d: %s" %  (args.test, len(bw.tweets), bw.tweets[args.test])



