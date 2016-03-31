# Deploying OpenStack with Ansible

- Requires Ansible 2.0.1
- Expects Ubuntu 14.04


## Ansible's Deployment


The management services deployed/configured on the controller node are as
follows:

- Nova: Uses MySQL to store VM info and state. The communication between
several Nova components are handled by RabbitMQ messaging system.

- Neutron: Uses MySQL as its backend database and RabbitMQ for interprocess
communication. The Neutron service uses the OpenVSwitch (LinuxBridge?) plugin to provide
network services. L2 and L3 services are taken care by Neutron.

- Cinder is not installed or configured.

- Keystone: Uses MySQL to store the tenant/user details and provides identity
and authorization service to all other components.

- Glance: Uses MySQL as the backend database, and images are stored on the
local filesystem.

- Horizon: Uses memcached to store user session details and provides UI
interface to endusers/admins.

The playbooks also configure the compute nodes with the following components:

- Nova Compute: The Nova Compute service is configured to use kvm  as the
hypervisor and uses libvirt to create/configure/teminate virtual machines.

- Neutron Agent: A Neutron Agent is also configured on the compute node which
uses OpenVSwitch or LinuxBridge to provide L2 services to the running virtual machines.



 
## Deploying OpenStack with Ansible

As discussed above this example deploys OpenStack in an multi-node set up, where
all the management services are deployed on a single host (controller node) and
the hypervisors (compute nodes) are deployed on the other nodes. 


#### Prerequisites:

- Ubuntu 14.04 
- All Nodes: Should have three NICs, one for accessing the systems (controller, 
compute, compute2), one for the management network, and one for the tenant data networks.

Before the playbooks are run please make sure that the following parameters in
group_vars/all are suited to your environment:

- Neutron_external_interface: eth2 # The nic that would be used for external
traffic. Make sure there is no IP assigned to it and it is in enabled state.

- Adjust openstack_version for the release, i.e. liberty or master(trunk)

- Adjust ml2_environment and interface_driv for either LinuxBridge or OpenVSwitch 
environments.

### Operation:

Once the prerequisites are satisfied and the group variables are changed to
suit your environment, modify the inventory file 'hosts' to match your
environment. Here's an example inventory:

    [openstack-ubu-controller]
    openstack-ubu-controller

    [openstack-ubu-compute]
    openstack-ubu-compute

    [openstack-ubu-compute2]
    openstack-ubu-compute2

Run the playbook to deploy the OpenStack Cloud:

        ansible-playbook -i hosts site.yml

Once the playbooks complete you can check the deployment by logging into the
controller node and "sourcing" the adminrc file. Then run "openstack compute
service list" and "neutron agent-list". Output should look similar to:

root@controller:~# openstack compute service list
+----+------------------+--------------------------+----------+---------+-------+----------------------------+
| Id | Binary           | Host                     | Zone     | Status  | State | Updated At                 |
+----+------------------+--------------------------+----------+---------+-------+----------------------------+
|  1 | nova-scheduler   | openstack-ubu-controller | internal | enabled | up    | 2016-03-17T13:16:49.000000 |
|  2 | nova-cert        | openstack-ubu-controller | internal | enabled | up    | 2016-03-17T13:16:51.000000 |
|  4 | nova-consoleauth | openstack-ubu-controller | internal | enabled | up    | 2016-03-17T13:16:52.000000 |
|  6 | nova-conductor   | openstack-ubu-controller | internal | enabled | up    | 2016-03-17T13:16:53.000000 |
|  8 | nova-compute     | openstack-ubu-compute    | nova     | enabled | up    | 2016-03-17T13:16:52.000000 |
|  9 | nova-compute     | openstack-ubu-compute2   | nova     | enabled | up    | 2016-03-17T13:16:57.000000 |
+----+------------------+--------------------------+----------+---------+-------+----------------------------+
root@controller:~# neutron agent-list
+-----------------------+--------------------+-----------------------+-------------------+-------+----------------+------------------------+
| id                    | agent_type         | host                  | availability_zone | alive | admin_state_up | binary                 |
+-----------------------+--------------------+-----------------------+-------------------+-------+----------------+------------------------+
| 1cc6af89-4387-4b2d-90 | Linux bridge agent | openstack-ubu-        |                   | :-)   | True           | neutron-linuxbridge-   |
| 18-fbfa2402173b       |                    | compute2              |                   |       |                | agent                  |
| 2357f62a-79fe-4657-b8 | L3 agent           | openstack-ubu-        | nova              | :-)   | True           | neutron-l3-agent       |
| b1-b365631da9ae       |                    | controller            |                   |       |                |                        |
| 9f9ca4ef-8ddb-4c87    | Linux bridge agent | openstack-ubu-compute |                   | :-)   | True           | neutron-linuxbridge-   |
| -acca-4a66faa986a9    |                    |                       |                   |       |                | agent                  |
| bbfccc8a-ca42-4b3b-   | DHCP agent         | openstack-ubu-        | nova              | :-)   | True           | neutron-dhcp-agent     |
| 8d21-acde358926dd     |                    | controller            |                   |       |                |                        |
| df431cd8-621d-47a7-8a | Linux bridge agent | openstack-ubu-        |                   | :-)   | True           | neutron-linuxbridge-   |
| 48-093520a266cc       |                    | controller            |                   |       |                | agent                  |
| f7ea50fd-d5df-441e-   | Metadata agent     | openstack-ubu-        |                   | :-)   | True           | neutron-metadata-agent |
| 82cb-0654bb52b378     |                    | controller            |                   |       |                |                        |
+-----------------------+--------------------+-----------------------+-------------------+-------+----------------+------------------------+


### Uploading an Image to OpenStack

Once OpenStack is deployed, an image can be uploaded to Glance for VM creation
using the following command. This uploads a cirros image from a an URL directly
to Glance.

wget http://download.cirros-cloud.net/0.3.4/cirros-0.3.4-x86_64-disk.img

glance image-create --name=cirros-qcow2 \
                    --disk-format=qcow2 \
                    --container-format=bare < cirros-0.3.4-x86_64-disk.img

