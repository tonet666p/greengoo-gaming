<?php
require('php/routeros_api.class.php');

function add_to_lst($server, $client_ip){
	$API = new RouterosAPI();
	$API->debug = true;
	
	if ($API->connect('172.16.11.1', 'greengoo', 'playwithgreengoo')) {

		$API->comm("/ip/firewall/address-list/add", array(
			"list" => "greengoo_client",
			"address" => "$client_ip",
			"disabled" => "no",
			"timeout" => "10m"
		));

		$API->disconnect();

	}
}
?>
