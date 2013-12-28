import os
import showtracker
import unittest
import tempfile


class TrackerTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, showtracker.app.config['DATABASE'] = tempfile.mkstemp()
        showtracker.app.config['TESTING'] = True
        self.app = showtracker.app.test_client()
        showtracker.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(showtracker.app.config['DATABASE'])

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_login_logout(self):
        rv = self.login('admin', 'default')
        assert 'You were logged in' in rv.data
        rv = self.logout()
        assert 'You were logged out' in rv.data
        rv = self.login('Hamms', 'default')
        assert 'Invalid username' in rv.data
        rv = self.login('admin', 'iphoney')
        assert 'Invalid password' in rv.data

    def test_empty_db(self):
        rv = self.app.get('/')
        assert 'Northern' in rv.data




if __name__ == '__main__':
    unittest.main()
