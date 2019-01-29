#
# Copyright (c) 2013, EMC Corporation
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Module Name:
#
#        query.py
#
# Abstract:
#
#        SMB2_QUERY_INFO command tests with SMB2_0_INFO_FILE type.
#
# Authors: Rafal Szczesniak (rafal.szczesniak@isilon.com)
import pike.model
import pike.smb2
import pike.test
import pike.ntstatus

class AlcsGetinfoTest(pike.test.PikeTest):
    def __init__(self, *args, **kwargs):
        super(AlcsGetinfoTest, self).__init__(*args, **kwargs)
        self.chan = None
        self.tree = None

    def open_file(self):
        """Helper to open basic file"""
        self.chan, self.tree = self.tree_connect()
        return self.chan.create(self.tree, "test12.txt", disposition=pike.smb2.FILE_SUPERSEDE).result()
    def test_Acls_getinfo(self):
        chan, tree = self.tree_connect()
        share_all = pike.smb2.FILE_SHARE_READ | pike.smb2.FILE_SHARE_WRITE | pike.smb2.FILE_SHARE_DELETE
        handle = chan.create(tree,
                              '111.txt',
                              share=share_all).result()


        secinfo = chan.acls_file_info(handle, pike.smb2.FILE_SEC_INFO)
        # print secinfo


        chan.close(handle)

    # def test_basic_test(self):
    #     """Helper to perform a basic query test"""
    #     # handle = self.open_file()
    #     # info = self.chan.query_file_info(handle, pike.smb2.FILE_STANDARD_INFORMATION)
    #     chan, tree = self.tree_connect()
    #     share_all = pike.smb2.FILE_SHARE_READ | pike.smb2.FILE_SHARE_WRITE | pike.smb2.FILE_SHARE_DELETE
    #     handle = chan.create(tree,
    #                          'Acls.txt',
    #                          share=share_all,
    #                          disposition=pike.smb2.FILE_SUPERSEDE).result()
    #
    #     info = chan.query_file_info(handle, pike.smb2.FILE_STANDARD_INFORMATION)
    #     print info
    #     chan.close(handle)




