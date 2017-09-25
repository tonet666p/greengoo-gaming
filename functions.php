<?php
require('php/routeros_api.class.php');

function add_addr($server, $client_addr){
        $API = new RouterosAPI();
        $API->debug = true;
        if ($API->connect('172.16.11.1', 'greengoo', 'playwithgreengoo')) {
                $API->comm("/ip/firewall/address-list/add", array(
                        "list" => "greengoo_client",
                        "address" => "$client_addr",
                        "disabled" => "no",
                        "timeout" => "5m"
                ));
                $API->disconnect();
        }
}
function rem_addr($rb, $client_addr){
        $API = new RouterosAPI();
        $API->debug = true;
        if ($API->connect($rb, 'greengoo', 'playwithgreengoo')) {
                # Get Ips from address list
                $API->write("/ip/firewall/address-list/print",false);
                $API->write("?list=greengoo_client",false);
                $API->write("?address=$client_addr",false);
                $API->write("=.proplist=.id");
                $line = $API->read()[0];
                $id = $line['.id'];
                $API->write("/ip/firewall/address-list/remove",false);
                $API->write("=.id=$id",true);
                sleep(2);
                $API->disconnect();
        }
}
?>
