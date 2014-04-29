from datetime import datetime
import json
import subprocess
import time


FMT = '%Y-%m-%d %I:%M %p'
SEC = 5 * 60  # Every 5 mins

def get_time():
    output = subprocess.check_output(["casperjs", "scrape.js"])
    lines = output.strip().split('\n')
    response = zip(lines[::2], lines[1::2])

    home, work = '94105', '94025'
    timestamp = datetime.now().strftime(FMT)
    ret = dict(time=timestamp)
    print timestamp
    for (header, info) in response:
        label, time = None, None
        try:
            label, _  = header.split(' - ')
        except ValueError, e:
            print "\theader:%s\n\t\t%s\n\t\t%s" % (e, header, info)

        try:
            _, time = info.split(': ')
        except ValueError, e:
            print "\tinfo:%s\n\t\t%s\n\t\t%s" % (e, header, info)

        if label and time:
            time = time.strip()
            
            slug = 'home' if label.endswith(home) else 'work'
            ret[slug] = time
            print '\t%s: %s' % (slug, time)

    return ret
    

def main():
    while True: 
        d = get_time()

        with open('data.txt', 'a') as f:
            f.write('%s\n' % json.dumps(d, sort_keys=True))

        time.sleep(SEC)



if __name__ == '__main__':
    main()
