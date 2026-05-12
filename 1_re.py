import time

from ipmininet.iptopo import IPTopo
from ipmininet.ipnet import IPNet
from ipmininet.cli import IPCLI
from mininet.log import setLogLevel, info
from mininet.node import OVSController
from ipmininet.router.config import OSPF6, RouterConfig
from ipmininet.srv6 import enable_srv6

class ExperimentoL3( IPTopo ):

    def build(self, *args, **kwargs):
        #hosts
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')

        #roteadores
        r0 = self.addRouter('r0', config=RouterConfig)
        r0.addDaemon(OSPF6, hello_int = 1)

        r1 = self.addRouter('r1', config=RouterConfig)
        r1.addDaemon(OSPF6, hello_int = 1)

        r2 = self.addRouter('r2', config=RouterConfig)
        r2.addDaemon(OSPF6, hello_int = 1)
    
        r3 = self.addRouter('r3', config=RouterConfig)
        r3.addDaemon(OSPF6, hello_int = 1)

        r4 = self.addRouter('r4', config=RouterConfig)
        r4.addDaemon(OSPF6, hello_int = 1)

        #switches
        s1 = self.addSwitch('s1')

        # enlaces
        lh1r0 = self.addLink(h1,r0, bw=100, igp_metric=1)
        lh1r0[h1].addParams(ip=("fd00:1::2/64"))
        lh1r0[r0].addParams(ip=("fd00:1::1/64"))

        lr0s1 = self.addLink(r0,s1, bw=100, igp_metric=1)
        lr0s1[r0].addParams(ip=("fd00:10::1/64"))

        ls1r1 = self.addLink(s1,r1, bw=100, igp_metric=1)
        ls1r1[r1].addParams(ip=("fd00:10::2/64"))

        lr1r2 = self.addLink(r1,r2, bw=100,igp_metric=1)
        lr1r2[r1].addParams(ip=("fd00:20::0/127"))
        lr1r2[r2].addParams(ip=("fd00:20::1/127"))

        lr1r3 = self.addLink(r1,r3, bw=50,igp_metric=2)
        lr1r3[r1].addParams(ip=("fd00:30::0/127"))
        lr1r3[r3].addParams(ip=("fd00:30::1/127"))

        lr2r4 = self.addLink(r2,r4, bw=100, igp_metric=1, delay='10ms')
        lr2r4[r2].addParams(ip=("fd00:40::0/127"))
        lr2r4[r4].addParams(ip=("fd00:40::1/127"))

        lr3r4 = self.addLink(r3,r4, bw=50, igp_metric=2)
        lr3r4[r3].addParams(ip=("fd00:50::0/127"))
        lr3r4[r4].addParams(ip=("fd00:50::1/127"))

        lr4h2 = self.addLink(r4,h2, bw=100, igp_metric=1)  
        lr4h2[r4].addParams(ip=("fd00:2::1/64"))   
        lr4h2[h2].addParams(ip=("fd00:2::2/64"))   

    def post_build(self, net):
        for n in net.hosts + net.routers:
            enable_srv6(n)
        return super().post_build(net)

def run():
    topo = ExperimentoL3()

    net = IPNet(topo=topo, controller=OVSController, allocate_IPs=False)

    net.start()

    h1, h2 = net.get('h1', 'h2')
    r0, r1, r2, r3, r4 = net.get('r0', 'r1', 'r2', 'r3', 'r4')
    #gateways
    h1.cmd('ip -6 route add default via fd00:1::1')
    h2.cmd('ip -6 route add default via fd00:2::1')

    info ( 'modo CLI' )
    IPCLI(net)

    info( 'rede parada' )
    net.stop()    

if __name__ == '__main__':
    setLogLevel( 'info' )
    run()