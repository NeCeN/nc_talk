<?php
try {
    require_once dirname(__FILE__) . "/../../../../core/php/core.inc.php";

    if (!jeedom::apiAccess(init('apikey'), 'nc_talk')) { //remplacez template par l'id de votre plugin
        echo __('Vous n\'etes pas autorisé à effectuer cette action', __FILE__);
        die();
    }
    if (init('test') != '') {
        echo 'OK';
        die();
    }
    $result = json_decode(file_get_contents("php://input"), true);
    if (!is_array($result)) {
        die();
    }

    if (isset($result['eq_id'])) {
	$eq=eqLogic::byId($result['eq_id']);
	$eq->checkAndUpdateCmd('read',$result['info']);
	log::add('nc_talk', 'debug',$result['eq_id']." < ".$result['info']); //remplacez template par l'id de votre plugin

	foreach ($eq->getCmd('action') as $cmd) {
		if ($cmd->askResponse($result['info']))
		{
			log::add('nc_talk', 'debug', 'Ask reply : ' .$result['info']);
			die();
		}
	}

	if ($eq->getConfiguration('isInteract', '0')=='1')
	{
		log::add('nc_talk', 'debug', 'Interaction ' . print_r($reply, true));
		$parameters['plugin'] = 'nc_talk';
		$reply = interactQuery::tryToReply($result['info'], $parameters);
		$request="curl -k -u '".config::byKey('nc_user','nc_talk', 'nc').":".config::byKey('nc_psw','nc_talk', 'nc')."' -d 'message=".$reply['reply']."' -H 'OCS-APIRequest: true' -X POST '".config::byKey('nc_url','nc_talk', 'nc')."/ocs/v2.php/apps/spreed/api/v1/chat/".$eq->getConfiguration('nc_talk_id', 'nc')."'"; //On prépare la requête curl
		exec($request);
		log::add('nc_talk', 'debug', 'Interaction reply done');



	}
    } else {
        log::add('nc_talk', 'error', 'unknown message received from daemon'); //remplacez template par l'id de votre plugin
    }
} catch (Exception $e) {
    log::add('nc_talk', 'error', displayException($e)); //remplacez template par l'id de votre plugin
}

?>
