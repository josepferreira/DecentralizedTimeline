import kademlia.*;
import kademlia.node.*;
import kademlia.routing.KademliaRoutingTable;

import java.io.IOException;
import java.net.InetAddress;

public class Bootstrap {


    public static void main(String[] args) {
        try {
            JKademliaNode kad1 = new JKademliaNode("Node1", new KademliaId("ASF45678947584567467"), 7574);
            JKademliaNode kad2 = new JKademliaNode("Node2", new KademliaId("ASERTKJDHGVHERJHGFLK"), 7572);

            System.out.println(kad1.getRoutingTable().getAllNodes());
            System.out.println(kad2.getRoutingTable().getAllNodes());

            KademliaId id = new KademliaId("ASERTKJDHGVHERJHGFLK");
            InetAddress ip = InetAddress.getByName("localhost");
            Node kadi2 = new Node(id,ip,7572);
            kad1.bootstrap(kadi2);

            System.out.println("Acabou");

            System.out.println(kad1.getRoutingTable().getAllNodes());
            System.out.println(kad2.getRoutingTable().getAllNodes());

            while(true){
                try {
                    System.out.println("A imprimir");
                    Thread.sleep(10000);
                    System.out.println("É o 1:");
                    System.out.println(kad1.getRoutingTable().getAllNodes());
                    System.out.println("É o 2:");
                    System.out.println(kad2.getRoutingTable().getAllNodes());
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }


        } catch (IOException e) {
            e.printStackTrace();
        }


    }

}
