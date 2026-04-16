export PATH=$PWD/bin:$PATH
export PYTHONPATH=$PWD:$PYTHONPATH
export MYOMCPATH=$PWD
if [ ! -f "$HOME/private/gridproxy/x509" ] || ! voms-proxy-info -exists -valid 1:00; then
    voms-proxy-init --voms cms -rfc --valid 192:00 --out ~/private/gridproxy/x509
fi
export X509_USER_PROXY=$HOME/private/gridproxy/x509
