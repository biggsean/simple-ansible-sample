import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    '.molecule/ansible_inventory').get_hosts('all')


def test_packages_are_installed(Package):
    pkgs = [
            'mariadb',
            'mariadb-server',
            'mariadb-libs',
            'MySQL-python',
            'perl-DBD-MySQL'
            ]
    for pkg in pkgs:
        p = Package(pkg)
        assert p.is_installed


def test_my_cnf_has_correct_attributes(File):
    f = File('/etc/my.cnf')
    assert f.exists
    assert f.is_file
    assert f.user == 'root'
    assert f.group == 'root'
    assert oct(f.mode) == '0644'


def test_error_log_has_correct_attributes(File):
    f = File('/var/log/mariadb/mariadb.log')
    assert f.exists
    assert f.is_file
    assert f.user == 'mysql'
    assert f.group == 'mysql'
    assert oct(f.mode) == '0640'


def test_slow_query_log_has_correct_attributes(File):
    f = File('/var/log/mysql-slow.log')
    assert f.exists
    assert f.is_file
    assert f.user == 'mysql'
    assert f.group == 'mysql'
    assert oct(f.mode) == '0640'


def test_data_dir_has_correct_attributes(File):
    f = File('/var/lib/mysql')
    assert f.exists
    assert f.is_directory
    assert f.user == 'mysql'
    assert f.group == 'mysql'
    assert oct(f.mode) == '0755'


def test_data_dir_has_correct_setype(Command):
    c = Command('ls -ldZ /var/lib/mysql')
    assert ':mysqld_db_t:' in c.stdout


def test_mariadb_is_running_and_enabled(Service):
    s = Service('mariadb')
    assert s.is_running
    assert s.is_enabled


def test_mariadb_sockets_are_listening(Socket):
    sockets = ['tcp://0.0.0.0:3306', 'unix:///var/lib/mysql/mysql.sock']
    for socket in sockets:
        s = Socket(socket)
        assert s.is_listening


def test_mysql_root_login_is_disabled_from_remote(Command):
    sql = 'SELECT * FROM mysql.user WHERE User="root" '\
          'AND Host NOT IN ("localhost", "127.0.0.1", "::1")'
    c = Command('mysql -NBe \'%s\'' % sql)
    assert c.rc == 0
    assert c.stdout == ''


def test_no_anonymous_users_exist(Command):
    sql = 'SELECT Host FROM mysql.user WHERE User = ""'
    c = Command('mysql -NBe \'%s\'' % sql)
    assert c.rc == 0
    assert c.stdout == ''


def test_test_database_does_not_exist(Command):
    sql = 'SHOW DATABASES'
    c = Command('mysql -NBe \'%s\'' % sql)
    assert c.rc == 0
    assert 'test' not in c.stdout


def test_sample_database_is_created(Command):
    sql = 'SHOW DATABASES'
    c = Command('mysql -NBe \'%s\'' % sql)
    assert c.rc == 0
    assert 'mycoolsample' in c.stdout


def test_sample_user_exists(Command):
    sql = 'SELECT User FROM mysql.user'
    c = Command('mysql -NBe \'%s\'' % sql)
    assert c.rc == 0
    assert "supercooluser" in c.stdout
