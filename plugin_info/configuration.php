<?php
/* This file is part of Jeedom.
*
* Jeedom is free software: you can redistribute it and/or modify
* it under the terms of the GNU General Public License as published by
* the Free Software Foundation, either version 3 of the License, or
* (at your option) any later version.
*
* Jeedom is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
* GNU General Public License for more details.
*
* You should have received a copy of the GNU General Public License
* along with Jeedom. If not, see <http://www.gnu.org/licenses/>.
*/

require_once dirname(__FILE__) . '/../../../core/php/core.inc.php';
include_file('core', 'authentification', 'php');
if (!isConnect()) {
  include_file('desktop', '404', 'php');
  die();
}
?>
<form class="form-horizontal">
  <fieldset>
    <div class="form-group">
      <label class="col-md-4 control-label">{{Nextcloud URL}}
        <sup><i class="fas fa-question-circle tooltips" title="{{Renseignez l'url de Nextcloud}}"></i></sup>
      </label>
      <div class="col-md-4">
        <input class="configKey form-control" data-l1key="nc_url"/>
      </div>
    </div>
    <div class="form-group">
      <label class="col-md-4 control-label">{{Nextcloud User Name}}
        <sup><i class="fas fa-question-circle tooltips" title="{{Renseignez le nom d'utilisateur}}"></i></sup>
      </label>
      <div class="col-md-4">
        <input class="configKey form-control" data-l1key="nc_user"/>
      </div>
    </div>
    <div class="form-group">
      <label class="col-md-4 control-label">{{Nextcloud User Password}}
        <sup><i class="fas fa-question-circle tooltips" title="{{Renseignez le mot de passe utilisateur}}"></i></sup>
      </label>
      <div class="col-md-4">
        <input class="configKey form-control" data-l1key="nc_psw"/>
      </div>
    </div>
    <div class="form-group">
      <label class="col-md-4 control-label">{{Base de Temps}}
        <sup><i class="fas fa-question-circle tooltips" title="{{Temps entre 2 lectures en secondes}}"></i></sup>
      </label>
      <div class="col-md-4">
        <input class="configKey form-control" data-l1key="nc_tps" placeholder="5"/>
      </div>
    </div>

    <div class="form-group">
      <label class="col-md-4 control-label">{{Socket Port}}
        <sup><i class="fas fa-question-circle tooltips" title="{{Port du démon}}"></i></sup>
      </label>
      <div class="col-md-4">
        <input class="configKey form-control" data-l1key="socket_port" placeholder="52029"/>
      </div>
    </div>

  </fieldset>
</form>
