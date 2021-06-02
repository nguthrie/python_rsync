import os
import unittest
import shutil
import sys
import pathlib as pl
import glob
sys.path.append("..")
import rsync

class TestCaseBase(unittest.TestCase):
 
    def assertIsFile(self, path):
        if not pl.Path(path).resolve().is_file():
            raise AssertionError("File does not exist: {}".format(path))

    def assertIsNotFile(self, path):
        if pl.Path(path).resolve().is_file():
            raise AssertionError("File exist: {}".format(path))

    def assertIsDir(self, path):
        if not pl.Path(path).resolve().is_dir():
            raise AssertionError("Directory does not exist: {}".format(path))

    def assertIsNotDir(self, path):
        if pl.Path(path).resolve().is_dir():
            raise AssertionError("Directory exist: {}".format(path))


class TestRsync(TestCaseBase):

    @staticmethod
    def remove_files_and_dirs(folder):
        """Input dir (str) to remove all files and dir in that location."""
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

    @classmethod
    def setUpClass(cls): 
        try:
            f = open('test_source/file0.txt', 'x')
            f.close()
            f = open('test_source/file1.txt', 'x')
            f.close()
            f = open('test_source/file2.txt', 'x')
            f.close()
            f = open('test_source/file3.png', 'x')
            f.close()
            f = open('test_source/file4.png', 'x')
            f.close()
            os.makedirs('test_source/testdir0/')
            os.makedirs('test_source/testdir1/')
        except Exception:
            pass

    @classmethod
    def tearDownClass(cls):
        """Delete all files from source after tests."""
        folder = 'test_source/'
        cls.remove_files_and_dirs(folder)        
        
    def setUp(self):
        '''Delete all files from test_source/ before test.'''
        folder = 'test_dest/'
        self.remove_files_and_dirs(folder)

    def tearDown(self):
        '''Delete all files from test_source/ after test.'''
        folder = 'test_dest/'
        self.remove_files_and_dirs(folder)

    def test_single_file(self):
        # Testing single file transfer
        print("this test")
        rsync.main(['test_source/file0.txt', 'test_dest/'])
        path = pl.Path("test_dest/file0.txt")
        print("end of test")
        print()
        self.assertIsFile(path)
        
    def test_single_dir(self):
        # Testing single directory transfer with option
        rsync.main(['-d', 'test_source/testdir0/', 'test_dest/testdir0/'])
        path = pl.Path("test_dest/testdir0/")
        self.assertIsDir(path)

    def test_single_dir_no_flag(self):
        # Testing single file transfer without option
        rsync.main(['test_source/testdir0/', 'test_dest/testdir0/'])
        path = pl.Path("test_dest/testdir0/")
        self.assertIsNotDir(path)

    def test_non_exist_file(self):
        # Testing single non-existent file
        rsync.main(['test_source/file10.txt', 'test_dest/'])
        path = pl.Path("test_dest/file10.txt")
        self.assertIsNotFile(path)

    def test_non_exist_dir(self):
        # Testing single non-existent directory
        rsync.main(['test_source/testdir10', 'test_dest/'])
        path = pl.Path("test_dest/testdir10/")
        self.assertIsNotDir(path)
   
    def test_directory_to_file(self):
        # Test transferring an existent directory to a file - fails
        rsync.main(['test_source/testdir10/', 'test_dest/file0.txt'])
        path = pl.Path("test_dest/file0.txt")
        self.assertIsNotDir(path) 
        self.assertIsNotFile(path)

    def test_multiple_files(self):
        # Test mutliple files transfer
        rsync.main(['test_source/file0.txt', 'test_source/file1.txt', 'test_dest/'])
        path0 = pl.Path("test_dest/file0.txt")
        path1 = pl.Path("test_dest/file1.txt")
        self.assertIsFile(path0)
        self.assertIsFile(path1)

    def test_multiple_files_with_wildcard(self):
        # Test mutliple files transfer with wildcard
        # Note: glob is resolved in Bash not Python, so passing the string literal 'test_source/*' as
        # a test case will fail
        inputs = ['-d']
        inputs += glob.glob('test_source/*')
        inputs.append('test_dest/')
        rsync.main(inputs)
        path0 = pl.Path("test_dest/file0.txt")
        path1 = pl.Path("test_dest/file1.txt")
        path2 = pl.Path("test_dest/file2.txt")
        path3 = pl.Path("test_dest/file3.png")
        path4 = pl.Path("test_dest/file4.png")
        path5 = pl.Path("test_dest/testdir0/")
        path6 = pl.Path("test_dest/testdir1/")
        self.assertIsFile(path0)
        self.assertIsFile(path1)
        self.assertIsFile(path2)
        self.assertIsFile(path3)
        self.assertIsFile(path4)
        self.assertIsDir(path5)
        self.assertIsDir(path6)


    def test_multiple_files_with_extension(self):
        # Test mutliple files transfer with wildcard
        # Note: glob is resolved in Bash not Python, so passing the string literal 'test_source/*' as
        # a test case will fail
        inputs = ['-d']
        inputs += glob.glob('test_source/*.txt')
        inputs.append('test_dest/')
        rsync.main(inputs)
        path0 = pl.Path("test_dest/file0.txt")
        path1 = pl.Path("test_dest/file1.txt")
        path2 = pl.Path("test_dest/file2.txt")
        path3 = pl.Path("test_dest/file3.png")
        path4 = pl.Path("test_dest/file4.png")
        path5 = pl.Path("test_dest/testdir0/")
        path6 = pl.Path("test_dest/testdir1/")
        self.assertIsFile(path0)
        self.assertIsFile(path1)
        self.assertIsFile(path2)
        self.assertIsNotFile(path3)
        self.assertIsNotFile(path4)
        self.assertIsNotDir(path5)
        self.assertIsNotDir(path6)


if __name__ == "__main__":
    unittest.main()

