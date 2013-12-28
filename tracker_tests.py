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

    def test_empty_db(self):
        rv = self.app.get('/')
        assert 'Unbelievable' in rv.data




if __name__ == '__main__':
    unittest.main()
