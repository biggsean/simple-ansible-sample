import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    '.molecule/ansible_inventory').get_hosts('all')


def test_apache_is_installed(Package):
    p = Package('httpd')
    assert p.is_installed


def test_apache_conf_d_file(File):
    f = File('/etc/httpd/conf.d/drupal.conf')
    assert f.exists
    assert f.is_file
    assert f.user == 'root'
    assert f.group == 'root'
    assert oct(f.mode) == '0644'


def test_apache_is_running_and_enabled(Service):
    s = Service('httpd')
    assert s.is_running
    assert s.is_enabled


def test_httpd_can_network_connect_is_on(Command):
    c = Command('getsebool httpd_can_network_connect')
    assert c.rc == 0
    assert 'httpd_can_network_connect --> on' in c.stdout


def test_php_dependencies_are_installed(Package):
    pkgs = [
            'php',
            'php-mysql',
            'php-gd',
            'php-ldap',
            'php-odbc',
            'php-pear',
            'php-xml',
            'php-xmlrpc',
            'php-mbstring',
            'php-snmp',
            'php-soap'
            ]
    for pkg in pkgs:
        p = Package(pkg)
        assert p.is_installed


def test_mariadb_client_is_installed(Package):
    p = Package('mariadb')
    assert p.is_installed


def test_drupal_is_installed_configured_and_running(Command):
    search_str = '<label for="edit-name">Username '\
                 '<span class="form-required" '\
                 'title="This field is required.">*</span></label>'
    c = Command('curl -s 127.0.0.1/drupal/')
    assert search_str in c.stdout
