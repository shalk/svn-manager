
import svnauth
from svnlog import svn_logger


passwd_file="/cvm/svn/SvnManager/passwd"
authz_file="/cvm/svn/SvnManager/authz"

my_auth = svnauth.SvnAuth(passwd_file,authz_file)

my_auth.display_group_priv("Host_Group")
my_auth.display_group_priv("Cloudview_CM")
my_auth.display_id_priv("xiaokun")
my_auth.id_add_priv("xiaokun","/Trunk")
my_auth.display_id_priv("xiaokun")

my_auth.write_passwdfile("/cvm/svn/SvnManager/passwd_new")
my_auth.write_authfile("/cvm/svn/SvnManager/authz_new")

