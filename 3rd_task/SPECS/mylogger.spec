Name:		mylogger
Version:	0.3
Release:	2%{?dist}
Summary:	Test package

#Group:		
License:	MIT
Source0:	my_logger.sh
Source1:	my_log.conf
Source2:	my_log_rotate
Source3:	unit_service_log_disk_usage
Source4:	my_cron_job


%description
Test package for logging disk usage every 20 minutes

%install
install -D -m 755 %{SOURCE0} $RPM_BUILD_ROOT/usr/sbin/my_logger.sh
install -D -m 644 %{SOURCE1} $RPM_BUILD_ROOT/etc/rsyslog.d/my_log.conf
install -D -m 644 %{SOURCE2} $RPM_BUILD_ROOT/etc/logrotate.d/my_log_rotate
install -D -m 644 %{SOURCE3} $RPM_BUILD_ROOT/usr/lib/systemd/system/my_log.service
install -D -m 644 %{SOURCE4} $RPM_BUILD_ROOT/etc/cron.d/my_cron_job

%pre
echo preinstall $1

%post
echo postinstall $1
#ln -s /usr/lib/systemd/system/my_log.service usr/lib/systemd/system/multi-user.target.wants/my_log.service 
if [ -f "/var/log/mylog_disk_usage.log" ]; then
    echo "File /var/log/mylog_disk_usage.log exists"
else
    touch /var/log/mylog_disk_usage.log
fi

#/bin/kill -HUP `cat /var/run/syslogd.pid 2> /dev/null` 2> /dev/null || true
systemctl restart rsyslog
systemctl enable my_log
systemctl start my_log

%preun
echo preuninstall $1

%postun
echo postuninstall $1
if [ "$1" == "0" ]; then
#    /bin/kill -HUP `cat /var/run/syslogd.pid 2> /dev/null` 2> /dev/null || true
    echo "delete file with log in /var/log/mylog_disk_usage.log"
    rm -f /var/log/mylog_disk_usage.log  
    systemctl restart rsyslog
fi

%files
/usr/sbin/my_logger.sh
/etc/rsyslog.d/my_log.conf
/etc/logrotate.d/my_log_rotate
/usr/lib/systemd/system/my_log.service
/etc/cron.d/my_cron_job


