from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSController
from mininet.cli import CLI
from mininet.log import setLogLevel, info

class TopologiaDiamante( Topo ):

    def build(self):
        #hosts
        h1 = self.addHost( 'h1' )
        h2 = self.addHost( 'h2' )

        #switches
        s1 = self.addSwitch( 's1' , stp=True, failMode='standalone')
        s2 = self.addSwitch( 's2' , stp=True, failMode='standalone')
        s3 = self.addSwitch( 's3' , stp=True, failMode='standalone')
        s4 = self.addSwitch( 's4' , stp=True, failMode='standalone')                        

        #links
        self.addLink(h1, s1)
        self.addLink(h2,s4)

        self.addLink(s1, s2)
        self.addLink(s1, s3)
        self.addLink(s2, s4)
        self.addLink(s3, s4)

def run():
    topo = TopologiaDiamante()

    net = Mininet(topo=topo, controller=OVSController)

    net.start()

    info( 'ping para testar rede' )
    net.pingAll()

    info ( 'modo CLI' )
    CLI(net)

    info( 'rede parada' )
    net.stop()    

if __name__ == '__main__':
    setLogLevel( 'info' )
    run()