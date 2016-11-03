import smtplib  
import sys  
import email.mime.text
import awfy
import datetime
import data
import time

def fetch_test_scores(machine_id, suite_id, name,
                      finish_stamp = (0,"UNIX_TIMESTAMP()"),
                      test_stamp = (0, "UNIX_TIMESTAMP()"), mode_id = 0):
    query = "SELECT STRAIGHT_JOIN r.id, r.stamp, b.cset, s.score, b.mode_id, v.id   \
             FROM awfy_run r                                                        \
             JOIN awfy_build b ON r.id = b.run_id                                   \
             JOIN awfy_breakdown s ON s.build_id = b.id                             \
             JOIN awfy_suite_test t ON s.suite_test_id = t.id                       \
             JOIN awfy_suite_version v ON v.id = t.suite_version_id                 \
             WHERE v.suite_id = %s                                                  \
             AND t.name = %s                                                        \
             AND r.status > 0                                                       \
             AND r.machine = %s                                                     \
             AND r.finish_stamp >= "+str(finish_stamp[0])+"                         \
             AND r.finish_stamp <= "+str(finish_stamp[1])+"                         \
             AND r.stamp >= "+str(test_stamp[0])+"                                  \
             AND r.stamp <= "+str(test_stamp[1])+"                                  \
             AND b.mode_id = %s                                                     \
             ORDER BY r.stamp ASC                                                   \
             "
    c = awfy.db.cursor()
    c.execute(query, [suite_id, name, machine_id, mode_id])
    return c.fetchall()

def fetch_suite_scores(machine_id, suite_id,
                       finish_stamp = (0,"UNIX_TIMESTAMP()"),
                       test_stamp = (0, "UNIX_TIMESTAMP()"), mode_id = 0):
    query = "SELECT STRAIGHT_JOIN r.id, r.stamp, b.cset, s.score, b.mode_id, v.id   \
             FROM awfy_run r                                                        \
             JOIN awfy_build b ON r.id = b.run_id                                   \
             JOIN awfy_score s ON s.build_id = b.id                                 \
             JOIN awfy_suite_version v ON v.id = s.suite_version_id                 \
             WHERE v.suite_id = %s                                                  \
             AND r.status > 0                                                       \
             AND r.machine = %s                                                     \
             AND r.finish_stamp >= "+str(finish_stamp[0])+"                         \
             AND r.finish_stamp <= "+str(finish_stamp[1])+"                         \
             AND r.stamp >= "+str(test_stamp[0])+"                                  \
             AND r.stamp <= "+str(test_stamp[1])+"                                  \
             AND b.mode_id = %s                                                     \
             ORDER BY r.stamp ASC                                                   \
             "
    c = awfy.db.cursor()
    c.execute(query, [suite_id, machine_id, mode_id])
    return c.fetchall()

def generateScore(start, end, name):
    score_template = '<div><b>%s</b> %s ~ %s delta:<span style="color:%s;">%.2f</span></div>\n'
    delta = 0
    start, end = float(start), float(end)

    if (start > 0):
        delta = ((end - start) / start) * 100

    color = 'green'
    if (abs(delta) >= 10):
        color = 'red'
    elif (abs(delta) >= 5):
        color = 'yellow'

    score = score_template % (name, start, end, color, delta)
    return score

def report(cx, machine, suite, date_range=(None,None)):
    startdate, endate = date_range

    # construct yesterday and today's timestamp
    if startdate is None or endate is None:
        endate = datetime.date.today()
        startdate = endate - datetime.timedelta(1)

    sdt = datetime.datetime(startdate.year, startdate.month, startdate.day)
    start_stamp = int(time.mktime(sdt.timetuple()))

    edt = datetime.datetime(endate.year, endate.month, endate.day)
    end_stamp = int(time.mktime(edt.timetuple()))

    # machine and suite
    suite_title = '<h3>%s</h3>' % suite.description
    suite_content = ''
    
    for mode in cx.modes:
        rows = fetch_suite_scores(machine.id, suite.id, finish_stamp=(start_stamp, end_stamp), mode_id=mode.id)
        if rows:
            suite_content += '<h4>%s</h4>\n' % mode.name
            suite_content += generateScore(rows[0][3], rows[-1][3], 'TOTAL')

            for test_name in suite.tests:
                rows = fetch_test_scores(machine.id, suite.id, test_name, finish_stamp=(start_stamp, end_stamp), mode_id=mode.id)
                if rows:
                    suite_content += generateScore(rows[0][3], rows[-1][3], test_name)

    if suite_content:
        suite_content = '' + suite_title + suite_content

    return suite_content

