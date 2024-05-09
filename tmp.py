import os
import re
#from signalbot.worker import start_bot, restart, register
os.system("systemctl daemon-reload && systemctl enable signal-cli.service && systemctl reload dbus.service && systemctl start signal-cli.service")

javaInstalled = input("\n\nSignal requires Java  and the Java Cryptography extension.\nFor Java, just do 'sudo apt-get install default-jdk'.\nFor the JCE, download it at  http://www.oracle.com/technetwork/java/javase/downloads/jce8-download-2133166.html\nand xopy the files in /usr/lib/jvm/<the Java folder>/lib/security/\nReplace the existing files if needed.\nAre Java and the JCE extension correctly installed? (Yes/No): ")
if javaInstalled in ['Oui', 'Yes', 'O', 'Y', 'oui', 'yes', 'o', 'y']:
    number = '+380978446281'
    version = '0.13.3'
    os.system("cd /tmp ; wget https://github.com/AsamK/signal-cli/releases/download/v" + version + "/signal-cli-" + version + ".tar.gz")
    os.system("tar xf /tmp/signal-cli-" + version + ".tar.gz -C /opt ; ln -sf /opt/signal-cli-" + version + "/bin/signal-cli /usr/local/bin/")
    os.system('apt-get install -y git')
    os.system("cd /tmp ; git clone https://github.com/AsamK/signal-cli.git")
    os.system("cd /tmp/signal-cli/data ; cp org.asamk.Signal.conf /etc/dbus-1/system.d/ ; cp org.asamk.Signal.service /usr/share/dbus-1/system-services/ ; cp signal-cli.service /etc/systemd/system/")
    os.system("""sed -i -e "s|%dir%|/opt/signal-cli-""" + version + """/|" -e "s|%number%|""" + number + """|" /etc/systemd/system/signal-cli.service""")

    os.system("""sed -i -e 's|policy user="signal-cli"|policy user="root"|' /etc/dbus-1/system.d/org.asamk.Signal.conf""")
    os.system("""sed -i -e 's|User=signal-cli|User=root|' /etc/systemd/system/signal-cli.service""")
    os.system("systemctl daemon-reload && systemctl enable signal-cli.service && systemctl reload dbus.service && systemctl start signal-cli.service")

    print("\nInstallation finished.")

    number = '+380934377445'
    os.system('''signal-cli --dbus-system send -m "Everything works as expected. The signal-cli client installation is finished.\nWell done!" ''' + number)