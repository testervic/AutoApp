# -*- coding: utf-8 -*-
import codecs
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import smtplib
import os
import time
import pandas as pd

now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime())
now2 = time.strftime("%Y-%m-%d", time.localtime())
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)
def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))
def send_mail(**kwargs):
    '''
    :param f: 附件路径
    :param to_addr:发给的人 []
    :return:
    '''
    from_addr = kwargs["mail_user"]
    password = kwargs["mail_pass"]
    # to_addr = "ashikun@126.com"
    smtp_server = kwargs["mail_host"]

    msg = MIMEMultipart()

    # msg = MIMEText('hello, send by Python...', 'plain', 'utf-8')
    msg['From'] = _format_addr('来自<%s>接口测试' % from_addr)
    msg['To'] = _format_addr(' <%s>' % kwargs["to_addr"])
    msg['Subject'] = Header(kwargs["header_msg"], 'utf-8').encode()
    msg.attach(MIMEText(kwargs["attach"], 'plain', 'utf-8'))
    file = open(PATH('../Report/Report.html')).read()
    msg.attach(MIMEText(file, 'html', 'utf-8'))

    if kwargs.get("report", "0") != "0":
        part = MIMEApplication(open(kwargs["report"], 'rb').read())
        part.add_header('Content-Disposition', 'attachment', filename=('gbk', '', kwargs["report_name"]))
        msg.attach(part)

    server = smtplib.SMTP_SSL(smtp_server, kwargs["port"])
    #server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, kwargs["to_addr"], msg.as_string())
    server.quit()

def isSend():
    to_addr = ["zw.vic@qq.com"]
    mail_host = "smtp.qq.com"
    mail_user = "zw.vic@qq.com"
    mail_pass = "lriftkyiakmybhig"
    port = "465"
    header_msg = "UiTestingReport_" + now2
    attach = "附件为测试报告详情\n该邮件为系统自动发送，请勿回复。"
    report = PATH("../Report/ReportDetail.xlsx")

    # 发送邮件
    send_mail(to_addr=to_addr, mail_host=mail_host, mail_user=mail_user, mail_pass=mail_pass,port=port,header_msg=header_msg, report=report, attach=attach, report_name="UiTestingReportDetail_"+now+".xlsx")
    print("邮件发送成功")

#excel转html
def excel_to_html(filepath):
    xd = pd.ExcelFile(PATH("../Report/ReportDetail.xlsx"))
    df = xd.parse()
    with codecs.open(PATH("../Report/Report.html"), 'w', 'utf-8') as html_file:
        html_file.write(df.to_html(header=True, index=False))
    file = open(PATH("../Report/Report.html")).read()
    return file


if __name__ == '__main__':
    to_addr = ["zw.vic@qq.com"]
    mail_host = "smtp.qq.com"
    mail_user = "zw.vic@qq.com"
    mail_pass = "lriftkyiakmybhig"
    port = "465"
    header_msg = "UiTesting"
    attach = "UiTesting"
    report = PATH("../Report/ReportDetail.xlsx")
    send_mail(to_addr = to_addr, mail_host = mail_host, mail_user=mail_user, port=port, mail_pass=mail_pass, header_msg=header_msg, report=report, attach=attach, report_name="接口测试报告.xlsx")