def sentV8Email(subject, message):
    mail_username='APKAutoBuildNotification@intel.com'  
    mail_password='whatever'  
    from_addr = mail_username
    #to_addrs='kanghua.yu@intel.com'
    to_addrs='''tianyou.li@intel.com;pan.deng@intel.com;jing.bao@intel.com;
    chunyang.dai@intel.com;shiyu.zhang@intel.com;kanghua.yu@intel.com;weiliang.lin@intel.com;zidong.jiang@intel.com'''

    # HOST & PORT  
    HOST = 'smtp.intel.com'
    PORT = 25
      
    # Create SMTP Object  
    smtp = smtplib.SMTP()
    print 'connecting ...'

    # show the debug log  
    # smtp.set_debuglevel(1)  
      
    # connet
    try:
        print smtp.connect(HOST,PORT)
    except:
        print 'CONNECT ERROR ****'  
    # gmail uses ssl
    #smtp.starttls()
    # login with username & password
    try:
        print 'loginning ...'
        smtp.login(mail_username,mail_password)
    except:  
        print 'LOGIN ERROR ****'
    # fill content with MIMEText's object

    msg = email.mime.text.MIMEText(message,'html')
    msg['From'] = from_addr
    msg['To'] = to_addrs
    msg['Subject'] = subject
    #print msg.as_string()
    smtp.sendmail(from_addr,to_addrs.split(';'),msg.as_string())
    smtp.quit()

if __name__ == "__main__":
    # yesterday ~ today
    endate = datetime.date.today()
    startdate = endate - datetime.timedelta(1)

    content = '''<html><head><meta charset="utf-8">
    <title>AreWeFastYet Daily Report</title>
    <link rel="stylesheet" href="http://code.jquery.com/ui/1.11.4/themes/smoothness/jquery-ui.css">
    <script src="http://code.jquery.com/jquery-1.10.2.js"></script>
    <script src="http://code.jquery.com/ui/1.11.4/jquery-ui.js"></script>
    <link rel="stylesheet" href="http://jqueryui.com/resources/demos/style.css">
    <script>
    $(function() {
    $( "#tabs" ).tabs();
    });
    </script>
    </head><body>
    <div id="time-range">From:%s To:%s</div>
    <div id="tabs">''' % (startdate, endate)

    ul_content = '<ul>'
    tab_content = ''

    has_data = False
    cx = data.Context()
    for machine in cx.machines:
        # Don't try to report machines that we're no longer tracking.
        if machine.active == 2:
            continue

        desc = machine.description
        ul_content += '<li><a href="#MACH_%s">%s</a></li>' % (machine.id, desc)
        tab_content += '<div id="MACH_%s">' % machine.id

        for benchmark in cx.benchmarks:
            machine_data = report(cx, machine, benchmark)
            if machine_data:
                has_data = True
            tab_content += machine_data

        tab_content += '</div>'
        #sentV8Email('AwfyReport-' + machine.description, content)

    ul_content += '</ul>'
    content += ul_content + tab_content + '</div>'

    # create file
    dst_html = '/home/user/work/awfy/website/reports/%s.html' % endate
    f = open(dst_html, 'w+')
    f.write(content)
    f.close()

    # send email
    if has_data:
        mailmsg = '''<html><head><title>AreWeFastYet Daily Report</title></head>
        <body><h3>Daily Report</h3>
        <p>Daily Report job has already begun. Scores from yesterday to today can be viewed from 
        <a href="http://user-awfy.sh.intel.com/awfy/reports/%s.html" > here </a></p>
        </body></html>''' % endate

        sentV8Email('Awfy Report', mailmsg)

