{% set node = 'node_1' if grains['fqdn'] == pillar['facts']['node_1']['fqdn'] else 'node_2' if grains['fqdn'] == pillar['facts']['node_2']['fqdn'] else None %}

Update lnet config file:
  file.managed:
    - name: /etc/modprobe.d/lnet.conf
    - contents:
      - options lnet networks=tcp({{ salt['pillar.get']("facts:{0}:data_if".format(node), 'lo') }})  config_on_load=1
    - user: root
    - group: root


Update EOSCore config:
  module.run:
    - eoscore.conf_update:
      - name: /etc/sysconfig/mero
      - ref_pillar: eoscore
      - backup: True