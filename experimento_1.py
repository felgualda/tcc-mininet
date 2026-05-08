from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSController
from mininet.node import Node
from mininet.cli import CLI
from mininet.log import setLogLevel, info

class LinuxRouter(Node):
    def config(self, **params):
        super(LinuxRouter, self).config(**params)

        self.cmd('sysctl -w net.ipv4.ip_forward=1')
        self.cmd('sysctl -w net.ipv6.conf.all.forwarding=1')

    def terminate(self):
        self.cmd('sysctl -w net.ipv4.ip_forward=0')
        self.cmd('sysctl -w net.ipv6.conf.all.forwarding=0')

        super(LinuxRouter, self).terminate()

    def start(self, controllers):
        pass

class ExperimentoL3( Topo ):

    def build(self):
        #hosts
        h1 = self.addHost('h1', ipv6='fd00:1::2/64')
        h2 = self.addHost('h2', ipv6='fd00:2::2/64')

        #roteadores
        r0 = self.addHost('r0', cls=LinuxRouter)
        r1 = self.addHost('r1', cls=LinuxRouter)
        r2 = self.addHost('r2', cls=LinuxRouter)
        r3 = self.addHost('r3', cls=LinuxRouter)
        r4 = self.addHost('r4', cls=LinuxRouter)

        #switches
        s1 = self.addSwitch('s1')

        # enlaces
        self.addLink(h1,r0)
        self.addLink(r0,s1)
        self.addLink(s1,r1)
        self.addLink(r1,r2)
        self.addLink(r1,r3)
        self.addLink(r2,r4)
        self.addLink(r3,r4)
        self.addLink(r4,h2)        


def run():
    topo = ExperimentoL3()

    net = Mininet(topo=topo, controller=OVSController)

    net.start()

    h1, h2 = net.get('h1', 'h2')
    r0, r1, r2, r3, r4 = net.get('r0', 'r1', 'r2', 'r3', 'r4')

    h1.cmd('ip -6 addr add fd00:1::2/64 dev h1-eth0')
    h2.cmd('ip -6 addr add fd00:2::2/64 dev h2-eth0')

    r0.cmd('ip -6 addr add fd00:1::1/64 dev r0-eth0')
    r0.cmd('ip -6 addr add fd00:10::1/64 dev r0-eth1')

    r1.cmd('ip -6 addr add fd00:10::2/64 dev r1-eth0')
    r1.cmd('ip -6 addr add fd00:20::0/127 dev r1-eth1')
    r1.cmd('ip -6 addr add fd00:30::0/127 dev r1-eth2')    

    r2.cmd('ip -6 addr add fd00:20::1/127 dev r2-eth0')
    r2.cmd('ip -6 addr add fd00:40::0/127 dev r2-eth1')

    r3.cmd('ip -6 addr add fd00:30::1/127 dev r3-eth0')
    r3.cmd('ip -6 addr add fd00:50::0/127 dev r3-eth1')

    r4.cmd('ip -6 addr add fd00:40::1/127 dev r4-eth0')
    r4.cmd('ip -6 addr add fd00:50::1/127 dev r4-eth1')
    r4.cmd('ip -6 addr add fd00:2::1/64 dev r4-eth2')   


    #gateways
    h1.cmd('ip -6 route add default via fd00:1::1')
    h2.cmd('ip -6 route add default via fd00:2::1')

    #rotas de ida
    r0.cmd('ip -6 route add fd00:2::/64 via fd00:10::2')
    r1.cmd('ip -6 route add fd00:2::/64 via fd00:20::1')
    r2.cmd('ip -6 route add fd00:2::/64 via fd00:40::1')
    #r4.cmd('ip -6 route add fd00:2::/64 via fd00:2::2')

    #rotas de volta
    #r0.cmd('ip -6 route add fd00:1::/64 via fd00:10::2')
    r1.cmd('ip -6 route add fd00:1::/64 via fd00:10::1')
    r3.cmd('ip -6 route add fd00:1::/64 via fd00:30::0')
    r4.cmd('ip -6 route add fd00:1::/64 via fd00:50::0')

    info ( 'modo CLI' )
    CLI(net)

    info( 'rede parada' )
    net.stop()    

if __name__ == '__main__':
    setLogLevel( 'info' )
    run()