6<?php
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
	log::add('nc_talk', 'debug',$result['eq_id']); //remplacez template par l'id de votre plugin
    } else {
        log::add('nc_talk', 'error', 'unknown message received from daemon'); //remplacez template par l'id de votre plugin
    }
} catch (Exception $e) {
    log::add('nc_talk', 'error', displayException($e)); //remplacez template par l'id de votre plugin
}

?>
