import unittest
import sys
import os

sys.path.append( os.path.join("..", "src", "bin") )
sys.path.append( os.path.join("..", "src", "appserver", "controllers") )

from lookup_edit import LookupEditor

class TestLookupEditController(unittest.TestCase):
    
    def stripSplunkPath(self, file_path):
        
        etc_start = file_path.find("/etc/")
        
        return file_path[etc_start:]
    
    def test_makeLookupFilename_Valid(self):
        
        lookup_editor = LookupEditor()
        
        # Global lookup
        self.assertEquals(self.stripSplunkPath(lookup_editor.makeLookupFilename("test.csv", namespace="some_app")), "/etc/apps/some_app/lookups/test.csv")
        self.assertEquals(self.stripSplunkPath(lookup_editor.makeLookupFilename("test.csv")), "/etc/apps/lookup_editor/lookups/test.csv")
        
        # User lookup
        self.assertEquals(self.stripSplunkPath(lookup_editor.makeLookupFilename("test.csv", owner='some_user')), "/etc/users/some_user/lookup_editor/lookups/test.csv")
        self.assertEquals(self.stripSplunkPath(lookup_editor.makeLookupFilename("test.csv", namespace="some_app", owner='some_user')), "/etc/users/some_user/some_app/lookups/test.csv")
        
        # A user of nobody
        self.assertEquals(self.stripSplunkPath(lookup_editor.makeLookupFilename("test.csv", owner='nobody')), "/etc/apps/lookup_editor/lookups/test.csv")
        
        # A user of blank
        self.assertEquals(self.stripSplunkPath(lookup_editor.makeLookupFilename("test.csv", owner='')), "/etc/apps/lookup_editor/lookups/test.csv")
        self.assertEquals(self.stripSplunkPath(lookup_editor.makeLookupFilename("test.csv", owner=' ')), "/etc/apps/lookup_editor/lookups/test.csv")
        
        
    def test_makeLookupFilename_Invalid(self):
        
        lookup_editor = LookupEditor()
        
        # Invalid characters
        self.assertEquals(self.stripSplunkPath(lookup_editor.makeLookupFilename("../test.csv")), "/etc/apps/lookup_editor/lookups/test.csv")
        self.assertEquals(self.stripSplunkPath(lookup_editor.makeLookupFilename("test.csv", namespace="../some_app")), "/etc/apps/some_app/lookups/test.csv")
        self.assertEquals(self.stripSplunkPath(lookup_editor.makeLookupFilename("test.csv", owner="../some_user")), "/etc/users/some_user/lookup_editor/lookups/test.csv")
        
if __name__ == "__main__":
    loader = unittest.TestLoader()
    suites = []
    suites.append(loader.loadTestsFromTestCase(TestLookupEditController))
    
    unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(suites))