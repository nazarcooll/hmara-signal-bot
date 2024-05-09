from signalbot import Signalbot
from argparse import ArgumentParser
import os
import re
import signal

import daemon.pidfile
import daemon

def terminate_process_by_pid(pid):
    try:
        os.kill(pid, signal.SIGTERM)  # or signal.SIGKILL for forceful termination
        print(f"Process with PID {pid} terminated successfully.")
    except ProcessLookupError:
        pass

def main():
    parser = ArgumentParser(description='Signalbot')
    parser.add_argument('--data-dir', help='Data and config directory')
    parser.add_argument('--mocker', action='store_true', default=False)
    parser.add_argument('--register', action='store_true', default=False)
    parser.add_argument('--restart', action='store_true', default=False)

    args = parser.parse_args()

    if args.register:
        register()
    if args.restart:
        restart()
    else:
        start_bot(args.data_dir, args.mocker)
        
def start_bot(data_dir, mocker):
    pid = os.getenv("SIGNAL_BOT_PID")
    if pid:
        terminate_process_by_pid(pid)

    pid_path = '/var/run/signal-bot.pid'
    #with daemon.DaemonContext():
    with Signalbot(data_dir=data_dir, mocker=mocker) as bot:
        bot.wait()

def register():
    javaInstalled = input("\n\nSignal requires Java  and the Java Cryptography extension.\nFor Java, just do 'sudo apt-get install default-jdk'.\nFor the JCE, download it at  http://www.oracle.com/technetwork/java/javase/downloads/jce8-download-2133166.html\nand xopy the files in /usr/lib/jvm/<the Java folder>/lib/security/\nReplace the existing files if needed.\nAre Java and the JCE extension correctly installed? (Yes/No): ")
    if javaInstalled in ['Oui', 'Yes', 'O', 'Y', 'oui', 'yes', 'o', 'y']:

        # Ask for Signal number and check if raw_input is matching the required format
        numberOK = False
        while not numberOK:
            number = input("""\nType in the phone number that will be associated to your Signal account.\nThis nimber must be formatted as follows: +CCXXXXXXXXX (CC : Country Code).\ne.g. for France: +33601020304.\nNumber: """)
            numberOK = re.match(r'^\+\d+$', number)
            if not numberOK:
                print("\nThis is not a valid number. Please retry.")

        # Ask for Signal version and check if raw_input is matching the required format
        versionOK = False
        while not versionOK:
            version = input("""\nPlease check the latest signal-cli version\non https://github.com/AsamK/signal-cli/releases and write it below.\nThe format must be x.y.z. e.g. : 0.6.2\nVersion: """)
            versionOK = re.match(r'^\d+\.\d+\.\d+$', version)
            if not versionOK:
                print("\nThis is not a valid number. Please retry.")

        os.system("cd /tmp ; wget https://github.com/AsamK/signal-cli/releases/download/v" + version + "/signal-cli-" + version + ".tar.gz")
        os.system("tar xf /tmp/signal-cli-" + version + ".tar.gz -C /opt ; ln -sf /opt/signal-cli-" + version + "/bin/signal-cli /usr/local/bin/")
        os.system('apt-get install -y git')
        os.system("cd /tmp ; git clone https://github.com/AsamK/signal-cli.git")
        os.system("cd /tmp/signal-cli/data ; cp org.asamk.Signal.conf /etc/dbus-1/system.d/ ; cp org.asamk.Signal.service /usr/share/dbus-1/system-services/ ; cp signal-cli.service /etc/systemd/system/")
        os.system("""sed -i -e "s|%dir%|/opt/signal-cli-""" + version + """/|" -e "s|%number%|""" + number + """|" /etc/systemd/system/signal-cli.service""")

        os.system("""sed -i -e 's|policy user="signal-cli"|policy user="root"|' /etc/dbus-1/system.d/org.asamk.Signal.conf""")
        os.system("""sed -i -e 's|User=signal-cli|User=root|' /etc/systemd/system/signal-cli.service""")
        sms = input("\nA validation PIN will be sent to the provided phone number.\nIf this phone cannot receive SMS (landline), the PIN will be given by a call.\nCan this phone number receive SMS? (Yes/No): ")
        if sms in ['Oui', 'Yes', 'O', 'Y', 'oui', 'yes', 'o', 'y']:
            captcha = version = input("""\nA captcha token is needed for this type of registration \nTo get the token, go to https://signalcaptchas.org/registration/generate.html \nCaptcha token: """)
            os.system("signal-cli --config /var/lib/signal-cli -u " + number + " register --captcha" + captcha)
        else:
            os.system("signal-cli --config /var/lib/signal-cli -u " + number + " register --voice")

        # Ask for verfication code and check if raw_input is matching the required format
        verifOK = False
        while not verifOK:
            verifCode  = input("Enter the 6-digit validation PIN you just received: ")
            verifOK = re.match(r'^\d{6}$', verifCode)
            if not verifOK:
                print("\nThis is not a valid number. Please retry.")

        os.system('signal-cli --config /var/lib/signal-cli -u ' + number + ' verify ' + verifCode)

        os.system("apt-get install libunixsocket-java")
        os.system("cp /usr/lib/jni/libunix-java.so /lib") # Because sometimes it says that libunix-java is not in java.library.path
        os.system("systemctl daemon-reload && systemctl enable signal-cli.service && systemctl reload dbus.service && systemctl start signal-cli.service")

        print("\nInstallation finished.")

        numberOK = False
        while not numberOK:
            number = input("\nIn order to check if the installation completed correctly,\nplease provide a phone number linked to a Signal account (not this one).\nThis number must be formatted as follows: +CCXXXXXXXXX (CC : Country Code).\ne.g. for France: +33601020304.\nNumber: ")
            numberOK = re.match(r'^\+\d+$', number)
            if not numberOK:
                print("\nThis is not a valid number. Please retry.")
            else:
                os.system('''signal-cli --dbus-system send -m "Everything works as expected. The signal-cli client installation is finished.\nWell done!" ''' + number)
                received = input("\nA message has just been sent to this number.\nHave you received it? (Yes/No): ")
                if received not in ['Oui', 'Yes', 'O', 'Y', 'oui', 'yes', 'o', 'y']:
                    numberOK = False

def restart():
    os.system("systemctl daemon-reload && systemctl restart signal-cli.service && systemctl reload dbus.service && systemctl restart signal-cli.service")

if __name__ == '__main__':
    main()