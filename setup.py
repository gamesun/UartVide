# -*- coding:utf-8 -*-

from distutils.core import setup
import py2exe

manifest = ''' 
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" 
manifestVersion="1.0"> 
<assemblyIdentity 
version="0.6.8.0" 
processorArchitecture="x86" 
name="YourApp" 
type="win32" 
/> 
<description>MyTerm</description> 
<trustInfo xmlns="urn:schemas-microsoft-com:asm.v3"> 
<security> 
<requestedPrivileges> 
<requestedExecutionLevel 
level="asInvoker" 
uiAccess="false" 
/> 
</requestedPrivileges> 
</security> 
</trustInfo> 
<dependency> 
<dependentAssembly> 
<assemblyIdentity 
type="win32" 
name="Microsoft.VC90.CRT" 
version="9.0.21022.8" 
processorArchitecture="x86" 
publicKeyToken="1fc8b3b9a1e18e3b" 
/> 
</dependentAssembly> 
</dependency> 
<dependency> 
<dependentAssembly> 
<assemblyIdentity 
type="win32" 
name="Microsoft.Windows.Common-Controls" 
version="6.0.0.0" 
processorArchitecture="x86" 
publicKeyToken="6595b64144ccf1df" 
language="*" 
/> 
</dependentAssembly> 
</dependency> 
</assembly> 
''' 


myOptions = {
    "py2exe":{
        "compressed": 1,
        "optimize": 2,
        "ascii": 1,
#         "includes":includes,
        "dll_excludes": ["MSVCP90.dll"],
        "bundle_files": 2
     }
}

setup(
    options = myOptions,
    zipfile = None,
    name = 'MyTerm',
    version = '1.0',
    description = 'abcde',
    author = 'gamesun',
    author_email = 'gamesun@123',
    url = r'https://github.com/gamesun/MyTerm',
    download_url = r'',
    license = 'Copywrong All Lefts Unreserved',
    windows = [
        {
            "script": "main.py",
            "other_resources": [(24,1,manifest)]
        }
    ],
    
    
      
      
)