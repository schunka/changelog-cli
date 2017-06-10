import os
import unittest

from click.testing import CliRunner

from changelog.commands import cli


class CliIntegrationTestCase(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()
        os.environ.setdefault('LC_ALL', 'en_US.utf-8')
        os.environ.setdefault('LANG', 'en_US.utf-8')

    def test_cli_init(self):
        with self.runner.isolated_filesystem():
            result = self.runner.invoke(cli, ['init'])
            self.assertTrue(os.path.isfile('CHANGELOG.md'))
            self.assertTrue(result)

    def test_cli_current(self):
        with self.runner.isolated_filesystem():
            self.runner.invoke(cli, ['init'])
            result = self.runner.invoke(cli, ['current'])
            self.assertEqual(result.output.strip(), '0.1.0')

    def test_cli_current_missing(self):
        with self.runner.isolated_filesystem():
            result = self.runner.invoke(cli, ['current'])
            self.assertEqual(result.output.strip(), '')

    def test_cli_suggest(self):
        with self.runner.isolated_filesystem():
            self.runner.invoke(cli, ['init'])
            result = self.runner.invoke(cli, ['suggest'])
            self.assertEqual(result.output.strip(), '0.1.1')

    def test_cli_suggest_missing(self):
        with self.runner.isolated_filesystem():
            result = self.runner.invoke(cli, ['suggest'])
            self.assertEqual(result.output.strip(), '')

    def test_cli_version_flag(self):
        result = self.runner.invoke(cli, ['--version'])
        self.assertTrue(result)

    def test_cli_new(self):
        with self.runner.isolated_filesystem():
            self.runner.invoke(cli, ['init'])
            result = self.runner.invoke(cli, ['new', 'Adding a new feature'])
            self.assertTrue(result)
            suggest = self.runner.invoke(cli, ['suggest'])
            self.assertEqual(suggest.output.strip(), '0.2.0')

    def test_cli_new_missing(self):
        with self.runner.isolated_filesystem():
            result = self.runner.invoke(cli, ['new', 'Adding a new feature'], input='y\n')
            self.assertEqual(result.output.strip(), 'No CHANGELOG.md Found, do you want to create one? [y/N]: y')

    def test_cli_change(self):
        with self.runner.isolated_filesystem():
            self.runner.invoke(cli, ['init'])
            result = self.runner.invoke(cli, ['change', 'Changing a feature'])
            self.assertTrue(result)
            suggest = self.runner.invoke(cli, ['suggest'])
            self.assertEqual(suggest.output.strip(), '0.1.1')

    def test_cli_change_missing(self):
        with self.runner.isolated_filesystem():
            result = self.runner.invoke(cli, ['change', 'changing a feature'], input='y\n')
            self.assertEqual(result.output.strip(), 'No CHANGELOG.md Found, do you want to create one? [y/N]: y')

    def test_cli_fix(self):
        with self.runner.isolated_filesystem():
            self.runner.invoke(cli, ['init'])
            result = self.runner.invoke(cli, ['fix', 'Fix a Bug'])
            self.assertTrue(result)
            suggest = self.runner.invoke(cli, ['suggest'])
            self.assertEqual(suggest.output.strip(), '0.1.1')

    def test_cli_fix_missing(self):
        with self.runner.isolated_filesystem():
            result = self.runner.invoke(cli, ['fix', 'Fix a Bug'], input='y\n')
            self.assertEqual(result.output.strip(), 'No CHANGELOG.md Found, do you want to create one? [y/N]: y')

    def test_cli_breaks(self):
        with self.runner.isolated_filesystem():
            self.runner.invoke(cli, ['init'])
            result = self.runner.invoke(cli, ['breaks', 'Breaking Change'])
            self.assertTrue(result)
            suggest = self.runner.invoke(cli, ['suggest'])
            self.assertEqual(suggest.output.strip(), '1.0.0')

    def test_cli_breaks_missing(self):
        with self.runner.isolated_filesystem():
            result = self.runner.invoke(cli, ['breaks', 'Breaking Change'], input='y\n')
            self.assertEqual(result.output.strip(), 'No CHANGELOG.md Found, do you want to create one? [y/N]: y')

    def test_cli_release(self):
        with self.runner.isolated_filesystem():
            self.runner.invoke(cli, ['init'])
            self.runner.invoke(cli, ['new', 'Adding a new feature'])
            result = self.runner.invoke(cli, ['release'])
            self.assertEqual(result.output.strip(), 'Planning on releasing version 0.2.0. Proceed? [y/N]:')

    def test_cli_release_y(self):
        with self.runner.isolated_filesystem():
            self.runner.invoke(cli, ['init'])
            self.runner.invoke(cli, ['new', 'Adding a new feature'])
            result = self.runner.invoke(cli, ['release', '--yes'])
            self.assertTrue(result)
            suggest = self.runner.invoke(cli, ['suggest'])
            self.assertEqual(suggest.output.strip(), '0.2.1')

    def test_cli_release_missing(self):
        with self.runner.isolated_filesystem():
            result = self.runner.invoke(cli, ['release'])
            self.assertEqual(result.output.strip(), 'No CHANGELOG.md Found, do you want to create one? [y/N]:')
