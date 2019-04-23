import kademlia.JKademliaNode;
import kademlia.node.KademliaId;
import kademlia.node.Node;

import java.io.IOException;
import java.net.InetAddress;

public class Nodo {
    public static void main(String[] args) throws IOException {

        for(int i = 11; i<100; i++) {
            JKademliaNode kad1 = new JKademliaNode("Node"+i, new KademliaId("FSF45678MA7584567Q"+i), 7600+i);


            KademliaId id = new KademliaId("ASERTKJDHGVHERJHGFLK");
            InetAddress ip = InetAddress.getByName("localhost");
            Node kadi2 = new Node(id, ip, 7572);
            kad1.bootstrap(kadi2);
            System.out.println(kad1.getRoutingTable().getAllNodes().size());
        }

    }
}
